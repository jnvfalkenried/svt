# TikTok Data Intelligence Application

The **TikTok Data Intelligence Application** is a streamlined, open-source solution for retrieving and analyzing TikTok content. Built with both user-friendliness and technical flexibility in mind, this platform provides an intuitive interface along with a customizable architecture that developers can extend and adapt to their specific needs.

---

## Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Project Links](#project-links)
- [Version](#version)
- [Resources](#resources)
- [Contributors](#contributors)
- [Licensing](#licensing)

---

## About

The TikTok Data Intelligence Application allows you to monitor hashtags, track content trends, and perform advanced image searches. Designed for both general users and developers, it features flexible scheduling, and customizable monitoring capabilities.

---

## Key Features

- **Comprehensive TikTok Content Retrieval**: Retrieve content and hashtag data from TikTok with detailed insights into trends and user interactions.
- **Hashtag Tracking**: Monitor specific hashtags to gather metrics on popularity, trends, and engagement over time.
- **Advanced Image and Content Search**: Perform detailed searches for specific content or images related to the hashtags you are monitoring.
- **Direct Content Linking**: Easily access TikTok content through direct links for further analysis or reference.
- **Open-Source and Customizable Architecture**: Adapt and extend the platform to meet your specific needs, whether for personal use or advanced integrations.
- **Data Refresh and Synchronization**: Keep your data up-to-date with a sophisticated scheduling mechanism:
  - **Hashtag monitoring**: Updates every 30 minutes.
  - **Content processing**: Runs at 00:01, 08:01, and 16:01.
  - **Post trends view refresh**: Occurs at 01:00, 09:00, and 17:00.
  - **Author trends view refresh**: Runs at 01:05, 09:05, and 17:05.

---

## Getting Started

> **Note**: This section will be filled out soon.

Instructions on how to set up the project locally, install dependencies, and run the application will be included here.

---

## Project Links

- GitHub Repository: [https://github.com/your-repo-link](https://github.com/your-repo-link)
- Documentation: [Coming soon]
- Issues Tracker: [https://github.com/your-repo-link/issues](https://github.com/your-repo-link/issues)

---

## Version

**TikTok Data Intelligence Application v1.0.0**

The initial release of the application, with features for hashtag tracking, content retrieval, and synchronization.

---

## Resources

- **GitHub Repository**: [https://github.com/your-repo-link](https://github.com/your-repo-link)
- **Documentation**: [Coming soon]
- **API Documentation**: [Coming soon]

---

## Contributors

- **Anand Mathew M S** — Data Scientist [https://github.com/your-repo-link](https://github.com/anandmatt)
- **Elise Hammarström** — Data Scientist [https://github.com/your-repo-link](https://github.com/elisehammarstrom)
- **Just Niklas von Falkenried** — Data Scientist [https://github.com/your-repo-link](https://github.com/jnvfalkenried)
- **Rustam Ismailov** — Data Scientist [https://github.com/your-repo-link](https://github.com/Ftalysh)

---

## Licensing

This project is licensed under the terms specified in the [LICENSE](LICENSE) file. You are free to use, modify, and distribute the software under these terms.

For more details on the license, view the full [LICENSE](LICENSE) file in our GitHub repository.

---

## Acknowledgements

> **Note**: This section will be added soon.
- Special thanks to contributors, open-source libraries, or resources used in the development of the project.




# Old content

## svt
Project in Cooperation with SVT


## Infra:
alembic for db version control
rabbitmq for queue management
postgresql (pgvector for storing embeddings)


### Alembic commands
- If you want to make changes to database models, add or modify files in [database_models](src/postgresql/database_models/).
- Following this, new migration script can be created using the command
    ```bash
        alembic revision --autogenerate -m "<Insert your message here>"
    ``` 

- The migrations can then be applied using the command:
    ```bash
        alembic upgrade head
    ```

## Code Quality Tools:
To keep your code clean, organized, and easy to maintain, here are some handy tools to consider (first 2 is highly recommended):
* Black: A strict, no-nonsense code formatter for Python that enforces consistent style. (VSCode Extension ID: ms-python.black-formatter)
* isort: Automatically sorts your imports, making them cleaner and easier to read. (VSCode Extension ID: ms-python.isort)
* Pylance: A fast, feature-packed language server for Python that boosts code analysis and autocomplete. (VSCode Extension ID: ms-python.vscode-pylance)
* autoDocstring: A useful extension for automatically generating docstrings for functions, saving you time and improving documentation. (VSCode Extension ID: njpwerner.autodocstring)

## .env skeleton, fill in your values

```env
# RabbitMQ Configuration
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASS=
RABBITMQ_EXCHANGE=
RABBITMQ_HASHTAG_QUEUE=
RABBITMQ_VIDEO_BYTES_QUEUE=
RABBITMQ_EMBEDDINGS_QUEUE=

# PostgreSQL Configuration
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# Other environment variables
HOME_DIR=


This project incorporates certain parts of the TikTok-Api project by David Teather
(https://github.com/davidteather/TikTok-Api), licensed under the MIT License.
The utilized portions include functionality for session creation and TikTok API interactions.
