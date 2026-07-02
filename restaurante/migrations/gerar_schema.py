import sys
import os

# Permite rodar o script de qualquer lugar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.schema import CreateTable

from app import create_app
from app.extensions import db

SAIDA = os.path.join(os.path.dirname(__file__), 'schema.sql')


def gerar_schema():
    app = create_app('development')

    with app.app_context():
        linhas = [
            '-- Gerado automaticamente por migrations/gerar_schema.py',
            '-- Não editar à mão — gere o db dnv após mudar os modelos em app/models/.',
            ''
        ]
        for tabela in db.metadata.sorted_tables:
            ddl = str(CreateTable(tabela).compile(db.engine)).strip()
            linhas.append(f'-- Tabela: {tabela.name}')
            linhas.append(f'{ddl};')
            linhas.append('')

        with open(SAIDA, 'w', encoding='utf-8') as f:
            f.write('\n'.join(linhas))

    print(f'Schema gerado em {SAIDA}')


if __name__ == '__main__':
    gerar_schema()
