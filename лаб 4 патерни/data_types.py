# тут визначено базовий тип DataType і його нащадки для перевірки коректності значень колонок таблиць.
from datetime import datetime

class DataType:
    def validate(self, value):
        return True

class IntegerType(DataType):
    def validate(self, value):
        return value is None or isinstance(value, int)

class StringType(DataType):
    def __init__(self, max_length=255):
        self.max_length = max_length
    
    def validate(self, value):
        return value is None or (isinstance(value, str) and len(value) <= self.max_length)

class BooleanType(DataType):
    def validate(self, value):
        return value is None or isinstance(value, bool)

class DateTimeType(DataType):
    def validate(self, value):
        if value is None:
            return True
        # Перевірка для datetime об'єкта
        if isinstance(value, datetime):
            return True
        # Перевірка для строки у форматі YYYY-MM-DD HH:MM:SS
        if isinstance(value, str):
            try:
                datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                return True
            except ValueError:
                return False
        return False

class DateType(DataType):
    def validate(self, value):
        if value is None:
            return True
        # Перевірка для datetime об'єкта
        if isinstance(value, datetime):
            return True
        # Перевірка для строки у форматі YYYY-MM-DD
        if isinstance(value, str):
            try:
                datetime.strptime(value, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        return False