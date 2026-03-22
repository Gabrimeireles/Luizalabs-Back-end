def test_create_account_success(client, auth_headers):
    response = client.post(
        "/accounts",
        json={"limite": "500.00", "limite_saques": 3},
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["agencia"] == "0001"
    assert body["saldo"] == "0.00"
    assert body["limite"] == "500.00"
    assert body["limite_saques"] == 3


def test_create_account_invalid_limit(client, auth_headers):
    response = client.post(
        "/accounts",
        json={"limite": "0.00", "limite_saques": 3},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_accounts_returns_created_accounts(client, auth_headers):
    client.post("/accounts", json={"limite": "500.00", "limite_saques": 3}, headers=auth_headers)
    client.post("/accounts", json={"limite": "700.00", "limite_saques": 4}, headers=auth_headers)

    response = client.get("/accounts", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_get_account_success(client, auth_headers):
    created = client.post(
        "/accounts",
        json={"limite": "500.00", "limite_saques": 3},
        headers=auth_headers,
    )
    account_id = created.json()["id"]

    response = client.get(f"/accounts/{account_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == account_id


def test_get_account_not_found(client, auth_headers):
    response = client.get("/accounts/999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta nao encontrada."


def test_user_cannot_access_other_user_account(client):
    client.post("/auth/register", json={"username": "user_one", "password": "123456"})
    login_1 = client.post("/auth/login", data={"username": "user_one", "password": "123456"})
    token_1 = login_1.json()["access_token"]
    headers_1 = {"Authorization": f"Bearer {token_1}"}

    created = client.post(
        "/accounts",
        json={"limite": "500.00", "limite_saques": 3},
        headers=headers_1,
    )
    account_id = created.json()["id"]

    client.post("/auth/register", json={"username": "user_two", "password": "123456"})
    login_2 = client.post("/auth/login", data={"username": "user_two", "password": "123456"})
    token_2 = login_2.json()["access_token"]
    headers_2 = {"Authorization": f"Bearer {token_2}"}

    response = client.get(f"/accounts/{account_id}", headers=headers_2)

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta nao encontrada."
