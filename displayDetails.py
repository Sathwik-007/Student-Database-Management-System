from tkinter import *
from tkinter import ttk
import userRoot
import json, os
from tabulate import tabulate
from PIL import Image, ImageTk

#textFont = 'JetBrains Mono' # => My fav font ;)
textFont = 'Conoslas'

global queriesJSON
queriesJSON = 'queries.json'

class showUserInfo():

    def windowGeometry(self,frame,page):

        window_width = 1360
        window_height = 700

        screen_width = page.winfo_screenwidth()
        screen_height = page.winfo_screenheight()

        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)

        return ('{}x{}+{}+{}'.format(window_width,window_height,x,y))

    def __init__(self,createUsr):
        # retrieves currently logged in user data and displays details in a sep window
        if len(userRoot.a) and len(userRoot.b) != 0:
            rollnum = userRoot.a
            password = userRoot.b
            data={}
            with open(userRoot.usersJSON,'r') as file:
                x = json.load(file)
                d = x['users']
                flag = False
                for i in d:
                    if rollnum in i.values() and password in i.values():
                        data.update(i)
                        break
            table = []
            displayProfilePic = ''
            
            for k in data.items():
                if k[0] == 'profile_pic':
                    displayProfilePic = k[1]
                elif k[0] != 'Password':
                    table.append(k[1])
            
            root = Tk()

            frame = Frame(root,bg='#b03e4b')
            root.state('zoomed')

            Label(frame,font=(textFont,20),text='User Data').grid(row=0,columnspan=2,padx=5,pady=10)

            innerFrame = Frame(frame)

            # ResiIng profile pic 
            pic = Image.open(displayProfilePic)
                                    # breadth,height
            resizedPic = pic.resize((125,150), Image.ANTIALIAS)

            newPic = ImageTk.PhotoImage(resizedPic)

            insideInnerFrame = Frame(innerFrame)

            imageLabel = Label(insideInnerFrame,image=newPic,relief=RIDGE,bd=10,padx=5,pady=10)
            imageLabel.pack(anchor=NE)

            treeview = ttk.Treeview(insideInnerFrame,selectmode='none')
            style = ttk.Style()
            style.configure('Treeview.Heading',font=('Conoslas',15))
            style.configure('Treeview',rowheight=30,font=('Conoslas',13),height=10)
            treeview['columns'] = ("Roll no","Department","Username","Email","Phno","Address","Cgpa")
            
            treeview.column("#0",width=0,anchor=W,stretch=NO)
            treeview.column("Roll no",anchor=W,width=120)
            treeview.column("Department",anchor=W,width=170)
            treeview.column("Username",anchor=W,width=160)
            treeview.column("Email",anchor=W,width=280)
            treeview.column("Phno",anchor=W,width=140)
            treeview.column("Address",anchor=W,width=240)
            treeview.column("Cgpa",anchor=W,width=80)

            treeview.heading("#0",text='',anchor=W)
            treeview.heading("Roll no",text='ROLL NO',anchor=W)
            treeview.heading("Department",text='DEPARTMENT',anchor=W)
            treeview.heading("Username",text='USERNAME',anchor=W)
            treeview.heading("Email",text='EMAIL',anchor=W)
            treeview.heading("Phno",text='PHNO',anchor=W)
            treeview.heading("Address",text='ADDRESS',anchor=W)
            treeview.heading("Cgpa",text='CGPA',anchor=W)

            treeview.insert(parent='',index='end',iid=1,values=(table[0],table[1],table[2],table[3],table[4],table[5],table[6]))
            treeview.pack(anchor=S)

            insideInnerFrame.grid(row=0,columnspan=2)
            innerFrame.grid(row=1,columnspan=2,padx=5,pady=10)

            Label(frame,text='Want to update details? \nclick on the update details button below to request admin to modify data',
            font=(textFont,12),bg='light pink').grid(row=2,columnspan=2,padx=5,pady=10)

            updateDetailsBtn = Button(frame,font=(textFont,12),bd=5,fg='white',activebackground='#e84f4f',bg='#e84f4f',activeforeground='white'
                            ,text='Update details',command=lambda : self.updateDetails(createUsr,root))
            updateDetailsBtn.grid(row=3,columnspan=2,pady=10)

            backToHome = Button(frame,font=(textFont,12),bd=5,fg='white',activebackground='#e84f4f',bg='#e84f4f',activeforeground='white',
                            text='Go back to Home',command=lambda: self.backToHomePage(root))
            backToHome.grid(row=4,columnspan=2,pady=15)

            frame.pack(expand=True)

            root.mainloop()    

    def backToHomePage(self,root):
        userRoot.a = ''
        userRoot.b = ''
        root.destroy()
        restartApp = userRoot.signIn()
        restartApp.signInWindow()
  
        restartDisplayProcess = showUserInfo(createUsr=False)
        

    def updateDetails(self,createUsr,root):
        
        try:
            file = open(queriesJSON,'r')
            if os.path.getsize(queriesJSON) == 0:
                print('file size is 0. Hence writing into file')
                with open(queriesJSON,'w') as fhand:
                    d = {"requests":[]}
                    json.dump(d,fhand,indent=4)
            file.close()
        except FileNotFoundError:
            with open(queriesJSON,'w') as fhand:
                d = {"requests":[]}
                json.dump(d,fhand,indent=4)
        d = dict()
      
        obj = userRoot.signIn()
        obj.register(createUsr= False,windowLabel='Update Information',windowBg='#db9625',
                        windowBtn='Send request to admin',windowLabelBg='#db9625')