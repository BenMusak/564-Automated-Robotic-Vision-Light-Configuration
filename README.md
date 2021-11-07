# Branch features.
- New page with elements for choosing parameters and starting tests.

# Group 564, Automated Robotic Vision Light Configuration
5th semester github for our project at AAU.

# Dependencies
Libraries required to run the program
- Flask 1.1 
- RoboDK (program and libraries)
- Numpy
- Colorama

# Numpy Anaconda issues.
- I you experience problems when installing numpy using Anaconda, then try pip install (Worked for me).

# How to install RoboDK libraries.
- Navigate to C:\RoboDK\Python37\Lib\site-packages (or wherever you installed RoboDK)
- find the folders "robodk" and "robolink"
- Copy the folders and paste them into your prefered python environment folder
  - Example: I pasted them into C:\Users\Kaj\anaconda3\envs\Flask_WebGUI

# RoboDK library install issues.
- If the above guide does not work, then try to install it using pip install (Worked for Kasper).

# How to run
 - Create a custom python environment that includes all the necesary dependencies. 
 - Link the python environment to the project.
 - Open Robodk and import an UR5e from the library.
 - Add at least one folder in the /static/images/ directory.
    - OBS! Do not add images directly into the /static/images folder, only subfolders!
 - Run the "runserver.py" file.

# Rules
Setup the rules here
- All files that only relates to your own pc should never be included in commits, make sure to add them to gitignore!.
- All custom environments should be added to gitignore.
- If you did not create the branch (or if it the main branch), please to not make direct commits, only pull requests.

# Tasks 
- [ ] 
- [ ] 

# Issues
- [ ] Server crashes if there are images in the /static/images folder.
- [ ] After running two robots simultaneously for a while, RoboDK gives an error and crashes. 

# Links
Further information about the Flask framework can be found here: https://code.visualstudio.com/docs/python/tutorial-flask 
