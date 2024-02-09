from pathlib import Path
from dotenv import load_dotenv
import os

from app import create_app
from app.db.initialization import init_database_schema


app = create_app()
ENV_PATH = "./db.env"

if __name__ == "__main__":
    load_dotenv(Path(ENV_PATH))
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    init_database_schema()
    app.run(host="0.0.0.0", debug=True)
