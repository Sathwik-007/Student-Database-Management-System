from tkinter import *
from tkinter import messagebox, filedialog, ttk
import json, os
from tabulate import tabulate
from PIL import Image, ImageTk
import adminInterface, showQueries


textFont = 'Conoslas' # Choose your favourite font
usersJSON = 'users.json'
class adminHome():

    def setWindowGeometry(self,window):
        window_width = 600
        window_height = 600

        screen_height = window.winfo_screenheight()
        screen_width = window.winfo_screenwidth()

        x = int(screen_height/2 - window_height/2)
        y = int(screen_width/2 - window_width/2)

        return ('{}x{}+{}+{}'.format(window_height,window_width,y,x))

    def __init__(self):

        root = Tk()
        root.title('Admin Menu')
        frame = Frame(root,bg='#7044b8')
        
        root.geometry(self.setWindowGeometry(root))

        Button(frame,text='View student details by rollno',
        command=lambda: self.viewByRollno()
        ,font=(textFont,12)).grid(row=0,columnspan=2,padx=5,pady=10)

        Button(frame,text='View student details by department',
        command=lambda: self.viewByDepartment()
        ,font=(textFont,12)).grid(row=1,columnspan=2,padx=5,pady=10)

        Button(frame,text='View students details cgpa',
        command=lambda : self.viewByCgpa()
        ,font=(textFont,12)).grid(row=2,columnspan=2,padx=5,pady=10)

        Button(frame,text='Update student details',
        command=lambda : self.updateDetailsQueries(root)
        ,font=(textFont,12)).grid(row=3,columnspan=2,padx=5,pady=10)

        Button(frame,text='Back to Admin main Page',command= lambda: self.back(root),
        font=(textFont,12)).grid(row=4,columnspan=2,padx=5,pady=10)

        frame.pack(expand=True)

        root.mainloop()

    def back(self,root):
        root.destroy()
        restartAdminapp = adminInterface.adminSignIn()
        try:
            if len(adminInterface.adUsrname) != 0 and len(adminInterface.adPswrd) != 0:
                print('launching admin menu')
                menu = adminHome()
        except AttributeError:
            print("Application closed")

    def retrieveData(self,entry,field):
        with open(usersJSON,'r') as file:
            x = json.load(file)
            d = x['users']
        
            data = []
           # capturePic=[]

            for i in d:
                if field == 'Roll no' and i[field] == entry:
                    data.append(list(i.values()))
                    break
                if field == 'Cgpa' and int(i[field]) >= int(entry):
                    data.append(list(i.values()))
                else:
                    if i[field] == entry:
                        data.append(list(i.values()))
   
            data.sort(key=lambda a: int(a[len(a)-2]),reverse=True) # sorts data according to cgpa
            for i in data:
                i.remove(i[3]) # removes password
                # capturePic.append(i[7])
                i.remove(i[7]) # removes profile_pic location
            
            # table = tabulate(data, headers=['Roll no','Department','Username','Email ID','Phno','Address','Cgpa'],
            #     tablefmt='pretty')
            # print(data)
            del d            
            return data

    def dataByRollno(self,window,treeview,entry,field):
        
        for i in treeview.get_children():
            treeview.delete(i)
        
        value = self.retrieveData(entry, field)

        treeview.insert(parent='',index='end',iid=0,values=(value[0][0],value[0][1],value[0][2],value[0][3],value[0][4],value[0][5],value[0][6]))
        
        window.state('zoomed')
    

    def viewByRollno(self):
        window = Toplevel()
        window.title('')
        window.state('zoomed')
        # window.geometry(self.setWindowGeometry(window))
        
        mainFrame = Frame(window,bg='#c95b5b')

        frame1 = Frame(mainFrame)
        
        chooseRollno = Entry(frame1,font=(textFont,12))
        chooseRollno.grid(row=0,columnspan=2,padx=5,pady=10)
  
        searchBtn = Button(frame1,font=(textFont,12),
        command=lambda : self.dataByRollno(window,treeview,
        chooseRollno.get().upper(),field='Roll no')
        ,text='search',bg='#36c2a6',activebackground='#36c2a6',fg='white',activeforeground='white')
        searchBtn.grid(row=1,columnspan=2,padx=5,pady=10)

        Button(frame1,text='< Back',font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6',
        command=window.destroy).grid(row=2,columnspan=2,
        padx=5,pady=15)
        
        frame1.grid(row=0,columnspan=2,padx=5,pady=10)

        frame2 = Frame(mainFrame,bg='#c95b5b')
        
        # displayPic = Label(frame2,font=(textFont,12),bg='light green',relief=RIDGE,bd=5)
        # displayPic.grid(row=0,columnspan=2,pady=10)
        
        treeview = ttk.Treeview(frame2,selectmode='none')
        treeview.grid(row=1,columnspan=2,pady=10)

        treeview['columns'] = ('Roll no','Department','Username','Email','Phno','Address','Cgpa')
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview.Heading',font=("Conoslas",15))
        style.configure('Treeview',font=('Conoslas',13),rowheight=140,background='white',foreground='black',fieldbackground='silver')

        treeview.column('#0', width=0,stretch=NO)
        treeview.column('Roll no',anchor=W,width=120)
        treeview.column('Department',anchor=W,width=170)
        treeview.column('Username',anchor=W,width=160)
        treeview.column('Email',anchor=W,width=280)
        treeview.column('Phno',anchor=W,width=140)
        treeview.column('Address',anchor=W,width=240)
        treeview.column('Cgpa',anchor=W,width=80)
        
        treeview.heading('#0',anchor=W,text='')
        treeview.heading('Roll no',anchor=W,text='Roll no')
        treeview.heading('Department',anchor=W,text='Department')
        treeview.heading('Username',anchor=W,text='Username')
        treeview.heading('Email',anchor=W,text='Email')
        treeview.heading('Phno',anchor=W,text='Phno')
        treeview.heading('Address',anchor=W,text='Address')
        treeview.heading('Cgpa',anchor=W,text='Cgpa')
        
        frame2.grid(row=1,columnspan=2,padx=5,pady=10)

        mainFrame.pack(expand=True)

        window.mainloop()

    def dataByOtherFields(self,window,secondFrame,entry,field,fieldbg):
        
        for widget in secondFrame.winfo_children():
            widget.destroy()
        
        window.state('zoomed')

        scrollbar = ttk.Scrollbar(secondFrame)
        scrollbar.pack(side='right',fill=Y)

        treeview = ttk.Treeview(secondFrame,selectmode='none',yscrollcommand=scrollbar.set)
        scrollbar.config(command=treeview.yview)
        treeview.pack(side='left')

        treeview['columns'] = ('Roll no','Department','Username','Email','Phno','Address','Cgpa')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.map('Treeview',background=[('selected','light blue')])
        style.configure('Treeview.Heading',font=("Conoslas",15))
        style.configure('Treeview',font=('Conoslas',13),rowheight=140,foreground='black',background='white',fieldbackground='silver')

        treeview.column('#0', width=0,stretch=NO)
        treeview.column('Roll no',anchor=W,width=120)
        treeview.column('Department',anchor=W,width=170)
        treeview.column('Username',anchor=W,width=160)
        treeview.column('Email',anchor=W,width=280)
        treeview.column('Phno',anchor=W,width=140)
        treeview.column('Address',anchor=W,width=240)
        treeview.column('Cgpa',anchor=W,width=80)

        treeview.heading('#0',anchor=W,text='')
        treeview.heading('Roll no',anchor=W,text='Roll no')
        treeview.heading('Department',anchor=W,text='Department')
        treeview.heading('Username',anchor=W,text='Username')
        treeview.heading('Email',anchor=W,text='Email')
        treeview.heading('Phno',anchor=W,text='Phno')
        treeview.heading('Address',anchor=W,text='Address')
        treeview.heading('Cgpa',anchor=W,text='Cgpa')

        rowData = self.retrieveData(entry, field)
        
        treeview.tag_configure('odd',background=fieldbg)
        treeview.tag_configure('even',background='white')

        for i in range(len(rowData)):
            if i%2 == 0:
                treeview.insert(parent='',index='end',iid=i,values=(rowData[i][0],rowData[i][1],rowData[i][2],rowData[i][3],rowData[i][4],rowData[i][5],rowData[i][6]),tags=('even',))
            else:
                treeview.insert(parent='',index='end',iid=i,values=(rowData[i][0],rowData[i][1],rowData[i][2],rowData[i][3],rowData[i][4],rowData[i][5],rowData[i][6]),tags=('odd',))
        
    def viewByDepartment(self):

        window = Toplevel()
        window.title('')
        window.geometry(self.setWindowGeometry(window))

        mainFrame = Frame(window,bg='#9dc236')
        mainFrame.pack(side='top',expand=True)

        # firstFrame = Frame(mainFrame,bg='#9dc236')
        # firstFrame.pack(side='top')

        branchEntry = Entry(mainFrame,font=(textFont,12))
        branchEntry.grid(row=0,columnspan=2,padx=5,pady=10)
  
        searchBtn = Button(mainFrame,font=(textFont,12),
        command=lambda : self.dataByOtherFields(window,secondFrame
        ,branchEntry.get().upper(),field='Department',fieldbg='#d5ed91'),text='search',fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6'
            )

        searchBtn.grid(row=1,columnspan=2,padx=5,pady=12)

        Button(mainFrame,text='< Back',font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6',
        command=window.destroy).grid(row=2,columnspan=2,padx=5,pady=12)

        secondFrame = Frame(window)
        secondFrame.pack(side='bottom')

        window.mainloop()

    def viewByCgpa(self):

        window = Toplevel()
        window.title('')
        window.geometry(self.setWindowGeometry(window))

        mainFrame = Frame(window)
        mainFrame.pack(expand=True)

        firstFrame = Frame(mainFrame,bg='#ca36c0')
        firstFrame.pack(side='top',expand=True)

        cgpaEntry = Entry(firstFrame,font=(textFont,12))
        cgpaEntry.grid(row=0,columnspan=2,padx=5,pady=10)
  
        searchBtn = Button(firstFrame,font=(textFont,12),
        command=lambda : self.dataByOtherFields(window,secondFrame,
        cgpaEntry.get().upper(),
        field='Cgpa',fieldbg='#f2a5ed'),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6',text='search')

        searchBtn.grid(row=1,columnspan=2,padx=5,pady=12)

        Button(firstFrame,text='< Back',font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6',
        command=window.destroy).grid(row=2,columnspan=2,padx=5,pady=12)

        secondFrame = Frame(window)
        secondFrame.pack(side='bottom')

        window.mainloop()
       
    def updateDetailsQueries(self,root):
        root.destroy()
        obj = showQueries.showRequests()
        restart = adminHome()
        