from datetime import datetime
import pytest
import pytz
from libre_link_up.client import (
    LibreLinkUpClient,
    _convert_timestamp_string_to_datetime,
)
from libre_link_up.custom_types import ReadingSource


@pytest.mark.dependency()
def test_login(client: LibreLinkUpClient) -> None:
    client.login()
    assert client.jwt_token is not None


@pytest.mark.dependency(depends=["test_login"])
def test_connections(client: LibreLinkUpClient) -> None:
    connections = client.get_connections()
    assert "data" in connections
    assert len(connections["data"]) > 0


# test the raw connection data
def test_raw_connection(client: LibreLinkUpClient) -> None:
    raw_connection = client.get_raw_connection()
    assert raw_connection["patientId"] is not None
    assert raw_connection["firstName"] is not None
    assert raw_connection["lastName"] is not None


@pytest.mark.dependency(depends=["test_login"])
def test_get_connection(client: LibreLinkUpClient) -> None:
    connection = client.get_connection()
    assert connection is not None


@pytest.mark.dependency(depends=["test_login"])
def test_get_raw_graph_data(client: LibreLinkUpClient) -> None:
    data = client.get_raw_graph_readings()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "connection" in data["data"]
    assert len(data["data"]["graphData"]) > 0


@pytest.mark.dependency(depends=["test_login"])
def test_get_graph_data(client: LibreLinkUpClient) -> None:
    graph_values = client.get_graph_readings()
    assert len(graph_values) > 0
    assert graph_values[0].unix_timestamp is not None
    assert graph_values[0].value is not None
    assert graph_values[0].value_in_mg_per_dl is not None
    assert graph_values[0].source == ReadingSource.GRAPH


@pytest.mark.dependency(depends=["test_login"])
def test_get_raw_logbook_data(client: LibreLinkUpClient) -> None:
    logbook_data = client.get_raw_logbook_readings()
    assert "data" in logbook_data
    assert len(logbook_data["data"]) > 0
    assert logbook_data["data"][0]["Value"] is not None


@pytest.mark.dependency(depends=["test_login"])
def test_get_logbook_data(client: LibreLinkUpClient) -> None:
    logbook_data = client.get_logbook_readings()
    assert len(logbook_data) > 0
    assert logbook_data[0].unix_timestamp is not None
    assert logbook_data[0].value is not None
    assert logbook_data[0].value_in_mg_per_dl is not None
    assert logbook_data[0].source == ReadingSource.LOGBOOK


@pytest.mark.dependency(depends=["test_login"])
def test_get_glucose_data(client: LibreLinkUpClient) -> None:
    glucose_data = client.get_latest_reading()
    assert glucose_data.unix_timestamp is not None
    assert glucose_data.value is not None
    assert glucose_data.value_in_mg_per_dl is not None
    assert glucose_data.source == ReadingSource.LATEST_READING


def test_without_timezone():
    timestamp = "4/1/2024 4:36:19 PM"
    expected = datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p").timestamp()
    result = _convert_timestamp_string_to_datetime(timestamp, None)
    assert result == 1711989379.0


def test_with_timezone():
    timestamp = "4/1/2024 4:36:19 PM"
    country = "GB"
    dt = datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p")
    result = _convert_timestamp_string_to_datetime(timestamp, country)
    assert result == 1711985779.0
