from tinydb import table
from nutritionist.database.engine import Engine

## BaseRepository é a classe base para todos os repositórios, fornecendo a conexão com o banco de dados e as operações básicas de CRUD.

class BaseRepository(Engine):
    def get_table(self, table_name: str) -> table.Table:
        return self.db.table(table_name)
