import unittest

from app.services.action_guide import build_action_guide_pdf


class ActionGuideTests(unittest.TestCase):
	def test_guide_builder_returns_a_pdf_document(self) -> None:
		content = build_action_guide_pdf()

		self.assertTrue(content.startswith(b"%PDF-"))
		self.assertGreater(len(content), 1000)