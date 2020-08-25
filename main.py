from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates("templates")


@app.get("/")
def dashboard(request: Request):
    """ Dashboard
    """
    return templates.TemplateResponse("home.html", {
        "request": request
    })


@app.post("/stock")
def create_stock():
    """ Method to create stock
    """
    return {
        "code": "sucess",
        "message": "stock created"
    }

