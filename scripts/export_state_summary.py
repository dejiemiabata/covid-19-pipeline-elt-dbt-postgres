import logging
import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2 import OperationalError, sql
from psycopg2.extensions import connection

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "localhost",
    "port": 5432,
}

OUTPUT_DIR = "scripts/outputs"
STATES = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def export_state_data(state: str, conn: connection):
    """Export data for a given state to a CSV file."""
    try:

        query = """
            SELECT
                date,
                percent_infected
            FROM
                ds.fct_state_daily_percent_infected
            WHERE
                state_id = %s
            ORDER BY
                date;
        """
        params = (state,)
        result_df = pd.read_sql(query, conn, params=params)

        if result_df.empty:
            logging.warning(f"No data found for state: {state}")
            return

        # Define the CSV file name
        output_file = os.path.join(OUTPUT_DIR, f"{state.lower()}.csv")

        # Save the DataFrame to a CSV file
        result_df.to_csv(output_file, index=False)
        logging.info(f"Exported data for state: {state} to {output_file}")

    except Exception as e:
        logging.error(f"Failed to export data for state: {state}. Error: {e}")


def main():
    """Function to export data for all states."""
    try:
        # Establish the postgres db connection
        conn: connection = psycopg2.connect(**DB_PARAMS)
        logging.info("Database connection established successfully.")

        # Loop through each state and export data
        for state in STATES:
            export_state_data(state, conn)

    except OperationalError as e:
        logging.error(f"Database connection failed. Error: {e}")

    finally:
        conn.close()
        logging.info("Database connection closed.")


if __name__ == "__main__":

    # Establish directory path
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    main()
