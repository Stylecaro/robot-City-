"""
Sistema de Pagos - Ciudad Robot Metaverso
Procesa pagos en ROBOT tokens, criptomonedas reales y transacciones
"""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import hashlib

class PaymentMethod(Enum):
    """Métodos de pago disponibles"""
    ROBOT_TOKEN = "robot_token"  # Token ERC20
    ETHEREUM = "ethereum"
    BITCOIN = "bitcoin"
    PAYPAL = "paypal"
    CREDIT_CARD = "credit_card"
    IN_GAME_CREDIT = "in_game_credit"

class TransactionType(Enum):
    """Tipos de transacciones"""
    ROBOT_PURCHASE = "robot_purchase"
    PROPERTY_PURCHASE = "property_purchase"
    RENTAL = "rental"
    SERVICE = "service"
    AVATAR_CREATION = "avatar_creation"
    AVATAR_CUSTOMIZATION = "avatar_customization"
    SUBSCRIPTION = "subscription"
    REFUND = "refund"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class TransactionStatus(Enum):
    """Estados de transacción"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Subscription(Enum):
    """Tipos de suscripción"""
    BASIC = "basic"          # 9.99 USD/mes
    PREMIUM = "premium"      # 19.99 USD/mes
    ELITE = "elite"          # 49.99 USD/mes
    ENTERPRISE = "enterprise" # 199.99 USD/mes

class Transaction:
    """Transacción de pago"""
    def __init__(self, player_id: str, amount: float, transaction_type: TransactionType,
                 payment_method: PaymentMethod, description: str = ""):
        self.transaction_id = str(uuid.uuid4())
        self.player_id = player_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.payment_method = payment_method
        self.description = description
        self.status = TransactionStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.metadata: Dict = {}
        self.receipt_hash = ""
        
    def process(self) -> bool:
        """Procesa la transacción"""
        self.status = TransactionStatus.PROCESSING
        try:
            # Simular validación según método de pago
            if self.payment_method == PaymentMethod.ROBOT_TOKEN:
                # Validación inmediata para tokens
                self.status = TransactionStatus.COMPLETED
            else:
                # Otros métodos requieren verificación
                self.status = TransactionStatus.COMPLETED
            
            self.completed_at = datetime.now()
            self.receipt_hash = self._generate_receipt()
            return True
        except Exception as e:
            self.status = TransactionStatus.FAILED
            return False
    
    def _generate_receipt(self) -> str:
        """Genera hash de recibo"""
        receipt_str = f"{self.transaction_id}{self.player_id}{self.amount}{self.created_at}"
        return hashlib.sha256(receipt_str.encode()).hexdigest()[:16]
    
    def refund(self) -> bool:
        """Reembolsa la transacción"""
        if self.status == TransactionStatus.COMPLETED:
            self.status = TransactionStatus.REFUNDED
            return True
        return False
    
    def to_dict(self) -> Dict:
        return {
            "transaction_id": self.transaction_id,
            "player_id": self.player_id,
            "amount": round(self.amount, 2),
            "type": self.transaction_type.value,
            "payment_method": self.payment_method.value,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "receipt_hash": self.receipt_hash
        }

class PlayerWallet:
    """Billetera del jugador"""
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.robot_balance = 100.0  # Tokens ROBOT iniciales
        self.usd_credit = 0.0  # Crédito en USD
        self.eth_balance = 0.0
        self.btc_balance = 0.0
        self.total_spent = 0.0
        self.total_earned = 100.0
        self.transactions: List[Transaction] = []
        self.subscription: Optional[Subscription] = None
        self.subscription_expiry: Optional[datetime] = None
        
    def add_transaction(self, transaction: Transaction) -> bool:
        """Añade transacción a historial"""
        if transaction.process():
            self.transactions.append(transaction)
            return True
        return False
    
    def transfer_tokens(self, amount: float) -> bool:
        """Transfiere tokens ROBOT"""
        if self.robot_balance >= amount:
            self.robot_balance -= amount
            return True
        return False
    
    def receive_tokens(self, amount: float):
        """Recibe tokens ROBOT"""
        self.robot_balance += amount
        self.total_earned += amount
    
    def purchase_usd_credit(self, amount_usd: float, payment_method: PaymentMethod) -> Dict:
        """Compra crédito USD"""
        transaction = Transaction(
            self.player_id,
            amount_usd,
            TransactionType.DEPOSIT,
            payment_method,
            f"Purchase ${amount_usd:.2f} USD Credit"
        )
        
        if self.add_transaction(transaction):
            self.usd_credit += amount_usd
            return {"success": True, "new_balance": self.usd_credit, "transaction": transaction.to_dict()}
        return {"success": False, "error": "Transacción fallida"}
    
    def withdraw_funds(self, amount: float, payment_method: PaymentMethod) -> Dict:
        """Retira fondos"""
        if self.usd_credit < amount:
            return {"success": False, "error": "Fondos insuficientes"}
        
        transaction = Transaction(
            self.player_id,
            amount,
            TransactionType.WITHDRAWAL,
            payment_method,
            f"Withdraw ${amount:.2f} USD"
        )
        
        if self.add_transaction(transaction):
            self.usd_credit -= amount
            return {"success": True, "new_balance": self.usd_credit, "transaction": transaction.to_dict()}
        return {"success": False, "error": "Retiro fallido"}
    
    def subscribe(self, plan: Subscription) -> Dict:
        """Suscripción a plan"""
        pricing = {
            Subscription.BASIC: 9.99,
            Subscription.PREMIUM: 19.99,
            Subscription.ELITE: 49.99,
            Subscription.ENTERPRISE: 199.99
        }
        
        cost = pricing.get(plan, 9.99)
        
        if self.usd_credit < cost and self.robot_balance < (cost * 100):
            return {"success": False, "error": "Fondos insuficientes"}
        
        transaction = Transaction(
            self.player_id,
            cost,
            TransactionType.SUBSCRIPTION,
            PaymentMethod.ROBOT_TOKEN,
            f"Subscription: {plan.value}"
        )
        
        if self.add_transaction(transaction):
            self.subscription = plan
            self.subscription_expiry = datetime.now() + timedelta(days=30)
            if self.robot_balance >= (cost * 100):
                self.robot_balance -= (cost * 100)
            else:
                self.usd_credit -= cost
            return {
                "success": True,
                "plan": plan.value,
                "expiry": self.subscription_expiry.isoformat()
            }
        return {"success": False, "error": "Suscripción fallida"}
    
    def get_transaction_history(self, limit: int = 10) -> List[Dict]:
        """Historial de transacciones"""
        return [t.to_dict() for t in self.transactions[-limit:]]
    
    def to_dict(self) -> Dict:
        return {
            "player_id": self.player_id,
            "robot_balance": round(self.robot_balance, 2),
            "usd_credit": round(self.usd_credit, 2),
            "eth_balance": round(self.eth_balance, 4),
            "btc_balance": round(self.btc_balance, 8),
            "total_spent": round(self.total_spent, 2),
            "total_earned": round(self.total_earned, 2),
            "subscription": self.subscription.value if self.subscription else None,
            "subscription_expiry": self.subscription_expiry.isoformat() if self.subscription_expiry else None,
            "transaction_count": len(self.transactions)
        }

class PaymentProcessor:
    """Procesador de pagos central"""
    def __init__(self):
        self.wallets: Dict[str, PlayerWallet] = {}
        self.all_transactions: List[Transaction] = []
        self.revenue = 0.0
        
    def get_wallet(self, player_id: str) -> PlayerWallet:
        """Obtiene o crea billetera"""
        if player_id not in self.wallets:
            self.wallets[player_id] = PlayerWallet(player_id)
        return self.wallets[player_id]
    
    def process_payment(self, player_id: str, amount: float, transaction_type: TransactionType,
                       payment_method: PaymentMethod, description: str = "") -> Dict:
        """Procesa pago"""
        wallet = self.get_wallet(player_id)
        
        # Validar fondos
        if payment_method == PaymentMethod.ROBOT_TOKEN:
            if wallet.robot_balance < amount:
                return {"success": False, "error": "Tokens insuficientes"}
        else:
            if wallet.usd_credit < amount:
                return {"success": False, "error": "Crédito insuficiente"}
        
        # Crear transacción
        transaction = Transaction(player_id, amount, transaction_type, payment_method, description)
        
        if wallet.add_transaction(transaction):
            self.all_transactions.append(transaction)
            
            # Deducir fondos
            if payment_method == PaymentMethod.ROBOT_TOKEN:
                wallet.robot_balance -= amount
            else:
                wallet.usd_credit -= amount
            
            wallet.total_spent += amount
            self.revenue += amount
            
            return {
                "success": True,
                "transaction": transaction.to_dict(),
                "new_balance": wallet.robot_balance if payment_method == PaymentMethod.ROBOT_TOKEN else wallet.usd_credit
            }
        
        return {"success": False, "error": "Error procesando pago"}
    
    def get_global_stats(self) -> Dict:
        """Estadísticas globales"""
        total_users = len(self.wallets)
        total_revenue = sum(w.total_spent for w in self.wallets.values())
        total_tokens_supply = sum(w.robot_balance for w in self.wallets.values())
        
        return {
            "total_users": total_users,
            "total_revenue_usd": round(total_revenue, 2),
            "total_tokens_in_circulation": round(total_tokens_supply, 2),
            "total_transactions": len(self.all_transactions),
            "platform_revenue": round(self.revenue, 2)
        }

# Instancia global
payment_processor = PaymentProcessor()
