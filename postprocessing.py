import json
import os

def uniform_json_data(json_data):
    """
    Transforms a list of dictionaries, modifying the 'class' key in each dictionary
    according to the provided mapping.

    Args:
        json_data: A list of dictionaries.  Each dictionary is expected to have
                   a 'class' and a 'text' key.

    Returns:
        A list of dictionaries with the 'class' keys modified as follows:
            'date_of_birth' becomes 'dob'
            'sex' becomes 'gender'
            'date_of_expiry' becomes 'expiry'
            (Leaves other 'class' values unchanged)
    """
    mapping = {
        'date_of_birth': 'dob',
        'sex': 'gender',
        'date_of_expiry': 'expiry'
    }

    for item in json_data:
        if 'class' in item:
            original_class = item['class']
            new_class = mapping.get(original_class, original_class)  # Default to original if not found
            item['class'] = new_class  #  <-- Corrected:  Modify the 'class' key, not create a new one.
    return json_data

def read_json_file(file_path):
    print(f"Reading JSON from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Read data: {data}")
            return data
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
 
"""
fill some duplicate classes in json data
output is another json which filled
"""    
def filter(json_path, name):
    # read json data
   
    data = read_json_file(json_path)
    class_probabilities = {}
# Create a dictionary to store the highest probability for each class
    for item in data:
        current_class = item["class"]
        current_prob = item["prob"]
        current_conf = item["confidence"]
        if current_class in class_probabilities:
            if current_prob > class_probabilities[current_class]["prob"] :
                class_probabilities[current_class] = item
        else:
            class_probabilities[current_class] = item
            
# Filter the duplicates and keep the ones with the highest probabilities
    new_data = list(class_probabilities.values())
    print("Data has been filled!")
# Now, new_data contains the objects with the highest probabilities for each class
    # Write the filtered data to a new JSON file
    file = str(json_path).split('/')[1]
    file_name, file_extension = os.path.splitext(file)
    output_path = f'output/{name}/'+file_name+'_filled'+file_extension
    print(f"Data has been written in {output_path}")
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(new_data, output_file, ensure_ascii=False, indent=2)

def find_text_by_class(json_data, target_class):
    for item in json_data:
        if item["class"] == target_class:
            return item["text"]
    return None  # Return None if the class is not found in the JSON data
    
def merge_permanent_residence(name):
    json_path = f'output/{name}/labeled_objects_filled.json'
    data = read_json_file(json_path)

    permanent_resident1 = find_text_by_class(data, 'permanent_residence1')
    permanent_resident2 = find_text_by_class(data, 'permanent_residence2')
    if permanent_resident1 is not None and permanent_resident2 is not None:
        permanent_resident = permanent_resident1 + " " + permanent_resident2
        # Create a new list with the merged permanent_resident class
        new_data = [{"class": "permanent_residence", "text": permanent_resident}]
    else:
        new_data = []

    # Filter and keep only "class" and "text" features
    new_data.extend([{"class": item["class"], "text": item["text"]} for item in data if item["class"] != "permanent_residence1" 
                     and item["class"] != "permanent_residence2"])
    # Write the modified data to the output JSON file
    # uniform the json data
    new_data = uniform_json_data(new_data)
    # Write the modified data to the output JSON file
    with open(f'output/{name}/result.json', 'w', encoding='utf-8') as output_file:
        json.dump(new_data, output_file, ensure_ascii=False, indent=2)

def mean_prob(name):
  #read json data
  json_path_input = f'output/{name}/labeled_objects_filled.json'
  with open(json_path_input, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
  prob_values = [entry["prob"] for entry in data]
  score_value = [entry["confidence"] for entry in data]

  # Calculate the mean
  mean_prob = sum(prob_values) / len(prob_values)
  mean_score = sum(score_value) / len(score_value)
  prob_percentage = mean_prob*100
  score_percentage = mean_score*100
  
  # Tạo một dictionary để chứa dữ liệu
  data_to_save = {
    "mean_confidence": mean_score,
    "score_percentage": round(score_percentage, 2),
    "mean_prob": mean_prob,
    "prob_percentage": round(prob_percentage, 2)
  }

  # Đường dẫn file JSON
  json_path_output = f'output/{name}/prob.json'

  # Ghi vào file định dạng JSON
  with open(json_path_output, 'w', encoding='utf-8') as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

  print(f"The result is saved in {json_path_output}")
# Print the mean
  print("Calculate the extract probability and score is finished !")
  print(f"Mean confidence of model: {mean_score}")
  print(f"Percentage of mean score value: {score_percentage:.2f}%")
  print("Mean of prob values:", mean_prob)
  print(f"Percentage of mean prob value: {prob_percentage:.2f}%")