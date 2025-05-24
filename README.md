# ID-card-extract-module
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This is a program to extract information from Vietnamese ID card

The program extract basic information such as name, ID number, date of birth,.... are extracted from ID card and issue date is extracted from QR code
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Download model file follow link:

   https://hub.ultralytics.com/models/hgfIRTQBokYdGBQS7orm (Model 1 - use for extract text on front side of IDcard except portrait and QR code) 

   Update new model: https://api.ultralytics.com/v1/predict/je3LTBqoLDRiZBtYRSYQ (Model 2 - use for extract QR code except text fields)
   
3. Dataset:
   - version 1 (not extract information from QR code): https://hub.ultralytics.com/datasets/EQ74fFtZdCei1GTLJRJF
   - version 2 (extract information from QR code): https://hub.ultralytics.com/datasets/G44KxW5Rce9ztGGqnI6X
4. Clone the module:
   ```sh
   git clone https://github.com/nguyen-tho/ID-card-extract-module.git
   ```
5. Install dependencies
 ```sh
 pip install -r requirements.txt
 ```   
5. Run process.py
   ```sh
   # run processing function in process.py
   python process.py
   #run REST API
   #python app.py
   # API is incomplete 
   #access http://127.0.0.1:5000 to observe the result
   ```

6. References
   - Label dataset tool: https://app.roboflow.com/
   - Training model tool: https://hub.ultralytics.com/
   - OCR extraction tool: https://github.com/pbcquoc/vietocr.git
   - QR code extract tool: https://pypi.org/project/qreader

7. New update
   - New model to detect QR code on Vietnamese ID card (depend on the detection model if they cannot detect QR code we cannot read issue date in the QR code)
   - Extract information from QR code such as issue date instead of create a new model to detect issue date at back-side of ID card
   - Update with REST API with Flask
   - Combine 2 models to improve the result
   - Update multi-processing with threads
8. Demo

   Input image

   ![input](https://github.com/nguyen-tho/ID-card-extract-module/blob/main/input/cccd.jpg)

   Output image

   ![output](https://github.com/nguyen-tho/ID-card-extract-module/blob/main/output/ngoc/output.jpg)

   Output result (json)

   ![click here to show json](https://github.com/nguyen-tho/ID-card-extract-module/blob/main/output/ngoc/result.json)

   Confidence and extraction probability
  ![click here to show](https://github.com/nguyen-tho/ID-card-extract-module/blob/main/output/ngoc/prob.txt)
9. Contact:

    Please contact with me at this email address to discuss: nguyencongtho116@gmail.com
10. New update (March 25th 2025)
    A simple UI using HTML, CSS and JS and an simple API using Flask
    ```sh
    # run app API
    python app.py
    ```
    To run app, we setup a localhost with port 5000
    ```
    localhost:5000
    #or
    127.0.0.1:5000
    ```
