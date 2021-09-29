import os 

def getSubFolders():
    folders = os.listdir("B_R_Illumination/static/images")
    

    images = []
    for i, item in enumerate(folders):
        images.append(os.listdir("B_R_Illumination/static/images/"+str(folders[i])))
        print(images[i])

    return folders, images

