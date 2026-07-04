import importlib.util
import unittest
from unittest.mock import patch


FASTAPI_AVAILABLE = importlib.util.find_spec("fastapi") is not None

if FASTAPI_AVAILABLE:
    from fastapi.testclient import TestClient

    from backend.api.main import app


    class ApiContractTests(unittest.TestCase):
        def setUp(self):
            self.client = TestClient(app)

        def test_toxic_contract(self):
            with patch("backend.api.inference.predict_toxic_text") as mock_predict:
                mock_predict.return_value = {
                    "label": "Toxic",
                    "confidence": 0.93,
                    "interpretation": "Strong toxic signal",
                }

                response = self.client.post("/toxic/predict", json={"text": "you are awful"})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "label": "Toxic",
                    "confidence": 0.93,
                    "interpretation": "Strong toxic signal",
                },
            )

        def test_bot_contract(self):
            with patch("backend.api.inference.predict_bot_user") as mock_predict:
                mock_predict.return_value = {
                    "prediction": "Bot",
                    "confidence": 0.87,
                    "interpretation": "High bot likelihood.",
                    "account_age_days": 14,
                }

                payload = {
                    "description": "new account",
                    "followers_count": 5,
                    "following_count": 1,
                    "tweet_count": 2,
                    "account_age_days": 14,
                }
                response = self.client.post("/bot/predict", json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "prediction": "Bot",
                    "confidence": 0.87,
                    "interpretation": "High bot likelihood.",
                    "account_age_days": 14,
                },
            )

        def test_combined_contract(self):
            with patch("backend.api.inference.analyze_combined_payload") as mock_predict:
                mock_predict.return_value = {
                    "toxic": {
                        "label": "Toxic",
                        "confidence": 0.92,
                        "interpretation": "Strong toxic signal",
                    },
                    "bot": {
                        "prediction": "Bot",
                        "confidence": 0.88,
                        "interpretation": "High bot likelihood.",
                        "account_age_days": 21,
                    },
                    "toxicity_risk": 0.92,
                    "bot_risk": 0.88,
                    "risk_score": 0.9,
                    "risk_level": "High Risk",
                    "summary": "The account and comment both show strong risk indicators.",
                    "recommendation": "Review this account and comment urgently.",
                }

                payload = {
                    "comment": "spam comment",
                    "description": "bio",
                    "followers_count": 4,
                    "following_count": 2,
                    "tweet_count": 3,
                    "account_age_days": 21,
                }
                response = self.client.post("/analysis/combined", json=payload)

            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["risk_level"], "High Risk")
            self.assertEqual(body["risk_score"], 0.9)
            self.assertIn("toxic", body)
            self.assertIn("bot", body)
else:

    class ApiContractTests(unittest.TestCase):
        @unittest.skip("fastapi is not installed in this environment")
        def test_api_contracts(self):
            pass


if __name__ == "__main__":
    unittest.main()
