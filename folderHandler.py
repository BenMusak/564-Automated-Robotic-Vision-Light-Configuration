import os 
import re

def getSubFolders():
    folders = os.listdir("B_R_Illumination/static/images")
    

    images = []
    for i, item in enumerate(folders):
        image_list = os.listdir("B_R_Illumination/static/images/"+str(folders[i]))
        nums = [re.findall('\d+',ss) for ss in image_list] # extracts numbers from strings
        numsint = [int(*n) for n in nums] # returns 0 for the empty list corresponding to the word
        sorted_image_list = [x for y, x in sorted(zip(numsint, image_list))] # sorts s based on the sorting of nums2
        images.append(sorted_image_list)
        #print(images[i])d

    return folders, images

