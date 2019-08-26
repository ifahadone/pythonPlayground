import numpy as np
import cv2


def scanProcess(imgO):
    

    def resize(img,height=1477):
        #resize image to given height
        rat = height/img.shape[0]
        
        return cv2.resize(img,(int(rat * img.shape[1]),height))
    
    #resize and convert to grayscale
    img = cv2.cvtColor(resize(imgO), cv2.COLOR_BGR2GRAY)
    #cv2.imshow('2',img)
    
    #bilateral filter preserv edges
    img = cv2.bilateralFilter(img,9, 75, 75)
    
    #Create black and white image based on adaptive threshold
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 4)
    #cv2.imshow('5',img)
    
    #Median filter clears small details
    img = cv2.medianBlur (img,11)
    #cv2.imshow('after median blur',img)
    
    #Add black border in case that page is touching an image border
    img = cv2.copyMakeBorder(img, 5,5,5,5, cv2.BORDER_CONSTANT, value=[0,0,0])
    #cv2.imshow('3',img)
    
    edges = cv2.Canny(img, 200, 250)
    #cv2.imshow('edgesssss',edges)
    
    
    #Getting contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #Finding contour of biggest rectangle
    #Otherwise return corners of original image
    #Don't forget on 5px border
    height = edges.shape[0]
    width = edges.shape[1]
    MAX_CONTOUR_AREA = (width - 10) * (height - 10)
    
    #Page fill at least half of image, then saving max area found
    maxAreaFound = MAX_CONTOUR_AREA * 0.5
    
    #Saving page contour
    pageContour = np.array([[5,5],[5,height-5],[width-5,height-5],[width-5,5]])
    
    
    #Go through all contours
    for cnt in contours:
        #Simplify contour
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 *perimeter, True)
        
        #Page has 4 corners and it is convex
        #Page area must be bigger than maxAreaFound
        if (len(approx) == 4 and cv2.isContourConvex(approx) and 
            maxAreaFound < cv2.contourArea(approx) < MAX_CONTOUR_AREA):
            
            maxAreaFound = cv2.contourArea(approx)
            pageContour = approx
        
    #Result in pageContour (numpy array of 4 points):
    
    def fourCornersSort(pts):
        #sort corners: top-left, bot-left, bot-right, top-right
        #Difference and sum of x and y value
        #inspired by http://www.pyimagesearch.com
        diff = np.diff(pts, axis=1)
        summ = pts.sum(axis=1)
        
        #Top-left point has smallest sum
        #np.argmin() returns INDEX of min
        return np.array([pts[np.argmin(summ)],
                             pts[np.argmax(diff)],
                             pts[np.argmax(summ)],
                             pts[np.argmin(diff)]])
        
    
    def contourOffset(cnt, offset):
        #Offset contour, by 5px
        #Matrix addition
        cnt += offset
        
        #if value < 0 => replace it by 0
        cnt[cnt < 0] = 0
        return cnt
    
    #Sort and offset corners 
    pageContour = fourCornersSort(pageContour[:,0])
    pageContour = contourOffset(pageContour,(-5,-5))
    
    #Recalculate to original scale - start Points
    sPoints = pageContour.dot(img.shape[0]/1477)
    
    
    #Using Euclidean distance
    #Calculate maximum height (maximal length of vertical edges) and width
    height = max(np.linalg.norm(sPoints[0] - sPoints[1]),
                 np.linalg.norm(sPoints[2] - sPoints[3]))
    width = max(np.linalg.norm(sPoints[1] - sPoints[2]),
                np.linalg.norm(sPoints[3] - sPoints[0]))
    
    #Create target points
    tPoints = np.array([[0,0], [0,height],
                        [width,height], [width,0]], np.float32)    
        
    #getPerspectiveTransform() needs float32
    if sPoints.dtype != np.float32:
        sPoints = sPoints.astype(np.float32)
        
    
    #Wraping perspective
    M = cv2.getPerspectiveTransform(sPoints, tPoints)
    newImg = cv2.warpPerspective(imgO, M, (int(width), int(height)))
    
    #cv2.namedWindow('cut out',cv2.WINDOW_NORMAL)
    #cv2.imwrite('cut-out.jpg',newImg)
    #cv2.imshow('cut out',newImg)
    
    return newImg
 
cv2.waitKey(0)

cv2.destroyAllWindows()