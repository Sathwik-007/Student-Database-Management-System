import adminInterface, adminMenu

adminApplication = adminInterface.adminSignIn()
try:
    if len(adminInterface.adUsrname) != 0 and len(adminInterface.adPswrd) != 0:
        adminInterface.adUsrname = ''
        adminInterface.adPswrd = ''
        menu = adminMenu.adminHome()    
except AttributeError:
    print("Application closed")