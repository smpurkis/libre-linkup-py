from libre_link_up import LibreLinkUpClient
import os
import dotenv
import json

dotenv.load_dotenv()


"""
We will do the following:
- Create a new `LibreLinkUpClient` instance
- Log in
- Get the latest reading
"""

if __name__ == "__main__":
    client = LibreLinkUpClient(
        username=os.environ["LIBRE_LINK_UP_USERNAME"],
        password=os.environ["LIBRE_LINK_UP_PASSWORD"],
        url=os.environ["LIBRE_LINK_UP_URL"],
        version="4.7.0",
    )
    client.login()
    glucose_data = client.get_latest_reading()
    print(json.dumps(glucose_data.model_dump(), sort_keys=True, indent=4))
