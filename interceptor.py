from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/listen/strategy/signal")
async def listen_strategy_signal(request: Request):
    entry_order = None
    stop_order = None

    body = await request.json()
    resp = { "data": body }
    print(body)
    
    signal_str = "Strategy: {}\n Symbol: {}\n Close: {}".format(body["strategy"], body["signal"]["symbol"], body["signal"]["close"])
    from telegram_signal import send_message
    send_message(signal_str)

    from order_processor import place_order
    entry_order, stop_order = place_order(body["signal"]["symbol"])

    if entry_order is not None:
        from order_risk_management import open_monitor_terminal
        open_monitor_terminal(entry_order, stop_order)
    return resp
