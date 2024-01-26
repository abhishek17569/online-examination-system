# Online Examination REST APIs

The technology stack used is Python + Flask + MongoDB

## Overview

This project is a Dockerized Flask API with MongoDB as the database. It consists of two containers: one for the server and one for the database. The API documentation is available at BASE_URL/api/v1.

## Prerequisites

- Docker installed on your machine

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/abhishek17569/online-examination-system.git
    ```

2. Change into the project directory:

    ```bash
    cd online-examination-system
    ```

3. Start the containers:

    ```bash
    docker-compose build && docker-compose up
    ```

    This will build the images and start the containers.

4. Access the API documentation at BASE_URL/api/v1.

5. Enter the server container bash:

    ```bash
    docker exec -it server-container bash
    ```

6. Inside the server container, execute `insert_sample_users.py` to add sample users:

    ```bash
    python insert_sample_users.py
    ```

## API Documentation

The API documentation is available at BASE_URL/api/v1. To authenticate, include the following headers in your requests:

- **Email**: Your registered email address
- **Password**: Your password

Example using cURL:

```bash
curl -X GET BASE_URL/api/v1/some_endpoint -H "email: your@email.com" -H "password: yourpassword"
