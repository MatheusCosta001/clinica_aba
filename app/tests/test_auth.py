def test_register_user(client):
    response = client.post("/register", data={
        "nome": "Usuário Teste",
        "email": "teste@example.com",
        "senha": "1234",
        "confirmar_senha": "1234"
    }, follow_redirects=True)

    # O esperado é que o servidor redirecione para a página de login
    # ou exiba alguma mensagem de sucesso
    assert response.status_code == 200
    assert b"Entrar" in response.data or b"Login" in response.data or b"Cadastro realizado" in response.data



def test_login_user(client):
    # primeiro registra
    client.post("/register", data={
        "nome": "Maria",
        "email": "maria@example.com",
        "senha": "1234",
        "confirmar_senha": "1234"
    })
    
    # depois tenta logar
    response = client.post("/login", data={
        "email": "maria@example.com",
        "senha": "1234"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"Bem-vindo" in response.data
