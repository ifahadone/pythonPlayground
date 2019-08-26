# Fly Detection and Counting

## Description
This project is about perform image segmentation in order to detect the number of flies in an image using OpenCV Python. The code is implemented together with Falcon framework to act as internal webservices. 

## Tools

Main tools used for this programs are:
1. Python 3.6
2. OpenCV Library 4.0
3. Falcon 2.0

## Prerequisite

There are some things need to take note on:

1. Preferable condition of input image
- Consistency of image taken
- In potrait view mode
- Same(almost) image brightness
- Avoid reflection
- Same distance of camera from object taken
- Position at almost the same place

2. Adjustment may need to be done according to the nature of image 

## Usage

Parts of code that can/need to be change accordingly

### Code

1. Function to cut-out the fly glue trap from main image
- this part is to avoid unnecessary background to disturb detection process
- two ways to perform:

a) using document scanner 
- import scanProcess function from pageScan.py if to use this method
- harder to set generic setting that would work with every image
- prone to give error if parameters setting not suitable with image, hence cannot give cut-out image
- current code setting works well with sample image flyA only
- for more details, refer: https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

b) using cropping
- import cropped function from crop.py if to use this method
- less problem to setup generic setting that suit with every image
- provided that pattern of image taken and input into is consistent

```python
# doing slicing arrays
# supply the startY and endY coordinates, followed by the startX and endX coordinates

cropped = img[0:img.shape[0], 150:img.shape[1]-200]
```
- difficulty only in getting the right coordinates values to crop out
- work easily if input image is closely the same, potrait view, such as sample images 1,2,3,5 and 7

Improvisation need to be done to able it run well with the image

## Remarks

Results may be vary and not have high accuracy. 
