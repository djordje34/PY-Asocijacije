import os
import random
import tkinter as tk
from tkinter import messagebox
import numpy as np
from tkinter import font

global buttons
buttons=list() 
global entries
entries=list()
global sols
sols=list()
global checkButtons
checkButtons=list()
color={"purple":"#461E52",
        "pink":"#DD517F",
        "yellow":"#E68E36",
        "darkblue":"#556DC8",
        "lightblue":"#7998EE"} 
simpledict=["А","Б","В","Г"]


def globalWordSim(w1,w2):
    cnt=0
    rng,total=min(len(w1),len(w2)),max(len(w1),len(w2))
    
    for x in range(rng):
        if w1[x]==w2[x]:
            cnt+=1
        else:
            break

    return (round(cnt*100/total,2))

def getAsocijacija():
    filepath=path=os.path.join("manual")

    test=random.choice([x for x in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, x))])
    print("Датотека ",filepath,test)
    
    with open(filepath+"\\"+test,encoding = 'utf-8', mode = 'r') as f:
        lines = list(line for line in (l.strip() for l in f) if line)
        #lines = f.readlines()[5:25]
        fin=lines[25]
        lines=lines[5:25]
        
        lines=[x.replace("\n","") for x in lines]
        
    lines=np.asarray(lines)
    asoc=np.zeros((4,5)).astype(str)

    y=0
    z=0
    for x in range(len(lines)):
        asoc[y,z]=str(lines[x])
        z+=1
        if z==5:
            z=0
            y+=1
    return asoc,fin.split("-",1)[1]

    

