# Student-Database-Management-System

This is a simple application software that provides interface at user-end. This application is mainly developed in the view of educational institutions which has a basic need 
storing student details and viewing them when wanted to. 

A BASIC WALKTHORUGH:

Student Interface:
    - Student interface has student login, register and change password options.
    - If a student is not registered yet, then he may register himself by clicking on the register button.
    - Student can change his password by clicking on the Change password button.
    - When a student logs in with his credentials, then a window is displayed viewing his details.
    - If any changes have to be made in his details, then he shall have to send a request to admin to modify his details.

Admin Interface:
    - Admin too can login, register and change password as well.
    - Admin can view student details according to student 'Roll no' or 'Branch' or 'cgpa'.
    - Admin can also view student requests and update them or deny them accordingly.


**NOTE:***
The following are some of the things to be noted ....

    1) You need to have your computer connected to the internet (otp authentication service)
    2) You may want to use your own api for text message service required for otp authentication service. If so modify these lines in files:
            - In AuthenticateDetails.py, line: 200, 202
            - In adminInterface.py, line: 213, 214
    3) All profile photos must be png format.
    4) In admin page, all details will be updated along with profile photos as well, but what profile pic is being updated is not shown to admin.
