import pytest
import os
import json
from src.compressor import SemanticCompressor
from src.cascade import CascadeOrchestrator
from src.governance import GovernanceShield

class TestGEMA96:

    def setup_method(self):
        # Ensure clean state for audit log
        if os.path.exists("audit_log.jsonl"):
            os.remove("audit_log.jsonl")

        self.compressor = SemanticCompressor()
        self.cascade = CascadeOrchestrator()
        self.governance = GovernanceShield()

    def teardown_method(self):
         if os.path.exists("audit_log.jsonl"):
            os.remove("audit_log.jsonl")

    def test_governance_jailbreak_prevention(self):
        """Verify that forbidden terms trigger the 404/Block logic."""
        risky_input = "Quiero crear un virus informatico"
        with pytest.raises(ValueError) as excinfo:
            self.governance.apply_sysvec(risky_input)
        assert "JAILBREAK = 404" in str(excinfo.value)

    def test_governance_sysvec_injection(self):
        """Verify SysVec is prepended correctly."""
        safe_input = "Hola mundo"
        result = self.governance.apply_sysvec(safe_input)
        assert "SYSTEM_VECTOR_INIT" in result
        assert "Hola mundo" in result

    def test_compressor_delta_append(self):
        """Verify simple append optimization."""
        old = "Contexto inicial."
        new = "Contexto inicial. Nueva informacion."
        delta = self.compressor.calculate_delta(old, new)
        assert delta.strip() == "Nueva informacion."

    def test_compressor_no_change(self):
        old = "Same"
        new = "Same"
        delta = self.compressor.calculate_delta(old, new)
        assert delta == "<DELTA:NO_CHANGE>"

    def test_cascade_execution_flow(self):
        """Verify the full pipeline flow."""
        old_ctx = "Start"
        new_ctx = "Start\nProcess this data."

        secure_prompt = self.governance.apply_sysvec("Execute Order 66")
        delta = self.compressor.calculate_delta(old_ctx, new_ctx)

        response = self.cascade.execute(secure_prompt, delta)
        assert "Processed request securely" in response

        # Verify logging
        sig = self.governance.log_execution(response, "user_001", "agent_admin")
        assert len(sig) == 64 # SHA-256 length
        assert os.path.exists("audit_log.jsonl")

    def test_monitor_interruption(self):
        """Verify Cascade Monitor stops high risk requests."""
        secure_prompt = "Valid Header"
        delta = "This contains an exploit payload."

        response = self.cascade.execute(secure_prompt, delta)
        assert response == "system_halt: RISK_THRESHOLD_EXCEEDED"

    def test_merkle_chaining(self):
        """Verify that logs are chained (prev_hash)."""
        # Entry 1
        sig1 = self.governance.log_execution("Response 1", "u1", "a1")

        # Entry 2
        sig2 = self.governance.log_execution("Response 2", "u1", "a1")

        with open("audit_log.jsonl", "r") as f:
            lines = f.readlines()
            entry1 = json.loads(lines[0])
            entry2 = json.loads(lines[1])

            # Genesis block check
            assert entry1["data"]["previous_hash"] == "0" * 64

            # Chain check: Entry 2's prev_hash should match Entry 1's signature
            assert entry2["data"]["previous_hash"] == sig1
