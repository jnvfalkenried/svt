from sqlalchemy import text


async def insert_author(
    id: str,
    nickname: str,
    signature: str,
    unique_id: str,
    verified: bool,
    digg_count: int,
    follower_count: int,
    following_count: int,
    heart_count: int,
    video_count: int,
    session,
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO authors (
                id, nickname, signature, unique_id, verified, digg_count, 
                follower_count, following_count, heart_count, video_count
            ) 
            VALUES (
                :id, :nickname, :signature, :unique_id, :verified, :digg_count, 
                :follower_count, :following_count, :heart_count, :video_count
            )
            """
        ).params(
            id=id,
            nickname=nickname,
            signature=signature,
            unique_id=unique_id,
            verified=verified,
            digg_count=digg_count,
            follower_count=follower_count,
            following_count=following_count,
            heart_count=heart_count,
            video_count=video_count,
        )
    )
