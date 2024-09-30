from libre_link_up.client import (
    LibreLinkUpClient,
)
import os
import dotenv

dotenv.load_dotenv()

client = LibreLinkUpClient(
    username=os.environ["LIBRE_LINK_UP_USERNAME"],
    password=os.environ["LIBRE_LINK_UP_PASSWORD"],
    url=os.environ["LIBRE_LINK_UP_URL"],
    version="4.8.0",
)

client.login()
print(client.get_latest_reading())
