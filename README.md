# ID-card-extract-module
1. Download model file follow link: https://hub.ultralytics.com/models/hgfIRTQBokYdGBQS7orm
2. Clone the module:
   ```sh
   pip install https://github.com/nguyen-tho/ID-card-extract-module.git
   ```
3. Run process.py
   ```sh
   python process.py
   ```
4. References
   - Label dataset tool: https://app.roboflow.com/
   - Training model tool: https://hub.ultralytics.com/
   - Enhancing resolution tool: https://github.com/xinntao/Real-ESRGAN

5. Advantages and disadvatages
   - Advantages:
     * YOLOv8x confidence: about 81-86%
     * VietOCR extract probability: about 90-92%
     * RealESRGAN may boost probability of extraction period more about 0.5-1%
   - Disadvantages:
     * Need to get an ID card image clear and balance about brightness to catch edge of the card
     * If preprocess feature cannot draw contour of the ID card -> show error and stop program immediately 
   
