import json,os
import userRoot,displayDetails


usrProcess = userRoot.signIn()
usrProcess.signInWindow() # createUsr=True
displayProcess = displayDetails.showUserInfo(createUsr=False)
