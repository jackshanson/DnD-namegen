# DnD-namegen
Save yourself some tedious dice rolls and use this name and stat generator for DnD. The algorithm is a heuristic letter selector based on a database of bigrams from your chosen gender and fantastical race or ethnicity. 

##What's in here?##
This initial commit contains the namegen.py script, which is the basis of the program. The namegen.spec file is used by the pyinstaller program, which builds the python script into a windows ".exe" file. Finally, the namedb folder contains the current name databases. The current name ethnicities and races are as follows:

Ethnicities  | Races
------------- | -------------
Dwarven  | Dragonborn
elvish (male and female)  | Dwarf
goblin | Elf
greek gods | Goblin
japanese (male and female) | Half-giant
orcish | Half-orc
western (male and female) | Halfling
 | Human
 | Tiefling

Please contact me if you wish to add your own, or feel free in your own distribution! 

Have fun!

##Making the executable##
You will need to build the file in windows first. Please download the PyInstaller program from http://www.pyinstaller.org/, and use the following command from the cmd terminal:

path-to-pyinstaller\pyinstaller namegen.spec --onefile

and the resultant ".exe" file will be located in the "dist" folder in the current directory.
