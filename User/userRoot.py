from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog, ttk
import AuthenticateDetails
import os, json

global rollNumberEntry,password_entry, a, b, profile_pic_path, signInRollNoEntry

global sign_in_username_entry,sign_in_password_entry,sign_up_retype_password_entry
global email_entry, phno_entry, address_text, cgpa_entry, profile_pic_path
global departmentEntry

global new_window


global usersJSON
global textFont

usersJSON = 'users.json'
#textFont = 'JetBrains Mono'
textFont = 'Conoslas'

class signIn():

    def windowGeometry(self,page):

        window_width = 600
        window_height = 600

        screen_width = page.winfo_screenwidth()
        screen_height = page.winfo_screenheight()

        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)

        return ('{}x{}+{}+{}'.format(window_height,window_width,x,y))

    def ifFileEmpty(self):

        with open(usersJSON,'w') as file:
            d = {"users":[]}
            json.dump(d,file,indent=4)
            rollNumberEntry.delete(0,END)
            password_entry.delete(0,END)
            fileNotExistFlag = True


    def upload_pic(self):
        
        global profile_pic_path
        
        profile_pic_path = filedialog.askopenfilename(parent=new_window,
                    filetypes=(('PNG files','*.png'),
                    ('JPEG file',"*.jpg")))
       
    def submit(self,usr,pw,createUsr):

        global rollNumberEntry,password_entry
        global window
        global a,b
    
        if len(usr) == 0:
            messagebox.showinfo(parent=window,title='Insufficient details',message='Username cant be empty')
        elif len(pw) == 0:
            messagebox.showinfo(parent=window,title='Insufficient details',message='Password cant be empty')
        
        else:
            fileNotExistFlag = False
            try:
                file = open(usersJSON,'r')
                file.close()
                
            except FileNotFoundError : 
                self.ifFileEmpty()
                
            if not fileNotExistFlag: 
                if os.path.getsize(usersJSON) == 0:
                    messagebox.showerror(parent=window,title='file empty',message='No user registered yet!. Please register and then try logging in')
                    rollNumberEntry.delete(0,END)
                    password_entry.delete(0,END)
                    self.ifFileEmpty()

                else:
                    with open(usersJSON,'r') as file:
                        
                        x = json.load(file)
                        d = x['users']

                        a = usr
                        b = pw
                        
                        if len(d) == 0:
                            messagebox.showerror(parent=window,title='File empty',message='No user registered yet! Please register to continue logging in')
                            rollNumberEntry.delete(0,END)
                            password_entry.delete(0,END)
                        else:
                            flag = False

                            for i in d:
                                if a == i['Roll no'] and b == i['Password']:
                                    flag=True
                                    break
                            
                            if flag:
                                messagebox.showinfo(parent=window,title='logged in ',message='User logged in successfully')
                                window.destroy()
                            elif not flag:
                                messagebox.showerror(parent=window,title='details doesnt exist',message='User not found. Please register')
                                rollNumberEntry.delete(0,END)
                                password_entry.delete(0,END)
                        
    def authenticate(self,createUsr):
        rollno = signInRollNoEntry.get().upper()
        dept = departmentEntry.get().upper()
        usr = sign_in_username_entry.get()
        if createUsr:
            pw = sign_in_password_entry.get()
            retype_pw = sign_up_retype_password_entry.get()
        email = email_entry.get()
        phno = phno_entry.get()
        addr = address_text.get('1.0',END)
        cgpa = cgpa_entry.get()
        pic = profile_pic_path

        if len(phno) == 0:
            messagebox.showwarning(parent=new_window,title='Invalid entry type',message='Phonenumber cannot be NULL.')
        else:
            if createUsr:
                try:
                    file = open(usersJSON,'r')
                    if os.path.getsize(usersJSON) == 0:
                        with open(usersJSON,'w') as f:
                            d = {"users":[]}
                            json.dump(d,f,indent=4)
                    file.close()
                except FileNotFoundError:
                    with open(usersJSON,'w') as fhand:
                        d = {"users":[]}
                        json.dump(d,fhand,indent=4)

        # check if every field is entered here itself
            if len(pic) == 0:
                messagebox.showwarning(parent=new_window,title='Choose photo',message='Please upload a profile picture by clicking on choose file button.')
            
            elif createUsr == False and (len(rollno) == 0 or len(dept) == 0 or len(usr) == 0 or len(email) == 0 or len(phno) == 0 or len(addr) == 0 or len(cgpa) == 0):
                messagebox.showerror(parent=new_window,title='Insufficient Data',message='All fields are required')
             
            elif createUsr == True and (len(rollno) == 0 or len(dept) == 0 or len(usr) == 0 or len(pw) == 0 or len(retype_pw) == 0 or len(email) == 0 or len(phno) == 0 or len(addr) == 0 or len(cgpa) == 0):
                messagebox.showerror(parent=new_window,title='Insufficient Data',message='All fields are required')

            elif createUsr and (len(pw) < 8 or len(pw) > 15):
                messagebox.showwarning(parent=new_window,title='Constraint',message='Password must contain minimum 8 characters and maximum of 15 characters')   
    
            elif createUsr and pw != retype_pw:
                messagebox.showerror(parent=new_window,title='Data Mismatch',message='Password and retype password are not same') 

            elif not phno.isdigit():
                messagebox.showwarning(parent=new_window,title='Inavlid entry',message='Phonenumber cannot contain alphanumeric characters or special symbols !')
            
            else:
                check = AuthenticateDetails.Validate() # guess it should be init method
                if createUsr:
                    l = [rollno,dept,usr,pw,email,phno,addr,cgpa,pic]

                elif not createUsr:
                    l = [rollno,dept,usr,email,phno,addr,cgpa,pic]

                check.checkEntries(createUsr,l)

                if check.dontOpenOtpWindow == False:
                    check.sendOtp(phno,rollno,createUsr,resetPw=False) # might need rollnoEntry sring as positional arg

    def resetPassword(self):
        global rollNumberEntry
        argRollNo = rollNumberEntry.get().upper()
        if len(argRollNo) == 0:
            messagebox.showerror(title='Empty entry',message='Roll number cannot be empty. Please enter roll no and then proceed.')
        else:
            capturePhno = ''
            try:
                file = open(usersJSON,'r')
                if os.path.getsize(usersJSON) == 0:
                    messagebox.showerror(title='File empty',message='Cannot reset password. No user registered yet. Please register and then try logging in')
                else:
                    x = json.load(file)
                    d = x['users']
                    for i in d:
                        if i['Roll no'] == argRollNo:
                            capturePhno = i['Phno']
                            break
                file.close()
            except FileNotFoundError:
                messagebox.showerror(title='File not found',message='No user registered yet. Please register and then try logging in.')
                

            frgtPw = AuthenticateDetails.Validate()
            frgtPw.sendOtp(capturePhno,argRollNo,createUsr=False,resetPw=True)


    def register(self,createUsr,windowLabel,windowBg,windowBtn,windowLabelBg):
        global new_window

        global sign_in_username_entry,sign_in_password_entry,sign_up_retype_password_entry
        global email_entry, phno_entry, address_text, cgpa_entry, profile_pic_path,signInRollNoEntry
        global departmentEntry

        global rollNumberEntry,password_entry

        if createUsr:
            rollNumberEntry.delete(0,END)
            password_entry.delete(0,END)

        profile_pic_path = ''
        new_window = Toplevel()
        new_window.geometry(self.windowGeometry(new_window))
        new_window.config(bg='light blue')

        new_frame = Frame(new_window,bd=10,relief=GROOVE)

        canvas = Canvas(new_frame,height=600,width=410)
        canvas.pack(side='left',expand=True)

        scrollbar = ttk.Scrollbar(new_frame,command = canvas.yview,orient=VERTICAL)
        scrollbar.pack(side='right',fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>',lambda e : canvas.configure(scrollregion=canvas.bbox('all')))

        secondFrame = Frame(canvas)
        canvas.create_window((0,0),window=secondFrame,anchor=NW)

        new_win_sign_in = Label(secondFrame,text=windowLabel,
                    font=(textFont,20,'bold'))
        new_win_sign_in.grid(row=0,columnspan=2,padx=5,pady=10)

        rollNo = Label(secondFrame,text='Roll No:',font=(textFont,12))
        rollNo.grid(row=1,column=0,padx=5,pady=10)

        signInRollNoEntry = Entry(secondFrame,font=(textFont,12),width=30)
        signInRollNoEntry.grid(row=1,column=1,padx=5,pady=10)

        Label(secondFrame,text='Department:',font=(textFont,12)).grid(row=2,column=0,padx=5,pady=10)

        departmentEntry = Entry(secondFrame,font=(textFont,12),width=30)
        departmentEntry.grid(row=2,column=1,padx=5,pady=10)

        sign_in_username = Label(secondFrame,text="Username:",font=(textFont,12))
        sign_in_username.grid(row=3,column=0,padx=5,pady=10)

        sign_in_username_entry = Entry(secondFrame,font=(textFont,12),width=30)
        sign_in_username_entry.grid(row=3,column=1,padx=5,pady=10)

        if createUsr:
            sign_up_password = Label(secondFrame,text="Password:",font=(textFont,12),)
            sign_up_password.grid(row=4,column=0,padx=5,pady=10)

            sign_in_password_entry = Entry(secondFrame,font=(textFont,12),width=30,
                                    show='*')
            sign_in_password_entry.grid(row=4,column=1,padx=5,pady=10)

            sign_up_retype_password = Label(secondFrame,text="Retype-password:",font=(textFont,12))
            sign_up_retype_password.grid(row=5,column=0,padx=5,pady=10)

            sign_up_retype_password_entry = Entry(secondFrame,font=(textFont,12),
                                            width=30,show='*')
            sign_up_retype_password_entry.grid(row=5,column=1,padx=5,pady=10)

        email_label = Label(secondFrame,text='Email: ',font=(textFont,12))
        email_label.grid(row=6,column=0,padx=5,pady=10)

        email_entry = Entry(secondFrame,font=(textFont,12),width=30)
        email_entry.grid(row=6,column=1,padx=5,pady=10)

        phno_label = Label(secondFrame,text='Contact: ',font=(textFont,12))
        phno_label.grid(row=7,column=0,padx=5,pady=10)

        phno_entry = Entry(secondFrame,font=(textFont,12),width=30)
        phno_entry.grid(row=7,column=1,padx=5,pady=10)

        address_label = Label(secondFrame,text='Address: ',font=(textFont,12))
        address_label.grid(row=8,column=0,padx=5,pady=10)

        address_text = Text(secondFrame,font=(textFont,12),width=30,height=5)
        address_text.grid(row=8,column=1,padx=5,pady=10)

        cgpa_label = Label(secondFrame,text='Cgpa: ',font=(textFont,12))
        cgpa_label.grid(row=9,column=0,padx=5,pady=10)

        cgpa_entry = Entry(secondFrame,font=(textFont,12),width=30)
        cgpa_entry.grid(row=9,column=1,padx=5,pady=10)

        pic_label = Label(secondFrame,text='Upload Profile Photo',fg='white'
        ,bg=windowLabelBg,font=(textFont,12))
        pic_label.grid(row=10,columnspan=2,padx=5,pady=10)

        upload_btn = Button(secondFrame,text='Choose file',font=(textFont,12),
                    command=lambda: self.upload_pic(),bg=windowBg,fg='white')
        upload_btn.grid(row=11,column=0,padx=5,pady=10)

        register = Button(secondFrame,text=windowBtn,font=(textFont,12),
                    command=lambda: self.authenticate(createUsr),bg=windowBg,fg='white')
        register.grid(row=12,columnspan=2,padx=5,pady=10)

        backBtn = Button(secondFrame,text='Go back',font=(textFont,12),
                    command=lambda: self.gotoPrevPage(new_window),bg=windowBg,fg='white')
        backBtn.grid(row=13,column=0,padx=5,pady=10)
        
        new_frame.pack(expand=True)

        new_window.mainloop()

    def gotoPrevPage(self,new_window):
        # b1['state'] = 'normal'
        new_window.destroy()


    def signInWindow(self):
        global rollNumberEntry,password_entry, window

        window = Tk()
       # window.state('zoomed') # maximises the window when invoked
        
        window.config(bg='light blue')
        window.geometry(self.windowGeometry(window))

        init_frame = Frame(window,bd=10,relief=RIDGE)

        frame_1 = Frame(init_frame)

        Label(frame_1,text='Sign in',
                        font=(textFont,20,'bold')).grid(row=0,columnspan=2,padx=5,pady=10)


        Label(frame_1,text='Roll no:',font=(textFont,12,)).grid(row=1,column=0,padx=10,pady=10)

        rollNumberEntry = Entry(frame_1,font=(textFont,12),width='27')
        rollNumberEntry.grid(row=1,column=1,padx=4,pady=10)

        Label(frame_1,text='Password:',font=(textFont,12,)).grid(row=2,column=0,padx=10,pady=10)

        password_entry = Entry(frame_1,font=(textFont,12),show='*',width='27')
        password_entry.grid(row=2,column=1,padx=4,pady=10)

        # frame_2 inside in frame_1

        frame_2 = Frame(init_frame,)

        b1 = Button(frame_2,text='Log in and view details',bg='#4465b8',fg='white',
        command=lambda:self.submit(rollNumberEntry.get().upper(),password_entry.get(),createUsr=False),
        font=(textFont,12),width='39')
        b1.grid(row=0,column=1,pady=10,padx=2)

        # Question label

        Label(frame_2,text='Dont have an account? Register',
                        font=(textFont,12)).grid(row=1,column=1,padx=5)

        Button(frame_2,text='Register',bg='#4465b8',fg='white',
        command=lambda: self.register(createUsr=True,
        windowLabel = 'Register', windowBg = '#3eb051', windowBtn='Sign up',
            windowLabelBg='#3eb051'),font=(textFont,12),
                    width='39').grid(row=2,column=1,pady=10)

        Label(frame_2,text='Forgot password?\nClick the below button to reset password',
            font=(textFont,12)).grid(row=3,column=1,padx=5)

        forgotPassowordBtn = Button(frame_2,text='Reset password',width='39'
                ,font=(textFont,12),command=lambda: self.resetPassword(),bg='#4465b8',fg='white')
        forgotPassowordBtn.grid(row=4,column=1,padx=5,pady=10)

        frame_1.grid(row=0,column=1)
        frame_2.grid(row=1,column=1)

        init_frame.pack(expand=True)

        window.mainloop()