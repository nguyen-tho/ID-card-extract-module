# ID-card-extract-module
1. Download model file follow link: https://hub.ultralytics.com/models/hgfIRTQBokYdGBQS7orm (Model 1 - use for extract text on front side of IDcard except portrait and QR code) 
2. Update new model: https://api.ultralytics.com/v1/predict/je3LTBqoLDRiZBtYRSYQ (Model 2 - use for extract QR code except text fields)
3. Clone the module:
   ```sh
   git clone https://github.com/nguyen-tho/ID-card-extract-module.git
   ```
4. Install dependancies
 ```sh
 pip install -r requirements.txt
 ```   
5. Run process.py
   ```sh
   # run processing function in process.py
   python process.py
   #run REST API
   python app.py
   #access http://127.0.0.1:5000 to observe the result
   ```

6. References
   - Label dataset tool: https://app.roboflow.com/
   - Training model tool: https://hub.ultralytics.com/
   - OCR extraction tool: https://github.com/pbcquoc/vietocr.git
   - QR code extract tool: https://pypi.org/project/qreader

7. Advantages and disadvatages
   - Advantages:
     * YOLOv8x confidence: about 80-90%
     * Information extract probability: about 80-93% (VietOCR about 88-92%)
   - Disadvantages:
     * Need to get an ID card image clear and balance about brightness to catch edge of the card
     * If preprocess feature cannot draw contour of the ID card -> show error and stop program immediately
     * Mean of extract probability may be affected by QR code extraction (If QR code can extract information -> probability is 1 -> mean probability increase, otherwise probability is 0 -> mean probability decrease)
8. New update
   - New model to detect QR code on Vietnamese ID card
   - Extract information from QR code such as issue date instead of create a new model to detect issue date at back-side of ID card
   - Update with REST API
   - Combine 2 models to improve the result
   
