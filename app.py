from flask import Flask
from config import Config
from models import db
from routes.patient_routes import patient_bp
from routes.evolution_routes import evolution_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco
db.init_app(app)

with app.app_context():
    db.create_all()  # Cria todas as tabelas automaticamente
    print("Tabelas criadas com sucesso!")

# Registra as rotas
app.register_blueprint(patient_bp)
app.register_blueprint(evolution_bp)

if __name__ == "__main__":
    app.run(debug=True)
