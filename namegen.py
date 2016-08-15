#!/usr/bin/python
'''
NAMEGEN.PY V1.0
Got it working, generating the names from one or many of several databases,
being Goblin, Western (m+f), Elf (m+f), Orc, and Greek Gods. Also is cross-
platform (only checks for which backslash it should use), which should save time
between two files. Currently the names are generated and scored through bigrams,
but I would like to have a better testing so that less nonsensical names (like
RONONONOR) aren't generated. Also added the number_names parameter to be edited
by the user.

NAMEGEN.PY V1.01
Added japanese names, reshaped gui to be much neater.

NAMEGEN.PY V1.1 
Adding stat generation and bonuses for your selected race
'''


import random, os, sys
import platform
import itertools, numpy as np
from Tkinter import *
import ttk
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}

system = platform.system()
if system == 'Windows':
    folderslash = '\\'
else:
    folderslash = '/'

DEFAULT_NUMBER_NAMES = 10

folders = ['Western_female','Western_male','elf_female','elf_male','goblin','orc','dwarf','greek','japanese_male','japanese_female']

classes = ['human','elf','goblin','half-orc','dwarf','halfling','dragonborn','half-giant','tiefling'] 
stat_names = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Char']
default_stats = [15,14,13,12,10,8]
stat_bonuses = [[1, 1, 1, 1, 1, 1], #human
         [0, 2, 0, 0, 0, 0], #elf
         [0, 2, 0, 0, 0, 0], #goblin
         [2, 1, 0, 0, 0, 0], #half-orc
         [0, 0, 2, 0, 0, 0], #dwarf
         [0, 2, 0, 0, 0, 0], #halfing
         [2, 0, 0, 0, 0, 1],#dragonborn
         [2, 0, 0, 0, 0, 0], #half-giant
         [0, 0, 0, 1, 0, 2] #tiefling
        ]

stat_preferences = [[1, 1, 1, 1, 1, 1], #human
         [5, 1, 3, 4, 2, 5], #elf
         [3, 1, 2, 3, 3, 3], #goblin
         [1, 2, 3, 4, 4, 4], #half-orc
         [2, 3, 1, 4, 6, 5], #dwarf
         [6, 1, 5, 4, 3, 2], #halfing
         [1, 5, 4, 6, 3, 2],#dragonborn
         [1, 4, 2, 6, 5, 3], #half-giant
         [6, 3, 4, 2, 5, 1] #tiefling
        ]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)

def find_ngrams(input_list, n):
    concat_list =  ''.join(input_list)
    return [concat_list[i:i+n] for i in range(len(concat_list)-n+1)]

