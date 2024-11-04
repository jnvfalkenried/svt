from sqlalchemy import text


async def insert_challenge(
    id: str, title: str, description: str, video_count: int, view_count: int, session
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO challenges (id, title, description, video_count, view_count) 
            VALUES (:id, :title, :description, :video_count, :view_count)
            ON CONFLICT (id) DO NOTHING
            """
        ).params(
            id=id,
            title=title,
            description=description,
            video_count=video_count,
            view_count=view_count,
        )
    )
