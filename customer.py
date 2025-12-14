from bill import Bill
from operator_class import Operator

class Customer:
    """Holds customer details"""

    def __init__(self, ID: int, name: str, age: int,
                 operator: Operator, bill: Bill, limitingAmount: float) -> None:
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = set()   # множина всіх операторів
        self.bill = bill
        self.bill.changeTheLimit(limitingAmount)

        # одразу прив’язуємо до початкового оператора
        self.addOperator(operator)

    def addOperator(self, operator: Operator) -> None:
        """Прив’язати клієнта до оператора"""
        self.operators.add(operator)
        operator.customers.add(self)

    def talk(self, minute: int, other: "Customer") -> None:
        # беремо першого оператора (поточний, для прикладу)
        operator = next(iter(self.operators))
        cost = operator.calculateTalkingCost(minute, self)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f"{self.name} talked with {other.name} for {minute} minutes. Cost={cost}")
        else:
            print("Talk failed: limit exceeded")

    def message(self, quantity: int, other: "Customer") -> None:
        operator = next(iter(self.operators))
        cost = operator.calculateMessageCost(quantity, self, other)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f"{self.name} sent {quantity} messages to {other.name}. Cost={cost}")
        else:
            print("❌ Message failed: limit exceeded")

    def connection(self, amount: float) -> None:
        operator = next(iter(self.operators))
        cost = operator.calculateNetworkCost(amount)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f"{self.name} used {amount} MB internet. Cost={cost}")
        else:
            print("❌ Connection failed: limit exceeded")

    def pay(self, amount: float) -> None:
        self.bill.pay(amount)
        print(f"{self.name} paid {amount}. Current debt={self.bill.getCurrentDebt()}")

    def changeOperator(self, new_operator: Operator) -> None:
        self.addOperator(new_operator)
        print(f"{self.name} now also connected to Operator {new_operator.ID}")

    def changeBillLimit(self, amount: float) -> None:
        self.bill.changeTheLimit(amount)
        print(f"{self.name} changed bill limit to {amount}")

    # --- геттери/сеттери ---
    def getAge(self) -> int:
        return self.age

    def setAge(self, age: int) -> None:
        self.age = age

    def getBill(self) -> Bill:
        return self.bill

    def setBill(self, bill: Bill) -> None:
        self.bill = bill

    def getOperators(self):
        return [op.ID for op in self.operators]
