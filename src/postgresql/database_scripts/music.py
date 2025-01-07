from sqlalchemy import text


async def insert_music(
    id: str, author_name: str, title: str, duration: int, original: bool, session
) -> None:
    """
    Insert a music into the database.

    If a row with the same id already exists, do nothing.

    Args:
        id (str): The unique identifier of the music.
        author_name (str): The name of the author of the music.
        title (str): The title of the music.
        duration (int): The duration of the music in seconds.
        original (bool): Whether the music is an original work.
        session: The database session to use for the operation.
    """

    await session.execute(
        text(
            """
            INSERT INTO music (id, author_name, title, duration, original) 
            VALUES (:id, :author_name, :title, :duration, :original)
            ON CONFLICT (id) DO NOTHING
            """
        ).params(
            id=id,
            author_name=author_name,
            title=title,
            duration=duration,
            original=original,
        )
    )
