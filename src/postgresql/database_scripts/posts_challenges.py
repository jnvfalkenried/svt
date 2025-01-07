from sqlalchemy import text


async def insert_post_challenge(post_id: str, challenge_id: str, session) -> None:
    """
    Inserts a post-challenge relationship into the posts_challenges table.

    If the post_id and challenge_id already exist in the table, this function does nothing.

    Args:
        post_id (str): The ID of the post.
        challenge_id (str): The ID of the challenge.
        session: The database session to use for the query.
    """

    await session.execute(
        text(
            """
            INSERT INTO posts_challenges (post_id, challenge_id) 
            VALUES (:post_id, :challenge_id)
            ON CONFLICT (post_id, challenge_id) DO NOTHING
            """
        ).params(
            post_id=post_id,
            challenge_id=challenge_id,
        )
    )
