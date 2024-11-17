from sqlalchemy import text


async def insert_user(
    id: str,
    username: str,
    email: str,
    password_hash: str,
    roles: list[str],
    session,
) -> None:
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
