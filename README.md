# Catalog Project
This is a Flask web app that runs on a local python server within a vagrant virtual machine. 
Once the application is running, the user opens a browser to http://localhost:8000 
to access the web app. This is the final project for Section 3 (The Backend: Databases and 
Applications) of the Fullstack Web Developers Nanodegree at Udacity.

## Project Description
In this project, you will be developing a web application that provides a list of items 
within a variety of categories and integrate third party user registration and 
authentication. Authenticated users should have the ability to post, edit, and delete 
their own items.  
  
You will be creating this project essentially from scratch, no templates have been 
provided for you. This means that you have free reign over the HTML, the CSS, and 
the files that include the application itself utilizing Flask.  
  
  
## Requirements
This program requires Python 2.7 to be installed.
Get it [here](https://www.python.org/downloads/).  
It also requires vagrant to be installed and configured with a specific
vagrantfile found 
[here](https://github.com/G1enB1and/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile).  


## Instructions
To summarize the instructions into a shortened version:
Download, extract, move or copy all files into your vagrant directory,
run vagrant up, vagrant ssh, cd into "/vagrant", cd into catalog, run application.py with
python 2.7, then open a browser and go to [http://localhost:8000](http://localhost:8000).
If you need further instructions, don't worry- just keep reading.  

First download these files by clicking the green button on GitHub that says
Clone or download, then click Download Zip.  
Next, you'll need to extract the zip file you downloaded. It will be named
fullstack-nanodegree-vm.zip.  


### Windows Users:
- Open Windows Explorer (or any folder) and browse to the location you
downloaded fullstack-nanodegree-vm.zip to.
- Right-click fullstack-nanodegree-vm.zip and then left-click "Extract All...".
(A new window will pop up that says "Extract Compressed (Zipped) Folders"
at the top.)
- Click the button that says "Extract" at the bottom.
This will make a new folder called fullstack-nanodegree-vm (without the .zip at
the end).
- You can now delete the .zip folder as it is no longer needed.
- Open the fullstack-nanodegree-vm folder.

Now you can move or copy all the files into your vagrant directory. See Requirements above if 
you don't have vagrant.

Once your files are together in your vagrant directory, open your terminal of
choice (I recommend GitBash for Windows users) and type the following
commands:  
"cd "Insert the path to your vagrant folder here""  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"cd catalog"  
"python application.py"  

Now open your browser of choice (I recommend Chrome) 
and browse to [http://localhost:8000](http://localhost:8000).


### Mac Users:
- Open The Finder and search for fullstack-nanodegree-vm or browse to where you
downloaded it.
- Select the zip file and click "Unzip" at the top center of The Finder window.
(If you don't see "Unzip"), then...
- Right-click the file fullstack-nanodegree-vm.zip
- left-click "Open With...",
- left-click "Archive Utility".

Now you can move or copy all the files into your vagrant directory. See Requirements above if 
you don't have vagrant.

Once your files are together in your vagrant directory, open your terminal and
type the following commands:  
"cd "Insert the path to your vagrant folder here""  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"cd catalog"  
"python application.py"  

Now open your browser of choice 
and browse to [http://localhost:8000](http://localhost:8000).  


### Terminal Users (Linux, Mac, or Windows):
- Open Terminal.
- Navigate to the directory where you downloaded or cloned fullstack-nanodegree-vm.
(Use cd to change directory and ls or dir to list what's in your current
directory.)

Now you can move or copy all the files into your vagrant directory. See Requirements above if 
you don't have vagrant.

Once your files are together in your vagrant directory, type the following
commands:  
"cd "Insert the path to your vagrant folder here""  
"vagrant up"  
"vagrant ssh"  
"cd /vagrant"  
"cd catalog"  
"python application.py"  

Now open your browser of choice 
and browse to [http://localhost:8000](http://localhost:8000).  


## License
MIT Licesne found [here](LICENSE.md)
