
# Hi, I'm Karthik 👋

# ATM Management Application
 This project is based on graphical user interface (GUI-Tkinter). It uses a simple database file approach to save and retrive user information.
## Technologies

 <img width="50px" src="https://ik.imagekit.io/ybyfbcvb8/python.png?updatedAt=1692968478421"/>  <img width="50px" src="https://ik.imagekit.io/ybyfbcvb8/62c46cd2a75b8945b1696713.png?updatedAt=1692968811131"/>


## Screenshots

![App Screenshot](https://ik.imagekit.io/ybyfbcvb8/SBI%20_%20HOME%20%2025-08-2023%2017_42_04.png?updatedAt=1692966101570)



## How to Run the Application

- Download the zip file 
- extract zip to desktop
- make sure to install python in your machine
- run the main.py file to start the project
- login page will open first click on create new account and create and account
- use the credentials to login.
- now you can perform simple task like withdraw money-transfer and balance-enquery and deposite pinchange


Modules Used:
--------------------------------------------------
Tkinter - For Graphical user interface (GUI).

sqlite3 - For Database Connectivity.

re - For strong passwords matchings.

PIL - For loading images and icons to project.

Datetime - For knowing the Transactions details.

time - For Stopping execution for some time(sleep).


  How it Works ?
---------------
This project consist of 2 forms (main.py and Signup_app.py) which redirect main.py <=> Signup_app.py by (Circular import).

* main.py:
  * Checking for login credentials in Database file(sbi.db)
  * Withdraw Operations
  * Balance Enquiry
  * Pinchange
  * Deposite Money
  * Transfer Money to A/c
* signup_app.py:
  * Creating a NewAccount into database file sbi.db
  * Strong Password Validation

     
