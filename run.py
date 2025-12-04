from app import create_app
from routes import create_task


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5555, debug=True)
