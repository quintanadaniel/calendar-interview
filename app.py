from http import HTTPStatus

from application import create_app
from application import page_not_found

app = create_app('default')


if __name__ == "__main__":
    app.register_error_handler(HTTPStatus.NOT_FOUND, page_not_found)
    app.run()
