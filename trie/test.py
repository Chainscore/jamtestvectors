import json
from pathlib import Path
import requests


def fetch_vector() :
    test_dir = Path(__file__).parent
    # Load test vectors
    with open(test_dir / "trie.json", "r") as f:
        vectors_json = json.load(f)

    return vectors_json


if __name__ == "__main__":
    vectors = fetch_vector()
    for vector in vectors:
        response = requests.post("http://localhost:8000/api/v1/trie/validtae", json={"input" : {"input" : vector["input"]}, "output" : { "output" : vector["output"]}})
        result = response.json()
        if result.status != "ok":
            print(f"Failed: {vector}")