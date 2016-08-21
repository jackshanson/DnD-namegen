#Name and Stat Generator for Dungeons and Dragons (D&D)#
Save yourself some tedious dice rolls and use this name and stat generator for DnD. The algorithm is a heuristic letter selector based on a database of bigrams from your chosen gender and fantasy race or ethnicity. The names it generates are completely random, and sometimes nonsensical (so be kind to it!), rather than picked from an existing list as most other name generators seem to be. 

The program also generates the age, height, weight, languages, and stats (Str, Dex, etc) for your chosen race and gender. These player characteristics can also be entered by a user and locked so that the program does not overwrite them. Furthermore, the stats already include their race bonuses when they are generated.

##What's in here?##
This initial commit contains the namegen.py script, which is the basis of the program. The namegen.spec file is used by the pyinstaller program, which builds the python script into a windows ".exe" file. Finally, the namedb folder contains the current name databases. The current name ethnicities and races are as follows:

Ethnicities  | Races
------------- | -------------
Dwarven  | Dragonborn
Elvish (male and female)  | Dwarf
Goblin | Elf
Greek gods | Goblin
Japanese (male and female) | Half-giant
Orcish | Half-orc
Western (male and female) | Halfling
 | Human
 | Tiefling

Please contact me if you wish to add your own, or feel free in your own distribution! 

Have fun!

##Making the windows executable##
First of all, please ensure you have Python installed on your windows machine. If you don't please click the Python 2.7.xx download at https://www.python.org/downloads/. After this, please run this command to install a dependency:

`pip install numpy`

Now for creating the executable file. Linux users can skip this, as they can obviously just run the python script from a terminal. Windows users will need to compile the file and its dependencies before usage.

Please download and install PyInstaller 3.2 from http://www.pyinstaller.org/, and use the following command from the cmd terminal inside the DnD-namegen directory:

`pyinstaller namegen.spec --onefile`

and the resultant ".exe" file will be located in the "dist" folder in the current directory.

##Useful links##
* A useful guide to installing Python on windows 10 can be found at: http://www.anthonydebarros.com/2015/08/16/setting-up-python-in-windows-10/
* How to install PyInstaller: http://pyinstaller.readthedocs.io/en/latest/installation.html


