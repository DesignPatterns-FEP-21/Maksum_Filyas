import json

class Database:
    _instance = None
    
    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.tables = {}
        return cls._instance
    
    def create_table(self, table):
        # Перевірка foreign keys
        for column in table.columns.values():
            if column.foreign_key:
                foreign_table_name, foreign_column_name = column.foreign_key
                if foreign_table_name not in self.tables:
                    raise ValueError(f"Foreign table {foreign_table_name} does not exist")
                
                foreign_table = self.tables[foreign_table_name]
                if foreign_column_name not in foreign_table.columns:
                    raise ValueError(f"Foreign column {foreign_column_name} does not exist in table {foreign_table_name}")
        
        self.tables[table.name] = table
        return table
    
    def get_table(self, table_name):
        return self.tables.get(table_name)
    
    def drop_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]
            return True
        return False
    
    def table_exists(self, table_name):
        return table_name in self.tables
    
    def list_tables(self):
        return list(self.tables.keys())
    
    