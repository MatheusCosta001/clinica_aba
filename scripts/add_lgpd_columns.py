"""
Ajuda para adicionar colunas relacionadas à LGPD caso estejam faltando.
Execute localmente: `python scripts/add_lgpd_columns.py` após ativar seu ambiente virtual.
Este é um auxiliar de migração simples que executa instruções ALTER TABLE quando necessário.
"""
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
            ensure_column(engine, 'usuarios', 'aceite_lgpd BOOLEAN DEFAULT FALSE')
            ensure_column(engine, 'usuarios', 'aceite_lgpd_at TIMESTAMP')
            ensure_column(engine, 'usuarios', 'anonimizado BOOLEAN DEFAULT FALSE')
            ensure_column(engine, 'usuarios', 'anonimizado_em TIMESTAMP')
        except Exception as e:
            print('Erro ao aplicar alterações em usuarios:', e)

        
        try:
            ensure_column(engine, 'pacientes', 'anonimizado BOOLEAN DEFAULT FALSE')
            ensure_column(engine, 'pacientes', 'anonimizado_em TIMESTAMP')
        except Exception as e:
            print('Erro ao aplicar alterações em pacientes:', e)

        
        try:
            ensure_column(engine, 'evolucoes', 'profissional_especialidade VARCHAR(100)')
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
                            paciente_id INTEGER NOT NULL,
                            gerado_por_id INTEGER,
                            gerado_em TIMESTAMP
                        )
                    '''))
        except Exception as e:
            print('Erro ao criar tabela relatorios:', e)

        
        try:
            insp = inspect(engine)
            if 'anonymizations' not in insp.get_table_names():
                print('Criando tabela anonymizations')
                with engine.begin() as conn:
                    conn.execute(text('''
                        CREATE TABLE anonymizations (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            who_id INTEGER,
                            reason VARCHAR(300),
                            "when" TIMESTAMP
                        )
                    '''))
        except Exception as e:
            print('Erro ao criar tabela anonymizations:', e)

    print('Verifique o resultado e rode suas migrations/backup conforme necessário.')
