from tkinter import *
import sqlite3
from tkinter import messagebox
import re

class RegistrationApp:

	def login(self,event): # -----------------   REDIRECT TO AtmApp   --------------------

			self.screen.destroy()
			from main import AtmApp
			root = Tk()
			start = AtmApp(root)

	def PswValidate(self,password): # -----------------   PASSWORD VALIDATE   --------------------

		self.test = None
		conditions = [re.search('[\d]+',password),re.search('[A-Z]+',password),re.search('[a-z]+',password),re.search('[!@#$%^&_]+',password)]
		if len(password) >= 8:
			for i in conditions:
				if i:
					self.test = password
				else:
					self.test = None
					break
		else:
			self.test = None
		return self.test

	def data_insert(self): # -----------------   INSERT INTO DATA BASE   --------------------
		if self.name_entry.get() != '':
			Name = self.name_entry.get().capitalize()
			psw = self.psw_entry.get()
			if self.PswValidate(psw):
				if self.crf_psw_entry.get() == psw:
					if self.blnc_entry.get().isdigit():
						blnce = int(self.blnc_entry.get())
						new_accnt = self.count+1
						confirm = messagebox.askquestion('SBI | INFO','Save Details ?')
						if confirm == 'yes':
							values = (new_accnt,Name,psw,blnce)
							sql = """INSERT INTO userdata (Account_no,Name,Pincode,balance) VALUES (?,?,?,?)"""
							self.mycursor.execute(sql,values)
							self.reset_field()
							messagebox.showinfo('status',' Saved Successfull !')
							self.mydb.commit()
							self.mydb.close()
							self.num_entry.delete(0,END)
							self.num_entry.insert(0,new_accnt+1)
							self.name_entry.focus()
						else:
							pass
					else:
						messagebox.showerror('SBI | Alert !','Pls Enter Valid Amount')
				else:
					messagebox.showerror('SBI | Alert !','Password Not Match')	
			else:
				messagebox.showerror('SBI | Alert !','Enter Strong Password')
		else:
			messagebox.showerror('SBI | Alert !','Enter Valid Name')

	def reset_field(self): # -----------------   RESET ALL FIELDS   --------------------

		self.name_entry.delete(0,END)
		self.psw_entry.delete(0,END)
		self.crf_psw_entry.delete(0,END)
		self.blnc_entry.delete(0,END)
		self.name_entry.focus()

	def __init__(self,screen): # ---------------   Intializing the Registration   --------------

		self.screen = screen
		self.screen.title('SBI | Account Registration')
		self.screen.config(bg = '#04233b')
		self.screen.iconbitmap(r'atm.ico')
		self.screen.geometry("700x550+380+140")
		self.screen.wm_maxsize(700,550)
		self.screen.wm_minsize(700,550)
		self.mydb = sqlite3.connect('sbi.db')
		self.mycursor = self.mydb.cursor()
		self.mycursor.execute('SELECT Account_no FROM userdata ORDER BY Account_no DESC LIMIT 1')
		for i in self.mycursor:
			self.count = sum(i)
		Label(self.screen, text="STATE BANK OF INDIA", bg="#04233b", font=("", 30, "bold"), fg='#acf3d4', justify='center').pack(pady = (40,10),fill = X)
		Label(self.screen, text="CREATE NEW ACCOUNT", bg="#acf3d4", font=("rockwell", 20, "bold"), fg='grey10', justify='center').pack(pady = (10),fill = X,ipady = 10)
		self.t_frame = LabelFrame(self.screen,text = "  User Details >> ",bg = '#04233b',font = ('',15,'italic','bold'),fg = '#acf3d4')
		self.t_frame.pack(ipadx = 15)
		#  frame1 =======================

		self.f1 = Frame(self.t_frame,bg = '#04233b')
		self.f1.pack(pady = (30,20))
		Label(self.f1,text = "Account Number ",bg = '#acf3d4', font = ('',15,'bold')).pack(side = 'left')
		self.num_entry = Entry(self.f1,font = ('',17,'bold'),width = 8,justify = 'center')
		self.num_entry.pack(side = 'left')
		self.num_entry.insert(0,int(self.count)+1)
		self.name_entry = Entry(self.f1,font = ('',17,'bold'),width = 15)
		self.name_entry.focus()
		self.name_entry.pack(side = 'right')
		Label(self.f1,text = "User Name ",bg = '#acf3d4', font = ('',15,'bold')).pack(side = 'right', padx = (30,0))
		#  frame2 =======================
		
		self.f2 = Frame(self.t_frame,bg = '#04233b')
		self.f2.pack(pady = 15)
		Label(self.f2,text = "Password ",bg = '#acf3d4', font = ('',15,'bold')).pack(side = 'left')
		self.psw_entry = Entry(self.f2,font = ('',17,'bold'),width = 8)
		self.psw_entry.pack(side = 'left')
		self.crf_psw_entry = Entry(self.f2,font = ('',17,'bold'),width = 8)
		self.crf_psw_entry.pack(side = 'right')
		Label(self.f2,text = "Confirm Password ",bg = '#acf3d4', font = ('',15,'bold')).pack(side = 'right', padx = (110,0))
		#  frame3 =======================

		self.f3 = Frame(self.t_frame,bg = '#04233b')
		self.f3.pack(pady = 20)
		Label(self.f3,text = "Balance ",bg = '#acf3d4', font = ('',15,'bold')).pack(side = 'left')
		self.blnc_entry = Entry(self.f3,font = ('',17,'bold'),width = 8,justify = 'center')
		self.blnc_entry.pack(side = 'left')

		#  bottom frame ==========================
		b_frame = Frame(self.screen,bg = '#04233b')
		b_frame.pack(pady = (20,10))
		Button(b_frame, text="Save", bg="green",font=("", 18), fg="white", command=self.data_insert).pack(side = 'right', padx = (70,0),ipadx = 10)
		Button(b_frame, text="Reset", bg="red",
                  fg="white", font=("", 18), command=self.reset_field).pack(side = 'left',ipadx = 10)
		bottom4 = Frame(self.screen,bg = '#04233b')
		bottom4.pack(pady = 10)
		registration  = Label(bottom4, text="Already having Account  >>> LOGIN", bg="#04233b", fg='white',font = ('courier',10,'bold','italic','underline'))
		registration.pack()
		registration.bind('<Button-1>', self.login)
		self.screen.mainloop()
		




