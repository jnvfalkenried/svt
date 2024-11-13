from sqlalchemy import text


async def insert_or_update_active_hashtag(id: str, title: str, session) -> None:
    active = True
    # TODO: Update on conflict
    await session.execute(
        text(
            """
            INSERT INTO active_hashtags (id, title, active) 
            VALUES (:id, :title, :active)
            """
        ).params(
            id=id,
            title=title,
            active=active
        )
    )
