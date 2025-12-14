# Цей клас реалізує SQL-подібний запит до таблиці, дозволяючи вибирати колонки (select), 
# фільтрувати рядки (where) і сортувати їх (order_by), а метод execute повертає відфільтровані, відсортовані та вибрані рядки.
from row import Row

class SimpleQuery:
    def __init__(self, table):
        self.table = table
        self.selected_columns = None
        self.filter_conditions = []
        self.sort_column = None
        self.sort_ascending = True
    
    def select(self, columns):
        self.selected_columns = columns
        return self
    
    def where(self, column, operator, value):
        self.filter_conditions.append((column, operator, value))
        return self
    
    def order_by(self, column, ascending=True):
        self.sort_column = column
        self.sort_ascending = ascending
        return self
    
    def _apply_condition(self, row, column, operator, value):
        row_value = row[column]
        
        if operator == "=":
            return row_value == value
        elif operator == "!=":
            return row_value != value
        elif operator == ">":
            return row_value > value
        elif operator == "<":
            return row_value < value
        elif operator == ">=":
            return row_value >= value
        elif operator == "<=":
            return row_value <= value
        elif operator == "like":
            return str(value) in str(row_value)
        else:
            return False
    
    def execute(self):
        # Фільтрація рядків
        filtered_rows = self.table.rows.copy()
        
        for column, operator, value in self.filter_conditions:
            filtered_rows = [row for row in filtered_rows 
                           if self._apply_condition(row, column, operator, value)]
        
        # Сортування
        if self.sort_column:
            filtered_rows.sort(
                key=lambda row: row[self.sort_column] if row[self.sort_column] is not None else "",
                reverse=not self.sort_ascending
            )
        
        # Вибір колонок
        results = []
        for row in filtered_rows:
            if self.selected_columns:
                new_row_data = {col: row[col] for col in self.selected_columns if col in row.data}
                new_row = Row(new_row_data)
                new_row.id = row.id
                results.append(new_row)
            else:
                results.append(row)
        
        return results