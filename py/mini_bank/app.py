from fastapi import FastAPI
from pydantic import BaseModel, Field
from models.manager import BankManager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")

app = FastAPI()
manager = BankManager("bank.db")
manager.create_table()

class LoginRequest(BaseModel):
    name: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    password: str
    account_type: str

class DepositRequest(BaseModel):
    account_id: int
    amount: float = Field(gt=0)

class WithdrawalRequest(BaseModel):
    account_id: int
    amount: float = Field(gt=0)

@app.post("/register")
def register(request: RegisterRequest):
    result = manager.register(request.name, request.password, request.account_type)
    return result

@app.post("/login")
def login(request: LoginRequest):
    token = manager.login(request.name, request.password)
    return {"token": token}

@app.post("/deposit")
def deposit(request: DepositRequest, user_id: int = Depends(get_current_user)):
    manager.deposit(request.account_id, request.amount)
    return {"message": "deposit successful"}

@app.post("/withdrawal")
def withdrawal(request: WithdrawalRequest, user_id: int = Depends(get_current_user)):
    manager.withdrawal(request.account_id, request.amount)
    return{"message": "withdrawal successful"}

@app.get("/balance/{account_id}")
def get_balance(account_id: int, user_id: int = Depends(get_current_user)):
    balance = manager.get_balance(account_id)
    return {"balance": balance}

@app.get("/transactions/{account_id}")
def get_transactions(account_id: int, user_id: int = Depends(get_current_user)):
    result = manager.get_transactions(account_id)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)