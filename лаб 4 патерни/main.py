from database import Database
from builders import TableBuilder, TableFactory
from data_types import IntegerType, StringType
from query import SimpleQuery
from joined_table import JoinedTable

def main():
    # Створення бази даних (Singleton)
    db = Database("mydb")
    
    print("=== Створення таблиць через Builder ===")
    
    # Створення таблиці users через Builder
    users_builder = TableBuilder("users")
    users_table = (users_builder
        .add_column("id", IntegerType(), primary_key=True, nullable=False)
        .add_column("name", StringType(50), nullable=False)
        .add_column("age", IntegerType(), nullable=True)
        .build(db))
    
    print(f"Створено таблицю: {users_table.name}")
    
    # Додавання даних
    users_table.insert({"id": 1, "name": "Іван", "age": 25})
    users_table.insert({"id": 2, "name": "Марія", "age": 30})
    users_table.insert({"id": 3, "name": "Петро", "age": 35})
    
    print("\n=== Дані в таблиці users ===")
    for row in users_table.select_all():
        print(f"ID: {row.id}, Дані: {row.data}")
    
    print("\n=== Запит до таблиці ===")
    query = SimpleQuery(users_table)
    results = query.select(["name", "age"]).where("age", ">", 25).execute()
    
    for row in results:
        print(f"Ім'я: {row['name']}, Вік: {row['age']}")
    
    
    orders_schema = {
        "columns": [
            {"name": "id", "type": "int", "nullable": False, "primary_key": True},
            {"name": "user_id", "type": "int", "nullable": False},
            {"name": "product", "type": "string", "nullable": False},
            {"name": "price", "type": "int", "nullable": True}
        ]
    }
    
    orders_table = TableFactory.create_table_from_schema(db, "orders", orders_schema)
    
    # Додавання замовлень
    orders_table.insert({"id": 1, "user_id": 1, "product": "Ноутбук", "price": 15000})
    orders_table.insert({"id": 2, "user_id": 2, "product": "Мишка", "price": 500})
    orders_table.insert({"id": 3, "user_id": 1, "product": "Клавіатура", "price": 800})
    
    print("\n=== JOIN запит ===")
    joined = JoinedTable(users_table, orders_table, "id", "user_id")
    
    for row in joined.rows:
        print(f"Користувач: {row['users.name']}, Товар: {row['orders.product']}, Ціна: {row['orders.price']}")
    
    print(f"\nУсі таблиці в базі: {db.list_tables()}")

if __name__ == "__main__":
    main()