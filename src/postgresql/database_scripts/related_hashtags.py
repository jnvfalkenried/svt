import hashlib

from sqlalchemy import text


def generate_hashed_id(antecedent_id, consequent_id):
    """
    Returns a string that is a SHA256 hash of the given antecedent_id and
    consequent_id. The IDs are sorted before being hashed, so the order of the
    IDs does not affect the hash.

    This is used to create a unique identifier for a rule in the related_hashtags
    table.
    """
    key = ",".join(sorted(antecedent_id)) + "|" + ",".join(sorted(consequent_id))
    return hashlib.sha256(key.encode()).hexdigest()


async def save_rules_to_db(rules, session):
    """
    Saves the given rules to the related_hashtags table in the database. If a
    rule already exists in the table, it will be updated with the new values. If
    the rule does not exist, it will be inserted into the table.

    Args:
        rules (pd.DataFrame): A DataFrame containing the rules, with the
            following columns:

            - antecedent_id (int): The id(s) of the antecedent hashtag(s).
            - antecedent_title (str): The title(s) of the antecedent hashtag(s).
            - consequent_id (int): The id(s) of the consequent hashtag(s).
            - consequent_title (str): The title(s) of the consequent hashtag(s).
            - antecedent_support (float): The support of the antecedent hashtag(s).
            - consequent_support (float): The support of the consequent hashtag(s).
            - support (float): The support of the rule.
            - confidence (float): The confidence of the rule.
            - lift (float): The lift of the rule.
        session: A SQLAlchemy session object.

    Returns:
        None
    """
    async with session() as s:
        for _, rule in rules.iterrows():
            antecedent_id = list(rule["antecedent_id"])
            consequent_id = list(rule["consequent_id"])
            hashed_id = generate_hashed_id(antecedent_id, consequent_id)

            check_query = text(
                """
            SELECT 1 FROM related_hashtags
            WHERE hashed_id = :hashed_id;
            """
            )
            existing_rule = await s.execute(check_query, {"hashed_id": hashed_id})
            existing_rule = existing_rule.scalar()

            if existing_rule:
                update_query = text(
                    """
                UPDATE related_hashtags
                SET antecedent_support = :antecedent_support,
                    consequent_support = :consequent_support,
                    support = :support,
                    confidence = :confidence,
                    lift = :lift
                WHERE hashed_id = :hashed_id;
                """
                )
                await s.execute(
                    update_query,
                    {
                        "antecedent_support": rule["antecedent_support"],
                        "consequent_support": rule["consequent_support"],
                        "support": rule["support"],
                        "confidence": rule["confidence"],
                        "lift": rule["lift"],
                        "hashed_id": hashed_id,
                    },
                )
            else:
                await s.execute(
                    text(
                        """
                    INSERT INTO related_hashtags (hashed_id, antecedent_id, antecedent_title, antecedent_support,
                                                consequent_id, consequent_title, consequent_support,
                                                support, confidence, lift)
                    VALUES (:hashed_id, :antecedent_id, :antecedent_title, :antecedent_support,
                            :consequent_id, :consequent_title, :consequent_support,
                            :support, :confidence, :lift);  
                    """
                    ),
                    {
                        "hashed_id": hashed_id,
                        "antecedent_id": antecedent_id,
                        "antecedent_title": list(rule["antecedent_title"]),
                        "antecedent_support": rule["antecedent_support"],
                        "consequent_id": consequent_id,
                        "consequent_title": list(rule["consequent_title"]),
                        "consequent_support": rule["consequent_support"],
                        "support": rule["support"],
                        "confidence": rule["confidence"],
                        "lift": rule["lift"],
                    },
                )

        await s.execute(
            text(
                """
            INSERT INTO rule_mining_log (processed_at) VALUES (NOW());     
            """
            )
        )

        await s.commit()
