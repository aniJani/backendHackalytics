from fastapi import FastAPI
from app.routers import dataset, visualization, chatbot, insights, fred
from app.utils.database import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dashboard App API")

# Set up CORS settings
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://infolaya.vercel.app",  # Vercel domain
    "https://www.infolaya.tech",  # Custom domain
    "https://infolaya.tech",  # Root domain (if needed)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    await init_db()


# Include routers with appropriate prefixes
app.include_router(dataset.router, prefix="/api/dataset", tags=["dataset"])
app.include_router(
    visualization.router, prefix="/api/visualization", tags=["visualization"]
)
# app.include_router(
#     chatbot.router, prefix="/api/chatbot", tags=["chatbot"]
# )  # this is useless
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(fred.router, prefix="/api/fred", tags=["fred"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Dashboard App API"}
