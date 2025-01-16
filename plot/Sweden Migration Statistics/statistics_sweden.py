from datetime import timedelta
from enum import Enum
from typing import Dict, Tuple

import pandas as pd
import requests
import requests_cache


class StatisticsSweden:
    BASE_URL = "https://api.scb.se/OV0104/v1/doris/en/ssd/"

    class Endpoint(Enum):

        POPULATION_REGION = "BE/BE0101/BE0101A/BefolkningNy"
        POPULATION_CITIZENSHIP_GROUP = "BE/BE0101/BE0101A/FolkmMedblandHVD"
        POPULATION_BIRTH_COUNTRY = "BE/BE0101/BE0101E/FodelselandArK"
        MIGRATION_BIRTH_COUNTRY = "BE/BE0101/BE0101J/ImmiEmiFod"
        FOREIGN_CITIZENS_COUNTRY = "BE/BE0101/BE0101F/UtlmedbR"
        POPULATION_CHANGES = "BE/BE0101/BE0101G/BefUtvKon1749"
        POPULATION_KEY = "BE/BE0101/BE0101X/NTBE0101"
        POPULATION_REGION_BIRTH = "BE/BE0101/BE0101E/FolkmRegFlandK"
        ENERGY_EL_SUPPLY = "EN/EN0108/EN0108A/EltillfM"

        @property
        def url(self):
            return StatisticsSweden.BASE_URL + self.value

    def __init__(self):
        requests_cache.install_cache(
            cache_name="../../http_cache",
            backend="filesystem",
            expire_after=timedelta(days=30),
            allowable_methods=("GET", "POST"),
        )

    def get_dataframe(
        self, endpoint: Endpoint, selected_fields: dict = None
    ) -> Tuple[pd.DataFrame, dict]:
        query = {"query": [], "response": {"format": "json"}}
        metadata = self._get_metadata(endpoint.url)

        for item in metadata["variables"]:
            field_code = item["code"]
            field_values = item["values"]

            if selected_fields and field_code in selected_fields:
                valid_values = [
                    value
                    for value in selected_fields[field_code]
                    if value in field_values
                ]
                if valid_values:
                    query["query"].append(
                        {
                            "code": field_code,
                            "selection": {
                                "filter": "item",
                                "values": valid_values,
                            },
                        }
                    )
            elif item.get("elimination", False):
                query["query"].append(
                    {
                        "code": field_code,
                        "selection": {
                            "filter": "item",
                            "values": field_values,
                        },
                    }
                )

        response = requests.post(endpoint.url, json=query, timeout=None)
        response.raise_for_status()
        response_data = response.json()

        return (
            self._transform_data(response_data, metadata),
            response_data["metadata"],
        )

    def show_fields(self, endpoint: Endpoint):
        metadata = self._get_metadata(endpoint.url)
        for item in metadata["variables"]:
            print(f"{item['code']}: {item['values']}")

    def _get_metadata(self, url: str) -> Dict:
        metadata_r = requests.get(url, timeout=None)
        metadata_r.raise_for_status()
        return metadata_r.json()

    @staticmethod
    def _transform_data(response_data: dict, metadata: dict) -> pd.DataFrame:
        columns_info = response_data["columns"]
        dimensions = [
            col["text"].lower().replace(" ", "_")
            for col in columns_info
            if col["type"] == "d"
        ]
        time_dimension = next(
            (
                col["text"].lower().replace(" ", "_")
                for col in columns_info
                if col["type"] == "t"
            ),
            None,
        )
        measures = [
            col["text"].lower().replace(" ", "_")
            for col in columns_info
            if col["type"] == "c"
        ]

        # Generate mappings for dimensions from metadata
        mappings = {
            var["text"]
            .lower()
            .replace(" ", "_"): dict(zip(var["values"], var["valueTexts"]))
            for var in metadata["variables"]
            if "values" in var
            and "valueTexts" in var
            and var["text"].lower().replace(" ", "_") in dimensions
        }

        # Generate records from response_data['data']
        records = []
        for item in response_data["data"]:
            record = dict(
                zip(
                    dimensions + ([time_dimension] if time_dimension else []),
                    item["key"],
                )
            )

            # Map measure values
            for i, value in enumerate(item["values"]):
                record[measures[i]] = value

            records.append(record)

        # Create DataFrame
        df = pd.DataFrame(records)

        # Convert numeric columns (measures)
        for measure in measures:
            if measure in df.columns:
                df[measure] = pd.to_numeric(df[measure], errors="coerce")

        # Convert time dimension if it exists
        if time_dimension and time_dimension in df.columns:
            df[time_dimension] = pd.to_numeric(df[time_dimension])

        # Apply mappings to dimension columns
        for dimension in dimensions:
            if dimension in df.columns and dimension in mappings:
                df[dimension] = df[dimension].map(mappings[dimension])

        return df
