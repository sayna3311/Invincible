
# !pip install imutils

import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import imutils
import pprint
from matplotlib import pyplot as plt
import random
import os


def extractSkin(image):
  # minRange for min skin color Rnage
  # maxRange for maximum skin color Range
  minRange = np.array([100,133,77],np.uint8)
  maxRange = np.array([235,173,127],np.uint8)
  #image = cv2.imread(r"/required_images/tryOn.jpg")
  image = cv2.imread(r"F:\Hackathon\nitriders_myntra\required_images\tryOn.jpeg")
  #image.show()

  # change our image bgr to ycr using cvtcolor() method 
  YCRimage = cv2.cvtColor(image,cv2.COLOR_BGR2YCR_CB)
  # apply min or max range on skin area in our image
  skinArea = cv2.inRange(YCRimage,minRange,maxRange)
  detectedSkin = cv2.bitwise_and(image, image, mask = skinArea)

  return detectedSkin
# ------------------------------------------------------------
def removeBlack(estimator_labels, estimator_cluster):
  # Check for black
  hasBlack = False
  
  # Get the total number of occurance for each color
  occurance_counter = Counter(estimator_labels)

  
  # Quick lambda function to compare to lists
  compare = lambda x, y: Counter(x) == Counter(y)
   
  # Loop through the most common occuring color
  for x in occurance_counter.most_common(len(estimator_cluster)):
    
    # Quick List comprehension to convert each of RBG Numbers to int
    color = [int(i) for i in estimator_cluster[x[0]].tolist() ]
    
  
    
    # Check if the color is [0,0,0] that if it is black 
    if compare(color , [0,0,0]) == True:
      # delete the occurance
      del occurance_counter[x[0]]
      # remove the cluster 
      hasBlack = True
      estimator_cluster = np.delete(estimator_cluster,x[0],0)
      break
      
   
  return (occurance_counter,estimator_cluster,hasBlack)
# -------------------------------------------------------------------------------------
def getColorInformation(estimator_labels, estimator_cluster,hasThresholding=False):
  
  # Variable to keep count of the occurance of each color predicted
  occurance_counter = None
  
  # Output list variable to return
  colorInformation = []
  
  
  #Check for Black
  hasBlack =False
  
  # If a mask has be applied, remove th black
  if hasThresholding == True:
    
    (occurance,cluster,black) = removeBlack(estimator_labels,estimator_cluster)
    occurance_counter =  occurance
    estimator_cluster = cluster
    hasBlack = black
    
  else:
    occurance_counter = Counter(estimator_labels)
 
  # Get the total sum of all the predicted occurances
  totalOccurance = sum(occurance_counter.values()) 
  
 
  # Loop through all the predicted colors
  for x in occurance_counter.most_common(len(estimator_cluster)):
    
    index = (int(x[0]))
    
    # Quick fix for index out of bound when there is no threshold
    index =  (index-1) if ((hasThresholding & hasBlack)& (int(index) !=0)) else index
    
    # Get the color number into a list
    color = estimator_cluster[index].tolist()
    
    # Get the percentage of each color
    color_percentage= (x[1]/totalOccurance)
    
    #make the dictionay of the information
    colorInfo = {"cluster_index":index , "color": color , "color_percentage" : color_percentage }
    
    # Add the dictionary to the list
    colorInformation.append(colorInfo)
    
      
  return colorInformation
# ----------------------------------------------------------------------------
def extractDominantColor(image,number_of_colors=5,hasThresholding=False):
  
  # Quick Fix Increase cluster counter to neglect the black(Read Article) 
  if hasThresholding == True:
    number_of_colors +=1
  
  # Taking Copy of the image
  img = image.copy()
  
  # Convert Image into RGB Colours Space
  img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  
  # Reshape Image
  img = img.reshape((img.shape[0]*img.shape[1]) , 3)
  
  #Initiate KMeans Object
  estimator = KMeans(n_clusters=number_of_colors, random_state=0)
  
  # Fit the image
  estimator.fit(img)
  
  # Get Colour Information
  colorInformation = getColorInformation(estimator.labels_,estimator.cluster_centers_,hasThresholding)
  return colorInformation
