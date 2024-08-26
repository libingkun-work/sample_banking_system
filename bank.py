import csv
import asyncio
from io import StringIO
from account import Account
from typing import Dict
from typing import TextIO
from decimal import Decimal


class Bank:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.locks: Dict[str, asyncio.Lock] = {}
        self.global_lock: asyncio.Lock = asyncio.Lock()

    async def create_account(self, account_number: str, initial_balance: Decimal) -> bool:
        async with self.global_lock:
            if account_number not in self.accounts:
                self.accounts[account_number] = Account(account_number=account_number, balance=initial_balance)
                self.locks[account_number] = asyncio.Lock()
                return True
            return False

    async def deposit(self, account_number: str, amount: Decimal) -> bool:
        if account_number in self.accounts:
            return await self.accounts[account_number].deposit(amount)
        return False

    async def withdraw(self, account_number: str, amount: Decimal) -> bool:
        if account_number in self.accounts:
            async with self.locks[account_number]:
                return await self.accounts[account_number].withdraw(amount)
        return False

    async def transfer(self, from_account: str, to_account: str, amount: Decimal) -> bool:
        if from_account in self.accounts and to_account in self.accounts and amount > 0:
            async with self.locks[from_account]:
                if await self.accounts[from_account].withdraw(amount):
                    await self.accounts[to_account].deposit(amount)
                    return True
        return False

    async def get_balance(self, account_number: str) -> Decimal:
        if account_number in self.accounts:
            async with self.locks[account_number]:
                return self.accounts[account_number].balance
        raise ValueError(f"Account {account_number} not found")
    
    async def export_data(self) -> str:
        output = StringIO()
        writer = csv.writer(output)
        for account in self.accounts.values():
            writer.writerow([account.account_number, account.balance])
        return output.getvalue()

    async def import_data(self, file: TextIO):
        reader = csv.reader(file)
        self.accounts = {}
        for row in reader:
            if len(row) == 2:
                account_number, balance = row
                await self.create_account(account_number, Decimal(balance))