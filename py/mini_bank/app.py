from fastapi import FastAPI
from pydantic import BaseModel, Field
from models.manager import BankManager

app = FastAPI()
manager = BankManager("bank.db")
manager.create_table()

class RegisterRequest(BaseModel):
    name: str
    account_type: str

class DepositRequest(BaseModel):
    account_id: int
    amount: float = Field(gt=0)

class WithdrawalRequest(BaseModel):
    account_id: int
    amount: float = Field(gt=0)

@app.post("/register")
def register(request: RegisterRequest):
    result = manager.register(request.name, request.account_type)
    return result 

@app.post("/deposit")
def deposit(request: DepositRequest):
    manager.deposit(request.account_id, request.amount)
    return {"message": "deposit successful"}

@app.post("/withdrawal")
def withdrawal(request: WithdrawalRequest):
    manager.withdrawal(request.account_id, request.amount)
    return{"message": "withdrawal successful"}

@app.get("/balance/{account_id}")
def get_balance(account_id: int):
    balance = manager.get_balance(account_id)
    return {"balance": balance}

@app.get("/transactions/{account_id}")
def get_transactions(account_id: int):
    result = manager.get_transactions(account_id)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)