from api.author_trends import router as author_trends_router
from api.authors import router as authors_router
from api.hashtag_trends import router as hashtag_trends_router
from api.hashtags import router as hashtags_router
from api.post_trends import router as post_trends_router
from api.posts import router as posts_router
from api.related_hashtags import router as related_hashtags_router
from api.search import router as search_router
from api.stats import router as stats_router
from api.users import router as users_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(posts_router)
app.include_router(post_trends_router)
app.include_router(hashtag_trends_router)
app.include_router(related_hashtags_router)
app.include_router(author_trends_router)
