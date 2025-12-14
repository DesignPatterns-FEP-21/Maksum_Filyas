# клас для JOIN операцій
from row import Row

class JoinedTable:
    def __init__(self, left_table, right_table, left_column, right_column):
        self.left_table = left_table
        self.right_table = right_table
        self.left_column = left_column
        self.right_column = right_column
        self.rows = self._perform_join()
    
    def _perform_join(self):
        joined_rows = []
        
        for left_row in self.left_table.rows:
            for right_row in self.right_table.rows:
                if left_row[self.left_column] == right_row[self.right_column]:
                    # Об'єднання даних з обох таблиць
                    joined_data = {}
                    
                    # Додаємо дані з лівої таблиці
                    for key in left_row.data:
                        joined_data[f"{self.left_table.name}.{key}"] = left_row[key]
                    
                    # Додаємо дані з правої таблиці
                    for key in right_row.data:
                        joined_data[f"{self.right_table.name}.{key}"] = right_row[key]
                    
                    joined_row = Row(joined_data)
                    joined_rows.append(joined_row)
        
        return joined_rows
    
    def __iter__(self):
        return iter(self.rows)