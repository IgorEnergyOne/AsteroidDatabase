from app import create_app
from waitress import serve


# app = create_app()
if __name__ == "__main__":
    app = create_app()
    serve(app, host="127.0.0.1", port=5000, url_scheme="http")
