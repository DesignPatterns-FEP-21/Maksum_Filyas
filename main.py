from customer import Customer
from operator_class import Operator
from bill import Bill

def main():
    customers = []
    operators = []
    bills = []

    # створюємо операторів
    op1 = Operator(0, 1.0, 0.5, 0.1, 20)
    op2 = Operator(1, 0.8, 0.4, 0.2, 10)
    operators.extend([op1, op2])

    # створюємо білли
    b1 = Bill(100)
    b2 = Bill(200)
    bills.extend([b1, b2])

    # створюємо клієнтів
    c1 = Customer(0, "Alice", 17, op1, b1, 100)
    c2 = Customer(1, "Bob", 30, op2, b2, 200)
    customers.extend([c1, c2])

    # симуляція
    c1.talk(10, c2)
    c1.message(5, c2)
    c2.connection(50)
    c1.pay(5)
    c2.changeBillLimit(300)
    c1.changeOperator(op2)  # тепер Alice має двох операторів

    print("\n=== Final Bills ===")
    for c in customers:
        print(f"{c.name}: Limit={c.getBill().getLimitingAmount()}, Debt={c.getBill().getCurrentDebt()}")

    print("\n=== Operator Customers ===")
    for op in operators:
        print(f"Operator {op.ID}: {op.getCustomers()}")

    print("\n=== Customer Operators ===")
    for c in customers:
        print(f"{c.name}: {c.getOperators()}")

if __name__ == "__main__":
    main()
