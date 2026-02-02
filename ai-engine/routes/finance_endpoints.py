"""
Endpoints de Bolsa de Valores - FastAPI
Wall Street, análisis en vivo, y trading de mercado.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from finance_system.stock_market import stock_market, OrderSide

router = APIRouter(prefix="/api/finance", tags=["finance"])


class MarketOrderRequest(BaseModel):
    player_id: str
    symbol: str
    side: str
    quantity: int


@router.get("/market")
async def get_market_snapshot():
    """Snapshot completo del mercado"""
    try:
        return {
            "success": True,
            "data": stock_market.get_market_snapshot()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/market/tick")
async def tick_market():
    """Actualiza precios (simulación en vivo)"""
    try:
        return {
            "success": True,
            "data": stock_market.tick_market()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks")
async def get_stocks():
    """Lista de acciones"""
    try:
        snapshot = stock_market.get_market_snapshot()
        return {
            "success": True,
            "stocks": snapshot["stocks"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    """Detalle de una acción"""
    try:
        stock = stock_market.get_stock(symbol)
        if not stock:
            raise HTTPException(status_code=404, detail="Acción no encontrada")
        return {
            "success": True,
            "stock": stock.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orders")
async def place_order(request: MarketOrderRequest):
    """Coloca una orden de compra/venta"""
    try:
        try:
            side_enum = OrderSide[request.side.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail="Side inválido. Usa buy/sell.")

        result = stock_market.place_order(
            request.player_id,
            request.symbol,
            side_enum,
            request.quantity
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return {
            "success": True,
            "order": result["order"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio/{player_id}")
async def get_portfolio(player_id: str):
    """Portafolio del jugador"""
    try:
        return {
            "success": True,
            "portfolio": stock_market.get_portfolio(player_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai/traders")
async def get_ai_traders():
    """Lista de traders IA activos"""
    try:
        return {
            "success": True,
            "traders": stock_market.get_ai_traders()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
