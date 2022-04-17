# Student-Database-Management-System

This is a simple application software that provides interface at user-end. This application is mainly developed in the view of educational institutions which have a common objective to store student details in a database that can be useful for different purposes. 


A BASIC WALKTHORUGH:

Student Interface:

    - Student interface has student login, register and change password options.
    
    - If a student is not registered yet, then he may register by clicking on the register button.
    
    - Student can change his password by clicking on the Change password button.
    
    - When a student logs in with his credentials, then a window is displayed viewing his details.
    
    - If any changes have to be made in his details, then he shall have to send a request to admin to modify his details.

Admin Interface:

    - Admin too can login, register and change password as well.

    - Admin can view student details according to student 'Roll no' or 'Branch' or 'cgpa'.
    
    - Admin can also view student requests and update them or deny them accordingly.

***NOTE:***
     
    The files admin_main.py and user_main.py are the kickstart files that fire up interfaces for student and admin respectively. You may convert these admin_main.py and user_main.py files into executable to run as application (pyinstaller).

    You may want to use your own api for text message service required for otp authentication service. If so modify these lines in files:
            - In AuthenticateDetails.py, line: 200, 202
            - In adminInterface.py, line: 213, 214.

    Since this application is not converted into an executable, modules used like PIL, pyotp need to installed into the machine before executing the code. Pip install the following libraries and you are good to go :).
            - pip3 install pillow
            - pip3 install pyotp

The following are some of the things to be aware of ....

    1) You need to have your computer connected to the internet (otp authentication service).
    2) All profile photos must be png format (you can convert any other formats into .png using online converters).
    3) In admin page, all details will be updated along with profile photos as well, but what profile pic is being updated is not shown to admin.

This application works really well. However, there is always room for improvement ;)
