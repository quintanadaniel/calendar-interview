from datetime import datetime

from application import db
from application.models import User
from tests.basics_test_case import BasicsTestCase


class TestModels(BasicsTestCase):
    def test_users_representation(self):
        users = User(
            username="test1",
            role="candidate",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(users)
        db.session.commit()

        self.assertEqual("test1", users.username)
        self.assertEqual("candidate", users.role)
        self.assertEqual(
            datetime.strptime("2022-10-10 10:00", "%Y-%m-%d %H:%M"),
            users.available_date,
        )
