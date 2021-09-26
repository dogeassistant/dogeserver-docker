import os
import re
import json
import yaml
from functools import reduce
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    included_keys = []

    secrets_dict = {}

    for key, value in json.load(open("homeassistant/secrets.json")).items():
        if value is True:
            secrets_dict[key] = os.getenv(key)
            continue

        if type(value) is str:
            r_keys = re.findall(r"\{([_A-Z]+)\}", value)

            replacement_strings = {}

            for r_key in r_keys:
                replacement_strings[r_key] = os.getenv(r_key)

            secrets_dict[key] = value.format(**replacement_strings)
            continue

    print(yaml.dump(secrets_dict))
