# Application entry point
from app import create_app

app = create_app()

if __name__ == "__main__":
    # TODO: Change debug to False in production
    app.run(debug=True, host='0.0.0.0', port=5000)