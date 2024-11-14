from postgresql.database_models.active_hashtags import *
from postgresql.database_models.authors import *
from postgresql.database_models.base import *
from postgresql.database_models.challenges import *
from postgresql.database_models.music import *
from postgresql.database_models.posts import *
from postgresql.database_models.posts_challenges import *
from postgresql.database_models.posts_reporting import *
from postgresql.database_models.video_embeddings import *

__all__ = ['Base', 'Posts', 'VideoEmbeddings']

from sqlalchemy.orm import configure_mappers

configure_mappers()
