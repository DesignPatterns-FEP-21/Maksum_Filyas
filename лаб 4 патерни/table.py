#  таблиця бази даних —  колонки, рядки та методи для додавання, видалення, оновлення і перегляду даних із перевіркою типів і ключів.
from row import Row

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = {column.name: column for column in columns}
        self.rows = []
        self.next_id = 1
    
    def __iter__(self):
        return iter(self.rows)
    
    def insert(self, row_data):
        # Валідація даних
        for column_name, column in self.columns.items():
            value = row_data.get(column_name)
            if not column.validate(value):
                raise ValueError(f"Invalid value for column {column_name}: {value}")
        
        # Перевірка унікальності primary key
        for column in self.columns.values():
            if column.primary_key:
                pk_value = row_data.get(column.name)
                for row in self.rows:
                    if row[column.name] == pk_value:
                        raise ValueError(f"Primary key violation: {pk_value} already exists")
        
        # Створення нового рядка
        row = Row(row_data)
        row.id = self.next_id
        self.next_id += 1
        self.rows.append(row)
        return row
    
    def select_all(self):
        return self.rows
    
    def delete(self, condition_func):
        rows_to_delete = [row for row in self.rows if condition_func(row)]
        for row in rows_to_delete:
            self.rows.remove(row)
        return len(rows_to_delete)
    
    def update(self, condition_func, updates):
        updated_count = 0
        for row in self.rows:
            if condition_func(row):
                for key, value in updates.items():
                    if key in self.columns and self.columns[key].validate(value):
                        row[key] = value
                updated_count += 1
        return updated_count