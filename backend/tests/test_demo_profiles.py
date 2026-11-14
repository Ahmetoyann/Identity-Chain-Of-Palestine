import unittest

from app.demo_profiles import build_demo_profiles


class DemoProfileTests(unittest.TestCase):
	def test_demo_profiles_are_twenty_synthetic_records(self) -> None:
		profiles = build_demo_profiles()

		self.assertEqual(len(profiles), 20)
		self.assertEqual(len({profile["slug"] for profile in profiles}), 20)
		self.assertTrue(all(profile["is_demo"] is True for profile in profiles))
		self.assertTrue(all(profile["status"] == "temsili" for profile in profiles))
		self.assertTrue(all("Test Kişi" not in profile["name"] for profile in profiles))
		self.assertTrue(all("gerçek" in profile["biography"].lower() for profile in profiles))
		self.assertTrue(all(profile["image_data"].startswith(b"<svg") for profile in profiles))
		self.assertTrue(all(profile["image_media_type"] == "image/svg+xml" for profile in profiles))