# ----------------------------------------------------------------------------------------------------
def plotColorBar(colorInformation):
  #Create a 500x100 black image
  color_bar = np.zeros((100,500,3), dtype="uint8")
  
  top_x = 0
  for x in colorInformation:    
    bottom_x = top_x + (x["color_percentage"] * color_bar.shape[1])

    color = tuple(map(int,(x['color'])))
  
    cv2.rectangle(color_bar , (int(top_x),0) , (int(bottom_x),color_bar.shape[0]) ,color , -1)
    top_x = bottom_x
  return color_bar
# -------------------------------------------------------------------------
def prety_print_data(color_info):
  for x in color_info:
    print(pprint.pformat(x))
    print()
# --------------------------------------------------------------------------------------------------------------
# Get Image from URL. If you want to upload an image file and use that comment the below code and replace with  image=cv2.imread("FILE_NAME")
#image =  imutils.url_to_image("https://images.iphonephotographyschool.com/24743/708/portrait-photography.jpg")
image = cv2.imread(r"F:\Hackathon\nitriders_myntra\required_images\tryOn.jpeg")

print(image)

# Resize image to a width of 250
image = imutils.resize(image,width=250)

#Show image
plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
plt.show()


# Apply Skin Mask
skin = extractSkin(image)

plt.imshow(cv2.cvtColor(skin,cv2.COLOR_BGR2RGB))
plt.show()



# Find the dominant color. Default is 1 , pass the parameter 'number_of_colors=N' where N is the specified number of colors 
dominantColors = extractDominantColor(skin,hasThresholding=True)



#Show in the dominant color information
print("Color Information")
prety_print_data(dominantColors)


#Show in the dominant color as bar
print("Color Bar")
colour_bar = plotColorBar(dominantColors)
plt.axis("off")
plt.imshow(colour_bar)
plt.show()

# """color extraction 

# """
# -----------------------------------------------------------
dom_list = dominantColors[0]['color']
#print(dom_list)

dark_path = "F:\Hackathon\nitriders_myntra\required_images\dark_cloth"
dark_list = []
for root, dirs, files in os.walk(dark_path):
  dark_list += files

medium_path = "F:\Hackathon\nitriders_myntra\required_images\medium_cloth"
medium_list = []
for root, dirs, files in os.walk(medium_path):
  medium_list += files

light_path = "F:\Hackathon\nitriders_myntra\required_images\light_cloth"
light_list = []
for root, dirs, files in os.walk(light_path):
  light_list += files


print("Recommended cloths according to your complexion")

if (dom_list[0] > 233 and dom_list[0] < 250) and (dom_list[1] > 190 and dom_list[1] < 226) and (dom_list[2] > 170 and dom_list[2] < 215):   #fair
  #print("fair complexion")
  for i in range(0, 5):
    img = random.choice(dark_list)
    img_path = dark_path + "/" + img
    image = cv2.imread(img_path)
    plt.imshow(image)
    plt.show()      

elif (dom_list[0] >= 226 and dom_list[0] < 233) and (dom_list[1] >= 150 and dom_list[1] < 190) and (dom_list[2] >= 130 and dom_list[2] < 170):    #medium
  #print("medium complexion")
  for i in range(0, 5):
    img = random.choice(medium_list)
    img_path = medium_path + "/" + img
    image = cv2.imread(img_path)
    plt.imshow(image)
    plt.show()

elif (dom_list[0] > 168 and dom_list[0] < 226) and (dom_list[1] > 90 and dom_list[1] < 150) and (dom_list[2] > 97 and dom_list[2] < 130):      #dark
  #print("dark complexion")
  for i in range(0, 10):
    img = random.choice(light_list)
    img_path = light_path + "/" + img
    image = cv2.imread(img_path)
    plt.imshow(image)
    plt.show()

else:
  for i in range(0, 10):
    img = random.choice(medium_list)
    img_path = medium_path + "/" + img
    image = cv2.imread(img_path)
    plt.imshow(image)
    plt.show()