import json
import os.path
from datetime import datetime



#### This is for agentA.py
def append_experiment_results_agent_version(filepath, answerObject):
    # Define the filename for the JSON file
    

    # If the file doesn't exist, create it with an empty list
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump([], f)

    # Load the existing contents of the file
    with open(filepath, "r") as f:
        data = json.load(f)

    # Add the new experiment result to the list
    new_experiment_result = answerObject
    new_experiment_result["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.append(new_experiment_result)

    # Save the updated contents back to the file
    with open(filepath, "w") as f:
        json.dump(data, f)


##### This is for main.py
def append_experiment_results(filepath, latitude, longitude, fullAddress, geology_response, regional_geology_subarea, regional_tectonic_geology_response, rewordedResponse):
    # Define the filename for the JSON file
    

    # If the file doesn't exist, create it with an empty list
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump([], f)

    # Load the existing contents of the file
    with open(filepath, "r") as f:
        data = json.load(f)

    # Add the new experiment result to the list
    new_experiment_result = {
        "latitude": latitude,
        "longitude": longitude,
        "fullAddress": fullAddress,
        "geology_response": geology_response,
        "regional_geology_subarea": regional_geology_subarea,
        "regional_tectonic_geology_response": regional_tectonic_geology_response,
        "reworded_text": rewordedResponse,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(new_experiment_result)

    # Save the updated contents back to the file
    with open(filepath, "w") as f:
        json.dump(data, f)

