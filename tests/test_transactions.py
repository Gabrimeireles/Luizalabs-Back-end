def _create_account(client, headers, limite="500.00", limite_saques=3):
    response = client.post(
        "/accounts",
        json={"limite": limite, "limite_saques": limite_saques},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_second_user_headers(client):
    client.post("/auth/register", json={"username": "visitor", "password": "123456"})
    login = client.post("/auth/login", data={"username": "visitor", "password": "123456"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_deposit_success(client, auth_headers):
    account_id = _create_account(client, auth_headers)

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "deposito", "valor": "1000.00"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["tipo"] == "deposito"


def test_withdraw_success(client, auth_headers):
    account_id = _create_account(client, auth_headers)
    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "deposito", "valor": "1000.00"},
        headers=auth_headers,
    )

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "200.00"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["tipo"] == "saque"


def test_transaction_negative_value_validation(client, auth_headers):
    account_id = _create_account(client, auth_headers)

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "deposito", "valor": "-10.00"},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_transaction_invalid_type_validation(client, auth_headers):
    account_id = _create_account(client, auth_headers)

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "pix", "valor": "10.00"},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_withdraw_insufficient_balance(client, auth_headers):
    account_id = _create_account(client, auth_headers)

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "50.00"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo insuficiente para saque."


def test_withdraw_exceeds_operation_limit(client, auth_headers):
    account_id = _create_account(client, auth_headers, limite="100.00")
    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "deposito", "valor": "1000.00"},
        headers=auth_headers,
    )

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "150.00"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "O valor do saque excede o limite por operacao."


def test_withdraw_exceeds_number_limit(client, auth_headers):
    account_id = _create_account(client, auth_headers, limite="500.00", limite_saques=2)
    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "deposito", "valor": "1000.00"},
        headers=auth_headers,
    )

    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "100.00"},
        headers=auth_headers,
    )
    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "100.00"},
        headers=auth_headers,
    )

    response = client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "100.00"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Numero maximo de saques excedido."


def test_transaction_account_not_found(client, auth_headers):
    response = client.post(
        "/accounts/999/transactions",
        json={"tipo": "deposito", "valor": "10.00"},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta nao encontrada."


def test_transaction_account_not_owned_by_user(client, auth_headers):
    owner_account_id = _create_account(client, auth_headers)
    other_headers = _create_second_user_headers(client)

    response = client.post(
        f"/accounts/{owner_account_id}/transactions",
        json={"tipo": "deposito", "valor": "10.00"},
        headers=other_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta nao encontrada."


def test_statement_empty(client, auth_headers):
    account_id = _create_account(client, auth_headers)

    response = client.get(f"/accounts/{account_id}/statement", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["saldo_atual"] == "0.00"
    assert body["transacoes"] == []


def test_statement_after_transactions(client, auth_headers):
    account_id = _create_account(client, auth_headers)
    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "deposito", "valor": "1000.00"},
        headers=auth_headers,
    )
    client.post(
        f"/accounts/{account_id}/transactions",
        json={"tipo": "saque", "valor": "300.00"},
        headers=auth_headers,
    )

    response = client.get(f"/accounts/{account_id}/statement", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["saldo_atual"] == "700.00"
    assert len(body["transacoes"]) == 2
    tipos = {tx["tipo"] for tx in body["transacoes"]}
    assert tipos == {"deposito", "saque"}


def test_statement_account_not_found(client, auth_headers):
    response = client.get("/accounts/999/statement", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Conta nao encontrada."
