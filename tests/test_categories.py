async def test_create_category(auth_client):
    response = await auth_client.post("/categories/", json={"name": "Tech"})
    assert response.status_code == 200
    assert response.json()["name"] == "Tech"


async def test_create_category_duplicate(auth_client):
    _ = await auth_client.post("/categories/", json={"name": "Tech"})

    response2 = await auth_client.post("/categories/", json={"name": "Tech"})

    assert response2.status_code == 409


async def test_get_categories(auth_client):
    _ = await auth_client.post("/categories/", json={"name": "Tech"})

    _ = await auth_client.post("/categories/", json={"name": "NoTech"})

    response3 = await auth_client.get("/categories/")

    assert len(response3.json()) == 2
