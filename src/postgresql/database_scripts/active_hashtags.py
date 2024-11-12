from sqlalchemy import text


async def get_active_hashtags(session) -> list:
    query = await session.execute(
        text("select title from active_hashtags where active is true")
    )
    response = query.fetchall()
    return [i[0] for i in response]
