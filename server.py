from fastapi import FastAPI, HTTPException, Response, UploadFile
from bank import Bank
import uvicorn
import codecs
from decimal import Decimal

app = FastAPI()
bank = Bank()

@app.post("/account")
async def create_account(account_number: str, initial_balance: Decimal):
    success = await bank.create_account(account_number, initial_balance)
    if success:
        return {"message": f"Account created for {account_number}"}
    raise HTTPException(status_code=400, detail="Account already exists")

@app.post("/deposit")
async def deposit(account_number: str, amount: Decimal):
    success = await bank.deposit(account_number, amount)
    if success:
        return {"message": f"Deposited {amount} to {account_number}'s account"}
    raise HTTPException(status_code=400, detail="Deposit failed")

@app.post("/withdraw")
async def withdraw(account_number: str, amount: Decimal):
    success = await bank.withdraw(account_number, amount)
    if success:
        return {"message": f"Withdrawn {amount} from {account_number}'s account"}
    raise HTTPException(status_code=400, detail="Withdrawal failed")

@app.post("/transfer")
async def transfer(from_account_number: str, to_account_number: str, amount: Decimal):
    success = await bank.transfer(from_account_number, to_account_number, amount)
    if success:
        return {"message": f"Transferred {amount} from {from_account_number} to {to_account_number}"}
    raise HTTPException(status_code=400, detail="Transfer failed")

@app.get("/balance/{account_number}")
async def get_balance(account_number: str):
    try:
        balance = await bank.get_balance(account_number)
        return {"balance": balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/export")
async def export_data():
    data = await bank.export_data()
    return Response(content=data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=bank_data.csv"})

@app.post("/import")
async def import_data(file: UploadFile):
    await bank.import_data(codecs.iterdecode(file.file, 'utf-8'))
    return {"message": "Data imported successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)