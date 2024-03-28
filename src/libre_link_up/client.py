from datetime import datetime
from typing import Any, Optional
from libre_link_up.types import (
    GlucoseSensorReading,
    LibreLinkUpUrl,
    Connection,
    ReadingSource,
)
import requests


def _convert_timestamp_string_to_datetime(timestamp: str) -> float:
    # "8/16/2023 10:16:34 AM"
    return datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p").timestamp()


class LibreLinkUpClient:
    def __init__(
        self,
        username: str,
        password: str,
        url: LibreLinkUpUrl = LibreLinkUpUrl.EU,
        version: str = "4.7.0",
    ):
        """
        Create a new LibreLinkUpClient instance
        Each instance is used for one connection
        Note: Creating this client does not log in to the LibreLinkUp API. You must call the `login` method to log in.

        Example usage:
        ```
        client = LibreLinkUpClient(username="...", password="...", url=LibreLinkUpUrl.EU, version="4.7.0")
        ```
        """
        self.username = username
        self.password = password
        self.url = url
        self.version = version
        self.headers: dict[str, str] = {
            "product": "llu.android",
            "version": version,
            "accept-encoding": "gzip",
            "cache-control": "no-cache",
            "connection": "Keep-Alive",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36",
        }
        self.jwt_token: Optional[str] = None

    def login(self) -> None:
        """
        Log in to the LibreLinkUp API and set the JWT token
        """
        response = requests.post(
            f"{self.url}/llu/auth/login",
            headers=self.headers,
            json={"email": self.username, "password": self.password},
        )
        response.raise_for_status()
        data = response.json()
        self.jwt_token = data["data"]["authTicket"]["token"]
        self.headers["Authorization"] = f"Bearer {self.jwt_token}"

    @property
    def connection(self) -> Connection:
        if not hasattr(self, "_connection"):
            self._connection = self.get_connection()
        return self._connection

    @connection.setter
    def connection(self, value: Connection) -> None:
        """
        Set the connection for this client instance
        """
        self._connection = value

    def get_connections(self) -> dict[str, Any]:
        """
        Get the connections you have access to

        Returns:
            Dict[str, Any]: Raw JSON response from the LibreLinkUp API
        """
        response = requests.get(f"{self.url}/llu/connections", headers=self.headers)
        response.raise_for_status()
        connections = response.json()
        return connections

    def get_raw_connection(self, index: int = 0) -> dict[str, Any]:
        """
        Get the raw connection data from the LibreLinkUp API
        This returns the raw JSON response from the API

        Returns:
            Dict[str, Any]: Raw JSON response from the LibreLinkUp API
        """
        raw_connections: list[dict[str, Any]] = self.get_connections()["data"]
        assert len(raw_connections) >= index + 1
        raw_connection = raw_connections[index]
        return raw_connection

    def get_connection(self, index: int = 0) -> Connection:
        """
        Get the ith connection
        """
        raw_connection = self.get_raw_connection(index)
        connection = Connection(
            patient_id=raw_connection["patientId"],
            first_name=raw_connection["firstName"],
            last_name=raw_connection["lastName"],
        )
        return connection

    def get_raw_graph_readings(self) -> dict[str, Any]:
        """
        Get the raw graph data from the LibreLinkUp API
        This is returns the raw JSON response from the API

        Returns:
            Dict[str, Any]: Raw JSON response from the LibreLinkUp API
        """
        response = requests.get(
            f"{self.url}/llu/connections/{self.connection.patient_id}/graph",
            headers=self.headers,
        )
        response.raise_for_status()
        cgm_data = response.json()
        return cgm_data

    def get_graph_readings(self) -> list[GlucoseSensorReading]:
        """
        Get the parsed graph data from the LibreLinkUp API

        Returns:
            list[GlucoseSensorReading]: List of parsed glucose sensor readings
                Example: [
                    GlucoseSensorReading(
                        timestamp=1704070800,
                        value=5.0,
                        value_in_mg_per_dl=90.0,
                        source="graph",
                    ),
                    ...
                ]
        """
        raw_graph_data = self.get_raw_graph_readings()
        graph_data = raw_graph_data["data"]["graphData"]
        glucose_readings = []
        for reading in graph_data:
            glucose_readings.append(
                GlucoseSensorReading(
                    unix_timestamp=_convert_timestamp_string_to_datetime(
                        reading["Timestamp"]
                    ),
                    value=reading["Value"],
                    value_in_mg_per_dl=reading["ValueInMgPerDl"],
                    source=ReadingSource.GRAPH,
                )
            )
        return glucose_readings

    def get_raw_logbook_readings(self) -> dict[str, Any]:
        """
        Get the raw logbook data from the LibreLinkUp API
        This returns the raw JSON response from the API

        Returns:
            Dict[str, Any]: Raw JSON response from the LibreLinkUp API
        """
        response = requests.get(
            f"{self.url}/llu/connections/{self.connection.patient_id}/logbook",
            headers=self.headers,
        )
        response.raise_for_status()
        logbook_data = response.json()
        return logbook_data

    def get_logbook_readings(self) -> list[GlucoseSensorReading]:
        """
        Get the parsed logbook data from the LibreLinkUp API

        Returns:
            list[GlucoseSensorReading]: List of parsed glucose sensor readings
                Example: [
                    GlucoseSensorReading(
                        timestamp=1704070800,
                        value=5.0,
                        value_in_mg_per_dl=90.0,
                        source="logbook",
                    ),
                    ...
                ]
        """
        response = self.get_raw_logbook_readings()
        logbook_data = []
        for logbook_entry in response["data"]:
            logbook_data.append(
                GlucoseSensorReading(
                    unix_timestamp=_convert_timestamp_string_to_datetime(
                        logbook_entry["Timestamp"]
                    ),
                    value=logbook_entry["Value"],
                    value_in_mg_per_dl=logbook_entry["ValueInMgPerDl"],
                    source=ReadingSource.LOGBOOK,
                )
            )
        return logbook_data

    def get_latest_reading(self) -> GlucoseSensorReading:
        """
        Get the latest glucose sensor reading from the LibreLinkUp API

        Returns:
            GlucoseSensorReading: Parsed glucose sensor reading
                Example: GlucoseSensorReading(
                    timestamp=1704070800,
                    value=5.0,
                    value_in_mg_per_dl=90.0,
                    source="latest_reading",
                )
        """
        resp = self.get_raw_graph_readings()
        raw_reading = resp["data"]["connection"]["glucoseMeasurement"]
        latest_reading = GlucoseSensorReading(
            unix_timestamp=_convert_timestamp_string_to_datetime(
                raw_reading["Timestamp"]
            ),
            value=raw_reading["Value"],
            value_in_mg_per_dl=raw_reading["ValueInMgPerDl"],
            source=ReadingSource.LATEST_READING,
        )
        return latest_reading
