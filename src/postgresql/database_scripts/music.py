from sqlalchemy import text


async def insert_music(
    id: str, author_name: str, title: str, duration: int, original: bool, session
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO music (id, author_name, title, duration, original) 
            VALUES (:id, :author_name, :title, :duration, :original)
            """
        ).params(
            id=id,
            author_name=author_name,
            title=title,
            duration=duration,
            original=original,
        )
    )
