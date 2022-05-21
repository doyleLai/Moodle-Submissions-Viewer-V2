# Moodle-Submissions-Viewer-V2
A python script that creates a web view of online-text submissions of Moodle's assignment activity.

# Description
This script creates a web view of online-text submissions. Compared to https://github.com/doyleLai/Moodle-Submissions-Viewer which requires Flask framework to set up a local server, this script create a single static HTML file. Because the file is static, there is no need to keep the python interpretor running once the web file is created.

# Create the web view
1. Download submissions on Moodle (Download submissions in folders) and unzip the folder.
1. Put the viewmake.py and the unzipped folder together.
1. Run `python viewmake.py <folder_name>`, where <folder_name> is the unzipped folder. After running, a <folder_name>.html is created in the current folder. 
1. Open the webpage in a web browser.
