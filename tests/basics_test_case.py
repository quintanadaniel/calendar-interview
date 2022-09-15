import unittest
from datetime import datetime

from flask import current_app

from application import create_app
from application import db
from application.models import User


class BasicsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
