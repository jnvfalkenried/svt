from sqlalchemy import text


async def get_active_hashtags(session) -> list:
    query = await session.execute(
        text("select title from active_hashtags where active is true")
    )
    response = query.fetchall()
    return [i[0] for i in response]

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
