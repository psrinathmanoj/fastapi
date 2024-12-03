from fastapi import FastAPI
import yfinance as yf
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# fast api to get all the stock data from yahoo finance package
@app.get("/stock")
def get_stock_data(symbol: str):
    stock_data = yf.Ticker(symbol)
    return stock_data.history(period="1d", interval="1m")

@app.get("/health")
def health_check():
    return {"status": "Healthy"}
