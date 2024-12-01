from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.authors import router as authors_router
from api.hashtags import router as hashtags_router
from api.users import router as users_router
from api.search import router as search_router
from api.stats import router as stats_router
from api.post_trends import router as post_trends_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(authors_router)
app.include_router(hashtags_router)
app.include_router(users_router)
app.include_router(search_router)
app.include_router(stats_router)
app.include_router(post_trends_router)
