def test_register_user(client):
    response = client.post("/register", data={
        "nome": "Usuário Teste",
        "email": "teste@example.com",
        "senha": "1234",
        "confirmar_senha": "1234"
    }, follow_redirects=True)


    assert response.status_code == 200
    assert b"Entrar" in response.data or b"Login" in response.data or b"Cadastro realizado" in response.data



def test_login_user(client):
  
    client.post("/register", data={
        "nome": "Maria",
        "email": "maria@example.com",
        "senha": "1234",
        "confirmar_senha": "1234"
    })
    
    
    response = client.post("/login", data={
        "email": "maria@example.com",
        "senha": "1234"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"Bem-vindo" in response.data
