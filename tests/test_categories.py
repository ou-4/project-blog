async def test_create_category(client):
    response = await client.post("/categories/", json={"name": "Tech"})
    assert response.status_code == 200
    assert response.json()["name"] == "Tech"


async def test_create_category_duplicate(client):
    _ = await client.post("/categories/", json={"name": "Tech"})

    response2 = await client.post("/categories/", json={"name": "Tech"})

    assert response2.status_code == 409


async def test_get_categories(client):
    _ = await client.post("/categories/", json={"name": "Tech"})

    _ = await client.post("/categories/", json={"name": "NoTech"})

    response3 = await client.get("/categories/")

    assert len(response3.json()) == 2
