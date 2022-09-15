from datetime import datetime

from application import db
from application.models import User
from tests.basics_test_case import BasicsTestCase


class TestInterviewers(BasicsTestCase):
    def test_create_when_not_valid_datetime(self):
        request = {"username": "test interviewer", "available_date": "2022-10-10 10:10"}
        response = self.client.post("/api/interviewers", json=request)

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

    def test_create_when_interviewer_exists(self):
        """Create an interviewer when use case exist in db"""
        users = User(
            username="test interviewer",
            role="interviewer",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(users)
        db.session.commit()

        request = {"username": "test interviewer", "available_date": "2022-10-10 10:00"}
        response = self.client.post("/api/interviewers", json=request)

        self.assertEqual(400, response.status_code)
        self.assertCountEqual({}, response.json)

    def test_create(self):
        request = {"username": "maria", "available_date": "2022-09-20 09:00"}
        response = self.client.post("/api/interviewers", json=request)

        self.assertEqual(201, response.status_code)
        self.assertCountEqual(
            {
                "available_date": "2022-09-20 09:00",
                "role": "interviewer",
                "username": "maria",
            },
            response.json,
        )

    def test_interviewer_all(self):
        """Create an interviewer when use case exist in db"""
        users = User(
            username="test interviewer",
            role="interviewer",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(users)
        db.session.commit()
        response = self.client.get("/api/interviewers")

        self.assertEqual(200, response.status_code)
        self.assertCountEqual(
            [
                {
                    "available_date": "2022-10-10 10:00",
                    "role": "interviewer",
                    "username": "test interviewer",
                }
            ],
            response.json,
        )

    def test_candidate_all_when_not_found(self):
        response = self.client.get("/api/interviewers")

        self.assertEqual(404, response.status_code)
        self.assertCountEqual(
            [],
            response.json,
        )
