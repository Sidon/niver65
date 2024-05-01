from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import MetaData

# Define metadados para gerenciamento de tabelas
metadata = MetaData(schema="base")

# Cria a classe base declarativa
ORMBase = declarative_base(metadata=metadata)
