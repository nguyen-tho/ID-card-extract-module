import numpy as np
import json
from PIL import ImageDraw, Image, ImageFont
from ultralytics import YOLO
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import cv2
import torch
import os 
from qreader import QReader
from datetime import datetime
import preprocessing as pre
import realesrgan as real
import postprocessing as post

class_name_dict = {0: 'QRcode',
                   1: 'addr1',
                   2: 'addr2',
                   3: 'dob',
                   4: 'expiry',
                   5: 'gender',
                   6: 'hometown',
                   7: 'id',
                   8: 'name',
                   9: 'nationality'}

class_name_dict_2 = {
    0: 'date_of_birth', 
    1: 'date_of_expiry', 
    2: 'hometown', 
    3: 'id', 
    4: 'name', 
    5: 'nationality', 
    6: 'permanent_residence1', 
    7: 'permanent_residence2', 
    8: 'person', 
    9: 'sex'
}
def read_image(image_path):
    img = Image.open(image_path)  # open image file
    return img
def model_result(model_path, img):
    model = YOLO(model_path)
    results = model(img)[0]
    return results

def set_detector():
    config = Cfg.load_config_from_name('vgg_transformer')
    #config['weights'] = '/content/drive/MyDrive/license-extractor/weight/vgg_transformer.pth'
    config['cnn']['pretrained']=False
    config['device'] = 'cpu'
    detector = Predictor(config)
    return detector
    


def extract_and_format_date(qr_code_image_path):
    # Create a QReader instance
    qreader = QReader()

    # Get the image that contains the QR code
    image = cv2.cvtColor(cv2.imread(qr_code_image_path), cv2.COLOR_BGR2RGB)

    # Use the detect_and_decode function to get the decoded QR data
    decoded_text = qreader.detect_and_decode(image=image)

    # Use the decoded QR data as input for the second part of your code
    input_string = str(decoded_text)

    # Extract the date string
    date_string = ''.join(c for c in input_string.split('|')[-1] if c.isdigit())

    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_string, '%d%m%Y')

    # Format the datetime object as a new string
    formatted_date = date_object.strftime('%d/%m/%Y')

    return formatted_date
'''
# Example usage
def ocr_extract(img_path,model_path, threshold):#input image is a PIL image
    img = read_image(img_path)
    labeled_objects = []
    results = model_result(model_path, img)
    detector = set_detector()
    i = 0
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
        # Draw a bounding box around the object
        #cv2.rectangle(img, (int(x1-1), int(y1+1)), (int(x2+1), int(y2-1)), (0, 255, 0), 2)
            img_array = np.array(img)
        #ocr_img = img[int(y1):int(y2), int(x1):int(x2), :].copy()
            roi = img_array[int(y1):int(y2), int(x1):int(x2)]
            ocr_img = Image.fromarray(roi)
            ocr_img.save('temp/o'+str(i)+'.jpg')
            
        #preprocess ROI images
        #roi = cv2.cvtColor(ocr_img, cv2.COLOR_BGR2GRAY)
       # _,roi = cv2.threshold(roi,128,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Perform OCR on the ROI and print the detected text using Tesseract
            text, prob = detector.predict(ocr_img, return_prob=True)
        # Check if the class_id exists in class_name_dict
            if class_id in class_name_dict:
                class_name = class_name_dict[class_id]

                if class_name != 'QRcode': # not to write the portrait info
                # Store the relevant information in the labeled_objects list
                    labeled_objects.append({
                    "class": class_name,
                    "text": text.strip(),
                    "prob": prob,
                    "confidence": score
                     })
                else:
                    try:
                        formatted_date = extract_and_format_date('temp/o'+str(i)+'.jpg')
                    except:
                        print('QR code extraction is in error')
                        labeled_objects.append({
                            "class": "issue_date",
                            "text": "",
                            "prob": 0, #QR code cannot extract by OCR and it will detect exactly
                            "confidence": score
                        })
                    else:
                        labeled_objects.append({
                            "class": "issue_date",
                            "text": formatted_date,
                            "prob": 1, #QR code cannot extract by OCR and it will detect exactly
                            "confidence": score
                        })
            i = i + 1
# Save labeled objects information to a JSON file
    with open('temp/labeled_objects.json', 'w', encoding='utf-8') as json_file:
        json.dump(labeled_objects, json_file, ensure_ascii=False, indent=4)

    labeled_objects = [] #clear data after use

# Save the modified image with bounding boxes drawn
# Create a drawing object to draw on the image
# show which class in each box
# Save the modified image with bounding boxes drawn
def save_output_image(img_path, model_path, threshold, name):
    img = read_image(img_path)
    draw = ImageDraw.Draw(img)
    results = model_result(model_path, img)
    
    font = ImageFont.truetype("arial.ttf", 36)  # Use a TTF font file and specify the font size
    
    # Define the text color
    text_color = (255, 0, 0)  # RGB color
    
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        
        if score > threshold:
            if class_id in class_name_dict:
                class_name = class_name_dict[class_id]
                # Draw a bounding box around the object
                draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], outline=(0, 255, 0), width=3)
                
                # Define the position for the text
                text_position = (int(x1), int(y1) - 10)  # Adjust the text position as needed
                
                # Draw the text on the image
                draw.text(text_position, f"{class_name}", fill=text_color, font=font)
    
    img.save(f'output/{name}/output.jpg')
    
'''    
def text_extract_ocr(img_path, threshold):
    dictionary = class_name_dict_2
    model_path = 'id_card_yolov8x.pt'
    img = read_image(img_path)
    labeled_objects = []
    results = model_result(model_path, img)
    detector = set_detector()
    i = 0
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
        # Draw a bounding box around the object
        #cv2.rectangle(img, (int(x1-1), int(y1+1)), (int(x2+1), int(y2-1)), (0, 255, 0), 2)
        # Check if the class_id exists in class_name_dict
            if class_id in dictionary:
                class_name = dictionary[class_id]

                if class_name != 'person': # not to write the portrait info
                # Store the relevant information in the labeled_objects list
                    img_array = np.array(img)
        #ocr_img = img[int(y1):int(y2), int(x1):int(x2), :].copy()
                    roi = img_array[int(y1):int(y2), int(x1):int(x2)]
                    ocr_img = Image.fromarray(roi)
                    ocr_img.save('temp/o'+str(i)+'.jpg')
            
                    text, prob = detector.predict(ocr_img, return_prob=True)
                    labeled_objects.append({
                    "class": class_name,
                    "text": text.strip(),
                    "prob": prob,
                    "confidence": score
                     })
            i = i + 1
    dictionary = class_name_dict
    model_path = 'ID-card-extractor-v2.pt'
    results = model_result(model_path, img)
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
        # Draw a bounding box around the object
        #cv2.rectangle(img, (int(x1-1), int(y1+1)), (int(x2+1), int(y2-1)), (0, 255, 0), 2)
            
        # Check if the class_id exists in class_name_dict
            if class_id in dictionary:
                class_name = dictionary[class_id]
                if class_name == 'QRcode': # not to write the portrait info
                    img_array = np.array(img)
        #ocr_img = img[int(y1):int(y2), int(x1):int(x2), :].copy()
                    roi = img_array[int(y1):int(y2), int(x1):int(x2)]
                    ocr_img = Image.fromarray(roi)
                    ocr_img.save('temp/o'+str(i)+'.jpg')
                    text, prob = detector.predict(ocr_img, return_prob=True)
                # Store the relevant information in the labeled_objects list
                    try:
                        formatted_date = extract_and_format_date('temp/o'+str(i)+'.jpg')
                    except:
                        print('QR code extraction is in error')
                        labeled_objects.append({
                            "class": "issue_date",
                            "text": "",
                            "prob": 0, #QR code cannot extract by OCR and it will detect exactly
                            "confidence": score
                        })
                    else:
                        labeled_objects.append({
                            "class": "issue_date",
                            "text": formatted_date,
                            "prob": 1, #QR code cannot extract by OCR and it will detect exactly
                            "confidence": score
                        })
            i = i + 1
    with open('temp/labeled_objects.json', 'w', encoding='utf-8') as json_file:
        json.dump(labeled_objects, json_file, ensure_ascii=False, indent=4)

    labeled_objects = [] #clear data after use
