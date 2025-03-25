import json
import os
from typing import Tuple

import requests

from spec_config import gen_flags


def fetch_vectors(spec: str):
    # Read the vetors from ./{spec}/{vector_name}.json
    result = []
    for file in os.listdir(f"./{spec}"):
        if file.endswith(".json"):
            with open(f"./{spec}/{file}", "r") as f:
                data = json.load(f)
                result.append((file, data))
    return result


def transform(vector: dict) -> Tuple[dict, dict, dict]:
    # Block transform
    block = vector["block"]
    pre_state = vector["pre_state"]
    post_state = vector["post_state"]
    return block, pre_state, post_state


if __name__ == "__main__":
    vectors = fetch_vectors("tiny")
    for file, vector in vectors:
        input, pre_state, post_state = transform(vector)

        # if "1_001" not in file:
        #     # print(f"Skipping {file} - not the target file")
        #     continue

        response = requests.post(
            "http://localhost:8000/api/v1/safrole/validate_keyval",
            json={
                "input": {"block": input, "state": pre_state},
                "output": {"state": post_state},
                "flags": gen_flags("tiny"),
            },
        )
        result = response.json()
        print("result for", file, result)
