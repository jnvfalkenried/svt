from sqlalchemy import select, text

from postgresql.database_models import ActiveHashtags


async def get_active_hashtags(session) -> list:
    result = await session.execute(
        select(ActiveHashtags).where(ActiveHashtags.active == True)
    )
    hashtags = result.scalars().all()
    return hashtags


async def insert_or_update_active_hashtag(id: str, title: str, session) -> None:
    # Create new hashtag instance
    new_hashtag = ActiveHashtags(id=id, title=title, active=True)

    try:
        # Add the new hashtag
        session.add(new_hashtag)

        await session.flush()
        print("Successfully flushed new hashtag")  # Debug print
    except Exception as e:
        print(f"Error in insert_or_update_active_hashtag: {e}")
        print(f"Error type: {type(e)}")
        raise e
