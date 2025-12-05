from sqlalchemy import inspect, text
from app import create_app, db


app = create_app()


def ensure_column(engine, table, column_sql):
    insp = inspect(engine)
    cols = [c['name'] for c in insp.get_columns(table)]
    col_name = column_sql.split()[0]
    if col_name not in cols:
        print(f"Adding column {col_name} to {table}")
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_sql}"))
    else:
        print(f"Column {col_name} already exists on {table}")


if __name__ == '__main__':
    with app.app_context():
        engine = db.get_engine()
        
        try:
            ensure_column(engine, 'usuarios', 'aceiteLgpd BOOLEAN DEFAULT FALSE')
            ensure_column(engine, 'usuarios', 'aceiteLgpdEm TIMESTAMP')
            ensure_column(engine, 'usuarios', 'anonimizado BOOLEAN DEFAULT FALSE')
            ensure_column(engine, 'usuarios', 'anonimizadoEm TIMESTAMP')
        except Exception as e:
            print('Erro ao aplicar alterações em usuarios:', e)

        
        try:
            ensure_column(engine, 'pacientes', 'anonimizado BOOLEAN DEFAULT FALSE')
            ensure_column(engine, 'pacientes', 'anonimizadoEm TIMESTAMP')
        except Exception as e:
            print('Erro ao aplicar alterações em pacientes:', e)

        
        try:
            ensure_column(engine, 'evolucoes', 'profissionalEspecialidade VARCHAR(100)')
        except Exception as e:
            print('Erro ao aplicar alterações em evolucoes:', e)

        
        try:
            insp = inspect(engine)
            if 'relatorios' not in insp.get_table_names():
                print('Criando tabela relatorios')
                with engine.begin() as conn:
                    conn.execute(text('''
                        CREATE TABLE relatorios (
                            id SERIAL PRIMARY KEY,
                            pacienteId INTEGER NOT NULL,
                            geradoPorId INTEGER,
                            geradoEm TIMESTAMP
                        )
                    '''))
        except Exception as e:
            print('Erro ao criar tabela relatorios:', e)

        
        try:
            insp = inspect(engine)
            if 'anonimizacao' not in insp.get_table_names():
                print('Criando tabela anonimizacao')
                with engine.begin() as conn:
                    conn.execute(text('''
                        CREATE TABLE anonimizacao (
                            id SERIAL PRIMARY KEY,
                            usuarioId INTEGER NOT NULL,
                            quemId INTEGER,
                            motivo VARCHAR(300),
                            "quando" TIMESTAMP
                        )
                    '''))
        except Exception as e:
            print('Erro ao criar tabela anonimizacao:', e)

    print('Verifique o resultado e rode suas migrations/backup conforme necessário.')
