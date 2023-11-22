import numpy as np
import cv2
import matplotlib.pyplot as plt
import realesrgan as real
from skimage.filters import threshold_local
from PIL import Image
def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def plot_rgb(image):
    plt.figure(figsize=(16,10))
    return plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def plot_gray(image):
    plt.figure(figsize=(16,10))
    return plt.imshow(image, cmap='Greys_r')

def approximate_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * peri, True)

def get_receipt_contour(contours):    
    # loop over the contours
    for c in contours:
        approx = approximate_contour(c)
        # if our approximated contour has four points, we can assume it is receipt's rectangle
        if len(approx) == 4:
            return approx

def contour_to_rect(contour, resize_ratio):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype = "float32")
    # top-left point has the smallest sum
    # bottom-right has the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # compute the difference between the points:
    # the top-right will have the minumum difference 
    # the bottom-left will have the maximum difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect / resize_ratio

def wrap_perspective(img, rect):
    # unpack rectangle points: top left, top right, bottom right, bottom left
    (tl, tr, br, bl) = rect
    # compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    # destination points which will be used to map the screen to a "scanned" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    # warp the perspective to grab the screen
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

def bw_scanner(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset = 5, method = "gaussian")
    return (gray > T).astype("uint8") * 255


def crop_surround(img, border_size):
    height, width = img.shape[:2]
    x1 = border_size
    y1 = border_size
    x2 = width - border_size
    y2 = height - border_size

# Crop the image using the defined coordinates
    cropped_image = img[y1:y2, x1:x2]
    return cropped_image

def boundary_extraction(input_img): #input is an gray image
    _,thresh = cv2.threshold(input_img, 128,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#binary_image = cv2.imread('binary_image.png', cv2.IMREAD_GRAYSCALE)

# Define a structuring element (e.g., a 3x3 square kernel)
    kernel = np.ones((3, 3), np.uint8)

# Erosion operation
# Dilation operation
    erosion = cv2.erode(thresh, kernel, iterations=1)

# Extract the boundary using subtraction
    boundary = thresh - erosion

    return boundary

def deskew(skewed_image):
    gray = cv2.cvtColor(skewed_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    angle = 0  # Initialize the angle to zero
    if lines is not None:
        for rho, theta in lines[0]:
            #if np.degrees(theta) > 45 and np.degrees(theta) < 135:
             #   angle = np.degrees(theta) - 90  # Calculate the angle
            angle = np.degrees(theta)
            
    print('Original angle: ', angle)
    milestones = [0, 90, 180]
    if angle >= milestones[1]:
        if angle - milestones[1] <= milestones[2] - angle:
            angle -= milestones[1]
        else:
            angle -= milestones[2]
    else:
        if angle - milestones[0] <= milestones[1] - angle:
            angle -= milestones[0]
        else:
            angle -= milestones[1]
        
    

# Note: The angle calculated here assumes that the skew is mainly in the vertical direction (common for text).
# If the skew is horizontal, you may need to modify the angle calculation.
    #deskew_angle = -angle
    print("Rotation Angle: ", angle)
    (h, w) = skewed_image.shape[:2]
    center = (w // 2, h // 2)

# Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed_image = cv2.warpAffine(skewed_image, M, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    return deskewed_image
"""
import fast_deskew
def deskew_image(image):
    #gray = cv2.cvtColor(image, cv2.)
    result_image, best_angle = fast_deskew.deskew_image(image) 
    print('Rotate angle: '+ str(best_angle))
    return result_image
"""
#img = cv2.imread('perspective.jpg')
#deskewed =deskew(img)
#cv2.imwrite('deskewed.jpg', deskewed)


def preprocessing(img_path): # input image is RGB or grayscale
    #read image
    image = cv2.imread(img_path)
    # Downscale image as finding receipt contour is more efficient on a small image
    resize_ratio = 500 / image.shape[0]
    original = image.copy()
    image = opencv_resize(image, resize_ratio)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #change into grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) # Gaussian Blur
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    dilated = cv2.dilate(blurred, rectKernel)
    edged = cv2.Canny(dilated, 50, 300, apertureSize=3)
    perspective_path = 'temp/perspective.jpg'
    #if canny cannot edge detection -> skip perspective 
    #it means from original to dwskew if the image was tilted
    try:
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0,255,0), 3)
        largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    #image_with_largest_contours = cv2.drawContours(image.copy(), largest_contours, -1, (0,255,0), 3)
        receipt_contour = get_receipt_contour(largest_contours)
    #image_with_receipt_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 2)
        scanned = wrap_perspective(original.copy(),
                               contour_to_rect(receipt_contour, resize_ratio))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        scanned = deskew(image)
        result = bw_scanner(scanned)
        print('Result image shape: ',result.shape)
        output_path = perspective_path
        cv2.imwrite(output_path, scanned)
        
    else:
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0,255,0), 3)
        largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    #image_with_largest_contours = cv2.drawContours(image.copy(), largest_contours, -1, (0,255,0), 3)
        receipt_contour = get_receipt_contour(largest_contours)
    #image_with_receipt_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 2)
        scanned = wrap_perspective(original.copy(),
                               contour_to_rect(receipt_contour, resize_ratio))
        
        scanned = deskew(scanned)
        result = bw_scanner(scanned)
        print('Result image shape: ',result.shape)
    #plt.figure(figsize=(16,10))
    #plt.imshow(scanned)
    # save image
        print('Preprocessing image has been saved in perspective.jpg')
        
        cv2.imwrite(perspective_path, scanned)
        output_path = real.realesrgan(perspective_path)
    
    return output_path #output is path of preprocessed image
    
    
    
#preprocessing('cccd.jpg')
