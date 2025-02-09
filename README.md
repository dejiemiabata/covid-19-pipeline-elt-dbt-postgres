# COVID-19 Data Ingestion and Analysis Pipeline

This project ingests COVID-19 data from REST APIs, processes it, and loads it into a PostgreSQL database. The data is then ready for further analysis using dbt. Data related to infection percent, by state, is also later exported to csv files.

### Prerequisites

- **Docker & Docker Compose** Download Docker Desktop [Docker Download](https://www.docker.com/products/docker-desktop/) and install it. Verify by running `docker --version` & `docker-compose --version`
- **Poetry** (for managing dependencies) Install python3.12 (https://www.python.org/downloads/macos/), Install Poetry by runing this command `curl -sSL https://install.python-poetry.org | python3 -` & ensure it exists in path `export PATH="$HOME/.local/bin:$PATH"`. You can verify by running  `python3 --version` & `poetry --version` in your local terminal
- **Environment variables** configured in a `.env` file that can be setup by running `cp env.template .env`


#### Sample `.env` file
```
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=covid_data
API_BASE_URL=https://api.covidtracking.com/v2/
POSTGRES_DATABASE_URL=postgresql://your_postgres_username:your_postgres_password@postgres:5432/covid_data?connect_timeout=15 
```

## Running the Code and Setup Instructions
Ensure Docker is running 
- Open the Docker application and ensure it's running

`docker compose build --no-cache && docker compose --profile postgres up` 

- This command will build the Docker images and start the services defined 
     - Start PostgreSQL database
     - Run the data ingestion pipeline and dbt models

- Logs can be viewed in the Docker application of by running `docker-compose logs -f data_pipeline` in your terminal


## Tools and Decision-Making


#### 1. **dlt (Data Load Tool)**

- **Reason**: dlt is a simple, fast, and flexible tool for loading data from REST APIs into a database. It abstracts away much of the boilerplate code required for data ingestion.
- **Website**: [dlthub.com](https://dlthub.com)

#### 2. **Poetry**

- **Reason**: Poetry is a modern dependency manager that simplifies handling Python packages, virtual environments, and packaging the project. It ensures reproducible environments and clean dependency management.
- **Website**: [python-poetry.org](https://python-poetry.org)


---

### Output Csv's

CSV outputs can be found in the `scripts/outputs` folder