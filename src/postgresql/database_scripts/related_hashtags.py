import hashlib

from sqlalchemy import text


def generate_hashed_id(antecedent_id, consequent_id):
    key = ",".join(sorted(antecedent_id)) + "|" + ",".join(sorted(consequent_id))
    return hashlib.sha256(key.encode()).hexdigest()

async def save_rules_to_db(rules, session):
    async with session() as s:
        for _, rule in rules.iterrows():
            antecedent_id = list(rule["antecedent_id"])
            consequent_id = list(rule["consequent_id"])
            hashed_id = generate_hashed_id(antecedent_id, consequent_id)
            
            check_query = text("""
            SELECT 1 FROM related_hashtags
            WHERE hashed_id = :hashed_id;
            """)
            existing_rule = await s.execute(
                check_query,
                {"hashed_id": hashed_id}
            )
            existing_rule = existing_rule.scalar()
            
            if existing_rule:
                update_query = text("""
                UPDATE related_hashtags
                SET antecedent_support = :antecedent_support,
                    consequent_support = :consequent_support,
                    support = :support,
                    confidence = :confidence,
                    lift = :lift
                WHERE hashed_id = :hashed_id;
                """)
                await s.execute(
                    update_query,
                    {
                        "antecedent_support": rule["antecedent_support"],
                        "consequent_support": rule["consequent_support"],
                        "support": rule["support"],
                        "confidence": rule["confidence"],
                        "lift": rule["lift"],
                        "hashed_id": hashed_id
                    }
                )
            else:
                await s.execute(
                    text("""
                    INSERT INTO related_hashtags (hashed_id, antecedent_id, antecedent_title, antecedent_support,
                                                consequent_id, consequent_title, consequent_support,
                                                support, confidence, lift)
                    VALUES (:hashed_id, :antecedent_id, :antecedent_title, :antecedent_support,
                            :consequent_id, :consequent_title, :consequent_support,
                            :support, :confidence, :lift);  
                    """),
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
                        "lift": rule["lift"]
                    }
                )
        
        await s.execute(
            text("""
            INSERT INTO rule_mining_log (processed_at) VALUES (NOW());     
            """)
        )
        
        await s.commit()