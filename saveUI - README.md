The saveUI.py works *only* for the steam game Card Survival: Tropical Island, and it allows you to save.

Source Path (the game's path that contains its own saves):
Click on the "browse" button of "Source Path", then navigate to where the game's savegames are (the general folder, where SaveData.json is located), then click on "save" next to it. This path should be something like:
C:\Users\<Your_Username>\AppData\LocalLow\WinterSpring Games\Card Survival - Tropical Island

Destination Path (the folder that will hold your own savegames):
Click on the "browse" button of "Destination Path" and select the path where the saved games will exist (preferably the folder where this file is also in).

Save Game:
First, quit the current session by selecting "save and quit".
After that, you can simply click on the "Save Game" tab, select a slot and a save name, and there. It will save it for you (it copies the files basically). 

Load Game:
Quit the game first completely, then click on "Load Game" tab on the UI, and select a slot.

It works for me!

Installing Python and dependancies:

Download Python from python.org
During installation, check "Add Python to PATH"
Verify installation by opening Command Prompt (Windows) or Terminal (Mac/Linux) and running:
python --version

Then, install the dependancy:
pip install tkinter

Then navigate to the folder where saveUI.py is, and run
python saveUI.py 
(for Windows)
or 
python3 saveUI.py 
(for Linux/MacOS)
