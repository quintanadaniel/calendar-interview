from datetime import datetime

from application import db
from application.models import User
from tests.basics_test_case import BasicsTestCase


class TestCalendar(BasicsTestCase):
    def test_all_calendar_interviews_when_not_arguments_param_with_bad_request(self):
        response = self.client.get("/api/calendarinterviews")

        self.assertEqual(400, response.status_code)

    def test_all_calendar_interviews_when_have_one_more_candidate_arguments_param_with_bad_request(
        self,
    ):
        response = self.client.get(
            "/api/calendarinterviews?candidate=daniel,&interviewers=pedro,rosa"
        )

        self.assertEqual(400, response.status_code)
        self.assertCountEqual({"error": "Maximum one candidate."}, response.json)

    def test_all_calendar_interviews_when_have_two_more_interviewers_arguments_param_with_bad_request(
        self,
    ):
        response = self.client.get(
            "/api/calendarinterviews?candidate=daniel&interviewers=pedro,rosa,"
        )

        self.assertEqual(400, response.status_code)
        self.assertCountEqual(
            {"error": "Maximum two interviewers in the list."}, response.json
        )

    def test_all_calendar_interviews_when_not_have_interviewers_arguments_param_with_bad_request(
        self,
    ):
        response = self.client.get("/api/calendarinterviews?candidate=daniel")

        self.assertEqual(400, response.status_code)
        self.assertCountEqual(
            {
                "error": "the arguments should be one candidate and two interviewers split by coma"
            },
            response.json,
        )

    def test_all_calendar_interviews_when_not_have_candidate_arguments_param_with_bad_request(
        self,
    ):
        response = self.client.get("/api/calendarinterviews?interviewers=pedro,rosa")

        self.assertEqual(400, response.status_code)
        self.assertCountEqual(
            {
                "error": "the arguments should be one candidate and two interviewers split by coma"
            },
            response.json,
        )

    def test_all_calendar_interviews_with_not_found(self):
        response = self.client.get(
            "api/calendarinterviews?candidate=daniel&interviewers=pedro,rosa"
        )

        self.assertEqual(404, response.status_code)
        self.assertCountEqual(
            [],
            response.json,
        )

    def test_all_calendar_interviews(self):
        candidate1 = User(
            username="maria",
            role="candidate",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(candidate1)
        db.session.commit()
        candidate2 = User(
            username="maria",
            role="candidate",
            available_date=datetime(2022, 10, 20, 15, 0),
        )
        db.session.add(candidate2)
        db.session.commit()

        interviewer1 = User(
            username="rosa",
            role="interviewer",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(interviewer1)
        db.session.commit()
        interviewer2 = User(
            username="carmen",
            role="interviewer",
            available_date=datetime(2022, 10, 10, 10, 0),
        )
        db.session.add(interviewer2)
        db.session.commit()

        response = self.client.get(
            "api/calendarinterviews?candidate=maria&interviewers=rosa,carmen"
        )

        self.assertEqual(200, response.status_code)
        self.assertCountEqual(
            [{
                "candidate": {
                    "available_date": "2022-10-10T10:00:00",
                    "role": "candidate",
                    "username": "maria",
                },
                "interviewers": [
                    {
                        "available_date": "2022-10-10T10:00:00",
                        "role": "interviewer",
                        "username": "carmen",
                    },
                    {
                        "available_date": "2022-10-10T10:00:00",
                        "role": "interviewer",
                        "username": "rosa",
                    },
                ],
            }],
            response.json,
        )