class Asoc():
    
    def __init__(self):
        
        self.buttons=list() 
        self.entries=list()
        self.sols=list()
        self.checkButtons=list()
        self.strVars=list()
        self.cache=list()
        self.win=tk.Tk() 
        self.fin=tk.StringVar()
        self.pts=tk.StringVar()
        self.posPts=[25,25,25,25]
        self.pts.set(0)
        for x in range(4):
            self.strVars.append(tk.StringVar())
        
        screen_width =  self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        self.win.geometry(str(screen_width)+"x"+str(screen_height))
        self.win.state('zoomed')
        self.startGame()
        self.win.mainloop()
        
    def resetGame(self):
        self.pts=tk.StringVar()
        self.pts.set(0)
        self.posPts=[25,25,25,25]
        self.buttons=list() 
        self.entries=list()
        self.sols=list()
        self.checkButtons=list()
        self.strVars=list()
        self.cache=list()
        self.fin=tk.StringVar()
        for x in range(4):
            self.strVars.append(tk.StringVar())
        self.startGame()
           
    def startGame(self):
        for widgets in self.win.winfo_children():
            widgets.destroy()
        mainF = font.Font(family='Helvetica', size=20, weight='bold')
        ctr=0
        pos=0
        self.asoc,self.res=getAsocijacija()
        for x in self.asoc:
            for idx, element in enumerate(x):
                if idx!=4:
                #buttons.append(tk.Button(text=idx).grid(row=idx,column=ctr,fg=color["lightblue"],bg=color["lightblue"],command=lambda x:))
                    x=tk.Button(text=simpledict[ctr]+str(idx+1),anchor="center",bg=color["lightblue"],
                                         activebackground=color["lightblue"],
                                         command=lambda pos=pos:self.showText(pos),font=mainF,foreground="white",activeforeground="white")
                    self.cache.append(element.split("-",1)[1])
                    
                    pos+=1
                    x.grid(row=idx,column=ctr,sticky='nsew',padx=20)
                    self.buttons.append(x)
                else:
                    y=tk.Entry(font=mainF, justify='center',textvariable=self.strVars[ctr])
                    
                    y.grid(row=idx,column=ctr,sticky='nsew',padx=20,ipady=10)
                    self.entries.append(y)
                    
                    self.sols.append(element.split("-")[1])
                    

            tk.Label(text="Тренутни број поена:\n",fg=color["purple"],font=mainF).grid(row=1,column=10)
            self.ukupno=tk.Label(textvariable=self.pts,fg=color["purple"],font=mainF).grid(row=2,column=10)
            ctr+=1
  
        for x in range(4):
            z=tk.Button(text="Потврди",fg=color["darkblue"],anchor="center",bg=color["lightblue"],
                                         activeforeground=color["darkblue"],activebackground=color["lightblue"],
                                         font=mainF,command=lambda x=x:self.checkEntry(x))
            z.grid(row=5,column=x,sticky='nsew',padx=20,ipady=10)
            self.checkButtons.append(z)
            
        self.kon=tk.Entry(font=mainF, justify='center',textvariable=self.fin)
        self.kon.grid(row=6,column=1,columnspan=2,sticky='nsew',padx=20,ipady=10) #DODAJ ZA KONACNO
        self.potv=tk.Button(text="Потврди",fg=color["darkblue"],anchor="center",bg=color["lightblue"],
                                         activeforeground=color["darkblue"],activebackground=color["lightblue"],
                                         command=self.checkFin,font=mainF)
        self.potv.grid(row=7,column=1,columnspan=2,sticky='nsew',padx=20,ipady=10)
        
        self.reset=tk.Button(text="Покрените изнова",fg=color["lightblue"],anchor="center",bg=color["purple"],
                                         activeforeground=color["lightblue"],activebackground=color["purple"],
                                         command=self.resetGame,font=mainF)
        
        self.reset.grid(row=8,column=1,columnspan=2,sticky='nsew',ipady=10,pady=150)
        
        
            
        
    def showText(self,idx):
        self.buttons[idx].config(foreground="white",activeforeground="white")
        self.buttons[idx]["text"]=self.cache[idx]
        self.posPts[idx//4]-=5

        
    def checkEntry(self,idxB):
        s1=self.strVars[idxB].get().lower()
        s2=self.sols[idxB].lower().replace(" ","",1)
        if globalWordSim(s1,s2)>75 and (self.strVars[idxB].get()!="" and self.strVars[idxB].get()!=" "):
            self.pts.set(str(int(self.pts.get())+self.posPts[idxB]))
            self.posPts[idxB]=0
            self.entries[idxB].config(bg=color["darkblue"],state='disabled')
            self.checkButtons[idxB].config(bg="#32b855",fg="#32b855")
            self.checkButtons[idxB]["state"]="disabled"
            
            for x in range(idxB*4,idxB*4+4):
                self.buttons[x].config(state='disabled')
            
            return True
        else:
            #self.checkButtons[idxB].config(bg="#ba1616",fg="#5c0f09")
            self.checkButtons[idxB].after(0, lambda: self.checkButtons[idxB].configure(bg="#ba1616",fg="#5c0f09"))
            self.checkButtons[idxB].after(500, lambda: self.checkButtons[idxB].configure(fg=color["darkblue"],anchor="center",bg=color["lightblue"]))
            self.strVars[idxB].set("")
        
        
    def checkFin(self):

            if globalWordSim(self.fin.get().lower(),self.res.lower().replace(" ","",1))>75:
                self.kon.config(bg=color["darkblue"],state='disabled')
                self.potv.config(bg="#32b855",fg="#32b855")
                self.potv["state"]="disabled"
                for element in self.buttons:
                    element['state']='disabled'
                for el in self.entries:
                    el.config(state='disabled')
                for e in self.checkButtons:
                    e['state']='disabled'
                self.pts.set(str(15+int(self.pts.get())+sum(self.posPts)))
                messagebox.showinfo("Победили сте!","Победили сте!")
            else:
                #self.potv.config(bg="#ba1616",fg="#5c0f09")
                self.potv.after(0, lambda: self.potv.configure(bg="#ba1616",fg="#5c0f09"))
                self.potv.after(500, lambda: self.potv.configure(fg=color["darkblue"],anchor="center",bg=color["lightblue"]))                
                self.fin.set("")
        
def main():
    x="slovak"
    y="slova"
    asoc=Asoc()
    
    
if __name__=="__main__":
    main()