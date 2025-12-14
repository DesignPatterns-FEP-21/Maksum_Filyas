from table import Table
from column import Column
from data_types import IntegerType, StringType, BooleanType, DateTimeType, DateType

class TableBuilder:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []
    
    def add_column(self, name, data_type, nullable=True, primary_key=False, foreign_key=None):
        column = Column(name, data_type, nullable, primary_key, foreign_key)
        self.columns.append(column)
        return self
    
    def build(self, db=None):
        table = Table(self.table_name, self.columns)
        if db:
            db.create_table(table)
        return table

class TableFactory:
    @staticmethod
    def create_table_from_schema(db, table_name, schema):
        type_mapping = {
            "int": IntegerType(),
            "string": StringType(),
            "boolean": BooleanType(),
            "datetime": DateTimeType(),
            "date": DateType()  # Додаємо DateType
        }
        
        columns = []
        for col_def in schema["columns"]:
            data_type = type_mapping.get(col_def["type"])
            if not data_type:
                raise ValueError(f"Unknown data type: {col_def['type']}")
            
            # Для StringType перевіряємо max_length
            if col_def["type"] == "string" and "max_length" in col_def:
                data_type = StringType(max_length=col_def["max_length"])
            
            column = Column(
                name=col_def["name"],
                data_type=data_type,
                nullable=col_def.get("nullable", True),
                primary_key=col_def.get("primary_key", False),
                foreign_key=col_def.get("foreign_key")
            )
            columns.append(column)
        
        table = Table(table_name, columns)
        return db.create_table(table)