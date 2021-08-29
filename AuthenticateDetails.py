from tkinter import *
from tkinter import filedialog, messagebox
import pyotp, os, json
import http.client
# project files
import userRoot

queriesJSON = 'queries.json'

textFont = 'Conoslas'

global otpWindow
global u,p,rp,em,ph,ad,cgp,pc

class Validate:

    dontOpenOtpWindow = False

    def windowGeometry(self,page,otpwindowFlag):

        if not otpwindowFlag:
            window_width = 600
            window_height = 600
        elif otpwindowFlag:
            window_width = 450
            window_height = 300

        screen_width = page.winfo_screenwidth()
        screen_height = page.winfo_screenheight()

        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)

        return ('{}x{}+{}+{}'.format(window_width,window_height,x,y))


    def confirmPasswordChange(self,usrRollno,newPw,retypePw,root):
        if newPw == retypePw:
            with open(userRoot.usersJSON,'r') as file:
                x = json.load(file)
                d = x['users']
                with open(userRoot.usersJSON,'w') as f:
                    for i in d:
                        if usrRollno == i['Roll no']:
                            i['Password'] = newPw
                            break
                    json.dump(x,f,indent=4)
            messagebox.showinfo(title='reset successful',message='Password has been successully reset. Now you can login with new password.')
        else:
            messagebox.showerror(title='incorrect data',message='New password and retype password are not same')
        root.destroy()

    def changePassword(self,usrRollno):
        root = Toplevel()

        root.geometry(self.windowGeometry(root,otpwindowFlag=False))
   
        frame = Frame(root,relief=GROOVE,bd=7)

        Label(frame,text='Change password',bg='#eba98d',font=(textFont,20)).grid(row=0,columnspan=2,padx=5,pady=10)

        Label(frame,text='New Password:',font=(textFont,10)).grid(row=1,column=0,padx=5,pady=10)
        
        newPwEntry = Entry(frame,font=('Conoslas',10),width='30',show='*')
        newPwEntry.grid(row=1,column=1,padx=5,pady=10)

        Label(frame,text='Retype New Password:',font=(textFont,10)).grid(row=2,column=0,padx=5,pady=10)
        
        retypeNewPwEntry = Entry(frame,font=(textFont,10),width='30',show='*')
        retypeNewPwEntry.grid(row=2,column=1,padx=5,pady=10)

        resetBtn = Button(frame,text='Confirm password',font=(textFont,10),
            command=lambda : self.confirmPasswordChange(usrRollno,newPwEntry.get(),retypeNewPwEntry.get(),root))
        resetBtn.grid(row=3,columnspan=2,padx=5,pady=10)

        frame.pack(expand=True)

        root.mainloop()

    
    def checkEntries(self,createUsr,l):

        global u,p,em,ph,ad,cgp,pc,rn,dpt
        
        if createUsr:
            # l = [rollno,dept,usr,pw,email,phno,addr,cgpa,pic]
            rn = l[0]; dpt = l[1]; u = l[2]; p = l[3]; em = l[4]; 
            ph = l[5]; ad = l[6]; cgp = l[7]; pc = l[8]
        elif not createUsr:
            # l = [rollno,dept,usr,email,phno,addr,cgpa,pic]
            rn = l[0]; dpt = l[1]; u = l[2]; em = l[3]; 
            ph = l[4]; ad = l[5]; cgp = l[6]; pc = l[7]
        with open(userRoot.usersJSON,'r') as file:
            x = json.load(file)
            d = x['users']
            if createUsr:
                detailsExist = False
                userExist = False
                for i in d:             
                    if rn in i.values() and dpt in i.values() and u in i.values() and p in i.values() and em in i.values() and ph in i.values() and pc in i.values():
                        userExist = True
                        break
                    elif (rn in i.values() and dpt in i.values()) or u in i.values() or em in i.values() or ph in i.values():
                        detailsExist = True
                        break
                    else:
                        Validate.dontOpenOtpWindow = False
            
                if detailsExist:
                    messagebox.showwarning(parent=userRoot.new_window,title='Data exist',message='Roll number or Username or phno or email are already taken')
                    Validate.dontOpenOtpWindow = True
                elif userExist:
                    Validate.dontOpenOtpWindow = True                    
                    messagebox.showerror(parent=userRoot.new_window,title='Details exist',message='User with details already exist.')
                
            elif not createUsr: # if user clicks on update details
                print('updating details')
                detailsExist = False
                # userExist = False
                for i in d:
                    if userRoot.a in i.values(): continue
                    elif (rn in i.values() and dpt in i.values()) or u in i.values() or em in i.values() or ph in i.values():
                        detailsExist = True
                        break
                if detailsExist:
                    messagebox.showwarning(parent=userRoot.new_window,title='Data exist',message='Roll number or Username or phno or email are already taken')
                    Validate.dontOpenOtpWindow = True
    
    def create_user(self):
        global u,p,em,ph,ad,cgp,pc,rn,dpt
        ad = ad.replace('\n','')
        ad = ad.replace(',',',\n')
        with open(userRoot.usersJSON,'r') as file: # This shoulndt be in write mode . if it is then it clears all data
            x = json.load(file)
            d = x['users']
            d.append({'Roll no':rn.upper(),'Department':dpt.upper(),'Username':u,'Password':p,'Email':em,'Phno':ph,'Address':ad,'Cgpa':cgp,
                    'profile_pic':pc})
            with open(userRoot.usersJSON,'w') as f:
                json.dump(x,f,indent=4)

        messagebox.showinfo(parent=userRoot.new_window,title='Registration success',message='User registered successfully')
        userRoot.new_window.destroy()
    
    def createQuery(self):
        requests = []
     
        department = userRoot.departmentEntry.get()
        usr = userRoot.sign_in_username_entry.get()
        # pw = userRoot.sign_in_password_entry.get()
        email = userRoot.email_entry.get()
        phno = userRoot.phno_entry.get()
        addr = userRoot.address_text.get('1.0',END)
        cgpa = userRoot.cgpa_entry.get()
        pic = userRoot.profile_pic_path
        addr = addr.replace('\n','')
        addr = addr.replace(',',',\n')

        with open(queriesJSON,'r') as file:
            x = json.load(file)
            requests = x['requests']
        
            with open(queriesJSON,'w') as f:
                temp = []
                d = {}
                temp.append({'Department':department.upper(),'Username':usr,
                'Email':email,'Phno':phno,'Addr':addr,'Cgpa':cgpa,'profile_pic':pic})
                d[userRoot.a] = temp
                requests.append(d)
                json.dump(x,f,indent=4)
        messagebox.showinfo(parent=userRoot.new_window,title='Request sent',message='Request has been sent to admin. Requested data will be updated soon enough.')
        userRoot.new_window.destroy()
      
    
    def verifyOtp(self,otp,code,usrRollno,createUsr,resetPw): # keyword boolean arg createUsr
        global otpWindow
      
        if otp == code:
            print('Otp authentication succesful')
            otpWindow.destroy() 
            if createUsr:
                self.create_user()
            elif not createUsr and resetPw:
                self.changePassword(usrRollno)
            elif not createUsr:
                self.createQuery()
        else:
            print('Invalid Otp entry')
            messagebox.showerror(title='invalid otp',message='Entered otp is invalid')
            otpWindow.destroy()


    def sendOtp(self,phno,usrRollno,createUsr,resetPw):
        # creates an otp window , asks to verify by entering otp
        global otpWindow
       
        totp = pyotp.TOTP('base32secret3232') #algorithm used for securing otp
        code=totp.now() #getting 6 digit otp randomly
        mobile_no=int(phno)
        print("OTP:",code)
        conn = http.client.HTTPSConnection("api.authkey.io")
        # modify below line with your own api key
        conn.request("GET", "/request?authkey=9cead05e00bf81ac&mobile="+str(mobile_no)+"&country_code=91&otp="+str(code)+"&sid=1082&time=60seconds&company=RIT")
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

        otpWindow = Toplevel()

        otpWindow.config(bg='#adb0ba')
        
        otpWindow.geometry(self.windowGeometry(otpWindow,otpwindowFlag=True))

        frame = Frame(otpWindow,bg='#697c91',relief=RIDGE,bd=7)

        authenticateLabel = Label(frame,font=(textFont,20),text='Authenticate')
        authenticateLabel.grid(row=0,columnspan=2,padx=5,pady=10)

        otpLabel = Label(frame,text='Enter otp: ',font=(textFont,12))
        otpLabel.grid(row=1,column=0,padx=5,pady=10)

        otpEntry = Entry(frame,font=(textFont,12))
        otpEntry.grid(row=1,column=1,padx=5,pady=10)

        verifyButton = Button(frame,text='verify',font=(textFont,12)
        ,command=lambda : self.verifyOtp(otpEntry.get(),code,usrRollno,createUsr,resetPw))
        
        verifyButton.grid(row=2,columnspan=2,padx=5,pady=10)

        messageLabel = Label(frame,
        text='Enter the otp that is sent to your mobile number.\n It is valid only for 60 seconds',
                font=(textFont,10))
        messageLabel.grid(row=3,columnspan=2,padx=5,pady=10)

        frame.pack(expand=True)

        otpWindow.mainloop()
