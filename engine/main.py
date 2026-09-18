import asyncio
import websockets
from mt5_engine import MKProEngine

engine = MKProEngine()

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        if data["command"] == "START":
            await engine.start_trading(data["symbol"], data["strategy"], data["risk"])
        elif data["command"] == "STOP":
            engine.running = False
        elif data["command"] == "CLOSE_ALL":
            engine.close_all_positions()

asyncio.run(websockets.serve(handler, "0.0.0.0", 8765))