class Operator:
    """описує оператора мобільного зв’язку і всі його характеристики та тарифи."""

    def __init__(self, ID: int, talkingCharge: float, messageCost: float,
                 networkCharge: float, discountRate: int) -> None:
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate
        self.customers = set()   # множина клієнтів

    def addCustomer(self, customer) -> None:
        """Додати клієнта і синхронізувати зв’язок"""
        self.customers.add(customer)
        customer.operators.add(self)

    # --- окремі функції для знижок ---
    def getDiscountForTalking(self, customer) -> float:
        if customer.age < 18 or customer.age > 65:
            return 1 - self.discountRate / 100.0
        return 1.0

    def getDiscountForMessage(self, customer, other) -> float:
        if customer in self.customers and other in self.customers:
            return 1 - self.discountRate / 100.0
        return 1.0

    # --- розрахунок вартості ---
    def calculateTalkingCost(self, minute: int, customer) -> float:
        return minute * self.talkingCharge * self.getDiscountForTalking(customer)

    def calculateMessageCost(self, quantity: int, customer, other) -> float:
        return quantity * self.messageCost * self.getDiscountForMessage(customer, other)

    def calculateNetworkCost(self, amount: float) -> float:
        return amount * self.networkCharge

    # --- геттери/сеттери ---
    def getTalkingCharge(self) -> float:
        return self.talkingCharge

    def setTalkingCharge(self, value: float) -> None:
        self.talkingCharge = value

    def getMessageCost(self) -> float:
        return self.messageCost

    def setMessageCost(self, value: float) -> None:
        self.messageCost = value

    def getNetworkCharge(self) -> float:
        return self.networkCharge

    def setNetworkCharge(self, value: float) -> None:
        self.networkCharge = value

    def getDiscountRate(self) -> int:
        return self.discountRate

    def setDiscountRate(self, value: int) -> None:
        self.discountRate = value

    def getCustomers(self):
        return [c.name for c in self.customers]

