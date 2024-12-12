import asyncio

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from sqlalchemy import text

from postgresql.config.db import session

async def fetch_last_processed_time():
    async with session() as s:
        query = text("""
        SELECT COALESCE(MAX(processed_at), NOW() - INTERVAL '1 hour')
        FROM rule_mining_log
        """)
        result = await s.execute(query)
        return result.scalar()

async def fetch_posts_challenges(last_processed_time):
    async with session() as s:
        query = text("""
        SELECT p.id AS post_id, 
               p.description,
               c.id AS challenge_id, 
               c.title AS challenge_title,
               c.hashtag_count
        FROM posts p
        JOIN posts_challenges pc ON p.id = pc.post_id
        JOIN challenges c ON pc.challenge_id = c.id
        WHERE p.inserted_at > :last_processed_time
        """)
        
        result = await s.execute(query, {"last_processed_time": last_processed_time})
        rows = result.fetchall()
        
        data = [dict(row._mapping) for row in rows]
        df = pd.DataFrame(data)
        return df
    
async def main():
    last_processed_time = await fetch_last_processed_time()
    df = await fetch_posts_challenges(last_processed_time)
    df[["post_id", "challenge_id"]] = df[["post_id", "challenge_id"]].map(int)
    df[["challenge_title"]] = df[["challenge_title"]].map(str)
    
    transactions = df.groupby("post_id")["challenge_title"].apply(list).to_list()

    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    txn_df = pd.DataFrame(te_ary, columns=te.columns_)
    
    frequent_itemsets = apriori(txn_df, min_support=0.05, use_colnames=True)
    
    rules = association_rules(frequent_itemsets, len(txn_df), metric="confidence", min_threshold=0.3)


if __name__ == "__main__":
    asyncio.run(main())