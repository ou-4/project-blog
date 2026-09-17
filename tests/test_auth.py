async def test_register(client):
    response = await client.post(
        "/auth/register", json={"email": "test@mail.ru", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@mail.ru"


async def test_register_duplicate(client):
    _ = await client.post(
        "/auth/register", json={"email": "test@mail.ru", "password": "password123"}
    )

    response2 = await client.post(
        "/auth/register", json={"email": "test@mail.ru", "password": "password123"}
    )

    assert response2.status_code == 409


async def test_login(client):
    _ = await client.post(
        "/auth/register", json={"email": "test@mail.ru", "password": "password123"}
    )

    response2 = await client.post(
        "/auth/login", json={"email": "test@mail.ru", "password": "password123"}
    )

    assert response2.status_code == 200


async def test_login_wrong_password(client):
    _ = await client.post(
        "/auth/register", json={"email": "test@mail.ru", "password": "password123"}
    )

    response2 = await client.post(
        "/auth/login", json={"email": "test@mail.ru", "password": "wrongpassword123"}
    )

    assert response2.status_code == 401
