from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Use your MongoDB Atlas connection string here.
    MONGODB_URL: str = (
        "mongodb+srv://<username>:<password>@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    MONGODB_DBNAME: str = "dashboard_db"
    OPENAI_API_KEY: str = "your_openai_api_key"  # Replace with your actual key

    class Config:
        env_file = ".env"


settings = Settings()
