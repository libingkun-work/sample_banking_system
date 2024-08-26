from pydantic import BaseModel, Field, validator
from typing import Dict
from decimal import Decimal

class Account(BaseModel):
    account_number: str
    balance: Decimal = Field(ge=Decimal('0.00'))

    @validator('account_number')
    def account_number_must_be_six_digits(cls, v):
        if not v.isdigit() or len(v) != 6:
            raise ValueError('Account number must be a 6-digit string')
        return v
    
    @validator('balance')
    def balance_must_be_positive(cls, v):
        if v < Decimal('0.00'):
            raise ValueError('Balance must be non-negative')
        return v

    async def deposit(self, amount: Decimal) -> bool:
        if amount > Decimal('0.00'):
            self.balance += amount
            return True
        return False

    async def withdraw(self, amount: Decimal) -> bool:
        if amount > Decimal('0.00') and self.balance >= amount:
            self.balance -= amount
            return True
        return False