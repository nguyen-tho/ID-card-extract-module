import json

data = [
    {
        "class": "date_of_birth",
        "text": "11/06/2001",
        "prob": 0.9323167979717255
    },
    {
        "class": "permanent_residence1",
        "text": "Tổ 17, Khu 6",
        "prob": 0.915483276049296
    },
    {
        "class": "hometown",
        "text": "Cát Trinh, Phù Cát, Bình Định",
        "prob": 0.8929033022502373
    },
    {
        "class": "date_of_expiry",
        "text": "11/06/2026",
        "prob": 0.9338173031806946
    },
    {
        "class": "sex",
        "text": "Nam",
        "prob": 0.8822495539983114
    },
    {
        "class": "permanent_residence2",
        "text": "TT. Tân Phú, Tân Phú, Đồng Na",
        "prob": 0.9172795805437811
    },
    {
        "class": "id",
        "text": "075201016578",
        "prob": 0.9201297362645467
    },
    {
        "class": "name",
        "text": "NGUYỄN CÔNG THỌ",
        "prob": 0.9354957858721415
    },
    {
        "class": "nationality",
        "text": "Việt Nam",
        "prob": 0.9334144443273544
    },
    {
        "class": "permanent_residence2",
        "text": "TT. Tân Phú, Tân Phú, Đồng Nai",
        "prob": 0.9292667150497437
    }
]

class_probabilities = {}

# Create a dictionary to store the highest probability for each class
for item in data:
    current_class = item["class"]
    current_prob = item["prob"]
    if current_class in class_probabilities:
        if current_prob > class_probabilities[current_class]["prob"]:
            class_probabilities[current_class] = item
    else:
        class_probabilities[current_class] = item

# Filter the duplicates and keep the ones with the highest probabilities
new_data = list(class_probabilities.values())

# Now, new_data contains the objects with the highest probabilities for each class
print(json.dumps(new_data, indent=2))
