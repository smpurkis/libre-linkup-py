import pytest
from libre_link_up import LibreLinkUpClient
import os
import dotenv

from typing import Generator
from libre_link_up.custom_types import LibreLinkUpUrl

dotenv.load_dotenv()

client_instance = LibreLinkUpClient(
    username=os.environ["LIBRE_LINK_UP_USERNAME"],
    password=os.environ["LIBRE_LINK_UP_PASSWORD"],
    url=os.environ["LIBRE_LINK_UP_URL"],
    version=os.getenv("LIBRE_LINK_UP_VERSION", "4.7.0"),
)


@pytest.fixture
def client() -> Generator[LibreLinkUpClient, None, None]:
    yield client_instance
