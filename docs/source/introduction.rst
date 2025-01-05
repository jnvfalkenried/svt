Introduction
========================

..
    _Overview of the application.
    _Technology stack used (Python, RabbitMQ, React, FastAPI).
    _Purpose (scraping TikTok data, processing, and displaying it).

The **TikTok Data Intelligence Application** is a streamlined, open-source solution for retrieving and analyzing TikTok content. Built with both user-friendliness and technical flexibility in mind, this platform provides an intuitive interface along with a customizable architecture that developers can extend and adapt to their specific needs.

**Purpose**: This application was created for Sveriges Television (SVT), the Swedish National Television Company, to fetch and process open-source TikTok data.

**Technology Stack**:
    * Python
    * RabbitMQ
    * React
    * FastAPI
    * PostgreSQL

Key Features
------------

1. **Comprehensive TikTok Content Retrieval**:
   Retrieve content and hashtag data from TikTok with detailed insights into trends and user interactions.

2. **Hashtag Tracking**:
   Monitor specific hashtags to gather metrics on popularity, trends, and engagement over time.

3. **Advanced Image and Content Search**:
   Perform detailed searches for specific content or images related to the hashtags you are monitoring.

4. **Direct Content Linking**:
   Easily access TikTok content through direct links for further analysis or reference.

5. **Open-Source and Customizable Architecture**:
   Adapt and extend the platform to meet your specific needs, whether for personal use or advanced integrations.

6. **Data Refresh and Synchronization**:
   Keep your data up-to-date with a sophisticated scheduling mechanism:
   
   - **Hashtag monitoring**: Updates every 30 minutes.
   - **Content processing**: Runs at 00:01, 08:01, and 16:01.
   - **Post trends view refresh**: Occurs at 01:00, 09:00, and 17:00.
   - **Author trends view refresh**: Runs at 01:05, 09:05, and 17:05.
   - **Recompute Association Rules**: Runs at 01:30.

Getting Started
---------------

To use the TikTok Data Intelligence Application:
#. Clone the repository from GitHub (https://github.com/jnvfalkenried/svt).
#. Follow the setup instructions to configure the environment.
#. Start the application and begin monitoring TikTok data.
