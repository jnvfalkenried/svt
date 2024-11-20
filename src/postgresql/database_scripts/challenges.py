from sqlalchemy import text


async def insert_or_update_challenge(
    id: str, title: str, description: str, session
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO challenges (id, title, description, hashtag_count) 
            VALUES (:id, :title, :description, 1)
            ON CONFLICT (id) 
            DO UPDATE SET 
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                hashtag_count = challenges.hashtag_count + 1
            """
        ).params(
            id=id,
            title=title,
            description=description,
        )
    )
