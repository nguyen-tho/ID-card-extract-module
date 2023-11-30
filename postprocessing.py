import json
import os


def read_json_file(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    return data
 
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
    with open(f'output/{name}/result.json', 'w', encoding='utf-8') as output_file:
        json.dump(new_data, output_file, ensure_ascii=False, indent=2)

def mean_prob(name):
  #read json data
  json_path = f'output/{name}/labeled_objects_filled.json'
  with open(json_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
  prob_values = [entry["prob"] for entry in data]
  score_value = [entry["confidence"] for entry in data]

# Calculate the mean
  mean_prob = sum(prob_values) / len(prob_values)
  mean_score = sum(score_value) / len(score_value)
  prob_percentage = mean_prob*100
  score_percentage = mean_score*100
  text_path = f'output/{name}/prob.txt'
  with open(text_path, 'w') as txt:
      txt.write(f"Mean confidence of model: {mean_score}\n")
      txt.write(f"Percentage of mean score value: {score_percentage:.2f}%\n")
      txt.write(f"Mean of prob values: {mean_prob}\n")
      txt.write(f"Percentage of mean prob value: {prob_percentage:.2f}%")
  print(f"The result is saved in {text_path}")
# Print the mean
  print("Calculate the extract probability and score is finished !")
  print(f"Mean confidence of model: {mean_score}")
  print(f"Percentage of mean score value: {score_percentage:.2f}%")
  print("Mean of prob values:", mean_prob)
  print(f"Percentage of mean prob value: {prob_percentage:.2f}%")