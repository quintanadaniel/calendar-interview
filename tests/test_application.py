from tests.basics_test_case import BasicsTestCase


class TestApplication(BasicsTestCase):
    def test_page_not_found_when_is_true(self):
        response = self.client.get("/test")

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            b"<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL "
            b"was not found on the server. If you entered the URL manually please check your spelling and try "
            b"again.</p>\n",
            response.data,
        )

    def test_page_not_found_when_is_false(self):
        response = self.client.get("/api/status")

        self.assertEqual(200, response.status_code)
