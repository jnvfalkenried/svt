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
