from abc import ABC, abstractmethod


# 1. ABSTRACTION & 3. POLYMORPHISM: Abstract Base Class
class Account(ABC):

  def __init__(self, account_number: str, currency: str, initial_balance: float):
    self.__account_number = account_number  # Encapsulation
    self.__currency = currency
    self.__balance = max(
        0.0, initial_balance
    )  # Validation: no negative initial balance

  # Getter for Encapsulation
  @property
  def balance(self) -> float:
    return self.__balance

  @property
  def account_number(self) -> str:
    return self.__account_number

  @property
  def currency(self) -> str:
    return self.__currency

  def deposit(self, amount: float) -> None:
    if amount <= 0:
      raise ValueError("Deposit amount must be positive.")
    self.__balance += amount

  def withdraw(self, amount: float) -> None:
    if amount <= 0:
      raise ValueError("Withdrawal amount must be positive.")
    if amount > self.__balance:
      raise ValueError("Insufficient funds.")
    self.__balance -= amount

  # Protected helper for subclasses to modify balance safely
  def _adjust_balance(self, amount: float) -> None:
    self.__balance += amount

  @abstractmethod
  def accrue_interest(self) -> None:
    pass

  @abstractmethod
  def deduct_fees(self) -> None:
    pass


# 2. INHERITANCE: Savings Account
class SavingsAccount(Account):
  INTEREST_RATE = 0.02
  MONTHLY_FEE = 5.00

  def accrue_interest(self) -> None:
    interest = self.balance * self.INTEREST_RATE
    self._adjust_balance(interest)

  def deduct_fees(self) -> None:
    if self.balance >= self.MONTHLY_FEE:
      self._adjust_balance(-self.MONTHLY_FEE)


# 2. INHERITANCE: Checking Account
class CheckingAccount(Account):
  OVERDRAFT_FEE = 15.00

  def accrue_interest(self) -> None:
    pass  # Checking accounts typically earn no interest

  def deduct_fees(self) -> None:
    # Example: fee if balance drops below threshold
    if self.balance < 100.0:
      self._adjust_balance(-self.OVERDRAFT_FEE)


# 2. INHERITANCE: High-Yield Account
class HighYieldAccount(Account):
  INTEREST_RATE = 0.05
  MONTHLY_FEE = 10.00

  def accrue_interest(self) -> None:
    interest = self.balance * self.INTEREST_RATE
    self._adjust_balance(interest)

  def deduct_fees(self) -> None:
    self._adjust_balance(-self.MONTHLY_FEE)


# 3. POLYMORPHIC TRANSACTION DISPATCHER
class LedgerEngine:

  @staticmethod
  def process_monthly_ledger(accounts: list[Account]) -> None:
    for acc in accounts:
      acc.accrue_interest()
      acc.deduct_fees()