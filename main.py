from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import datetime as dt
import sqlite3
import re


class AtmApp():
    count = 0

    def animations(self):
        self.marque.after(1, self.marque.place(x=-440+AtmApp.count, y=30))
        self.marque.config(fg="#acf3d4")
        AtmApp.count += 2
        if AtmApp.count > 1150:
            AtmApp.count = 0
        self.marque.after(1, self.animations)
    # -----------------   Redirect to Registration   --------------------

    def registration(self, event):

        self.root.destroy()
        from signup_app import RegistrationApp
        screen = Tk()
        start = RegistrationApp(screen)

    def withdraw(self):  # ------------   Withdraw   ----------------

        self.root.title(" SBI | WITHDRAW ")
        self.user_with = Frame(
            self.user_win, background="#acf3d4", width=900, height=500)
        self.user_with.place(x=0, y=0)

        def clear():
            self.user_entry.delete(0, END)

        def wi():
            if self.user_entry.get().isdigit() and int(self.user_entry.get()) % 100 == 0:
                if self.user_details[3] > int(self.user_entry.get()):
                    self.mycursor.execute(
                        f"update userdata set balance = {self.user_details[3]-int(self.user_entry.get())} where Account_no = {self.user_details[0]}")
                    confirm = messagebox.askquestion(
                        'SBI | INFO', f'Confirm to WithDraw ? \n\t{self.user_entry.get()} ₹')
                    if confirm == 'yes':
                        self.submit_btn.config(state='disabled')
                        Label(self.user_with, text='successfully amount WithDraw', font=(
                            '', 10, 'bold'), bg='orange').place(x=270, y=150)
                        self.user_details[3] -= int(self.user_entry.get())
                        self.mydb.commit()
                        self.mydb.close()
                        show_blnce = messagebox.askquestion(
                            'SBI | INFO', ' Show Balance ? ')
                        if show_blnce == 'yes':
                            self.balance()
                        else:
                            self.user_win.after(0, self.exit)
                    else:
                        pass
                else:
                    messagebox.showerror(
                        'SBI | Error', 'Insufficient Balance !')
                    self.clear()
            else:
                messagebox.showerror(
                    'SBI | Error', 'Enter Valid Amount !')
                self.clear()

        Label(self.user_with, text='WITHDRAW', font=(
            '', 30, 'bold'), bg='grey20', fg='white').pack(side='top', fill='x', pady=50)
        Label(self.user_with, text=' Enter Amount ', font=(
            '', 15, 'bold'), bg='grey20', fg='white').pack(pady=(50, 30), padx=285)
        Label(self.user_with, text=' * NOTE :  Pls Enter 100, 200, 500, 2000 only ! ', font=(
            '', 15, 'bold'), bg='grey20', fg='white').pack(pady=(20, 50))
        f1 = Frame(self.user_with, bg='#acf3d4')
        f1.pack()
        self.user_entry = Entry(f1, width=10, font=(
            '', 30, 'bold'), bg='white', fg='grey10', justify='center', state='normal')
        self.user_entry.pack(side='left')
        self.user_entry.focus()
        Label(f1, text=" ₹ ", fg='green', font=(
            '', 30, 'bold'), bg='grey10').pack(side='right')
        f2 = Frame(self.user_with, bg='#acf3d4')
        f2.pack()
        Button(f2, text='Cancel', font=(
            '', 15, 'bold'), bg='red', fg='white', command=self.exit).pack(side='left', pady=30, padx=100)
        Button(f2, text='Clear', font=(
            '', 15, 'bold'), bg='red', fg='white', command=clear).pack(side='left')
        self.submit_btn = Button(f2, text='Submit', font=(
            '', 15, 'bold'), bg='green', fg='white', command=wi)
        self.submit_btn.pack(side='right', padx=100)

    def balance(self):  # ------------   Balance   ----------------

        self.root.title(" SBI | BALANCE ")
        self.user_blnc = Frame(
            self.user_win, background="#acf3d4", width=900, height=500)
        self.user_blnc.place(x=0, y=0)

        Label(self.user_blnc, text=' BALANCE', font=(
            '', 30, 'bold'), bg='grey20', fg='white').pack(side='top', fill='x', pady=50)

        Label(self.user_blnc, text='A/C no : xxxx'+str(
            self.user_details[0]), bg='#acf3d4', fg='grey10', font=('', 25, 'bold')).pack(pady=20)

        Label(self.user_blnc, text=self.user_details[1].capitalize(), font=(
            '', 30, 'bold'), bg='#acf3d4', fg='orange').pack(pady=20)

        Label(self.user_blnc, text=str(
            float(self.user_details[3]))+' ₹', font=('', 20, 'bold'), bg='#acf3d4', fg='grey10').pack(pady=20, padx=300)

        Label(self.user_blnc, text='Last successfully Checked----'+str(dt.datetime.now()),
              font=('', 10, 'italic'), bg='green').pack(side='right', pady=(125, 0), padx=10)
        self.user_win.after(4000, self.exit)

    def pinchange(self):  # ------------   Pinchange   ----------------

        self.root.title(" SBI | PIN CHANGE ")
        self.user_pinchange = Frame(
            self.user_win, background="#acf3d4", width=900, height=500)
        self.user_pinchange.place(x=0, y=0)

        def clear():
            self.o_pinentry.delete(0, END)
            self.n_pinentry.delete(0, END)
            self.cn_pinentry.delete(0, END)

        def passw(string):
            test = None
            conditions = [re.search('[\d]+', string), re.search('[A-Z]+', string),
                          re.search('[a-z]+', string), re.search('[$@_!]+', string)]
            if len(string) >= 8:
                for i in conditions:
                    if i:
                        test = string
                    else:
                        test = None
                        break
            return test

        def confirm():
            if self.o_pinentry.get() == self.user_details[2]:
                if passw(self.n_pinentry.get()):
                    if self.n_pinentry.get() == self.cn_pinentry.get():

                        confirm = messagebox.askquestion(
                            'SBI | INFO', 'Confirm to Save')
                        if confirm == 'yes':
                            self.user_details[2] = self.cn_pinentry.get()
                            update_sql = 'UPDATE userdata SET Pincode = (?) WHERE Account_no = (?)'
                            values = (
                                self.user_details[2], self.user_details[0])
                            self.mycursor.execute(update_sql, values)
                            self.mydb.commit()
                            self.mydb.close()
                            s_label = Label(self.user_pinchange, text='Pin Change Successfully----'+str(
                                dt.datetime.now()), font=("", 15, 'bold'), bg='orange', fg='grey20')
                            s_label.place(x=90, y=105)
                            messagebox.showinfo(
                                'SBI | INFO', ' Pinchange Succesfully !')
                            self.crf_btn.config(state='disabled')
                            self.clear()
                            self.user_win.after(2000, self.exit)
                        else:
                            pass
                    else:
                        messagebox.showerror(
                            'SBI | Error', 'Pin not match !')
                    self.clear()
                else:
                    messagebox.showerror(
                        'SBI | Error', 'Enter strong Password !')
            else:
                messagebox.showerror('SBI | Error', 'Wrong Pin !')
                self.clear()
        Label(self.user_pinchange, text='PIN CHANGE', font=(
            "", 30, 'bold'), bg='grey20', fg='white').pack(side='top', fill='x', pady=50)
        f = Frame(self.user_pinchange, bg='#acf3d4')
        f.pack()
        f1 = Frame(f, bg='#acf3d4')
        f1.pack(side='left')
        Label(f1, text='Enter Old Pin    ', font=(
            '', 15, 'bold'), bg='grey20', fg='white').pack(padx=(50, 0), pady=21)
        Label(f1, text='New Pin  ', font=(
            '', 15, 'bold'), bg='grey20', fg='white').pack(padx=(50, 0), pady=21)
        Label(f1, text='Confirm  Pin     ', font=(
            '', 15, 'bold'), bg='grey20', fg='white').pack(padx=(50, 0), pady=21)

        f2 = Frame(f, bg='#acf3d4')
        f2.pack(side='right')
        self.o_pinentry = Entry(
            f2, width=7, font=('', 18, 'bold'))
        self.o_pinentry.pack(padx=(0, 412), pady=20)
        self.o_pinentry.focus()
        self.o_pinentry.config(show='*')
        self.n_pinentry = Entry(
            f2, width=7, font=('', 18, 'bold'))
        self.n_pinentry.pack(padx=(0, 412), pady=20)
        self.cn_pinentry = Entry(
            f2, width=7, font=('', 18, 'bold'))
        self.cn_pinentry.pack(padx=(0, 412), pady=20)
        b_f = Frame(self.user_pinchange, bg='#acf3d4')
        b_f.pack(pady=52)
        self.crf_btn = Button(b_f, text='Confirm', font=(
            '', 15, 'bold'), bg='green', fg='white', command=confirm)
        self.crf_btn.pack(side='right', pady=20, padx=80)
        Button(b_f, text='Clear', font=(
            '', 15, 'bold'), bg='red', fg='white', command=clear).pack(side='left', pady=20, padx=80)
        Button(b_f, text='Cancel', font=(
            '', 15, 'bold'), bg='red', fg='white', command=self.exit).pack(side='right', pady=20)

    def deposite(self):  # ------------   Deposite   ----------------
        self.root.title(" SBI | DEPOSITE ")
        self.user_dep = Frame(
            self.user_win, background="#acf3d4", width=900, height=500)
        self.user_dep.place(x=0, y=0)

        def dep():
            if self.user_entry.get().isdigit() and int(self.user_entry.get()) % 100 == 0:
                self.mycursor.execute(
                    f"update userdata set balance = {self.user_details[3]+int(self.user_entry.get())} where Account_no = {self.user_details[0]}")

                confirm_dep = messagebox.askquestion(
                    "SBI | INFO", f"Confirm Deposite {self.user_entry.get()}₹")
                if confirm_dep == "yes":
                    Label(self.user_dep, text=' Amount Deposite Successfully !', font=(
                        '', 10, 'bold'), bg='orange').place(x=270, y=300)
                    self.submit_btn.config(state='disabled')
                    self.mydb.commit()
                    self.mydb.close()
                    self.user_details[3] += int(self.user_entry.get())
                    show_blnce = messagebox.askquestion(
                        'SBI | INFO', ' Show Balance ? ')
                    if show_blnce == 'yes':
                        self.balance()
                    else:
                        self.user_win.after(0, self.exit)
                else:
                    pass
            else:
                messagebox.showerror('SBI | Error', 'Enter Valid Amount')
                clear()

        def clear():
            self.user_entry.delete(0, END)

        Label(self.user_dep, text=' DEPOSITE ', font=(
            '', 30, 'bold'), bg='grey20', fg='white').pack(side='top', fill='x', pady=50)
        Label(self.user_dep, text=' Enter Amount ', font=(
            '', 20, 'bold'), bg='grey20', fg='white').pack(pady=10, padx=260)
        Label(self.user_dep, text=' * NOTE :  Pls Enter 100, 200, 500, 2000 only ! ', font=(
            '', 15, 'bold'), bg='grey20', fg='white').pack(pady=(20, 50))
        entry_frame = Frame(self.user_dep, bg='#acf3d4')
        entry_frame.pack()
        self.user_entry = Entry(entry_frame, width=10, font=(
            '', 30, 'bold'), bg='white', fg='grey10', justify='center', state='normal')
        self.user_entry.pack(pady=40, side='left')
        self.user_entry.focus()
        Label(entry_frame, text=" ₹ ", fg='green', font=(
            '', 30, 'bold'), bg='grey10').pack(side='right')

        self.btn_frame = Frame(self.user_dep, background='#acf3d4')
        self.btn_frame.pack()
        Button(self.btn_frame, text='Cancel', font=(
            '', 15, 'bold'), bg='red', fg='white', command=self.exit).pack(side='left', padx=50)
        Button(self.btn_frame, text='Clear', font=(
            '', 15, 'bold'), bg='red', fg='white', command=clear).pack(side='left', padx=30)
        self.submit_btn = Button(self.btn_frame, text='Submit', font=(
            '', 15, 'bold'), bg='green', fg='white', command=dep)
        self.submit_btn.pack(side='right', padx=50)

    def transfer(self):  # ------------   Transfer   ----------------
        self.root.title(" SBI | TRANSFER ")
        self.user_transfer = Frame(
            self.user_win, background="#acf3d4", width=900, height=500)
        self.user_transfer.place(x=0, y=0)

        def cls():
            self.send_entry.delete(0, END)
            self.crf_entry.delete(0, END)
            self.amt_entry.delete(0, END)

        def tra():
            try:
                self.send_ac = int(self.send_entry.get())
                self.crf_ac = int(self.crf_entry.get())
                self.amt = int(self.amt_entry.get())
                if self.send_ac == self.crf_ac and self.crf_ac != self.acno:
                    self.receiver = []
                    self.mycursor.execute(
                        f"select Account_no,Name,balance from userdata where Account_no = {self.crf_ac}")
                    for i in self.mycursor:
                        self.receiver.extend(i)
                    if self.receiver != []:
                        if self.amt < self.user_details[3]:
                            self.mycursor.execute(
                                f"update userdata set balance = {self.user_details[3]-self.amt} where Account_no = {self.user_details[0]}")
                            self.mycursor.execute(
                                f"update userdata set balance = {self.receiver[2]+self.amt} where Account_no = {self.receiver[0]}")
                            confirm = messagebox.askquestion(
                                'SBI | INFO', 'Confirm to Send')
                            if confirm == 'yes':
                                Label(self.user_transfer, text='Money Transfered Succesfully!----' +
                                      f'{dt.datetime.now()}', font=('', 10, 'italic', 'bold'), bg='orange', fg='grey20').place(x=200, y=120)
                                self.mydb.commit()
                                self.user_details[3] -= int(
                                    self.amt_entry.get())
                                cls()
                                show_blnce = messagebox.askquestion(
                                    'SBI | INFO', ' Show Balance ? ')
                                if show_blnce == 'yes':
                                    self.balance()
                                else:
                                    self.user_win.after(0, self.exit)
                            else:
                                pass
                        else:
                            messagebox.showerror(
                                'SBI | Error', 'Insufficient Balance')
                    else:
                        messagebox.showerror(
                            'SBI | Error', 'User Not Found !')
                else:
                    messagebox.showerror(
                        'SBI | Error', 'A/c Not Matched!')
            except Exception as e:
                messagebox.showwarning('SBI | Error', 'Failed')
                cls()

        Label(self.user_transfer, text='TRANSFER', font=(
            '', 30, 'bold'), bg='grey20', fg='white').pack(fill='x', pady=50)
        f_1 = Frame(self.user_transfer, bg='#acf3d4')
        f_1.pack(pady=30)
        Label(
            f_1, text='Recipient a/c  ', bg='grey10', fg="white", font=('', 15, 'bold')).pack(side='left', padx=(50, 0))
        self.send_entry = Entry(
            f_1, width=7, font=('', 16, 'bold'))
        self.send_entry.pack(side='right', padx=(0, 423))
        f_2 = Frame(self.user_transfer, bg='#acf3d4')
        f_2.pack(pady=30)
        Label(
            f_2, text='Confirm  a/c  ', bg='grey10', fg="white", font=('', 15, 'bold')).pack(side='left', padx=(50, 0))
        self.crf_entry = Entry(
            f_2, width=7, font=('', 16, 'bold'))
        self.crf_entry.pack(side='right', padx=(0, 423))
        f_3 = Frame(self.user_transfer, bg='#acf3d4')
        f_3.pack(pady=30)
        Label(
            f_3, text='Amount  ', bg='grey10', fg="white", font=('', 15, 'bold')).pack(side='left', padx=(50, 0))
        self.amt_entry = Entry(
            f_3, width=9, font=('', 16, 'bold'))
        self.amt_entry.pack(side='right', padx=(0, 423))
        f_4 = Frame(self.user_transfer, bg='#acf3d4')
        f_4.pack()
        Button(f_4, text='Send', bg='green', fg='white', font=(
            '', 15, 'bold'), command=tra).pack(side='right', padx=80, pady=50)
        Button(f_4, text='Clear', bg='red', fg='white', font=(
            '', 15, 'bold'), command=cls).pack(side='left', padx=80, pady=50)
        Button(f_4, text='Cancel', bg='red', fg='white', font=(
            '', 15, 'bold'), command=self.exit).pack(pady=50)
        self.send_entry.focus()

    def exit(self):  # ------------   Exit   ----------------
        self.user_win.destroy()
        self.root.title(' SBI | HOME ')
        self.login_entry.focus()
        self.mydb.close()

    def service(self):  # ------------   Service   ----------------

        messagebox.showinfo('SBI | INFO', 'Login Success !')
        self.user_win = Frame(
            self.root, background='#acf3d4', width=700, height=550)
        self.user_win.place(x=0, y=0)
        self.root.title(" SBI | SERVICE ")
        Label(self.user_win, text="SERVICE", font=(
            'arial', 30, 'bold'), bg='grey20', fg='white').pack(side='top', pady=(40, 40), fill='x', ipady=10)
        Label(self.user_win, text="Hello_ "+self.user_details[1].capitalize(), font=(
            'arial', 28, 'bold'), bg='#acf3d4', fg='orange').pack(side='top', pady=20)
        #   ----------------       frame1       ----------------------

        f1_ = Frame(self.user_win, bg='#acf3d4')
        f1_.pack(side='top')
        Button(f1_, text='WithDraw', width=15, font=(
            'arial', 15, 'bold'), command=self.withdraw, bg='#3C4048', fg='white', activebackground='green').pack(side='left', padx=(110, 50), pady=(30, 20))
        Button(f1_, text='Balance', bg='#3C4048', width=15, font=(
            'arial', 15, 'bold'), command=self.balance, fg='white').pack(side='right', padx=(50, 110), pady=(30, 20))
        #     =------------        frame2      -----------------------
        f2_ = Frame(self.user_win, bg='#acf3d4')
        f2_.pack(side='top')
        Button(f2_, text='Pinchange', bg='#3C4048', width=15, font=(
            'arial', 15, 'bold'), command=self.pinchange, fg='white').pack(side='left', padx=(110, 50), pady=20)
        Button(f2_, text='Deposite', bg='#3C4048', width=15, font=(
            'arial', 15, 'bold'), command=self.deposite, fg='white').pack(side='right', padx=(50, 110), pady=20)
        #     =------------        frame2      -----------------------
        f3_ = Frame(self.user_win, bg='#acf3d4')
        f3_.pack(side='top')
        Button(f3_, text='Send', bg='#3C4048', width=15, font=(
            'arial', 15, 'bold'), command=self.transfer, fg='white').pack(side='left', padx=(110, 50), pady=(20, 80))
        Button(f3_, text='Exit', bg='red', width=15, font=(
            'arial', 15, 'bold'), command=self.exit, fg='white').pack(side='right', padx=(50, 110), pady=(20, 80))
        #self.user_win.after(20000, self.exit)

    def submit(self):  # ------------    loginChecker   ---------------------

        if self.login_entry.get().isdigit():
            self.acno = int(self.login_entry.get())
            self.mydb = sqlite3.connect('sbi.db')
            self.mycursor = self.mydb.cursor()
            # self.mycursor.execute(f"select * from userdata")
            # for i in self.mycursor:
            #     print(i)
            self.mycursor.execute(
                f"select * from userdata where Account_no = {self.acno}")
            self.user_details = []
            for i in self.mycursor:
                self.user_details.extend(i)
            if self.user_details != []:
                if self.psw_entry.get() == self.user_details[2]:
                    self.clear()
                    self.service()
                else:
                    messagebox.showerror("SBI | Error", "Incorrect Password !")
                    self.psw_entry.delete(0, END)
            else:
                messagebox.showerror("SBI | Error", "Details Not Found!")
                self.clear()
        else:
            messagebox.showerror("SBI | Error", "Login Failed !")
            self.clear()

    def clear(self):  # ---------------   Clear the fields   ---------------
        self.login_entry.delete(0, END)
        self.psw_entry.delete(0, END)
        self.login_entry.focus()

    def __init__(self, root):  # ---------------   Intializing the AtmApp   --------------

        self.root = root
        self.root.config(bg='#04233b')
        self.root.iconbitmap(r'atm.ico')
        self.root.title(" SBI | HOME ")
        self.root.geometry("700x550+380+140")
        self.root.wm_maxsize(700, 550)
        self.root.wm_minsize(700, 550)
        self.marque = Label(root, text="STATE BANK OF INDIA", bg="#04233b", font=(
            "", 30, "bold"), fg='#acf3d4', justify='center')
        self.marque.place(x=130, y=50)
        frame = Frame(root, width=100, height=100, bg="#04233b")
        frame.pack(pady=(130, 0))
        self.img = ImageTk.PhotoImage(Image.open("log-in.png"))
        self.login_logo = Label(frame, image=self.img, bg="#04233b")
        self.login_logo.pack()
        self.img_ = ImageTk.PhotoImage(Image.open("login.png"))
        self.login_ = Label(frame, image=self.img_, bg="#04233b")
        self.login_.pack(pady=(0, 0))

