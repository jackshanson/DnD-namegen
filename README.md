# DnD-namegen
Save yourself some tedious dice rolls and use this name and stat generator for DnD. The algorithm is a heuristic letter selector based on a database of bigrams from your chosen gender and fantastical race or ethnicity. 

You may need to build the file in windows first. Please download the PyInstaller program from http://www.pyinstaller.org/, and use the namegen.spec file and --onefile option to create your own file.

This initial commit contains the namegen.py script, which is the basis of the program. The namegen.spec file is used by the pyinstaller program, which builds the python script into a windows ".exe" file. Finally, the namedb folder contains the current database names, which currently consists of:
* Dwarf
* elf (male and female)
* goblin
* greek gods
* japanese (male and female)
* orc
* western (male and female)

Please contact me if you wish to add your own, or feel free in your own distribution! 

Have fun!
