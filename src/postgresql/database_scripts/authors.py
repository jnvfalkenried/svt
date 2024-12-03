from sqlalchemy import text
from datetime import datetime


async def insert_author(
    id: str,
    nickname: str,
    signature: str,
    unique_id: str,
    verified: bool,
    session,
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO authors (
                id, nickname, signature, unique_id, verified
            ) 
            VALUES (
                :id, :nickname, :signature, :unique_id, :verified
            )
            ON CONFLICT (id) DO NOTHING
            """
        ).params(
            id=id,
            nickname=nickname,
            signature=signature,
            unique_id=unique_id,
            verified=verified,
        )
    )
