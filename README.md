# ID-card-extract-module
1. Download model file follow link: https://hub.ultralytics.com/models/hgfIRTQBokYdGBQS7orm (Not allowed)
2. Update new model: https://api.ultralytics.com/v1/predict/je3LTBqoLDRiZBtYRSYQ
3. Clone the module:
   ```sh
   git clone https://github.com/nguyen-tho/ID-card-extract-module.git
   ```
4. Run process.py
   ```sh
   python process.py
   ```
5. References
   - Label dataset tool: https://app.roboflow.com/
   - Training model tool: https://hub.ultralytics.com/
   - Enhancing resolution tool: https://github.com/xinntao/Real-ESRGAN
   - OCR extraction tool: https://github.com/pbcquoc/vietocr.git

6. Advantages and disadvatages
   - Advantages:
     * YOLOv8x confidence: about 71-80%
     * Information extract probability: about 80-93% (VietOCR about 88-90%)
     * RealESRGAN may boost probability of extraction period more about 0.5-1%
   - Disadvantages:
     * Need to get an ID card image clear and balance about brightness to catch edge of the card
     * If preprocess feature cannot draw contour of the ID card -> show error and stop program immediately
     * Confidence decrease from 80-86% to 71-80%
     * Mean of extract probability may be affected by QR code extraction (If QR code can extract information -> probability is 1 -> mean probability increase, otherwise probability is 0 -> mean probability decrease)
7. New update
   - New model to detect QR code on Vietnamese ID card
   - Extract information from QR code such as issue date instead of create a new model to detect issue date at back-side of ID card
   
