import processQueries
from tkinter import *
from tkinter import ttk,messagebox
import json, os

textFont = "Conoslas"

class showRequests():
    def __init__(self):
        
        root = Tk()
        root.state('zoomed')

        queryObj = processQueries.displayQueries()

        Label(root,text='Queries List',font=(textFont,25),
        fg='black',bg='light blue').pack(side='top',expand=True)

        ButtonFrame = Frame(root,bg='white')
        ButtonFrame.pack(side='left',expand=True)

        b1 = Button(ButtonFrame,text='Approve all',command=lambda : 
        queryObj.approveAll(root,treeview,b1,b2,b3,b4)
        ,font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6')
        b1.grid(row=0,columnspan=2,padx=5,pady=10)

        b2 = Button(ButtonFrame,text='Approve selected',command=lambda : 
        queryObj.approveSelected(root,treeview,b1,b2,b3,b4)
        ,font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6')
        b2.grid(row=1,columnspan=2,padx=5,pady=10)

        b3 = Button(ButtonFrame,text='Deny all',command=lambda : 
        queryObj.denyAll(root,treeview,b1,b2,b3,b4)
        ,font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6')
        b3.grid(row=2,columnspan=2,padx=5,pady=10)

        b4 = Button(ButtonFrame,text='Deny selected',command=lambda : 
        queryObj.denySelected(treeview,b1,b2,b3,b4)
        ,font=(textFont,12),fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6')
        b4.grid(row=3,columnspan=2,padx=5,pady=10)

        Button(ButtonFrame,text=' < Go Back',command=root.destroy,font=(textFont,12),
        fg='white',bg='#36c2a6',activeforeground='white',activebackground='#36c2a6').grid(row=4,columnspan=2,padx=5,pady=10)

        frame2 = Frame(root)
        frame2.pack(side='bottom',expand=True)

        scrollbar = ttk.Scrollbar(frame2)
        scrollbar.pack(side='right',fill=Y)

        treeview = ttk.Treeview(frame2,yscrollcommand=scrollbar.set)
        treeview.pack(side='left')
        scrollbar.config(command=treeview.yview)

        style = ttk.Style()
        style.theme_use('alt')
        style.configure('Treeview.Heading',font=("Conoslas",15))
        style.configure('Treeview',font=('Conoslas',13),rowheight=130,foreground='black',fieldbackground='silver',background='white')
        style.map('Treeview',background=[('selected','#36c2a6')])

        treeview['columns'] = ('Roll no','Department','Username','Email','Phno','Address','Cgpa')

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

        data = queryObj.retrieveQueries(root,b1,b2,b3,b4)
        treeview.tag_configure('odd',background='light blue')
        treeview.tag_configure('even',background='white')
        if data != None:
            # print(data)
            for row in range(len(data)):
                if row%2 == 0:
                    treeview.insert(parent='',iid=row,index='end',values=(data[row][0],data[row][1],data[row][2],data[row][3],data[row][4],data[row][5],data[row][6]),tags=('even',))
                else:
                    treeview.insert(parent='',iid=row,index='end',values=(data[row][0],data[row][1],data[row][2],data[row][3],data[row][4],data[row][5],data[row][6]),tags=('odd',))

        root.mainloop()

