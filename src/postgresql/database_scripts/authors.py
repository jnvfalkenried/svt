from datetime import datetime

from sqlalchemy import text


async def insert_author(
    id: str,
    nickname: str,
    signature: str,
    unique_id: str,
    verified: bool,
    session,
) -> None:
    """
    Insert an author into the authors table.

    If a row with the same id already exists, do nothing.

    Args:
        id (str): The unique identifier of the author.
        nickname (str): The nickname of the author.
        signature (str): The signature of the author.
        unique_id (str): The unique identifier of the author.
        verified (bool): Whether the author is verified or not.
        session: The database session to use for the operation.
    """

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
