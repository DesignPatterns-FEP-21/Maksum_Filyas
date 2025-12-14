import unittest
from datetime import datetime
from data_types import IntegerType, StringType, BooleanType, DateTimeType, DateType
from column import Column
from table import Table

class TestDatabase(unittest.TestCase):
    
    def test_1_integer_validation(self):
        """Тест валідації IntegerType"""
        int_type = IntegerType()
        self.assertTrue(int_type.validate(10))
        self.assertTrue(int_type.validate(None))
        self.assertTrue(int_type.validate(0))
        self.assertFalse(int_type.validate("10"))  # Повинно бути False для строки
        self.assertFalse(int_type.validate(10.5))  # Повинно бути False для float
    
    def test_2_string_validation(self):
        """Тест валідації StringType з обмеженням довжини"""
        string_type = StringType(max_length=5)
        self.assertTrue(string_type.validate("hello"))
        self.assertTrue(string_type.validate(None))
        self.assertTrue(string_type.validate("hi"))
        self.assertFalse(string_type.validate("hello world"))  # Занадто довга строка
        self.assertFalse(string_type.validate(123))  # Не строка
    
    def test_3_datetime_validation(self):
        """Тест валідації DateTimeType"""
        datetime_type = DateTimeType()
        # Коректні значення
        self.assertTrue(datetime_type.validate(datetime.now()))
        self.assertTrue(datetime_type.validate("2024-01-15 14:30:00"))
        self.assertTrue(datetime_type.validate(None))
        # Некоректні значення
        self.assertFalse(datetime_type.validate("2024-01-15"))  # Немає часу
        self.assertFalse(datetime_type.validate("15.01.2024"))  # Неправильний формат
        self.assertFalse(datetime_type.validate(12345))
    
    def test_4_date_validation(self):
        """Тест валідації DateType"""
        date_type = DateType()
        # Коректні значення
        self.assertTrue(date_type.validate(datetime.now()))
        self.assertTrue(date_type.validate("2024-01-15"))
        self.assertTrue(date_type.validate(None))
        # Некоректні значення
        self.assertFalse(date_type.validate("2024-01-15 14:30:00"))  # Містить час
        self.assertFalse(date_type.validate("15.01.2024"))  # Неправильний формат
        self.assertFalse(date_type.validate(12345))
    
    def test_5_column_validation(self):
        """Тест валідації колонки з різними типами даних"""
        # Колонка з IntegerType, не nullable
        int_column = Column("age", IntegerType(), nullable=False)
        self.assertTrue(int_column.validate(25))
        self.assertFalse(int_column.validate(None))  # Не може бути null
        
        # Колонка з DateTimeType, nullable
        date_column = Column("created_at", DateTimeType(), nullable=True)
        self.assertTrue(date_column.validate("2024-01-15 10:00:00"))
        self.assertTrue(date_column.validate(None))  # Може бути null
        self.assertFalse(date_column.validate("invalid date"))  # Неправильна дата

if __name__ == '__main__':
    unittest.main()