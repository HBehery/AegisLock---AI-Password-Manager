'''
AegisLock Password Manager
Name: Hamzah Behery 
'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import string
import random
from transformers import pipeline

pipe = pipeline("text-classification", model="DunnBC22/codebert-base-Password_Strength_Classifier")

#Globals

global serviceVar,usernameVar,passwordVar,serviceList,usernameList,passwordList,passScoreVar

#Functions

######SUBMIT######

def submit():
    global user,passwrd,serv,serviceVar,usernameVar,passwordVar
    user = usernameVar.get()
    passwrd = passwordVar.get()
    serv = serviceVar.get()

    setLabelsBlue()
    
    redWarningLabel()
    
    if user != "" and passwrd != "" and serv != "":
        submitCheck()
        
def removeAccount(account):
    serviceList.remove(serviceList[account])
    usernameList.remove(usernameList[account])
    passwordList.remove(passwordList[account])
    populate()

def populate():
    listServices.delete(0,tk.END)
    for i in serviceList:
        listServices.insert(serviceList.index(i),i)

def setLabelsBlue():
    usernameLabel.config(foreground = "#2a5e89")
    passwordLabel.config(foreground = "#2a5e89")
    serviceLabel.config(foreground = "#2a5e89")

def redWarningLabel():
    global user,passwrd,serv,serviceList,usernameList,passwordList
    
    if user == "" or user in usernameList and serv in serviceList:
        usernameLabel.config(foreground = "red")
    if passwrd == "":
        passwordLabel.config(foreground = "red")
    if serv == "" or serv in serviceList:
        serviceLabel.config(foreground = "red")
    if serv in serviceList and user in usernameList and passwrd in passwordList:
        serviceLabel.config(foreground = "red")
        usernameLabel.config(foreground = "red")
        passwordLabel.config(foreground = "red")

def appendAccount():
    global user,passwrd,serv,serviceList,usernameList,passwordList
    usernameList.append(user)
    serviceList.append(serv)
    passwordList.append(passwrd)

def messageBox():
    var = messagebox.askquestion("Duplicate Account", f'You already have an account with {serviceVar.get()}, would you like to overwrite it?', icon='warning')
    if var == "yes":
        indx = serviceList.index(serviceVar.get())

        appendAccount()
        
        removeAccount(indx)

        serviceLabel.config(foreground = "#2a5e89")
        listServices.bind('<Double-Button-1>', retrieve)
        populate()

    elif var == "no":
        pass

def submitCheck():
    global user,serv,serviceList,usernameList
    if serv in serviceList and user not in usernameList:
        messageBox()
    elif user in usernameList and serv in serviceList:
        pass
    else:
        listServices.bind('<Double-Button-1>', retrieve)
        appendAccount() 
        populate()

######RETRIEVE######

def retrieve(event):
    global serviceList
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])

    retrieveIndex = serviceList.index(value)
    
    updateAccountLabels(retrieveIndex)

def updateAccountLabels(retrieveIndex):
    global serviceVar,usernameVar,passwordVar,serviceList,usernameList,passwordList
    serviceVar.set(serviceList[retrieveIndex])
    usernameVar.set(usernameList[retrieveIndex])
    passwordVar.set(passwordList[retrieveIndex])
    
######SCORE######

def score():
    global passScoreVar
    if pipe(passScoreVar.get())[0]['label'] == 'LABEL_0':
        percentageLabel.config(text = "Strength: WEAK")
    elif pipe(passScoreVar.get())[0]['label'] == 'LABEL_1':
        percentageLabel.config(text = "Strength: MEDIUM")
    elif pipe(passScoreVar.get())[0]['label'] == 'LABEL_2':
        percentageLabel.config(text = "Strength: STRONG")
    else:
        percentageLabel.config(text = "Strength: Try Again")


def determineScore(password):
    
    passLabel = pipe(password)[0]['label']
    print(passLabel)
    return passLabel

def length(password):
    length= len(password)
    if length >= 10:
        points = 50
    elif length < 10:
        points = length * 5
    
    return points

def uppercase(password):
    uPoints = 0
    uLetters = 0
    
    for char in password:
        if char in string.ascii_uppercase:
            uLetters+=1
            
    uppercasePercent = calculateUppercasePercent(uLetters,password, base = 10)
    
    if uppercasePercent > 50:
        uPoints += 100 - uppercasePercent
    elif uppercasePercent <= 50:
        uPoints += uppercasePercent

    return uPoints

def calculateUppercasePercent(uLetters,password,base = 10):
    lengthPercent = len(password)
    percent = 100*(uLetters/lengthPercent)
    return int(base * round((percent)/base))

def consecutive(password):
    consecCounter = 0

    for i in range(0, len(password)-1):
        if password[i] == password[i+1]:
            consecCounter+= 0.1
            
    if consecCounter > 1:
        consecCounter = 1
    
    return consecCounter

######GENERATE######

def generate():
    chars = '0123456789abcdefghijklmnopqrstuvwxyz!"#$%&\'()*+,-./:;?@[\\]^_`{|}~'
    generatedList = []
    
    generatedPass = generatePassword(generatedList, chars)
    generatedResult = ruleCheck(generatedPass)

    if generatedResult == False:
        generate()
    else:
        passGenLabel.config(text = f'Password: {generatedPass}')
        if generatedResult == 'LABEL_1':
            genStrengthLabel.config(text = "Password Strength: MEDIUM")
        else:
            genStrengthLabel.config(text = "Password Strength: STRONG")

        
def generatePassword(generatedList, chars):
    for i in range(6):
        generatedList.append(random.choice(chars))
        generatedList.append(random.choice(string.ascii_uppercase))
            
    generatedPass = ''.join(generatedList)
        
    return generatedPass

def ruleCheck(generatedPass):
    scoreLabel = determineScore(generatedPass)
    if scoreLabel == 'LABEL_1' or scoreLabel == "LABEL_2":
        return scoreLabel
    else:
        return False
  
#Mainframe
root = tk.Tk()
root.config(background='#ffce99')
root.resizable(False,False)

mainframe = tk.Frame(root)
mainframe.config(background='#ffe6cc')

serviceList = []
usernameList = []
passwordList = []

titleLabel = ttk.Label(mainframe,text = "AegisLock Password Manager", font=('Courier', 25))
subTitleLabel = ttk.Label(mainframe,text = "Keeping Your Information Safe.", style = 'sub.TLabel')

    #STORE
storeFrame= ttk.Frame(mainframe, style = 'yellow.Label',width=400,height=400)
storeFrame.grid_propagate(False)
storeLabel= ttk.Label(storeFrame,text = "Store an Account",style='frame.TLabel')

serviceLabel = ttk.Label(storeFrame,text = "Service:* ", style = 'frameSub.TLabel')
serviceVar = tk.StringVar()
serviceVar.set("")
serviceEntry = ttk.Entry(storeFrame, textvariable = serviceVar, width = 17, font=('Courier',18))


usernameLabel = ttk.Label(storeFrame,text = "Username:*", style = 'frameSub.TLabel')
usernameVar = tk.StringVar()
usernameVar.set("")
usernameEntry = ttk.Entry(storeFrame, textvariable = usernameVar, width = 17, font=('Courier',18))

passwordLabel = ttk.Label(storeFrame,text = "Password:*", style = 'frameSub.TLabel')
passwordVar = tk.StringVar()
passwordVar.set("")
passwordEntry = ttk.Entry(storeFrame, textvariable =passwordVar, width = 17, font=('Courier',18))

requiredLabel = ttk.Label(storeFrame,text = "* = Required Field", style = 'frameSub.TLabel',foreground="red4")
submitButton = ttk.Button(storeFrame,  text="Submit",command = submit)

    #RETRIEVE
retrieveFrame= ttk.Frame(mainframe, style = 'yellow.Label',width=400,height=400)
retrieveFrame.grid_propagate(False)
retrieveLabel= ttk.Label(retrieveFrame,text = "Retrieve an Account",style='frame.TLabel')
choiceLabel = ttk.Label(retrieveFrame,text = "Choose a Service: ", style = 'frameSub.TLabel')
scrollbar = tk.Scrollbar(retrieveFrame)
listServices = tk.Listbox(retrieveFrame,yscrollcommand=scrollbar.set,height=10,width=60, background="#ffffff",borderwidth=0, foreground="#2a5e89",font=('Courier', 18))
scrollbar.config(command=listServices.yview) 

    #SCORE
scoreFrame= ttk.Frame(mainframe, style = 'yellow.Label',width=400,height=400)
scoreFrame.grid_propagate(False)
scoreLabel= ttk.Label(scoreFrame,text = "AI Password Score",style='frame.TLabel')
basedLabel = ttk.Label(scoreFrame,text = "Based On: ", style = 'frameSub.TLabel')
lengthLabel = ttk.Label(scoreFrame,text = "  -Length of Password ", style = 'frameSub.TLabel')
uppercaseLabel = ttk.Label(scoreFrame,text = "  -# of UpperCase Letters", style = 'frameSub.TLabel')
consecutiveLabel = ttk.Label(scoreFrame,text = "  -# of Consecutive Letters", style = 'frameSub.TLabel')
passScoreLabel = ttk.Label(scoreFrame,text = "Password:", style = 'frameSub.TLabel')
passScoreVar = tk.StringVar()
passScoreEntry = ttk.Entry(scoreFrame, textvariable =passScoreVar, width = 17, font=('Courier',18))
scoreButton = ttk.Button(scoreFrame,  text="Score",command = score)
percentageLabel = ttk.Label(scoreFrame,text = "", style = 'frameSub.TLabel')

    #GENERATE
genFrame= ttk.Frame(mainframe, style = 'yellow.Label',width=400,height=400)
genFrame.grid_propagate(False)
genLabel= ttk.Label(genFrame,text = " AI Password Generator",style='frame.TLabel')
basedGenLabel = ttk.Label(genFrame,text = "Recommended Values: ", style = 'frameSub.TLabel')
lengthGenLabel = ttk.Label(genFrame,text = " -10+ Character Length", style = 'frameSub.TLabel')
uppercaseGenLabel = ttk.Label(genFrame,text = " -Symbols, Different Casing", style = 'frameSub.TLabel')
consecutiveGenLabel = ttk.Label(genFrame,text = " -No Consecutive Letters", style = 'frameSub.TLabel')
passGenLabel = ttk.Label(genFrame,text = "Password:", style = 'frameSub.TLabel')
genStrengthLabel = ttk.Label(genFrame,text = "Password Strength:", style = 'frameSub.TLabel')
genButton = ttk.Button(genFrame,  text="Generate",command = generate)

#Styles
styleLabel = ttk.Style()
styleLabel.configure('TLabel', foreground="#12283a", font=('Courier', 22), background='#ffe6cc')
styleLabel.configure('sub.TLabel', foreground="#2a5e89", font=('Courier', 16))
styleLabel.configure('frame.TLabel', font=('Courier', 22),background='#fff3e6')
styleLabel.configure('frameSub.TLabel', foreground="#2a5e89",font=('Courier', 18),background='#fff3e6')

sLabelFrame = ttk.Style()
sLabelFrame.configure('Label', background = '#fff3e6')

styleButton = ttk.Style()
styleButton.configure('TButton', foreground="red4", font=('Courier', 19))

#Gridding Widgets
mainframe.grid(padx = 10, pady = 10)

    #Mainframe
titleLabel.grid(row=1, column=1, columnspan=3,pady=5)
subTitleLabel.grid(row=2, column=1, columnspan=3,pady=5)

    #Store
storeFrame.grid(row=3, column=1,padx=5,pady=5)
storeLabel.grid(row=1, column=1, columnspan=3,pady=5)

serviceLabel.grid(row=2,column=1,pady=20,sticky=tk.W)
serviceEntry.grid(row=2,column=3,pady=20)

usernameLabel.grid(row=3,column=1,pady=20,sticky=tk.W)
usernameEntry.grid(row=3,column=3,pady=20)

passwordLabel.grid(row=4,column=1,pady=20,sticky=tk.W)
passwordEntry.grid(row=4,column=3,pady=20)

requiredLabel.grid(row=5,column=1,pady=12,sticky=tk.W,columnspan=3)
submitButton.grid(row=6,column=1,pady=12,columnspan=3)

        #Retrieve
retrieveFrame.grid(row=3, column=3,padx=5,pady=5)
retrieveLabel.grid(row=1, column=1, columnspan=3,pady=5,padx=5)
choiceLabel.grid(row=2, column =1,padx=5, columnspan=3)
scrollbar.grid(row=3,rowspan=3,column=1, sticky=(tk.W ,tk.N,tk.S ))
listServices.grid(row=3,column=3, sticky=(tk.N,tk.S),rowspan=3,columnspan=2)


        #Score
scoreFrame.grid(row=4, column=1,padx=5,pady=5)
scoreLabel.grid(row=1, column=1, columnspan=3,pady=5)
basedLabel.grid(row=2,column=1,pady=10,sticky=tk.W)
lengthLabel.grid(row=3,column=1,pady=10,sticky=tk.W,columnspan = 3)
uppercaseLabel.grid(row=4,column=1,pady=10,sticky=tk.W,columnspan = 3)
consecutiveLabel.grid(row=5,column=1,pady=10,sticky=tk.W,columnspan = 3)
passScoreLabel.grid(row=6,column=1,pady=20,sticky=tk.W)
passScoreEntry.grid(row=6,column=3,pady=20)
scoreButton.grid(row=7,column=1,pady=12,sticky=tk.W,columnspan = 3)
percentageLabel.grid(row=7, column=3,pady=12,sticky=tk.E)

        #Generate
genFrame.grid(row=4, column=3,padx=5,pady=5)
genLabel.grid(row=1, column=1,columnspan = 3,pady=5)
basedGenLabel.grid(row=2,column=1,pady=10,sticky=tk.W)
lengthGenLabel.grid(row=3,column=1,pady=10,sticky=tk.W,columnspan = 3)
uppercaseGenLabel.grid(row=4,column=1,pady=10,sticky=tk.W,columnspan = 3)
genButton.grid(row=5,column=1,pady=20,columnspan = 3)
genStrengthLabel.grid(row=6,column=1,pady=10,sticky=tk.W,columnspan = 3)
passGenLabel.grid(row=7,column=1,pady=20,sticky=tk.W,columnspan=3)

root.mainloop()
