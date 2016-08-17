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
Adding stat generation and bonuses for your selected race, which you can 
(obviously) now select. 
'''


import random, os, sys
import platform
import tkFont
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

DEFAULT_NUMBER_NAMES = 1

folders = ['Western_female','Western_male','elf_female','elf_male','goblin','orc','dwarf','greek','japanese_male','japanese_female']

classes = ['human','elf','goblin','half-orc','dwarf','halfling','dragonborn','half-giant','tiefling'] 
stat_names = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Char']
info_labels =['Name','Age','Height','Weight','Languages']
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

age = [[18, 60], #human
         [100,700], #elf
         [3,15], #goblin
         [14,55] , #half-orc
         [50,300], #dwarf
         [20, 120], #halfing
         [15,60],#dragonborn
         [20, 70], #half-giant
         [18, 70] #tiefling
        ]

height = [[4.8, 6.5], #human
         [5, 6.5], #elf
         [3, 4], #goblin
         [5.2,6.5], #half-orc
         [4,5], #dwarf
         [2.5, 3.5], #halfing
         [6, 7],#dragonborn
         [7, 10], #half-giant
         [5, 6] #tiefling
        ]

weight = [[85, 180], #human
         [80, 150], #elf
         [30, 55], #goblin
         [130, 250], #half-orc
         [100,220], #dwarf
         [30,60], #halfing
         [150,300],#dragonborn
         [250,500], #half-giant
         [85,180] #tiefling
        ]


speed = [30, #human
         30, #elf
         30, #goblin
         30, #half-orc
         25, #dwarf
         25, #halfing
         30,#dragonborn
         30, #half-giant
         30 #tiefling
        ]

languages = [['Common'], #human
         ['Common','Elvish'], #elf
         ['Common','Goblin'], #goblin
         ['Common','Orc'], #half-orc
         ['Common','Dwarvish'], #dwarf
         ['Common','Halfling'], #halfing
         ['Common','Draconic'],#dragonborn
         ['Common','Giant'], #half-giant
         ['Common','Infernal'] #tiefling
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
        self.race_age =dict((classes[i],age[i]) for i in range(len(classes)))
        self.race_height =dict((classes[i],height[i]) for i in range(len(classes)))
        self.race_weight =dict((classes[i],weight[i]) for i in range(len(classes)))
        self.race_speed =dict((classes[i],speed[i]) for i in range(len(classes)))
        self.race_languages =dict((classes[i],languages[i]) for i in range(len(classes)))

    def create_widgets(self):
        """Create buttons that do stuff"""
        #create first button      
        self.instruction = Label(self, text = 'Step 1: Choose name ethnicity:')
        self.instruction.grid(row = 0, column = 0, columnspan = 3, sticky = W)  
        f = tkFont.Font(self.instruction, self.instruction.cget("font"))
        f.configure(underline = True,weight = 'bold')
        self.instruction.configure(font=f)
        self.instruction1 = Label(self, text = 'Preset styles:')
        self.instruction1.grid(row = 1, column = 0, sticky = W)
        self.cb_var = []
        for i,k in enumerate(folders):
            var = StringVar()      
            self.cb_var.append(var)
            l = Checkbutton(self,text=k,variable=self.cb_var[i],onvalue=resource_path('namedb'+folderslash+k+'_names.txt'),offvalue='')
            #print(int(i%np.floor(len(folders)/4)+2),int(np.floor(i/np.floor(len(folders)/4))))
            currentrow = int(i%np.floor(len(folders)/4)+2)
            currentcol = int(np.floor(i/np.floor(len(folders)/4)))
            l.grid(row = currentrow,column = currentcol,sticky = W) 
        self.instruction2 = Label(self, text = '   OR   ')
        self.instruction2.grid(row = currentrow+1, column = 0,columnspan=2, sticky = W)   
        self.instruction3 = Label(self, text = 'Your own file location:')
        self.instruction3.grid(row = currentrow+2, column = 0, sticky = W)
        self.flocation = Entry(self)
        self.flocation.grid(row = currentrow+3, column = 0,columnspan=2, sticky = W)
        self.load_button = Button(self,text = 'Step 2: Load Data',command = self.loadngrams)
        self.load_button.grid(row = currentrow+3, column = 3,columnspan=3, sticky = W)       
        self.load_button.configure(font=f)
        self.race_var = StringVar()
        self.race = ttk.Combobox(self,values=classes, textvariable = self.race_var)
        self.race.current(0)
        self.race.grid(row = currentrow+6, column = 0,columnspan=2,sticky=W)
        self.instruction4 = Label(self, text = 'Step 3: Select race:')
        self.instruction4.grid(row = currentrow+5, column = 0,columnspan=2,sticky = W)  
        self.instruction4.configure(font=f)
        #self.instruction4 = Label(self, text = 'Number required:')
        #self.instruction4.grid(row = currentrow+5, column = 0, sticky = W)
        #self.number = Entry(self,width=10)
        self.submit_button = Button(self,text = 'Step 4: Generate!',command = self.getnames)
        self.submit_button.grid(row = currentrow+7, column = 1,columnspan = 2, sticky = W) 
        self.submit_button.configure(font=f)
        self.lock = Label(self, text = 'Lock')
        self.lock.grid(row=currentrow+7,column=3,sticky=W)
        self.char_info = []
        self.char_labels = []
        self.char_info_lock = []
        for i,k in enumerate(info_labels):
            self.char_info.append(Entry(self))  
            self.char_info[i].grid(row = currentrow+9+i, column = 1,columnspan=2, sticky = E) 
            self.char_labels.append(Label(self, text = k+': '))
            self.char_labels[i].grid(row = currentrow+9+i, column = 0,sticky = E)
            var = IntVar()      
            self.char_info_lock.append(var)
            l = Checkbutton(self,variable=self.char_info_lock[i],onvalue=1,offvalue=0)
            l.grid(row = currentrow+9+i, column = 3,sticky = W)
        self.stats = []
        self.stat_labels = []
        for i,k in enumerate(stat_names):
            self.stat_labels.append(Label(self, text = k+': '))
            self.stat_labels[i].grid(row = currentrow+14+i, column = 0, sticky = E) 
            self.stats.append(Entry(self))
            self.stats[i].grid(row = currentrow+14+i, column = 1,columnspan=2, sticky = E) 

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
        #self.text.delete(0.0,END)
        message = 'Bigrams loaded!' + self.flocation.get() + '\n'
        #self.text.insert(0.0,message)
        self.loadtrigrams()
        message = 'Trigrams loaded!' + self.flocation.get() + '\n'
        #self.text.insert(0.0,message)

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
        #if self.number.get():
         #   number_names = int(self.number.get())
       # else: 
        number_names = DEFAULT_NUMBER_NAMES
        #print(number_names)
        self.resultant_names = []
        self.scores = []
        #self.text.delete(0.0,END)
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
            #print(new_name)
            if score2 > self.thresh2/1.4:
                self.resultant_names.append(new_name)
                self.scores.append([score2, score3])
        self.scores, self.resultant_names = (list(t) for t in zip(*sorted(zip(self.scores, self.resultant_names))))
        for n in self.resultant_names:
            self.getinfo()
            #THIS IS WHERE THE PRINTING HAPPENS!!
            #note that tkinter prints and then shifts down, meaning that the operations are
            #opposite to reading order
            print_info = []
            print_info.append(n) # name
            print_info.append("%3.0f"%(self.player_age))         
            height_ft = np.floor(self.player_height) 
            print_info.append("%2.0f"%(height_ft)+'ft'+"%2.0f"%((self.player_height-height_ft)*12)+'in')
            print_info.append("%3.0f"%(self.player_weight)+'lbs')
            lang = ''.join(str(i+', ') for i in self.player_languages)
            print_info.append(lang)
            #self.text.insert(0.0,'\n')
            #self.text.insert(0.0,print_stats)
            #self.text.insert(0.0,'Stats:')
            #print player info
            for i,k in enumerate(info_labels):
                if self.char_info_lock[i].get() == 0:
                    self.char_info[i].delete(0,END)
                    self.char_info[i].insert(0,print_info[i])  
            #print player stats
            for i,k in enumerate(self.player_stats):
                self.stats[i].delete(0,END)
                self.stats[i].insert(0,self.player_stats[i])

    def getinfo(self):
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
        self.player_height = random.gauss(np.mean(self.race_height[self.race_var.get()]),np.mean(self.race_height[self.race_var.get()])/10)
        self.player_weight = random.gauss(np.mean(self.race_weight[self.race_var.get()]),np.mean(self.race_weight[self.race_var.get()])/10)
        self.player_age = random.uniform(*self.race_age[self.race_var.get()])
        self.player_languages = self.race_languages[self.race_var.get()]
        #print(self.player_stats)



root = Tk()
root.title('NPC generator')
root.geometry("500x470")
app = Application(root)
root.mainloop()






