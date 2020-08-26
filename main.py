import yfinance
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from models import Base
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Stock

from fastapi.encoders import jsonable_encoder


Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates("templates")


class StockRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def dashboard(request: Request, forward_pe = None, dividend_yield = None, ma_50 = None, ma_200 = None, db: Session = Depends(get_db)):
    """ Dashboard
    """
    stocks = db.query(Stock)

    if forward_pe is not None:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)


    print(stocks)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "stocks": stocks
    })


def fetch_stock_data(id: id):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()

    # stock.forward_pe = 10

    yahoo_data = yfinance.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info["twoHundredDayAverage"]
    stock.ma50 = yahoo_data.info["fiftyDayAverage"]
    stock.price = yahoo_data.info["previousClose"]
    stock.forward_pe = yahoo_data.info["forwardPE"]
    stock.forward_eps = yahoo_data.info["forwardEps"]
    
    if yahoo_data.info["dividendYield"] is not None:
        stock.dividend_yield = yahoo_data.info["dividendYield"]

    db.add(stock)
    db.commit()


@app.post("/stock/")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """ Method to create stock
    """
    stock = Stock()
    stock.symbol = stock_request.symbol

    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {
        "code": "sucess",
        "message": f"stock {stock_request.symbol} created"
    }


# @app.get("/stock/")
# def get_stock():
#     db = SessionLocal()
#     stocks = db.query(Stock).all()
#     stocks_json = jsonable_encoder(stocks)
#     return {"my_stock": stocks_json}