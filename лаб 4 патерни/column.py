# тут зберігається опис колонки таблиці — її назва, тип даних, nullable, primary key, foreign key та метод validate() для перевірки значень.c
class Column:
    def __init__(self, name, data_type, nullable=True, primary_key=False, foreign_key=None):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable # показує, чи може колонка мати порожнє значення (None).
        self.primary_key = primary_key  # вказує, що ця колонка є унікальним ідентифікатором рядків у таблиці (наприклад, id).
        self.foreign_key = foreign_key  # (table_name, column_name) задає зв’язок з іншою таблицею,
    

    # метод, який перевіряє, чи значення відповідає типу даних
    def validate(self, value):
        if value is None:
            return self.nullable
        return self.data_type.validate(value)