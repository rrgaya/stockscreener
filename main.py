from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from models import Base
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates("templates")


class StockRequest(BaseModel):
    symbol: str



@app.get("/")
def dashboard(request: Request):
    """ Dashboard
    """
    return templates.TemplateResponse("home.html", {
        "request": request
    })


@app.post("/stock")
def create_stock(stock_request: StockRequest):
    """ Method to create stock
    """
    return {
        "code": "sucess",
        "message": f"stock {stock_request.symbol} created"
    }

