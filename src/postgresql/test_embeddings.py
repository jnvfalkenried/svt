import os
import sys
import asyncio
import numpy as np
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import sqlalchemy as sa

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)  # src directory
sys.path.append(src_dir)

# Now import your models
from postgresql.database_models.base import Base
from postgresql.database_models.posts import Posts
from postgresql.database_models.video_embeddings import VideoEmbeddings

async def test_embeddings():
    # Create async engine
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/svt_db",
        echo=True
    )
    
    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Test inserting embeddings
    async with async_session() as session:
        # First delete the existing embedding
        await session.execute(
            sa.delete(VideoEmbeddings).where(VideoEmbeddings.id == '7254498547880561922')
        )
        await session.commit()
        print("Deleted existing embedding if it existed")

        # First get an existing post ID from the database
        existing_post = await session.execute(
            select(Posts.id).limit(1)
        )
        post_id = existing_post.scalar_one()  # gets the first post ID
        
        try:
            # Create a test embedding
            test_embedding = VideoEmbeddings(
                id=post_id,  # This should match an existing post id
                video_embedding=np.random.rand(1408).tolist(),
                description_embedding=np.random.rand(1408).tolist(),
                description="Test video description"
            )
            
            session.add(test_embedding)
            await session.commit()
            
            print("Successfully inserted test embedding")
            
            # Test querying similar videos
            query_embedding = np.random.rand(1408).tolist()
            similar_videos = await VideoEmbeddings.find_similar(
                session, 
                query_embedding,
                limit=5
            )
            
            print("\nSimilar videos:")
            for video in similar_videos:
                print(f"Video ID: {video.id}, Description: {video.description}")
                
        except Exception as e:
            print(f"Error: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(test_embeddings())