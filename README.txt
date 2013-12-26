README.txt

Welcome to DrumMaster 9000!

For those who want to see the code, open up "final-code.py".

Otherwise, follow the proceeding instructions:

In order to run the program, you're going to need a Mac (I think you can run it on a Windows too, but I'm not sure).

First, you're going to want to install macports. It can be found at 
http://www.macports.org/

Just click the download button and download it.

Then, opening up terminal, you're going to want to install python 2.7 THROUGH macports (you might already have python on your computer, but you're gonna need to install another one with macports. To do this, open up terminal and then type "sudo port install python27" and hit enter.  This should install python through macports.

Now we're going to want to have our default python be that python that we just installed. To do this, we're going to want to type "sudo port select python python27" into the terminal. This will select the python 2.7 that we just installed.

Now that we've done this, we're going to want to install the modules that we need to run this program. Type in "sudo port install numpy" to install NumPy. After that's finishing installing, type in "sudo port -v install opencv +python27" to instal OpenCV with python bindings. This may take a while (like around half an hour).

When that's finished installing, type in "sudo port install py27-game" to install pygame.


If all of this is done successfully, then you now have everything you need to run the program! Assuming you have all the necessary files, run the script from terminal and it should work!