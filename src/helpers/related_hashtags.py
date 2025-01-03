from datetime import datetime

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from sqlalchemy import text

from postgresql.config.db import session
from postgresql.database_scripts.related_hashtags import save_rules_to_db


async def fetch_last_processed_time():
    async with session() as s:
        query = text(
            """
        SELECT COALESCE(MAX(processed_at), NOW() - INTERVAL '1 hour')
        FROM rule_mining_log
        """
        )
        result = await s.execute(query)
        return result.scalar()


async def fetch_posts_challenges(last_processed_time):
    async with session() as s:
        query = text(
            """
        SELECT p.id AS post_id, 
               p.description,
               c.id AS challenge_id, 
               c.title AS challenge_title,
               c.hashtag_count
        FROM posts p
        JOIN posts_challenges pc ON p.id = pc.post_id
        JOIN challenges c ON pc.challenge_id = c.id
        WHERE p.inserted_at > :last_processed_time
        """
        )

        result = await s.execute(query, {"last_processed_time": last_processed_time})
        rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]
        df = pd.DataFrame(data)
        return df


async def fetch_previous_rules():
    async with session() as s:
        query = text(
            """
        SELECT antecedent_id, antecedent_title, 
               consequent_id, consequent_title,
               antecedent_support, consequent_support,
               support, confidence, lift
        FROM related_hashtags             
        """
        )

        result = await s.execute(query)
        rows = result.fetchall()

        if not rows:
            return pd.DataFrame(
                columns=[
                    "antecedent_id",
                    "antecedent_title",
                    "consequent_id",
                    "consequent_title",
                    "antecedent_support",
                    "consequent_support",
                    "support",
                    "confidence",
                    "lift",
                ]
            )

        data = [dict(row._mapping) for row in rows]
        df = pd.DataFrame(data)
        return df


def merge_frequent_itemsets(old_rules_df, new_txn_df):
    print("Merging frequent itemsets...")

    def compute_support(titles):
        # Filter titles to include only those present in new_txn_df columns
        valid_titles = [title for title in titles if title in new_txn_df.columns]
        if valid_titles:  # If there are valid titles
            return new_txn_df[valid_titles].all(axis=1).mean()
        else:
            return 0  # Return 0 if no valid titles are found

    old_copy_df = old_rules_df.copy()
    old_copy_df["new_antecedent_support"] = old_copy_df["antecedent_title"].apply(
        # lambda x: new_txn_df[te.columns_.isin(x)].all(axis = 1).mean()
        lambda x: compute_support(x) if isinstance(x, list) else 0
    )
    old_copy_df["new_consequent_support"] = old_copy_df["consequent_title"].apply(
        # lambda x: new_txn_df[te.columns_.isin(x)].all(axis = 1).mean()
        lambda x: compute_support(x) if isinstance(x, list) else 0
    )
    old_copy_df["new_support"] = old_copy_df.apply(
        lambda row: (
            compute_support(row["antecedent_title"] + row["consequent_title"])
            if isinstance(row["antecedent_title"], list)
            and isinstance(row["consequent_title"], list)
            else 0
        ),
        axis=1,
    )

    old_rules_df["antecedent_support"] = (
        old_rules_df["antecedent_support"] + old_copy_df["new_antecedent_support"]
    )
    old_rules_df["consequent_support"] = (
        old_rules_df["consequent_support"] + old_copy_df["new_consequent_support"]
    )
    old_rules_df["support"] = old_rules_df["support"] + old_copy_df["new_support"]
    return old_rules_df


def detect_and_add_new_rules(
    new_txn_df, old_rules_df, posts_challenges_df, confidence_threshold
):
    print("Detecting and adding new rules...")
    frequent_itemsets = apriori(new_txn_df, min_support=0.05, use_colnames=True)

    new_rules = association_rules(
        frequent_itemsets,
        len(new_txn_df),
        metric="confidence",
        min_threshold=confidence_threshold,
    )

    existing_antecedents = old_rules_df["antecedent_title"].apply(set).tolist()
    existing_consequents = old_rules_df["consequent_title"].apply(set).tolist()

    def is_new_rule(antecedent, consequent):
        for existing_antecedent, existing_consequent in zip(
            existing_antecedents, existing_consequents
        ):
            if (
                set(antecedent) == existing_antecedent
                and set(consequent) == existing_consequent
            ):
                return False
        return True

    new_rules = new_rules[
        new_rules.apply(
            lambda row: is_new_rule(row["antecedents"], row["consequents"]), axis=1
        )
    ]

    new_rules_df = pd.DataFrame(
        {
            "antecedent_title": new_rules["antecedents"].apply(list),
            "consequent_title": new_rules["consequents"].apply(list),
            "antecedent_support": new_rules["antecedent support"],
            "consequent_support": new_rules["consequent support"],
            "support": new_rules["support"],
            "confidence": new_rules["confidence"],
            "lift": new_rules["lift"],
        }
    )

    new_rules_df.loc[:, "antecedent_id"] = new_rules_df["antecedent_title"].apply(
        lambda x: [
            posts_challenges_df.loc[
                posts_challenges_df["challenge_title"] == title, "challenge_id"
            ].iloc[0]
            for title in x
        ]
    )
    new_rules_df.loc[:, "consequent_id"] = new_rules_df["consequent_title"].apply(
        lambda x: [
            posts_challenges_df.loc[
                posts_challenges_df["challenge_title"] == title, "challenge_id"
            ].iloc[0]
            for title in x
        ]
    )

    return new_rules_df


