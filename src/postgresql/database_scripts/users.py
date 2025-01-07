from sqlalchemy import text


async def insert_user(
    id: str,
    username: str,
    email: str,
    password_hash: str,
    roles: list[str],
    session,
) -> None:
    """
    Insert a user into the users table.

    If a row with the same id already exists, this function does nothing.

    Args:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        roles (list[str]): The roles assigned to the user.
        session: The database session to use for the operation.

    Returns:
        None
    """

    await session.execute(
        text(
            """
            INSERT INTO users (id, username, email, password_hash, active, roles) 
            VALUES (:id, :username, :email, :password_hash, :active, :roles)
            ON CONFLICT (id) DO NOTHING
            """
        ).params(
            id=id,
            username=username,
            email=email,
            password_hash=password_hash,
            active=True,
            roles=roles,
        )
    )
