import logging
import os
from datetime import date, timedelta
from typing import Any, Iterator, Optional

import dlt
from date_range import date_range
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    rest_api_source,
)
from dotenv import load_dotenv

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

api_base_url = os.getenv("API_BASE_URL", "")
postgres_database_url = os.getenv("POSTGRES_DATABASE_URL", "")

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dlt.resource(write_disposition="replace")
def states_and_territories() -> Iterator[dict]:
    path = "states.json"
    yield from rest_api_source(
        {
            "client": {"base_url": api_base_url},
            "resources": [
                {
                    "name": "states_and_territories",
                    "endpoint": {"path": path},
                }
            ],
        }
    )


@dlt.resource(write_disposition="replace")
def daily_cases(start_date: date, end_date: date) -> Iterator[dict]:
    # Generate endpoints for US daily cases across the date range
    for single_date in date_range(start_date, end_date):
        path = f"us/daily/{single_date.isoformat()}/simple.json"
        yield from rest_api_source(
            {
                "client": {"base_url": api_base_url},
                "resources": [
                    {
                        "name": "daily_cases",
                        "endpoint": {"path": path},
                    }
                ],
            }
        )


@dlt.resource(write_disposition="replace")
def state_daily_cases(start_date: date, end_date: date) -> Iterator[dict]:
    # Generate endpoints for each state's daily data
    for state in STATES:
        for single_date in date_range(start_date, end_date):
            path = f"states/{state.lower()}/{single_date.isoformat()}/simple.json"
            yield from rest_api_source(
                {
                    "client": {"base_url": api_base_url},
                    "resources": [
                        {
                            "name": "state_daily_cases",
                            "endpoint": {"path": path},
                        }
                    ],
                }
            )


@dlt.source(name="covid19")
def covid19_source() -> Any:
    # Define the date range
    start_date = date(2021, 2, 1)
    end_date = date(2021, 2, 28)

    # Yield each resource, passing parameters as needed
    yield states_and_territories()
    yield daily_cases(start_date, end_date)
    yield state_daily_cases(start_date, end_date)


def load_covid19_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="covid19_data_pipeline",
        destination=dlt.destinations.postgres(postgres_database_url),
        dataset_name="covid19_states_data",
    )

    load_info = pipeline.run(covid19_source())
    logger.info(load_info)


if __name__ == "__main__":
    load_dotenv()
    load_covid19_data()