class Application(Frame):
    """ Gui application for this stuff"""
    def __init__(self,master):
        """Initialise the frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
        self.loadfile = ''
        self.name = dict((e1,[]) for e1 in alphabet)
        self.race_bonuses = dict((classes[i],stat_bonuses[i]) for i in range(len(classes)))
        self.race_preference = dict((classes[i],stat_preferences[i]) for i in range(len(classes)))

    def create_widgets(self):
        """Create buttons that do stuff"""
        #create first button
        self.instruction1 = Label(self, text = 'Preset styles:')
        self.instruction1.grid(row = 0, column = 0, sticky = W)
        self.cb_var = []
        for i,k in enumerate(folders):
            var = StringVar()      
            self.cb_var.append(var)
            l = Checkbutton(self,text=k,variable=self.cb_var[i],onvalue=resource_path('namedb'+folderslash+k+'_names.txt'),offvalue='')
            #print(i%4+1,i%2)
            currentrow = int(i%np.floor(len(folders)/2)+1)
            currentcol = int(np.floor(i/np.floor(len(folders)/2)))
            l.grid(row = currentrow,column = currentcol,sticky = W)    
        self.instruction2 = Label(self, text = '   OR   ')
        self.instruction2.grid(row = currentrow+1, column = 0, sticky = W)   
        self.instruction3 = Label(self, text = 'Your own file location:')
        self.instruction3.grid(row = currentrow+2, column = 0, sticky = W)
        self.flocation = Entry(self)
        self.flocation.grid(row = currentrow+3, column = 0,columnspan = 2, sticky = W)
        self.load_button = Button(self,text = 'Load Data',command = self.loadngrams)
        self.load_button.grid(row = currentrow+4, column = 0, sticky = W)
        self.instruction4 = Label(self, text = 'Number required:')
        self.instruction4.grid(row = currentrow+5, column = 0, sticky = W)
        self.number = Entry(self,width=10)
        self.number.insert(END,'10')
        self.number.grid(row = currentrow+6, column = 0,columnspan = 1, sticky = W)
        self.text = Text(self, width = 60, height = 15, wrap = WORD)    
        self.text.grid(row = 3, column = 4, columnspan = 5,rowspan = currentrow+5, sticky =W)    
        self.submit_button = Button(self,text = 'Generate!',command = self.getnames)
        self.submit_button.grid(row = 2, column = 4, sticky = W)
        self.race_var = StringVar()
        self.race = ttk.Combobox(self,values=classes, textvariable = self.race_var)
        self.race.current(0)
        self.race.grid(row = 1, column = 4)
        self.instruction4 = Label(self, text = 'Now select your race and generate!')
        self.instruction4.grid(row = 0, column = 4, columnspan = 2,sticky = W)

    def loadngrams(self):
        if self.flocation.get()!="":
            self.style = self.flocation.get()
            text_file = open(self.flocation.get(), "r")
            lines = text_file.readlines()
            self.lines = [i.upper() for i in lines]
            #print(self.lines)
            text_file.close()
        else:
            self.lines = []
            for i in self.cb_var:
                if i.get():
                    text_file = open(i.get(),'r')
                    lines = text_file.readlines()
                    self.lines.append([i.upper() for i in lines])
                    text_file.close()
            self.lines = list(itertools.chain.from_iterable(self.lines))
        self.loadbigrams()
        self.text.delete(0.0,END)
        message = 'Bigrams loaded!' + self.flocation.get() + '\n'
        self.text.insert(0.0,message)
        self.loadtrigrams()
        message = 'Trigrams loaded!' + self.flocation.get() + '\n'
        self.text.insert(0.0,message)

    def loadbigrams(self):
        bg = find_ngrams(self.lines,2)
        self.bg_new = [i.upper() for i in bg if i[0]!='\n']
        [self.name[i[0]].append(i) for i in self.bg_new]
        self.bgl = [(g[0], (float(len(list(g[1])))/len(self.bg_new))) for g in itertools.groupby(sorted(self.bg_new))]
        self.bscores = dict(self.bgl)
        min_bscore = min(self.bscores.values())
        for i in alphabet:
            for j in alphabet:
                key = i+j
                if key not in self.bscores.keys():
                        self.bscores[key] = min_bscore

    def loadtrigrams(self):
        tg = find_ngrams(self.lines,3)
        self.tg_new = [i.upper() for i in tg if i[0]!='\n']
        [self.name[i[0]].append(i) for i in self.bg_new]
        self.tgl = [(g[0], (float(len(list(g[1])))/len(self.tg_new))) for g in itertools.groupby(sorted(self.tg_new))]
        self.tscores = dict(self.tgl)
        min_tscore = min(self.tscores.values())
        for i in alphabet:
            for j in alphabet:
                for k in alphabet:
                    key = i+j+k
                    if key not in self.tscores.keys():
                        self.tscores[key] = min_tscore
                    

    def getnames(self):
        self.thresh2 = np.mean([np.mean([self.bscores[new_name[i:i+2]] for i in range(len(new_name)-1)]) for new_name in self.lines])
        self.thresh3 = np.mean([np.mean([self.tscores[new_name[i:i+3]] for i in range(len(new_name)-2)]) for new_name in self.lines])
        #print(self.thresh)
        if self.number.get():
            number_names = int(self.number.get())
        else: 
            number_names = DEFAULT_NUMBER_NAMES
        #print(number_names)
        self.resultant_names = []
        self.scores = []
        self.text.delete(0.0,END)
        while len(self.resultant_names) < number_names:
            new_name = self.bg_new[random.randint(0,len(self.bg_new)-1)]
            while new_name[1] == '\n':
                new_name = self.bg_new[random.randint(0,len(self.bg_new)-1)]
            end_name = False
            while 1:        
                if random.randint(3,10) < len(new_name)+1:
                    break
                hi = self.name[new_name[-1]][random.randint(0,len(self.name[new_name[-1]])-1)]
                while  hi[1] == '\n':
                    hi = self.name[new_name[-1]][random.randint(0,len(self.name[new_name[-1]])-1)]
                new_name = new_name + hi[1]
            #print(new_name)            
            score3 = np.mean([self.tscores[new_name[i:i+3]] for i in range(len(new_name)-2)])            
            score2 = np.mean([self.bscores[new_name[i:i+2]] for i in range(len(new_name)-1)])
            print(new_name)
            if score2 > self.thresh2/1.4:
                self.resultant_names.append(new_name)
                self.scores.append([score2, score3])
        self.scores, self.resultant_names = (list(t) for t in zip(*sorted(zip(self.scores, self.resultant_names))))
        for n in self.resultant_names:
            self.getstats()
            #THIS IS WHERE THE PRINTING HAPPENS!!
            #note that tkinter prints and then shifts down, meaning that the operations are
            #opposite to reading order
            a = ''.join(str(s+': '+str(self.player_stats[i])+', ') for i,s in enumerate(stat_names))
            message = n+'\n'
            self.text.insert(0.0,'\n')
            self.text.insert(0.0,a)
            self.text.insert(0.0,message)

    def getstats(self):
        player_stats = [sum(sorted(np.random.randint(6, size=4)+1)[1:]) for i in range(6)]
        if sum(player_stats) < sum(default_stats) - 1:
            player_stats = default_stats
        #print(player_stats)
        player_pref = self.race_preference[self.race_var.get()][:]
        for j in range(1,len(stat_preferences[0])):
            inds = [i for i,val in enumerate(self.race_preference[self.race_var.get()]) if val==j]
            if len(inds) > 1:
                matching_pref = range(len(inds))
                random.shuffle(matching_pref)
                for i,k, in enumerate(inds):
                    player_pref[k] = player_pref[k] + matching_pref[i]
        #have to sort them according to the race, now
        player_stats = [sorted(player_stats,reverse=True)[i-1] for i in player_pref]
        self.player_stats = [sum(x) for x in zip(player_stats, self.race_bonuses[self.race_var.get()])]
        #print(self.player_stats)



root = Tk()
root.title('NPC generator')
root.geometry("700x300")
app = Application(root)
root.mainloop()






