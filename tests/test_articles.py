async def test_create_article(client):
    response1 = await client.post("/categories/", json={"name": "Tech"})

    cat_id = response1.json()["id"]
    response2 = await client.post(
        "/articles/",
        json={"title": "string", "content": "string", "category_id": cat_id, "image_url": "string"},
    )
    assert response2.status_code == 200
    assert response2.json()["title"] == "string"


async def test_create_article_no_category(client):
    response = await client.post(
        "/articles/",
        json={"title": "string", "content": "string", "category_id": 1, "image_url": "string"},
    )
    assert response.status_code == 404


async def test_get_articles(client):
    response1 = await client.post("/categories/", json={"name": "Tech"})
    cat_id = response1.json()["id"]
    _ = await client.post(
        "/articles/",
        json={"title": "string", "content": "string", "category_id": cat_id, "image_url": "string"},
    )
    response3 = await client.get("/articles/")
    assert len(response3.json()) > 0


async def test_get_article_by_id(client):
    response1 = await client.post("/categories/", json={"name": "Tech"})

    cat_id = response1.json()["id"]

    response2 = await client.post(
        "/articles/",
        json={"title": "string", "content": "string", "category_id": cat_id, "image_url": "string"},
    )

    art_id = response2.json()["id"]
    response3 = await client.get(f"/articles/{art_id}")
    assert response3.status_code == 200
    assert response3.json()["title"] == "string"


async def test_update_article(client):
    response1 = await client.post("/categories/", json={"name": "Tech"})

    cat_id = response1.json()["id"]

    response2 = await client.post(
        "/articles/",
        json={"title": "string", "content": "string", "category_id": cat_id, "image_url": "string"},
    )

    art_id = response2.json()["id"]

    response3 = await client.put(
        f"/articles/{art_id}",
        json={
            "title": "new_string",
            "content": "string",
            "category_id": cat_id,
            "image_url": "string",
        },
    )

    assert response3.json()["title"] == "new_string"


async def test_delete_article(client):
    response1 = await client.post("/categories/", json={"name": "Tech"})

    cat_id = response1.json()["id"]
    response2 = await client.post(
        "/articles/",
        json={"title": "string", "content": "string", "category_id": cat_id, "image_url": "string"},
    )
    art_id = response2.json()["id"]
    _ = await client.delete(f"/articles/{art_id}")
    response4 = await client.get(f"/articles/{art_id}")
    assert response4.status_code == 404
