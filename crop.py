import cv2

def cropped(img):
    
    cropped = img[0:img.shape[0], 150:img.shape[1]-200]
    
    return cropped

cv2.waitKey(0)

cv2.destroyAllWindows()