from sqlalchemy import text


async def insert_post(
    id: str,
    created_at: int,
    description: str,
    duet_enabled: bool,
    duet_from_id: str,
    is_ad: bool,
    can_repost: bool,
    collect_count: int,
    comment_count: int,
    digg_count: int,
    play_count: str,
    repost_count: str,
    share_count: str,
    author_id: str,
    music_id: str,
    session,
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO posts (
                id, created_at, description, duet_enabled, duet_from_id, is_ad, 
                can_repost, collect_count, comment_count, digg_count,
                play_count, repost_count, share_count, author_id, music_id
            ) 
            VALUES (
                :id, :created_at, :description, :duet_enabled, :duet_from_id, :is_ad, 
                :can_repost, :collect_count, :comment_count, :digg_count,
                :play_count, :repost_count, :share_count, :author_id, :music_id
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
            collect_count=collect_count,
            comment_count=comment_count,
            digg_count=digg_count,
            play_count=play_count,
            repost_count=repost_count,
            share_count=share_count,
            author_id=author_id,
            music_id=music_id,
        )
    )
