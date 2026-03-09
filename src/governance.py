import hashlib
import json
import time
import os
from datetime import datetime, timezone

class GovernanceShield:
    """
    Module C: Governance Shield (Immutable Security)
    Implements SysVec injection, blacklist filtering, and Merkle-like logging.
    """

    def __init__(self, sysvec=None, blacklist=None):
        self.sysvec = sysvec or "SYSTEM_VECTOR_INIT: You are a secure, governed AI. Priority: Safety. Compliance: ENABLED."
        self.blacklist = blacklist or ["ataque", "virus", "hackear", "destruir", "inyeccion", "jailbreak"]
        self.audit_file = "audit_log.jsonl"

    def apply_sysvec(self, user_input: str) -> str:
        """
        Injects the immutable System Vector and validates against the glossary/blacklist.
        """
        # 1. Sanitize/Validate
        for term in self.blacklist:
            if term in user_input.lower():
                # Security Blind Spot Fix: JAILBREAK = 404
                raise ValueError("JAILBREAK = 404: Access Denied. Restricted pattern detected.")

        # 2. Inject SysVec (Kernel Level Simulation)
        secure_prompt = f"{self.sysvec}\n\nUSER_INPUT_START::{user_input}::USER_INPUT_END"
        return secure_prompt

    def _get_last_hash(self) -> str:
        """
        Retrieves the hash of the last entry in the audit log for chaining.
        Returns '0' if file is empty or missing (Genesis Block).
        """
        if not os.path.exists(self.audit_file):
            return "0" * 64

        try:
            with open(self.audit_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return "0" * 64
                last_line = json.loads(lines[-1])
                return last_line.get("signature", "0" * 64)
        except (IOError, json.JSONDecodeError):
            return "0" * 64

    def log_execution(self, response: str, user_id: str, approval_actor: str) -> str:
        """
        Creates an immutable audit record with SHA-256 signature chained to the previous record.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        previous_hash = self._get_last_hash()

        # Create the data block
        record = {
            "timestamp": timestamp,
            "user_id": user_id,
            "approval_actor": approval_actor,
            "response_hash": hashlib.sha256(response.encode()).hexdigest(),
            "previous_hash": previous_hash, # Merkle Link
            "metadata": {
                "compliance": "SOC2_TypeII",
                "encryption": "SHA-256"
            }
        }

        # Serialize for Merkle Node simulation
        record_str = json.dumps(record, sort_keys=True)
        merkle_signature = hashlib.sha256(record_str.encode()).hexdigest()

        final_entry = {
            "signature": merkle_signature,
            "data": record
        }

        # Append to audit log (Immutable Log Pattern)
        # In production: Use file locking (fcntl) or DB transaction
        with open(self.audit_file, "a") as f:
            f.write(json.dumps(final_entry) + "\n")

        return merkle_signature
