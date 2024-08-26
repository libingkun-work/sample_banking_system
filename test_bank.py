import asyncio
import unittest
from bank import Bank
from pydantic import ValidationError

class TestBank(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bank = Bank()
        await self.bank.create_account("100000", 1000)
        await self.bank.create_account("200000", 500)

    async def test_create_account(self):
        self.assertTrue(await self.bank.create_account("300000", 200))
        self.assertFalse(await self.bank.create_account("100000", 100))

    async def test_deposit(self):
        self.assertTrue(await self.bank.deposit("100000", 200))
        self.assertEqual(await self.bank.get_balance("100000"), 1200)
        self.assertFalse(await self.bank.deposit("100000", -100))

    async def test_withdraw(self):
        self.assertTrue(await self.bank.withdraw("200000", 200))
        self.assertEqual(await self.bank.get_balance("200000"), 300)
        self.assertFalse(await self.bank.withdraw("200000", 400))

    async def test_transfer(self):
        self.assertTrue(await self.bank.transfer("100000", "200000", 300))
        self.assertEqual(await self.bank.get_balance("100000"), 700)
        self.assertEqual(await self.bank.get_balance("200000"), 800)
        self.assertFalse(await self.bank.transfer("100000", "200000", 1000))

    async def test_concurrent_transfers(self):
        await self.bank.create_account("300000", 1000)

        async def transfer(from_name, to_name, amount):
            await self.bank.transfer(from_name, to_name, amount)

        tasks = []
        for _ in range(6):
            tasks.append(asyncio.create_task(transfer("100000", "200000", 50)))
            tasks.append(asyncio.create_task(transfer("200000", "300000", 50)))
            tasks.append(asyncio.create_task(transfer("300000", "100000", 50)))

        await asyncio.gather(*tasks)

        self.assertEqual(await self.bank.get_balance("100000"), 1000)
        self.assertEqual(await self.bank.get_balance("200000"), 500)
        self.assertEqual(await self.bank.get_balance("300000"), 1000)

    async def test_negative_balance(self):
        with self.assertRaises(ValidationError):
            await self.bank.create_account("David", -100)

if __name__ == '__main__':
    unittest.main()