def recompute_association_rules(merged_rules_df, confidence_threshold):
    print("Recomputing association rules...")
    merged_rules_df["confidence"] = (
        merged_rules_df["support"] / merged_rules_df["antecedent_support"]
    )
    merged_rules_df["lift"] = (
        merged_rules_df["confidence"] / merged_rules_df["consequent_support"]
    )

    updated_rules = merged_rules_df[
        (merged_rules_df["confidence"] >= confidence_threshold)
        & (merged_rules_df["support"] >= 0.05)
    ]

    return updated_rules


async def compute_related_hashtags():
    confidence_threshold = 0.3
    last_processed_time = await fetch_last_processed_time()
    if last_processed_time.tzinfo is not None:
        last_processed_time = last_processed_time.replace(tzinfo=None)

    df = await fetch_posts_challenges(last_processed_time)
    if df.empty:
        print("No new posts to process.")
        return

    # df[["post_id", "challenge_id"]] = df[["post_id", "challenge_id"]].map(int)
    df[["challenge_title"]] = df[["challenge_title"]].map(str)

    new_transactions = df.groupby("post_id")["challenge_title"].apply(list).to_list()

    te = TransactionEncoder()
    te_ary = te.fit(new_transactions).transform(new_transactions)
    new_txn_df = pd.DataFrame(te_ary, columns=te.columns_)

    old_rules_df = await fetch_previous_rules()
    columns_to_convert = [
        "antecedent_support",
        "consequent_support",
        "support",
        "confidence",
        "lift",
    ]
    old_rules_df[columns_to_convert] = old_rules_df[columns_to_convert].astype(
        float, errors="ignore"
    )

    if old_rules_df.empty:
        print("First-time rule mining: calculating rules for the first time.")

        frequent_itemsets = apriori(new_txn_df, min_support=0.05, use_colnames=True)

        updated_rules = association_rules(
            frequent_itemsets,
            len(new_txn_df),
            metric="confidence",
            min_threshold=confidence_threshold,
        )

        updated_rules.rename(
            columns={
                "antecedents": "antecedent_title",
                "antecedent support": "antecedent_support",
                "consequents": "consequent_title",
                "consequent support": "consequent_support",
            },
            inplace=True,
        )

        final_rules_df = updated_rules.copy()[
            [
                "antecedent_title",
                "antecedent_support",
                "consequent_title",
                "consequent_support",
                "support",
                "confidence",
                "lift",
            ]
        ]

        final_rules_df.loc[:, "antecedent_id"] = final_rules_df[
            "antecedent_title"
        ].apply(
            lambda x: [
                df.loc[df["challenge_title"] == title, "challenge_id"].iloc[0]
                for title in x
            ]
        )
        final_rules_df.loc[:, "consequent_id"] = final_rules_df[
            "consequent_title"
        ].apply(
            lambda x: [
                df.loc[df["challenge_title"] == title, "challenge_id"].iloc[0]
                for title in x
            ]
        )

    else:
        print("Incremental rule mining: merging old rules with new transactions.")

        merged_rules_df = merge_frequent_itemsets(old_rules_df, new_txn_df)

        new_rules_df = detect_and_add_new_rules(
            new_txn_df, old_rules_df, df, confidence_threshold
        )

        merged_rules_df = pd.concat([merged_rules_df, new_rules_df], ignore_index=True)

        final_rules_df = recompute_association_rules(
            merged_rules_df, confidence_threshold
        )

    print("Saving rules to database...")
    await save_rules_to_db(final_rules_df, session=session)
    print("Rules saved to database.")
    print("Rule mining completed.")
