# Libre-linkup-py

## TL;DR

Unofficial client to get your glucose readings from the LibreLinkUp API in Python.
Supports Python 3.9 and above

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)

## Installation

    pip install libre-linkup-py

## Usage

Note: I recommend using something like [python-dotenv](https://pypi.org/project/python-dotenv/) to manage your environment variables.

1. Create a .env file with the following contents:

```bash
LIBRE_LINK_UP_USERNAME=...
LIBRE_LINK_UP_PASSWORD=...
LIBRE_LINK_UP_URL=https://api-eu2.libreview.io
LIBRE_LINK_UP_VERSION=4.7.0  # Optional
```

The url for `LIBRE_LINK_UP_URL` may be different depending on where you live, current [options](src/libre_link_up/types.py), also see [here](https://gist.github.com/khskekec/6c13ba01b10d3018d816706a32ae8ab2) for more information.

2. Paste this code into a file and run it:
```python
from libre_link_up import LibreLinkUpClient
import os
import dotenv
import json

dotenv.load_dotenv()

client = LibreLinkUpClient(
    username=os.environ["LIBRE_LINK_UP_USERNAME"],
    password=os.environ["LIBRE_LINK_UP_PASSWORD"],
    url=os.environ["LIBRE_LINK_UP_URL"],
    version="4.7.0",
)
client.login()
glucose_data = client.get_latest_reading()
print(json.dumps(glucose_data.model_dump(), sort_keys=True, indent=4))
```

The output should look something like:
```json
{
    "high_at_the_time": false,
    "low_at_the_time": false,
    "unix_timestamp": 1709830900.0,
    "value": 7.9,
    "value_in_mg_per_dl": 143.0
}
```

## Examples

See the [examples](examples/) directory for more examples.

## Contributing

If you find a bug :bug:, please open a [bug report](https://github.com/smpurkis/libre-linkup-py/issues/new?assignees=&labels=bug&template=bug_report.md&title=).
If you have an idea for an improvement or new feature :rocket:, please open a [feature request](https://github.com/smpurkis/libre-linkup-py/issues/new?assignees=&labels=Feature+request&template=feature_request.md&title=).