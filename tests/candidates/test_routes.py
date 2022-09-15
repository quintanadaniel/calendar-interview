from datetime import datetime

from application import db
from application.models import User
from tests.basics_test_case import BasicsTestCase


class TestCandidates(BasicsTestCase):

    def test_create_when_not_valid_datetime(self):
        request = {"username": "test candidate", "available_date": "2022-10-10 10:10"}
        response = self.client.post("/api/candidates", json=request)

        self.assertEqual(400, response.status_code)
        self.assertCountEqual(
            {
                "messages": {
                    "json": {
                        "available_date": ["The range of time should be for hour."]
                    }
                }
            },
            response.json,
        )

    def test_create_when_candidate_exists(self):
        """Create a candidate when use case exist in db"""
        users = User(
            username="test candidate",
            role="candidate",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(users)
        db.session.commit()

        request = {"username": "test candidate", "available_date": "2022-10-10 10:00"}
        response = self.client.post("/api/candidates", json=request)

        self.assertEqual(400, response.status_code)
        self.assertCountEqual({}, response.json)

    def test_create(self):
        request = {"username": "maria", "available_date": "2022-09-20 09:00"}
        response = self.client.post("/api/candidates", json=request)

        self.assertEqual(201, response.status_code)
        self.assertCountEqual(
            {
                "available_date": "2022-09-20 09:00",
                "role": "candidate",
                "username": "maria",
            },
            response.json,
        )

    def test_candidate_all(self):
        """Create a candidate when use case exist in db"""
        users = User(
            username="test candidate",
            role="candidate",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(users)
        db.session.commit()
        response = self.client.get("/api/candidates")

        self.assertEqual(200, response.status_code)
        self.assertCountEqual(
            [
                {
                    "available_date": "2022-10-10 10:00",
                    "role": "candidate",
                    "username": "test candidate",
                }
            ],
            response.json,
        )

    def test_candidate_all_when_not_found(self):
        response = self.client.get("/api/candidates")

        self.assertEqual(404, response.status_code)
        self.assertCountEqual(
            [],
            response.json,
        )
