from sqlalchemy import text


async def insert_post_challenge(post_id: str, challenge_id: str, session) -> None:
    await session.execute(
        text(
            """
            INSERT INTO posts_challenges (post_id, challenge_id) 
            VALUES (:post_id, :challenge_id)
            """
        ).params(
            post_id=post_id,
            challenge_id=challenge_id,
        )
    )
