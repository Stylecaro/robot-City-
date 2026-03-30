"""
integration_demo.py — Robot City Platform Integration Demo
=============================================================
Demonstrates how the new modular foundation fits together:

  service-robots + simulation + payments + web3 + quantum-blockchain

Run with:
    python integration_demo.py
"""

import sys
import os

# --- Path helpers (so we can run from repo root without installing packages)
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Hyphenated directories need their own path entries for absolute imports
for subdir in ["service-robots", "quantum-security", "quantum-blockchain", "simulation-system"]:
    sys.path.insert(0, os.path.join(REPO_ROOT, subdir))

# Non-hyphenated directories are importable as packages from repo root
sys.path.insert(0, REPO_ROOT)


# ──────────────────────────────────────────────────────────────────────────────
# 1. Service Robots
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  1. SERVICE ROBOTS")
print("=" * 60)

from base_robot import RobotType, RobotStatus   # noqa: E402  (service-robots/)
from medical_robot import MedicalRobot           # noqa: E402
from security_robot import SecurityRobotService  # noqa: E402
from transport_robot import TransportRobot       # noqa: E402
from robot_registry import ServiceRobotRegistry  # noqa: E402

registry = ServiceRobotRegistry()

med = MedicalRobot(name="MediBot-Alpha")
sec = SecurityRobotService(name="GuardBot-01")
trn = TransportRobot(name="SpeedBot-X1")

registry.register_robot(med)
registry.register_robot(sec)
registry.register_robot(trn)

print(f"Registered robots: {len(registry.get_all_robots())}")
print(f"Stats: {registry.get_stats()}")

dispatch = registry.dispatch_robot("medical", "emergency_response")
print(f"Medical dispatch: {dispatch}")


# ──────────────────────────────────────────────────────────────────────────────
# 2. Crypto Payments
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  2. CRYPTO PAYMENTS")
print("=" * 60)

from payments.crypto_invoice import SupportedAsset   # noqa: E402
from payments.payment_service import CryptoPaymentService  # noqa: E402

pay_svc = CryptoPaymentService()

eth_inv  = pay_svc.create_invoice(SupportedAsset.ETH,  0.05,  "Robot rental - ETH")
btc_inv  = pay_svc.create_invoice(SupportedAsset.BTC,  0.001, "City service fee - BTC")
usdt_inv = pay_svc.create_invoice(SupportedAsset.USDT, 100.0, "Subscription - USDT")

print(f"ETH invoice id : {eth_inv.invoice_id}")
print(f"BTC invoice id : {btc_inv.invoice_id}")
print(f"USDT invoice id: {usdt_inv.invoice_id}")

instructions = pay_svc.get_payment_instructions(eth_inv.invoice_id)
print(f"Payment instructions: {instructions}")

receipt = pay_svc.mark_paid(eth_inv.invoice_id, tx_hash="0xdeadbeef", amount_received=0.05)
print(f"Receipt: {receipt.to_dict()}")
print(f"Payment stats: {pay_svc.get_stats()}")


# ──────────────────────────────────────────────────────────────────────────────
# 3. Web3 Multi-Chain
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  3. WEB3 MULTI-CHAIN")
print("=" * 60)

from web3.chain_registry import ChainRegistry  # noqa: E402
from web3.base_chain import ChainType           # noqa: E402

chain_reg = ChainRegistry.get_default_registry()
print(f"Available chains: {[c.value for c in chain_reg.get_all_chains()]}")

test_addresses = {
    ChainType.ETHEREUM: "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12",
    ChainType.SOLANA:   "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin",
    ChainType.BITCOIN:  "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq",
    ChainType.TRON:     "TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH",
}

for chain_type, address in test_addresses.items():
    try:
        valid = chain_reg.validate_address_on_chain(chain_type, address)
        print(f"  {chain_type.value}: {address[:20]}... valid={valid}")
    except Exception as exc:
        print(f"  {chain_type.value}: {exc}")


# ──────────────────────────────────────────────────────────────────────────────
# 4. Wallet Management
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  4. WALLET MANAGEMENT")
print("=" * 60)

from wallets.wallet_manager import WalletManager    # noqa: E402
from wallets.wallet_validator import WalletValidator  # noqa: E402

wallet_mgr = WalletManager()
validator   = WalletValidator()

wallet_mgr.add_wallet("user-001", "ETH", "0xAbCdEf1234567890AbCdEf1234567890AbCdEf12")
wallet_mgr.add_wallet("user-001", "BTC", "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq")

print(f"Wallets: {wallet_mgr.list_wallets()}")

result = validator.validate_address("0xAbCdEf1234567890AbCdEf1234567890AbCdEf12", "ETH")
print(f"EVM address validation: {result}")


# ──────────────────────────────────────────────────────────────────────────────
# 5. Quantum Security
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  5. QUANTUM SECURITY")
print("=" * 60)

from pqc_wrapper import PQCWrapper, PQCAlgorithm  # noqa: E402  (quantum-security/)
from key_manager import KeyManager   # noqa: E402

km  = KeyManager()
pqc = PQCWrapper()

bundle = km.generate_key_bundle("robot-alpha", PQCAlgorithm.ML_DSA_65)
print(f"Key bundle: id={bundle.key_id}, algo={bundle.algorithm}")

msg_hash = pqc.hash_message(b"City Robot Event 001")
print(f"SHA3-256 hash: {msg_hash}")


# ──────────────────────────────────────────────────────────────────────────────
# 6. Quantum Blockchain Event Ledger
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  6. QUANTUM BLOCKCHAIN EVENT LEDGER")
print("=" * 60)

from event_ledger import EventLedger, EventCategory  # noqa: E402  (quantum-blockchain/)

ledger = EventLedger()

ev1 = ledger.record_robot_event(
    "robot-alpha", "task.completed",
    {"task": "emergency_response", "zone": "medical"}
)
ev2 = ledger.record_payment_event(
    eth_inv.invoice_id, "paid",
    {"asset": "ETH", "amount": 0.05}
)

print(f"Event 1: {ev1.event_id} | integrity_ok={ev1.verify_integrity()}")
print(f"Event 2: {ev2.event_id} | integrity_ok={ev2.verify_integrity()}")
print(f"Ledger stats: {ledger.get_stats()}")


# ──────────────────────────────────────────────────────────────────────────────
# 7. City Simulation
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  7. CITY SIMULATION")
print("=" * 60)

from city_simulation import CitySimulation  # noqa: E402  (simulation-system/)

sim = CitySimulation(city_name="Ciudad Robot Demo")
sim.attach_robot_registry(registry)
sim.attach_event_ledger(ledger)
sim.initialize(num_citizens=30)

for _ in range(3):
    result = sim.tick()
    print(f"Tick {result['tick']}: {result['summary']}")

state = sim.get_city_state()
print(f"\nCity zones active : {len(state['zones'])}")
print(f"Avg satisfaction  : {state['citizens']['avg_satisfaction']}")
print(f"Recent events     : {len(state['recent_events'])}")

print("\n" + "=" * 60)
print("  Integration demo complete.")
print("=" * 60)
