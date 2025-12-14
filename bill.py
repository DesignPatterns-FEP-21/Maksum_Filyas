class Bill:
    """зберігає ліміт витрат (limitingAmount) і поточний борг (currentDebt)."""

    def __init__(self, limitingAmount: float) -> None:
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def __str__(self) -> str:
        return f"Bill(limit={self.limitingAmount}, currentDebt={self.currentDebt})"

    # перевіряє, чи можна додати певну суму до боргу, не перевищивши ліміт.
    def check(self, amount: float) -> bool:
        return (self.currentDebt + amount) <= self.limitingAmount

    # додає суму до боргу, якщо не перевищується ліміт.
    def add(self, amount: float) -> None:
        if self.check(amount):
            self.currentDebt += amount
        else:
            raise ValueError("Limit exceeded!")

    # зменшує борг на певну суму
    def pay(self, amount: float) -> None:
        self.currentDebt = max(0, self.currentDebt - amount)

    def changeTheLimit(self, amount: float) -> None:
        self.limitingAmount = amount

    # Getters
    def getLimitingAmount(self) -> float:
        return self.limitingAmount

    def getCurrentDebt(self) -> float:
        return self.currentDebt
