from sqlalchemy import text


async def insert_post(
    id: str,
    created_at: int,
    description: str,
    duet_enabled: bool,
    duet_from_id: str,
    is_ad: bool,
    can_repost: bool,
    author_id: str,
    music_id: str,
    url: str,
    session,
) -> None:
    """
    Inserts a post into the database. If the post already exists, this function does nothing.

    Parameters:
        id (str): The ID of the post.
        created_at (int): The timestamp when the post was created.
        description (str): The description of the post.
        duet_enabled (bool): Whether the post allows duets.
        duet_from_id (str): The ID of the original post that this post is a duet of.
        is_ad (bool): Whether the post is an advertisement.
        can_repost (bool): Whether the post can be reposted.
        author_id (str): The ID of the author of the post.
        music_id (str): The ID of the music used in the post.
        url (str): The URL of the post.
        session: The SQLAlchemy session to use for the database query.
    """
    await session.execute(
        text(
            """
            INSERT INTO posts (
                id, created_at, description, duet_enabled, duet_from_id, 
                is_ad, can_repost, author_id, music_id, url
            ) 
            VALUES (
                :id, :created_at, :description, :duet_enabled, :duet_from_id, 
                :is_ad, :can_repost, :author_id, :music_id, :url
            )
            ON CONFLICT (id) DO NOTHING
            """
        ).params(
            id=id,
            created_at=created_at,
            description=description,
            duet_enabled=duet_enabled,
            duet_from_id=duet_from_id,
            is_ad=is_ad,
            can_repost=can_repost,
            author_id=author_id,
            music_id=music_id,
            url=url,
        )
    )
