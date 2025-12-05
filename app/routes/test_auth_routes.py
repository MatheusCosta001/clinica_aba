def test_register_user(client):
    response = client.post("/register", data={
        "nome": "Usuário Teste",
        "email": "teste@example.com",
        "senha": "Teste@123456",
        "confirmar_senha": "Teste@123456",
        "papel": "profissional",
        "aceiteLgpd": "on"
    }, follow_redirects=True)


    assert response.status_code == 200
    assert b"Entrar" in response.data or b"Login" in response.data or b"Cadastro realizado" in response.data



def test_login_user(client):
  
    client.post("/register", data={
        "nome": "Maria",
        "email": "maria@example.com",
        "senha": "Maria@123456",
        "confirmar_senha": "Maria@123456",
        "papel": "profissional",
        "aceiteLgpd": "on"
    })
    
    
    response = client.post("/login", data={
        "email": "maria@example.com",
        "senha": "Maria@123456"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"Bem-vindo" in response.data
