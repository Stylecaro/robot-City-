"""
Tests de Validación PQC — Ciudad Robot
=======================================
Verifica todas las operaciones de criptografía post-cuántica:
ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA (SPHINCS+), PQCManager.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quantum-blockchain'))

from pqc_crypto import (
    MLKEM, MLDSA, SLHDSA, PQCManager,
    KyberKeypair, DilithiumKeypair, DilithiumSignature,
    SPHINCSKeypair, PQCKeyBundle,
    sha3_256, sha3_512, shake256, secure_random,
)


class TestUtilities(unittest.TestCase):
    """Tests de funciones criptográficas base."""

    def test_secure_random_length(self):
        r = secure_random(32)
        self.assertEqual(len(r), 32)
        self.assertIsInstance(r, bytes)

    def test_secure_random_unique(self):
        a = secure_random(32)
        b = secure_random(32)
        self.assertNotEqual(a, b)

    def test_sha3_256_deterministic(self):
        data = b"Robot City PQC"
        h1 = sha3_256(data)
        h2 = sha3_256(data)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 32)

    def test_sha3_512_length(self):
        h = sha3_512(b"test")
        self.assertEqual(len(h), 64)

    def test_shake256_variable_length(self):
        for length in [16, 32, 64, 128, 1024]:
            out = shake256(b"test", length)
            self.assertEqual(len(out), length)


class TestMLKEM(unittest.TestCase):
    """Tests de ML-KEM (Kyber) — encapsulación de claves."""

    def test_keygen_default(self):
        kem = MLKEM()
        kp = kem.keygen()
        self.assertIsInstance(kp, KyberKeypair)
        self.assertEqual(kp.parameter_set, "ML-KEM-768")
        self.assertEqual(len(kp.public_key), 1184)
        self.assertEqual(len(kp.secret_key), 2400)

    def test_keygen_all_parameter_sets(self):
        for ps, params in MLKEM.PARAMETER_SETS.items():
            kem = MLKEM(ps)
            kp = kem.keygen()
            self.assertEqual(len(kp.public_key), params["pk_size"])
            self.assertEqual(len(kp.secret_key), params["sk_size"])

    def test_encapsulate_produces_correct_sizes(self):
        kem = MLKEM()
        kp = kem.keygen()
        encap = kem.encapsulate(kp.public_key)
        self.assertEqual(len(encap.ciphertext), 1088)
        self.assertEqual(len(encap.shared_secret), 32)

    def test_decapsulate_produces_shared_secret(self):
        kem = MLKEM()
        kp = kem.keygen()
        encap = kem.encapsulate(kp.public_key)
        ss = kem.decapsulate(kp.secret_key, encap.ciphertext)
        self.assertEqual(len(ss), 32)
        self.assertIsInstance(ss, bytes)

    def test_invalid_parameter_set_raises(self):
        with self.assertRaises(ValueError):
            MLKEM("ML-KEM-256")

    def test_keypair_to_dict(self):
        kem = MLKEM()
        kp = kem.keygen()
        d = kp.to_dict()
        self.assertIn("public_key_hex", d)
        self.assertIn("parameter_set", d)
        self.assertEqual(d["parameter_set"], "ML-KEM-768")


class TestMLDSA(unittest.TestCase):
    """Tests de ML-DSA (Dilithium) — firmas digitales."""

    def test_keygen_default(self):
        dsa = MLDSA()
        kp = dsa.keygen()
        self.assertIsInstance(kp, DilithiumKeypair)
        self.assertEqual(kp.parameter_set, "ML-DSA-65")

    def test_keygen_all_parameter_sets(self):
        for ps, params in MLDSA.PARAMETER_SETS.items():
            dsa = MLDSA(ps)
            kp = dsa.keygen()
            self.assertEqual(len(kp.public_key), params["pk_size"])
            self.assertEqual(len(kp.secret_key), params["sk_size"])

    def test_sign_produces_correct_size(self):
        dsa = MLDSA()
        kp = dsa.keygen()
        sig = dsa.sign(kp.secret_key, b"test message")
        self.assertIsInstance(sig, DilithiumSignature)
        self.assertEqual(len(sig.signature), 3309)
        self.assertEqual(sig.parameter_set, "ML-DSA-65")

    def test_sign_deterministic(self):
        dsa = MLDSA()
        kp = dsa.keygen()
        msg = b"deterministic test"
        sig1 = dsa.sign(kp.secret_key, msg)
        sig2 = dsa.sign(kp.secret_key, msg)
        self.assertEqual(sig1.signature, sig2.signature)

    def test_sign_different_messages_different_signatures(self):
        dsa = MLDSA()
        kp = dsa.keygen()
        sig1 = dsa.sign(kp.secret_key, b"message A")
        sig2 = dsa.sign(kp.secret_key, b"message B")
        self.assertNotEqual(sig1.signature, sig2.signature)

    def test_signature_to_dict(self):
        dsa = MLDSA()
        kp = dsa.keygen()
        sig = dsa.sign(kp.secret_key, b"test")
        d = sig.to_dict()
        self.assertIn("signature_hex", d)
        self.assertIn("parameter_set", d)
        self.assertIn("signer", d)


class TestSLHDSA(unittest.TestCase):
    """Tests de SLH-DSA (SPHINCS+) — firmas hash-based."""

    def test_keygen_default(self):
        slh = SLHDSA()
        kp = slh.keygen()
        self.assertIsInstance(kp, SPHINCSKeypair)
        self.assertEqual(kp.parameter_set, "SLH-DSA-SHAKE-128f")
        self.assertEqual(len(kp.public_key), 32)
        self.assertEqual(len(kp.secret_key), 64)

    def test_keygen_all_parameter_sets(self):
        for ps, params in SLHDSA.PARAMETER_SETS.items():
            slh = SLHDSA(ps)
            kp = slh.keygen()
            self.assertEqual(len(kp.public_key), params["pk_size"])
            self.assertEqual(len(kp.secret_key), params["sk_size"])

    def test_sign_correct_size(self):
        slh = SLHDSA()
        kp = slh.keygen()
        sig = slh.sign(kp.secret_key, b"test")
        self.assertEqual(len(sig), 17088)

    def test_verify_valid_signature(self):
        slh = SLHDSA()
        kp = slh.keygen()
        sig = slh.sign(kp.secret_key, b"valid message")
        self.assertTrue(slh.verify(kp.public_key, b"valid message", sig))

    def test_verify_wrong_size_returns_false(self):
        slh = SLHDSA()
        kp = slh.keygen()
        self.assertFalse(slh.verify(kp.public_key, b"test", b"short"))


class TestPQCManager(unittest.TestCase):
    """Tests del orquestador PQC completo."""

    def setUp(self):
        self.mgr = PQCManager()

    def test_generate_key_bundle(self):
        bundle = self.mgr.generate_key_bundle("robot-001")
        self.assertIsInstance(bundle, PQCKeyBundle)
        self.assertEqual(bundle.entity_id, "robot-001")
        self.assertIn("robot-001", self.mgr.key_store)

    def test_sign_transaction(self):
        self.mgr.generate_key_bundle("signer-A")
        result = self.mgr.sign_transaction("signer-A", b"tx-data-001")
        self.assertIn("ml_dsa_signature", result)
        self.assertIn("tx_hash_sha3", result)
        self.assertIn("algorithms", result)
        self.assertEqual(result["signer_id"], "signer-A")

    def test_verify_transaction_valid(self):
        self.mgr.generate_key_bundle("verifier-B")
        data = b"valid-transaction-data"
        sig = self.mgr.sign_transaction("verifier-B", data)
        result = self.mgr.verify_transaction("verifier-B", data, sig)
        self.assertTrue(result["valid"])
        self.assertTrue(result["hash_valid"])
        self.assertTrue(result["ml_dsa_valid"])

    def test_verify_transaction_tampered_data(self):
        self.mgr.generate_key_bundle("tamper-test")
        original_data = b"original data"
        sig = self.mgr.sign_transaction("tamper-test", original_data)
        result = self.mgr.verify_transaction("tamper-test", b"tampered data", sig)
        self.assertFalse(result["valid"])

    def test_sign_unregistered_entity_raises(self):
        with self.assertRaises(ValueError):
            self.mgr.sign_transaction("nonexistent", b"data")

    def test_verify_unregistered_entity(self):
        result = self.mgr.verify_transaction("ghost", b"data", {})
        self.assertFalse(result["valid"])

    def test_establish_secure_channel(self):
        self.mgr.generate_key_bundle("node-A")
        self.mgr.generate_key_bundle("node-B")
        result = self.mgr.establish_secure_channel("node-A", "node-B")
        self.assertIn("session_key_hex", result)
        self.assertEqual(len(bytes.fromhex(result["session_key_hex"])), 32)
        self.assertEqual(result["initiator"], "node-A")
        self.assertEqual(result["responder"], "node-B")

    def test_secure_channel_unregistered_raises(self):
        self.mgr.generate_key_bundle("exists")
        with self.assertRaises(ValueError):
            self.mgr.establish_secure_channel("exists", "missing")

    def test_security_status(self):
        status = self.mgr.get_security_status()
        self.assertTrue(status["pqc_enabled"])
        self.assertTrue(status["quantum_resistant"])
        self.assertEqual(status["security_level"], 3)
        self.assertIn("FIPS_203", status["nist_standards"])
        self.assertIn("FIPS_204", status["nist_standards"])
        self.assertIn("FIPS_205", status["nist_standards"])

    def test_audit_log_recorded(self):
        self.mgr.generate_key_bundle("audit-entity")
        self.mgr.sign_transaction("audit-entity", b"audit-test")
        log = self.mgr.get_audit_log()
        self.assertGreater(len(log), 0)
        actions = [e["action"] for e in log]
        self.assertIn("keygen", actions)
        self.assertIn("sign", actions)

    def test_key_bundle_to_dict(self):
        bundle = self.mgr.generate_key_bundle("dict-test")
        d = bundle.to_dict()
        self.assertEqual(d["entity_id"], "dict-test")
        self.assertIn("kem", d)
        self.assertIn("dsa", d)
        self.assertIn("hash_sig", d)


class TestPQCBlockchainIntegration(unittest.TestCase):
    """Verifica la integración PQC con quantum_blockchain."""

    def test_blockchain_block_has_pqc_signature(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quantum-blockchain'))
        from quantum_blockchain import QuantumBlockchain
        bc = QuantumBlockchain("PQC Test Chain")
        block = bc.add_block({"tipo": "test", "val": 42})
        self.assertIn("pqc_signature", block.to_dict())
        self.assertIn("ml_dsa_signature", block.pqc_signature)

    def test_blockchain_block_pqc_verification(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quantum-blockchain'))
        from quantum_blockchain import QuantumBlockchain
        bc = QuantumBlockchain("PQC Verify Chain")
        block = bc.add_block({"tipo": "verify_test"})
        self.assertTrue(block.verify_pqc_signature())

    def test_blockchain_chain_validation_with_pqc(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quantum-blockchain'))
        from quantum_blockchain import QuantumBlockchain
        bc = QuantumBlockchain("Validation Chain")
        bc.add_block({"tipo": "block_1"})
        bc.add_block({"tipo": "block_2"})
        bc.add_block({"tipo": "block_3"})
        self.assertTrue(bc.validate_chain())

    def test_blockchain_state_includes_pqc(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quantum-blockchain'))
        from quantum_blockchain import QuantumBlockchain
        bc = QuantumBlockchain("State Chain")
        state = bc.get_chain_state()
        self.assertIn("pqc_security", state)
        self.assertTrue(state["pqc_security"]["pqc_enabled"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
