Setup and Installation
======================

..
    _Prerequisites (Python version, RabbitMQ setup, Node.js for React).
    _How to install and configure the application.

Follow these steps to get started with using this project.

Prerequisites
-------------

Ensure you have the following installed on your system:

- **Docker Engine**: Required for running the application in a containerized environment.

Installation
------------

1. **Clone the Repository**:

   Open your terminal and run the following commands:

   .. code-block:: bash

      git clone https://github.com/jnvfalkenried/svt.git
      cd svt

2. **Configure the Environment Variables**:

   Copy the example environment file and edit it to suit your environment:

   .. code-block:: bash

      cp .env.example .env

   Open the `.env` file in a text editor and update the values as needed for your setup.

3. **Build and Start the Docker Containers**:

   Run the following command to build and start the application:

   .. code-block:: bash

      docker compose up -d --build

4. **Check the Status of the Containers**:

   Ensure all containers are running as expected:

   .. code-block:: bash

      docker compose ps

Additional Notes
----------------

- To stop the application, use:

  .. code-block:: bash

     docker compose down

- For troubleshooting or viewing logs, use:

  .. code-block:: bash

     docker compose logs -f

*Tip: Make sure your Docker Desktop is running before starting the containers.*

