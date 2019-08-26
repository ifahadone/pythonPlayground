import numpy as np
import cv2
#from pageScan import scanProcess
from m4.crop import cropped

def detect(a):
    
    # convert data into image format
    img = cv2.imdecode(a, cv2.IMREAD_COLOR) # like cv2.imread()
    
    # function to snip the image of fly glue trap
    #img = scanProcess(img)
    img = cropped(img)
    
    # virtually save the image of new cut-out image
    # convert the image format into streaming data
    ret, imgCrop = cv2.imencode('.jpg', img) # like cv2.imwrite()
    # cnvert into image format for later use
    imgCrop = cv2.imdecode(imgCrop, cv2.IMREAD_COLOR)

    #perform grayscale conversion and thresholding
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    thresh = gridline(gray, thresh)

    #Setting up size of objects(number of pixel) to segment
    ret, markers,stats,centroids = cv2.connectedComponentsWithStats(thresh)
    size=stats[1:,-1]; ret=ret-1
    
    #declaration for answer image 
    imgB = np.zeros((markers.shape))

    #to keep only the component in the image that is above min size
    for i in range(0,ret):
        if (size[i] > 350  ):
                imgB[markers == i+1] = 255
    
    #convert image data type to 8 bit unsigned interger
    imgB = np.uint8(imgB)

    img = cover350(imgB,img)

    # noise removal
    kernel = np.ones((2,3),np.uint8)
    kernel2 = np.ones((1,2),np.uint8)

    #opening - erosion then dilate
    opening = cv2.morphologyEx(imgB,cv2.MORPH_OPEN,kernel, iterations = 2)
    
    #closing - dilate then erosion
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel2, iterations = 1)
    
    #sure background area
    sureBack = cv2.dilate(imgB,kernel,iterations=1)
    
    #finding sure foreground area
    dist_transform = cv2.distanceTransform(closing,cv2.DIST_L2, 3)
    
    # Threshold
    ret, sureFore = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)
    
    #finding unknown region
    sureFore = np.uint8(sureFore)
    unknown = cv2.subtract(sureBack,sureFore)
    
    #marker labelling
    ret, markers,stats,centroids = cv2.connectedComponentsWithStats(sureFore)
    
    #add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    
    #mark the region of unknown with zero
    markers[unknown==255] = 0
    
    # apply watershed
    markers = cv2.watershed(img,markers)
    img[markers == -1] = [0,0,255] #label in red
    img[markers> 1 ] = [255,0,0] #label in blue
    
    # to count object detection with area greateer than 350
    am,pm = ((np.unique(markers,return_counts=True)))
    countB= 0

    for i in range(len(am)):
        if am[i] > 1 and pm[i] > 350:
            countB+=1     
    
    # virtually save the result image
    ret, imgMark = cv2.imencode('.jpg', img)
    imgDiff = cv2.imdecode(imgMark, cv2.IMREAD_COLOR)
    
    # to calculate difference of initial and after detection image
    # use to find coverage percentage
    difference = cv2.absdiff(imgDiff, imgCrop)

    result = difference.astype(np.uint8) #if difference is all zeros it will return False

    percentage = (np.count_nonzero(result) * 100/result.size)

    if (percentage < 66):
        percentage = percentage*1.5
    
    coverage = ("Coverage of the flies is  {0:.2f}%".format(percentage))   

    result = ("[INFO] {} unique segments found".format(countB))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return imgMark, result, coverage;

def gridline(gray, thresh):
        # to remove grid line, extract horizontal and vertical line
        
        # apply adaptiveThreshold at the bitwise_not of gray
        gray = cv2.bitwise_not(gray)
        bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
        
        # create the images that will use to extract the horizontal and vertical lines
        horizontal = np.copy(bw)
        vertical = np.copy(bw)
        
        # specify size on horizontal axis
        cols = horizontal.shape[1]
        horizontal_size = cols // 30
        
        # create structure element for extracting horizontal lines through morphology operations
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

        # apply morphology operations
        horizontal = cv2.erode(horizontal, horizontalStructure)
        horizontal = cv2.dilate(horizontal, horizontalStructure)
        
        # inverse horizontal image, mask it to cover the lines
        mask = cv2.bitwise_not(horizontal)
        horimask = cv2.bitwise_and(thresh, thresh, mask=mask)

        # specify size on vertical axis
        rows = vertical.shape[0]
        verticalsize = rows //30

        # create structure element for extracting vertical lines
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

        # apply morphology operations
        vertical = cv2.erode(vertical, verticalStructure)
        vertical = cv2.dilate(vertical, verticalStructure)

        # inverse vertical image, mask it to cover the lines
        vmask = cv2.bitwise_not(vertical)
        nogrid = cv2.bitwise_and(horimask, horimask, mask=vmask)

        return nogrid

def cover350(picS,img):
    
    #marker labelling
    ret, markers = cv2.connectedComponents(picS)
    
    #add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    
    markers = cv2.watershed(img,markers)
    img[markers> 1 ] = [255,0,0] #label in blue      

    return  img
      
    


    