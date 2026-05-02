import json
import os

# Gen #3 : Helper for the new creator web lecture thing.

# Get the absolute path to the src/Data/lectures folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "lectures")

# Ensure the directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def save_lecture(file_name: str, payload: dict):
    """Saves a dictionary payload to a JSON file."""
    # Ensure file ends with .json
    if not file_name.endswith(".json"):
        file_name += ".json"
        
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, "w") as f:
        json.dump(payload, f, indent=4)

def load_all_lectures() -> list[dict]:
    """Reads all JSON files in the directory and returns a list of payloads."""
    lectures = []
    if not os.path.exists(DATA_DIR):
        return lectures
        
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r") as f:
                try:
                    data = json.load(f)
                    # Embed the filename as an ID so we can reference it later
                    data["file_id"] = filename 
                    lectures.append(data)
                except json.JSONDecodeError:
                    pass
    return lectures

def delete_lecture(file_name: str):
  """Deletes a lecture JSON file from the Data directory."""
  if not file_name.endswith(".json"):
      file_name += ".json"
  file_path = os.path.join(DATA_DIR, file_name)
  if os.path.exists(file_path):
      os.remove(file_path)