from tkinter import *
from tkinter import filedialog, messagebox
import json,os, pyotp, http.client

textFont = 'Conoslas'
global adminJSON
global adminUsernameEntry, adminPasswordEntry

global adUsrname, adPswrd

adminJSON = 'admins.json'

class adminSignIn():

    def setWindowGeometry(self,window,otpWindowFlag):
        if not otpWindowFlag:
            window_width = 600
            window_height = 600
        elif otpWindowFlag:
            window_width = 450
            window_height = 300

        screen_height = window.winfo_screenheight()
        screen_width = window.winfo_screenwidth()

        x = int(screen_height/2 - window_height/2)
        y = int(screen_width/2 - window_width/2)

        return ('{}x{}+{}+{}'.format(window_width,window_height,y,x))

    def __init__(self):
        root = Tk()
        root.title('Admin Home')
        global adminUsernameEntry, adminPasswordEntry

        root.geometry(self.setWindowGeometry(root,otpWindowFlag=False))

        frame = Frame(root,bg='#4a754f')

        Label(frame,text='Admin Login Page',font=(textFont,20)).grid(row=0,columnspan=2,padx=5,pady=10)

        Label(frame,text='Admin Username',font=(textFont,12)).grid(row=1,column=0,padx=5,pady=10)

        adminUsernameEntry = Entry(frame,font=(textFont,12))
        adminUsernameEntry.grid(row=1,column=1,padx=5,pady=10)

        Label(frame,text='Admin Password',font=(textFont,12)).grid(row=2,column=0,padx=5,pady=10)

        adminPasswordEntry = Entry(frame,font=(textFont,12),show='*')
        adminPasswordEntry.grid(row=2,column=1,padx=5,pady=10)

        Button(frame,text='Log in',font=(textFont,12),bd=3,activeforeground='#ffffff',activebackground='#173d22',fg='#ffffff',bg='#81a349'
        ,command=lambda : self.adminLogIn(adminUsernameEntry.get(),
        adminPasswordEntry.get(),root)).grid(row=3,columnspan=2,padx=5,pady=10)

        Label(frame,text='Not registered?\nclick on the below button to register',
        font=(textFont,12),bg='#4a754f').grid(row=4,columnspan=2,padx=5,pady=10)

        Button(frame,text='Register',font=(textFont,12),bd=3,activeforeground='#ffffff',activebackground='#173d22',fg='#ffffff',bg='#81a349'
        ,command=lambda : self.adminRegister(root)).grid(row=5,columnspan=2,padx=5,pady=10)

        frame.pack(expand=True)

        root.mainloop()

    def adminLogIn(self,username,password,root):
        
        global adminUsernameEntry, adminPasswordEntry
        global adUsrname, adPswrd
        if len(username) == 0 or len(password) == 0:
            messagebox.showwarning(parent=root,title='Empty fields',message='Username or password are empty')
        
        else:
            fileNotExistFlag = False
            try:
                file = open(adminJSON,'r')
                file.close()
                
            except FileNotFoundError : 
                with open(adminJSON,'w') as f:
                    d = {"admins":[]}
                    json.dump(d,f,indent=4)

            if not fileNotExistFlag: 
                if os.path.getsize(adminJSON) == 0:
                    messagebox.showerror(parent=root,title='File empty',message='No admin registered yet!. Please register and then try logging in')
                    with open(adminJSON,'w') as f:
                        d = {"admins":[]}
                        json.dump(d,f,indent=4)
                else:
                    with open(adminJSON,'r') as file:
                        
                        x = json.load(file)
                        d = x['admins']

                        if len(d) == 0:
                            messagebox.showerror(parent=root,title='File empty',message='No admin registered yet! Please register to continue logging in')
                            adminUsernameEntry.delete(0,END)
                            adminPasswordEntry.delete(0,END)
                        else:
                            flag = False

                            for i in d:
                                if username in i.values() and password in i.values():
                                    flag=True
                                    break
                            
                            if flag:
                                adUsrname = username
                                adPswrd = password
                                messagebox.showinfo(parent=root,title='logged in ',message='Admin logged in successfully')
                                
                                root.destroy()
                            elif not flag:
                                messagebox.showerror(parent=root,title='details doesnt exist',message='Admin not found. Please register')
                                adminUsernameEntry.delete(0,END)
                                adminPasswordEntry.delete(0,END)
    
    def adminRegister(self,root):
        
        window = Toplevel()
        window.title('Admin SignUp')
        global adminUsernameEntry, adminPasswordEntry
        
        adminUsernameEntry.delete(0,END)
        adminPasswordEntry.delete(0,END)

        window.geometry(self.setWindowGeometry(window,otpWindowFlag=False))

        frame = Frame(window,bg='#eb4034')

        Label(frame,font=(textFont,20),text='Admin Register Page').grid(row=0,columnspan=2,padx=5,pady=10)

        Label(frame,font=(textFont,12),text='Username:').grid(row=1,column=0,padx=5,pady=10)

        adSignInUsrEntry = Entry(frame,font=(textFont,12))
        adSignInUsrEntry.grid(row=1,column=1,padx=5,pady=10)

        Label(frame,font=(textFont,12),text='Password:').grid(row=2,column=0,padx=5,pady=10)

        adSignInPwEntry = Entry(frame,font=(textFont,12),show='*')
        adSignInPwEntry.grid(row=2,column=1,padx=5,pady=10)

        Label(frame,font=(textFont,12),text='Retype password:').grid(row=3,column=0,padx=5,pady=10)

        adSignInRetypePwEntry = Entry(frame,font=(textFont,12),show='*')
        adSignInRetypePwEntry.grid(row=3,column=1,padx=5,pady=10)

        Label(frame,font=(textFont,12),text='Phone number:').grid(row=4,column=0,padx=5,pady=10)

        adPhnoEntry = Entry(frame,font=(textFont,12))
        adPhnoEntry.grid(row=4,column=1,padx=5,pady=10)

        Button(frame,text='Sign up',font=(textFont,12,),bd=3,command=lambda : self.adminSignUp(adSignInUsrEntry.get(),adSignInPwEntry.get()
        ,adSignInRetypePwEntry.get(),adPhnoEntry.get(),window),activeforeground='#ffffff',activebackground='#96372d',fg='#ffffff',bg='#96372d'
        ,).grid(row=5,columnspan=2,padx=5,pady=10)

        Button(frame,text='< Back',font=(textFont,12,),bd=3,
        command=lambda : self.goBack(window),activeforeground='#ffffff',activebackground='#96372d',fg='#ffffff',bg='#96372d').grid(row=6,columnspan=2,padx=5,pady=10)

        frame.pack(expand=True)

        window.mainloop()
    
    def goBack(self,window):
        window.destroy()

    def adminSignUp(self,adusr,adpw,adrepw,adphno,window):
        
        if len(adusr) == 0 or len(adpw) == 0 or len(adrepw) == 0 or len(adphno) == 0:
            messagebox.showwarning(parent=window,title='Insufficient data',message='All fields are required to be filled.')
        
        elif len(adpw) < 8 or len(adpw) > 15:
            messagebox.showwarning(parent=window,title='Constraint',message='Password must contain minimum 8 characters and maximum of 15 characters')   
 
        elif adpw != adrepw:
            messagebox.showerror(parent=window,title='Data Mismatch',message='Password and retype password are not same') 

        else:
            try:
                file = open(adminJSON,'r')
                if os.path.getsize(adminJSON) == 0:
                    with open(adminJSON,'w') as f:
                        d = {'admins':[]}
                        json.dump(d,f,indent=4)
                file.close()
            except FileNotFoundError:
                with open(adminJSON,'w') as f:
                    d = {'admins':[]}
                    json.dump(d,f,indent=4)
            existingDetails = False
            existingAdmin = False
            d = {}
            with open(adminJSON,'r') as fhand:
                x = json.load(fhand)
                d = x['admins']
                for i in d:
                    if adusr in i.values() and adpw in i.values() and adphno in i.values():
                        existingAdmin = True
                        break
                    elif adusr in i.values() or adphno in i.values():
                        existingDetails = True
                        break
                if existingAdmin:
                    messagebox.showwarning(parent=window,title='Admin exist',message='Admin with these details already exist.')
                elif existingDetails:
                    messagebox.showerror(parent=window,title='Details exist',message='Username or Phone number already taken')
                else:
                    totp = pyotp.TOTP('base32secret3232') #algorithm used for securing otp
                    code=totp.now() #getting 6 digit otp randomly
                    mobile_no=int(adphno)
                    print(code)
                    conn = http.client.HTTPSConnection("api.authkey.io")
                    conn.request("GET", "/request?authkey=9cead05e00bf81ac&mobile="+str(mobile_no)+"&country_code=91&otp="+str(code)+"&sid=1082&time=60seconds&company=RIT")
                    res = conn.getresponse()
                    data = res.read()
                    print(data.decode("utf-8"))

                    otp = Toplevel()
                    otp.config(bg='#adb0ba')
                    otp.geometry(self.setWindowGeometry(otp,otpWindowFlag=True))
                    frame = Frame(otp,bg='#697c91',relief=RIDGE,bd=7)

                    authenticateLabel = Label(frame,font=(textFont,20),text='Authenticate')
                    authenticateLabel.grid(row=0,columnspan=2,padx=5,pady=10)

                    otpLabel = Label(frame,text='Enter otp: ',font=(textFont,12))
                    otpLabel.grid(row=1,column=0,padx=5,pady=10)

                    otpEntry = Entry(frame,font=(textFont,10))
                    otpEntry.grid(row=1,column=1,padx=5,pady=10)

                    verifyButton = Button(frame,text='verify',font=(textFont,12)
                    ,command=lambda : self.otpVerification(otpEntry.get(),code,adusr,adpw,adphno,otp,window))
                    
                    verifyButton.grid(row=2,columnspan=2,padx=5,pady=10)

                    messageLabel = Label(frame,
                    text='Enter the otp that is sent to your mobile number.\n It is valid only for 60 seconds',
                            font=(textFont,10))
                    messageLabel.grid(row=3,columnspan=2,padx=5,pady=10)

                    frame.pack(expand=True)

                    otp.mainloop()

    def otpVerification(self,usrEnteredOtp,code,adusr,adpw,adphno,otp,window):
        if usrEnteredOtp == code:
            self.createAdmin(adusr,adpw,adphno,window)
            print('Otp authentication successful')
            otp.destroy()
        else:
            print('Invalid Otp Entry!')
            messagebox.showerror(parent=window,title='Wrong entry',message='Invalid otp')
            otp.destroy()

    def createAdmin(self,adusr,adpw,adphno,window):
        try:
            fhand = open(adminJSON,'r') 
            if os.path.getsize(adminJSON) == 0:
                with open(adminJSON,'w') as file:
                    d = {'admins':[]}
                    json.dump(d,file,indent=4)
            fhand.close()
        except FileNotFoundError:
            with open(adminJSON,'w') as file:
                d = {'admins':[]}
                json.dump(d,file,indent=4)
        with open(adminJSON,'r') as file:
            x = json.load(file)
            d = x['admins']
            
            with open(adminJSON,'w') as f:
                d.append({'Username':adusr,'Password':adpw,'Phno':adphno})
                json.dump(x,f,indent=4)
  
        messagebox.showinfo(parent=window,title='Registered',message='Registered succesfully!')
        window.destroy()