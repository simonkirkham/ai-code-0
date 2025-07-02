import unittest
from datetime import datetime, timedelta
from src.countdown import get_countdown_string

class TestCountdownString(unittest.TestCase):
    def test_future_date(self):
        future = datetime.now() + timedelta(days=2, hours=3, minutes=4, seconds=5)
        result = get_countdown_string(future)
        self.assertIn('d', result)
        self.assertIn('h', result)
        self.assertIn('m', result)
        self.assertIn('s left', result)

    def test_past_date(self):
        past = datetime.now() - timedelta(days=1)
        result = get_countdown_string(past)
        self.assertEqual(result, "The date/time has already passed!")

    def test_now(self):
        now = datetime.now()
        result = get_countdown_string(now)
        self.assertTrue(result.startswith('0d'))

if __name__ == "__main__":
    unittest.main()
