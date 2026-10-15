async def test_ask_question(auth_client):
    _ = await auth_client.post("/categories/", json={"name": "Tech"})
    response = await auth_client.post("/ai/ask", json={"question": "What is FastAPI"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Test answer"


async def test_ask_unauthorized(client):
    response = await client.post("/ai/ask", json={"question": "What is FastAPI"})
    assert response.status_code == 401
