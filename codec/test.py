import json
import os
import requests
import re
from pathlib import Path

def fetch_vectors(spec: str):
    result = []
    for file in os.listdir(f"./{spec}"):
        if file.endswith(".json"):
            with open(f"./{spec}/{file}", "r") as f:
                data = json.load(f)
                result.append((file, data))
    return result


if __name__ == "__main__":

    vectors = fetch_vectors("data")
    for (file, vector) in vectors:

        # Removing json from files like: block.json => block
        file_name = file.replace(".json", "")

        # By file of the file name get bin file : block => bock.bin
        test_dir = Path(__file__).parent / "data"
        with open(test_dir / f"{file_name}.bin", "rb") as f:
            expected_bytes = f.read().hex()

        # file name formatting : header_0 => header
        label = re.sub(r'_\d+$', '', file_name)

        response = requests.post("http://localhost:8000/api/v1/types/type_id/json_to_codec/validate", json={"input": {"file": vector, "label": label }})
        result = response.json()

        assert result["data"] == expected_bytes

        if result["status"] != "Ok":
            print(f"Failed: {label}")