from uuid import uuid4


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_user_success(client):
    payload = {"username": f"gabriel_{uuid4().hex[:8]}", "password": "123456"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == payload["username"]
    assert "id" in body
    assert "created_at" in body


def test_register_user_duplicate_username(client):
    payload = {"username": "duplicado", "password": "123456"}

    first = client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "Ja existe usuario com esse username."


def test_register_user_invalid_password(client):
    response = client.post(
        "/auth/register",
        json={"username": "curto", "password": "123"},
    )

    assert response.status_code == 422


def test_login_success(client):
    username = f"login_{uuid4().hex[:8]}"
    password = "123456"
    client.post("/auth/register", json={"username": username, "password": password})

    response = client.post("/auth/login", data={"username": username, "password": password})

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    username = f"login_fail_{uuid4().hex[:8]}"
    client.post("/auth/register", json={"username": username, "password": "123456"})

    response = client.post("/auth/login", data={"username": username, "password": "senha_errada"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario ou senha invalidos."


def test_protected_endpoint_requires_token(client):
    response = client.get("/accounts")

    assert response.status_code == 401
