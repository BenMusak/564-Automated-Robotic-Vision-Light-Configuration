# Group 564, Automated Robotic Vision Light Configuration
5th semester github for our project at AAU.

# Dependencies
Libraries required to run the program
- Flask 1.1 
- RoboDK (program and libraries)
- Numpy

# Numpy Anaconda issues.
- I you experience problems when installing numpy using Anaconda, then try pip install (Worked for me).

# How to install RoboDK libraries.
- Navigate to C:\RoboDK\Python37\Lib\site-packages (or wherever you installed RoboDK)
- find the folders "robodk" and "robolink"
- Copy the folders and paste them into your prefered python environment folder
  - Example: I pasted them into C:\Users\Kaj\anaconda3\envs\Flask_WebGUI

# How to run
 - Create a custom python environment that includes all the necesary dependencies. 
 - Link the python environment to the project.
 - Open Robodk and import an UR5e from the library.
 - Run the "runserver.py" file.

# Rules
Setup the rules here
- All files that only relates to your own pc should never be included in commits, make sure to add them to gitignore!.
- All custom environments should be added to gitignore.
- If you did not create the branch (or if it the main branch), please to not make direct commits, only pull requests.

# Tasks 
- [ ] Add socket dependency
- [ ] Create script for tcp/ip or udp/ip communication with B&R Automation studio.

# Issues
- [ ] Issues tasks here 

# Links
Further information about the Flask framework can be found here: https://code.visualstudio.com/docs/python/tutorial-flask 
