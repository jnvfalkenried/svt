# TikTok Data Intelligence Application

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

The **TikTok Data Intelligence Application** is a streamlined, open-source solution for retrieving and analyzing TikTok content. Built with both user-friendliness and technical flexibility in mind, this platform provides an intuitive interface along with a customizable architecture that developers can extend and adapt to their specific needs.

This application was created as a product for the Swedish National Television Company, Sveriges Television (SVT). SVT asked us to build an application that fetches and processes open source tiktok data. 

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

> **Note**: Add more text here

Follow these steps to get started with using this project.

### Prerequisites

Make sure you have the following installed on your system:
- Docker Desktop

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/jnvfalkenried/svt.git
    cd your-repo
    ```

2. **Copy the example environment file and configure it:**

    ```sh
    cp .env.example .env
    # Edit the .env file to configure your environment variables
    ```

3. **Build and start the Docker containers:**

    ```sh
    docker compose up -d --build
    ```

4. **Check the status of the containers:**

    ```sh
    docker compose ps
    ```

### Usage

Once the containers are up and running, you can access the services as follows:

- **FastAPI**: Access the FastAPI documentation at [http://localhost/docs](http://localhost/docs)
- **RabbitMQ**: Access the RabbitMQ web interface at [http://localhost:15672](http://localhost:15672)
- **PostgreSQL**: Access the PostgreSQL database by running:

    ```sh
    docker exec -it svt-postgres-1 psql -U postgres -d svt_db
    ```

### Additional Commands

- **Clean old cache:**

    ```sh
    docker builder prune
    ```

- **Build with no cache:**

    ```sh
    docker compose build --no-cache
    ```

- **Remove old containers and volumes:**

    ```sh
    docker compose down -v
    ```

- **Start specific containers:**

    ```sh
    docker compose up postgres db-api react-frontend
    ```

For more detailed information, refer to the individual Dockerfiles and scripts in the repository.

Feel free to reach out to the contributors if you have any questions or need further assistance.

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

- **Anand Mathew M S** — Data Scientist [https://github.com/anandmatt](https://github.com/anandmatt)
- **Elise Hammarström** — Data Scientist [https://github.com/elisehammarstrom](https://github.com/elisehammarstrom)
- **Just Niklas von Falkenried** — Data Scientist [https://github.com/jnvfalkenried](https://github.com/jnvfalkenried)
- **Rustam Ismailov** — Data Scientist [https://github.com/Ftalysh](https://github.com/Ftalysh)

---

## Licensing

This project is licensed under the terms specified in the [LICENSE](LICENSE) file. You are free to use, modify, and distribute the software under these terms.

For more details on the license, view the full [LICENSE](LICENSE) file in our GitHub repository.

---

## Acknowledgements

> **Note**: This section will be added soon.
- Special thanks to contributors, open-source libraries, or resources used in the development of the project.

- This project incorporates certain parts of the TikTok-Api project by David Teather
(https://github.com/davidteather/TikTok-Api), licensed under the MIT License.
The utilized portions include functionality for session creation and TikTok API interactions.

## Misc

### Code Quality Tools:
To keep your code clean, organized, and easy to maintain, here are some handy tools to consider (first 2 is highly recommended):
* Black: A strict, no-nonsense code formatter for Python that enforces consistent style. (VSCode Extension ID: ms-python.black-formatter)
* isort: Automatically sorts your imports, making them cleaner and easier to read. (VSCode Extension ID: ms-python.isort)
* Pylance: A fast, feature-packed language server for Python that boosts code analysis and autocomplete. (VSCode Extension ID: ms-python.vscode-pylance)
* autoDocstring: A useful extension for automatically generating docstrings for functions, saving you time and improving documentation. (VSCode Extension ID: njpwerner.autodocstring)