#       ----------   fram1   ------------
        f1 = Frame(root)
        f1.pack(pady=(10, 30))
        Label(f1, text="A/c number ", font=("", 25, 'bold'),
              bg="orange").pack(side='left')
        self.login_entry = Entry(
            f1, width=14, justify="right", font=("", 25, 'bold'))
        self.login_entry.pack(side='right')
        self.login_entry.focus()
#       ----------   fram2   ------------

        f2 = Frame(root)
        f2.pack(pady=(20, 30))
        Label(f2, text="Password    ",
              font=("", 25, 'bold'), bg="orange").pack(side='left')
        self.psw_entry = Entry(f2, width=14, justify="right",
                               font=("", 25, 'bold'), bg='snow')
        self.psw_entry.pack(side='right')
        self.psw_entry.config(show='*')
#       ----------   fram3   ------------
        f3 = Frame(root, bg='#04233b')
        f3.pack()

        Button(f3, text="Submit", bg="green", font=("", 18), fg="white",
               command=self.submit).pack(side='right', padx=(70, 0))

        Button(f3, text="Clear", bg="red",
               fg="white", font=("", 18), command=self.clear).pack(side='left')
#       ----------   fram4   ------------
        f4 = Frame(root, bg='#04233b')
        f4.pack()
        registration = Label(f4, text="Create a New Account  >>> SIGNUP", bg="#04233b",
                             fg='white', font=('courier', 10, 'bold', 'italic', 'underline'))
        registration.pack(pady=15)
        registration.bind('<Button-1>', self.registration)
        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    start = AtmApp(root)
