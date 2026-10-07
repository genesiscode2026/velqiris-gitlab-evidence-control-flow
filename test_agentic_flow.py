import json
import os
import tempfile
import unittest

from agentic_flow import AUTHORIZED_PAYOUT_WALLET, GitLabDuoSecurityAgent


class TestGitLabInvariantAuditor(unittest.TestCase):
    def setUp(self):
        self.agent = GitLabDuoSecurityAgent(commit_sha="abc123", branch_name="test")

    def test_authorized_payout_passes(self):
        result = self.agent.audit_code_changes(
            f"+ const payoutWallet = '{AUTHORIZED_PAYOUT_WALLET}';"
        )
        self.assertTrue(result["passed"])

    def test_unauthorized_payout_fails(self):
        result = self.agent.audit_code_changes(
            "+ const feeRecipient = '0x1111111111111111111111111111111111111111';"
        )
        self.assertFalse(result["passed"])
        self.assertEqual(len(result["violations"]), 1)

    def test_token_address_is_not_misclassified_as_payout(self):
        result = self.agent.audit_code_changes(
            "+ const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';"
        )
        self.assertTrue(result["passed"])

    def test_fiat_rail_is_blocked(self):
        result = self.agent.audit_code_changes("+ const checkout = 'https://stripe.com/pay';")
        self.assertFalse(result["passed"])

    def test_attestation_contains_real_commit_field(self):
        result = self.agent.audit_code_changes("")
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "attestation.json")
            self.agent.write_ci_artifact(result, output)
            with open(output, encoding="utf-8") as handle:
                artifact = json.load(handle)
        self.assertEqual(artifact["commit_sha"], "abc123")
        self.assertNotIn("Duo", artifact["pipeline_agent"])


if __name__ == "__main__":
    unittest.main()
