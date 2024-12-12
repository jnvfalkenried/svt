from datetime import datetime

from pydantic import BaseModel


class HashtagRequest(BaseModel):
    """
    Schema for requesting data based on a specific hashtag.
    
    This class represents a request that contains a hashtag to filter or search for posts related to that hashtag.
    """
    hashtag: str
    """The hashtag to filter posts or data by. Only posts containing this hashtag will be included."""


class UserRequest(BaseModel):
    """
    Schema for creating or updating a user account.

    This class contains the necessary attributes for creating a new user or updating an existing user account, 
    including their username, email, password, and assigned roles.
    """
    username: str
    """The unique username of the user. Used for login and identification."""
    email: str
    """The email address of the user. Used for communication and account verification."""
    password: str
    """The password associated with the user account. Used for authentication."""
    roles: str
    """The roles assigned to the user (e.g., "admin", "user", etc.), determining their permissions as JSON string."""


class LoginRequest(BaseModel):
    """
    Schema for user login.

    This class contains the necessary fields for a user to authenticate and log into the platform, 
    including their username and password.
    """
    username: str
    """The username of the user attempting to log in."""
    password: str
    """The password associated with the user account for authentication."""


class PostsRequest(BaseModel):
    """
    Schema for filtering and sorting posts based on various criteria.
    
    This class represents the request parameters used for fetching posts, including filtering by date range, 
    hashtag, sorting by a specific category, and limiting the number of posts returned.
    """
    feed: bool
    """Indicates whether to sort the posts based on their appearance in the feed."""
    start_date: datetime
    """The start date for filtering posts. Only posts collected on or after this date will be included."""
    end_date: datetime
    """The end date for filtering posts. Only posts collected on or before this date will be included."""
    hashtag: str
    """The hashtag to filter posts. Only posts containing this hashtag will be included."""
    category: str
    """The category used to sort the posts (e.g., "Likes", "Comments"). Determines the metric to rank posts by."""
    limit: int
    """The maximum number of posts to return in the response."""


class PlatformGrowthRequest(BaseModel):
    """
    Schema for requesting platform growth data over a specified time interval.
    
    This class represents the parameters used to fetch platform growth data, with the ability to specify the time 
    interval for the growth measurement (e.g., daily, weekly, or monthly).
    """
    interval: str
    """The time interval for measuring platform growth (e.g., "Day", "Week", "Month")."""
