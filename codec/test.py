import json
import os
import requests
import re


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
        file_name = file.replace(".json", "")
        label = re.sub(r'_\d+$', '', file_name)
        print(label)
        response = requests.post("http://localhost:8000/api/v1/codec/validate", json=vector, data=label )
        result = response.json()
        if result.status != "ok":
            print(f"Failed: {file}")
            break