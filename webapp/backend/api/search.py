# api/search.py
import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from schemas.response import AuthorResponse, MatchResponse, PostResponse
from sqlalchemy import text
from vertexai.vision_models import Image, MultiModalEmbeddingModel

from postgresql.config.db import session

router = APIRouter()


@router.post("/api/search/multimodal")
async def multimodal_search(
    query: str = Form(default=None),
    image: UploadFile = File(default=None),
    limit: int = 3000,
) -> list[MatchResponse]:
    """
    Perform a multimodal search (text and/or image) for posts, retrieving the most similar posts 
    based on a query or an uploaded image.
    
    Args:
        query (str): Optional textual query for search.
        image (UploadFile): Optional image file for search.
        limit (int): Number of top results to return (default: 3000).
    
    Returns:
        List[MatchResponse]: List of matched posts with their authors and similarity details.
    
    Raises:
        HTTPException: If either query or image is not provided, or if an error occurs.
    """
    print(f"Received request - query: {query}, image present: {image is not None}")

    if not query and not image:
        raise HTTPException(
            status_code=400, detail="Either query text or image is required"
        )

    try:
        model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
        query_embedding = None

        if query:
            print(f"Processing text query: {query}")
            query = query.strip().lower()
            embeddings = model.get_embeddings(contextual_text=query, dimension=1408)
            query_embedding = embeddings.text_embedding
            print("Text embedding generated successfully")

        if image:
            print("Processing uploaded image")
            contents = await image.read()
            with open("temp_search.jpg", "wb") as f:
                f.write(contents)

            image_obj = Image.load_from_file("temp_search.jpg")
            embeddings = model.get_embeddings(image=image_obj, dimension=1408)
            query_embedding = embeddings.image_embedding
            print("Image embedding generated successfully")

            import os

            os.remove("temp_search.jpg")

        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate embedding")

        print("Starting database search")
        async with session() as s:
            try:
                if isinstance(query_embedding, np.ndarray):
                    query_embedding = query_embedding.tolist()

                vector_str = "[" + ",".join(str(x) for x in query_embedding) + "]"
                print(f"Vector string length: {len(vector_str)}")

                search_query = text(
                    """
                WITH ranked_embeddings AS (
                    SELECT 
                        p.*,
                        ve.element_id,
                        1 - (ve.embedding <=> cast(:query_vector as vector)) as cosine_similarity,
                        ROW_NUMBER() OVER (
                            PARTITION BY p.id 
                            ORDER BY 1 - (ve.embedding <=> cast(:query_vector as vector)) DESC
                        ) as rank
                    FROM 
                        video_embeddings ve
                        JOIN posts p ON ve.post_id = p.id
                    WHERE (1 - (ve.embedding <=> cast(:query_vector as vector))) > 0.2
                )
                SELECT *
                FROM ranked_embeddings
                WHERE rank = 1
                ORDER BY cosine_similarity DESC
                LIMIT :search_limit
                """
                )

                results = await s.execute(
                    search_query, {"query_vector": vector_str, "search_limit": limit}
                )

                matches = results.fetchall()
                print(f"Found {len(matches)} matches")

                if not matches:
                    return []

                author_ids = [match.author_id for match in matches]
                authors_query = await s.execute(
                    text(
                        """
                        WITH post_stats AS (
                            SELECT
                                id,
                                MAX(digg_count) AS max_digg_count,
                                MAX(play_count) AS max_play_count,
                                MAX(share_count) AS max_share_count,
                                MAX(collect_count) AS max_collect_count
                            FROM posts_reporting
                            GROUP BY id
                        ),
                        author_stats AS (
                            SELECT
                                id,
                                MAX(follower_count) AS follower_count,
                                MAX(following_count) AS following_count
                            FROM authors_reporting
                            GROUP BY id
                        )
                        SELECT
                            a.id,
                            a.nickname,
                            a.signature,
                            astats.follower_count,
                            astats.following_count,
                            p.description,
                            s.max_digg_count,
                            s.max_play_count,
                            s.max_share_count,
                            s.max_collect_count
                        FROM posts p
                        LEFT JOIN post_stats s ON p.id = s.id
                        LEFT JOIN authors a ON p.author_id = a.id
                        LEFT JOIN author_stats astats ON a.id = astats.id
                        WHERE a.id = ANY(:ids)"""
                    ),
                    {"ids": author_ids},
                )
                authors_dict = {str(author.id): author for author in authors_query}

                formatted_results = []
                for match in matches:
                    author = authors_dict.get(str(match.author_id))
                    result = MatchResponse(
                        post_id=str(match.id),
                        description=match.description or "",
                        similarity=float(match.cosine_similarity),
                        element_id=str(match.element_id),
                        author=AuthorResponse(
                            id=str(author.id),
                            nickname=author.nickname or "Unknown",
                            signature=author.signature or "Unknown",
                            follower_count=author.follower_count or 0,
                            following_count=author.following_count or 0,
                        ),
                        post=PostResponse(
                            id=str(match.id),
                            created_at=(
                                int(match.created_at) if match.created_at else None
                            ),
                            description=match.description or "",
                            duet_enabled=match.duet_enabled or False,
                            duet_from_id=(
                                str(match.duet_from_id) if match.duet_from_id else None
                            ),
                            is_ad=match.is_ad or False,
                            can_repost=match.can_repost or False,
                            author_id=str(match.author_id) if match.author_id else None,
                            music_id=str(match.music_id) if match.music_id else None,
                            max_digg_count=author.max_digg_count or 0,
                            max_play_count=author.max_play_count or 0,
                            max_share_count=author.max_share_count or 0,
                            max_collect_count=author.max_collect_count or 0,
                        ),
                    )
                    formatted_results.append(result)

                return formatted_results

            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                raise HTTPException(
                    status_code=500, detail=f"Database error: {str(db_error)}"
                )

    except Exception as e:
        print(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
