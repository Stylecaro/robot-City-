"""
Sistema de Bolsa de Valores - Ciudad Robot Metaverso
Mercado financiero simulado con seguimiento en vivo, IA traders y sectores.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import random


class MarketSector(Enum):
    """Sectores del mercado"""
    TECHNOLOGY = "technology"
    ENERGY = "energy"
    DEFENSE = "defense"
    WORKFORCE = "workforce"
    MEDICAL = "medical"
    REAL_ESTATE = "real_estate"
    INDUSTRIAL = "industrial"


class OrderSide(Enum):
    """Tipo de orden"""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """Estado de la orden"""
    PENDING = "pending"
    FILLED = "filled"
    REJECTED = "rejected"


@dataclass
class Stock:
    symbol: str
    name: str
    sector: MarketSector
    price: float
    change: float = 0.0
    change_percent: float = 0.0
    volume: int = 0
    last_update: str = field(default_factory=lambda: datetime.now().isoformat())
    history: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "sector": self.sector.value,
            "price": round(self.price, 2),
            "change": round(self.change, 2),
            "change_percent": round(self.change_percent, 2),
            "volume": self.volume,
            "last_update": self.last_update,
            "history": self.history[-50:]
        }


@dataclass
class MarketOrder:
    order_id: str
    player_id: str
    symbol: str
    side: OrderSide
    quantity: int
    price: float
    status: OrderStatus
    created_at: str

    def to_dict(self) -> Dict:
        return {
            "order_id": self.order_id,
            "player_id": self.player_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "quantity": self.quantity,
            "price": round(self.price, 2),
            "status": self.status.value,
            "created_at": self.created_at
        }


@dataclass
class AITrader:
    trader_id: str
    name: str
    strategy: str
    risk_level: int

    def to_dict(self) -> Dict:
        return {
            "trader_id": self.trader_id,
            "name": self.name,
            "strategy": self.strategy,
            "risk_level": self.risk_level
        }


class StockMarket:
    """Mercado de valores con actualización en vivo"""

    def __init__(self):
        self.stocks: Dict[str, Stock] = {}
        self.orders: List[MarketOrder] = []
        self.portfolios: Dict[str, Dict[str, int]] = {}
        self.ai_traders: List[AITrader] = []
        self._initialize_market()

    def _initialize_market(self):
        """Inicializa acciones base"""
        base_stocks = [
            ("RBTX", "Robotex Dynamics", MarketSector.TECHNOLOGY, 120.50),
            ("ENRG", "Quantum Energy Grid", MarketSector.ENERGY, 88.20),
            ("DEFN", "Cyber Defense Corp", MarketSector.DEFENSE, 142.35),
            ("WORK", "WorkForce Nexus", MarketSector.WORKFORCE, 52.80),
            ("MEDI", "Medical AI Labs", MarketSector.MEDICAL, 96.75),
            ("REAL", "Neo Real Estate", MarketSector.REAL_ESTATE, 73.40),
            ("INDU", "Industrial Robotics", MarketSector.INDUSTRIAL, 110.10)
        ]

        for symbol, name, sector, price in base_stocks:
            self.stocks[symbol] = Stock(
                symbol=symbol,
                name=name,
                sector=sector,
                price=price,
                history=[price]
            )

        self.ai_traders = [
            AITrader(str(uuid.uuid4()), "Atlas", "trend_following", 3),
            AITrader(str(uuid.uuid4()), "Nova", "mean_reversion", 2),
            AITrader(str(uuid.uuid4()), "Helix", "momentum", 4),
            AITrader(str(uuid.uuid4()), "Orion", "defensive", 1)
        ]

    def tick_market(self) -> Dict:
        """Actualiza precios de mercado"""
        updates = []
        for stock in self.stocks.values():
            drift = random.uniform(-0.8, 1.2)
            volatility = random.uniform(0.5, 2.5)
            change = drift * volatility

            old_price = stock.price
            stock.price = max(1.0, stock.price + change)
            stock.change = stock.price - old_price
            stock.change_percent = (stock.change / old_price) * 100
            stock.volume += random.randint(100, 2000)
            stock.last_update = datetime.now().isoformat()
            stock.history.append(round(stock.price, 2))

            updates.append({
                "symbol": stock.symbol,
                "price": round(stock.price, 2),
                "change": round(stock.change, 2),
                "change_percent": round(stock.change_percent, 2)
            })

        self._simulate_ai_trades()

        return {
            "timestamp": datetime.now().isoformat(),
            "updates": updates
        }

    def _simulate_ai_trades(self):
        """Simula operaciones de traders IA"""
        for trader in self.ai_traders:
            stock = random.choice(list(self.stocks.values()))
            side = random.choice([OrderSide.BUY, OrderSide.SELL])
            quantity = random.randint(10, 200)
            order = MarketOrder(
                order_id=str(uuid.uuid4()),
                player_id=trader.trader_id,
                symbol=stock.symbol,
                side=side,
                quantity=quantity,
                price=stock.price,
                status=OrderStatus.FILLED,
                created_at=datetime.now().isoformat()
            )
            self.orders.append(order)

    def get_market_snapshot(self) -> Dict:
        """Resumen de mercado"""
        return {
            "timestamp": datetime.now().isoformat(),
            "stocks": [s.to_dict() for s in self.stocks.values()],
            "top_gainers": self._get_top_movers(gainers=True),
            "top_losers": self._get_top_movers(gainers=False)
        }

    def _get_top_movers(self, gainers: bool = True) -> List[Dict]:
        """Top alzas/bajas"""
        sorted_stocks = sorted(
            self.stocks.values(),
            key=lambda s: s.change_percent,
            reverse=gainers
        )
        return [s.to_dict() for s in sorted_stocks[:3]]

    def get_stock(self, symbol: str) -> Optional[Stock]:
        return self.stocks.get(symbol.upper())

    def place_order(self, player_id: str, symbol: str, side: OrderSide, quantity: int) -> Dict:
        """Coloca una orden de mercado"""
        stock = self.get_stock(symbol)
        if not stock:
            return {"error": "Acción no encontrada"}

        if quantity <= 0:
            return {"error": "Cantidad inválida"}

        order = MarketOrder(
            order_id=str(uuid.uuid4()),
            player_id=player_id,
            symbol=stock.symbol,
            side=side,
            quantity=quantity,
            price=stock.price,
            status=OrderStatus.FILLED,
            created_at=datetime.now().isoformat()
        )
        self.orders.append(order)

        # Actualizar portafolio
        portfolio = self.portfolios.setdefault(player_id, {})
        current_qty = portfolio.get(stock.symbol, 0)
        if side == OrderSide.BUY:
            portfolio[stock.symbol] = current_qty + quantity
        else:
            portfolio[stock.symbol] = max(0, current_qty - quantity)

        return {
            "success": True,
            "order": order.to_dict()
        }

    def get_portfolio(self, player_id: str) -> Dict:
        """Portafolio del jugador"""
        holdings = self.portfolios.get(player_id, {})
        detailed = []
        total_value = 0.0

        for symbol, qty in holdings.items():
            stock = self.get_stock(symbol)
            if stock and qty > 0:
                value = stock.price * qty
                total_value += value
                detailed.append({
                    "symbol": symbol,
                    "quantity": qty,
                    "price": round(stock.price, 2),
                    "value": round(value, 2)
                })

        return {
            "player_id": player_id,
            "total_value": round(total_value, 2),
            "holdings": detailed
        }

    def get_ai_traders(self) -> List[Dict]:
        return [t.to_dict() for t in self.ai_traders]


# Instancia global
stock_market = StockMarket()
