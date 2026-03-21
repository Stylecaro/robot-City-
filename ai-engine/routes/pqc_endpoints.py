"""
Endpoints PQC — Criptografía Post-Cuántica para AI Engine
=========================================================
Provee API REST para operaciones PQC desde el motor de IA:
keygen, firma, verificación, canales seguros y estado.
"""

import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

# Importar PQC
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'quantum-blockchain'))
from pqc_crypto import pqc_manager

router = APIRouter(prefix="/api/pqc", tags=["pqc"])


class KeygenRequest(BaseModel):
    entity_id: str


class SignRequest(BaseModel):
    signer_id: str
    data: str


class VerifyRequest(BaseModel):
    signer_id: str
    data: str
    signature: Dict


class SecureChannelRequest(BaseModel):
    initiator_id: str
    responder_id: str


@router.get("/status")
async def pqc_status():
    """Estado del sistema de seguridad PQC."""
    return pqc_manager.get_security_status()


@router.post("/keygen")
async def pqc_keygen(req: KeygenRequest):
    """Genera un key bundle PQC para una entidad."""
    bundle = pqc_manager.generate_key_bundle(req.entity_id)
    return {"success": True, **bundle.to_dict()}


@router.post("/sign")
async def pqc_sign(req: SignRequest):
    """Firma datos con ML-DSA (Dilithium)."""
    if req.signer_id not in pqc_manager.key_store:
        raise HTTPException(status_code=404, detail=f"Entidad no registrada: {req.signer_id}")
    result = pqc_manager.sign_transaction(req.signer_id, req.data.encode("utf-8"))
    return {"success": True, **result}


@router.post("/verify")
async def pqc_verify(req: VerifyRequest):
    """Verifica una firma PQC."""
    if req.signer_id not in pqc_manager.key_store:
        raise HTTPException(status_code=404, detail=f"Entidad no registrada: {req.signer_id}")
    result = pqc_manager.verify_transaction(
        req.signer_id, req.data.encode("utf-8"), req.signature
    )
    return {"success": True, **result}


@router.post("/secure-channel")
async def pqc_secure_channel(req: SecureChannelRequest):
    """Establece canal seguro post-cuántico entre dos entidades."""
    for eid in [req.initiator_id, req.responder_id]:
        if eid not in pqc_manager.key_store:
            raise HTTPException(status_code=404, detail=f"Entidad no registrada: {eid}")
    result = pqc_manager.establish_secure_channel(req.initiator_id, req.responder_id)
    return {"success": True, **result}


@router.get("/audit-log")
async def pqc_audit_log():
    """Devuelve el audit log PQC."""
    return {"entries": pqc_manager.get_audit_log()}