def save_output(img_path, threshold, name):
    dictionary = class_name_dict_2
    model_path = 'id_card_yolov8x.pt'
    img = read_image(img_path)
    draw = ImageDraw.Draw(img)
    results = model_result(model_path, img)
    
    font = ImageFont.truetype("arial.ttf", 36)  # Use a TTF font file and specify the font size
    
    # Define the text color
    text_color = (255, 0, 0)  # RGB color
    
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        
        if score > threshold:
            if class_id in dictionary:
                class_name = dictionary[class_id]
                if class_name != 'person':
                    draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], outline=(0, 255, 0), width=3)
                
                # Define the position for the text
                    text_position = (int(x1), int(y1) - 10)  # Adjust the text position as needed
                
                # Draw the text on the image
                    draw.text(text_position, f"{class_name}", fill=text_color, font=font)
    
    dictionary = class_name_dict
    model_path = 'ID-card-extractor-v2.pt'
    results = model_result(model_path, img)
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        
        if score > threshold:
            if class_id in dictionary:
                class_name = dictionary[class_id]
                if class_name == 'QRcode':
                    draw.rectangle([(int(x1), int(y1)), (int(x2), int(y2))], outline=(0, 255, 0), width=3)
                
                # Define the position for the text
                    text_position = (int(x1), int(y1) - 10)  # Adjust the text position as needed
                
                # Draw the text on the image
                    draw.text(text_position, f"{class_name}", fill=text_color, font=font)    
    
    img.save(f'output/{name}/output.jpg')
                
def processing(input_img_path, name):

    print("Cuda available: ",torch.cuda.is_available())
    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # not need to change
    directory_path = f'output/{name}/'
    if not os.path.exists(directory_path):
    # If it doesn't exist, create the directory and any necessary parent directories
        os.makedirs(directory_path)
    else:
        print(f"The {directory_path} is exist")
    preprocessed = pre.preprocessing(input_img_path)
    text_model_path = 'id_card_yolov8x.pt' #model path
    img = cv2.imread(input_img_path)
    #real_in_path = 'temp/real_in.jpg'
    #cv2.imwrite(real_in_path, img)
    #real_out = real.realesrgan(real_in_path)
    #real_out = real.realesrgan(preprocessed)
    try:
        text_extract_ocr(preprocessed, 0.5)
        save_output(preprocessed, 0.5, name)
    except:
        print("ERROR! Please try with another image")
    post.filter("temp/labeled_objects.json", name)
    post.merge_permanent_residence(name)
    post.mean_prob(name)
    
#processing('input/cccd2.jpg', 'tho')