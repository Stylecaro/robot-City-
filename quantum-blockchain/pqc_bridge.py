"""
Bridge PQC — Interfaz CLI para endpoints Node.js
=================================================
Recibe comandos JSON por stdin y ejecuta operaciones PQC.
Devuelve resultados por stdout en JSON.
"""

import sys
import json
from pqc_crypto import pqc_manager


def handle_command(payload: dict) -> dict:
    command = payload.get("command", "")

    if command == "status":
        return pqc_manager.get_security_status()

    elif command == "keygen":
        entity_id = payload["entity_id"]
        bundle = pqc_manager.generate_key_bundle(entity_id)
        return bundle.to_dict()

    elif command == "sign":
        signer_id = payload["signer_id"]
        data = payload["data"].encode("utf-8")
        return pqc_manager.sign_transaction(signer_id, data)

    elif command == "verify":
        signer_id = payload["signer_id"]
        data = payload["data"].encode("utf-8")
        signature = payload["signature"]
        return pqc_manager.verify_transaction(signer_id, data, signature)

    elif command == "secure_channel":
        initiator_id = payload["initiator_id"]
        responder_id = payload["responder_id"]
        return pqc_manager.establish_secure_channel(initiator_id, responder_id)

    elif command == "audit_log":
        return {"entries": pqc_manager.get_audit_log()}

    else:
        return {"error": f"Comando desconocido: {command}"}


def main():
    raw = sys.stdin.read()
    payload = json.loads(raw)
    result = handle_command(payload)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
