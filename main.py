from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime as dt
import re

from services import AuthService, AccountService, TransactionService
from utils import (
    ValidationError,
    AuthenticationError,
    InsufficientFundsError,
    InvalidAccountError,
    AtmException
)
from ui import MessageDialog, ConfirmDialog
import config


class LoginWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.current_user = None
        self.user_window = None
        self._setup_window()
        self._create_ui()

    def _setup_window(self):
        self.root.config(bg=config.COLOR_PRIMARY)
        self.root.iconbitmap(r'atm.ico')
        self.root.title(f"{config.BANK_SHORT} | HOME")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+380+140")
        self.root.wm_maxsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.root.wm_minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    def _create_ui(self):
        Label(
            self.root,
            text=config.BANK_NAME,
            bg=config.COLOR_PRIMARY,
            font=("", 30, "bold"),
            fg=config.COLOR_SECONDARY,
            justify='center'
        ).place(x=130, y=50)

        frame = Frame(self.root, width=100, height=100, bg=config.COLOR_PRIMARY)
        frame.place(x=300, y=130)

        self.img = ImageTk.PhotoImage(Image.open("log-in.png"))
        Label(frame, image=self.img, bg=config.COLOR_PRIMARY).pack()

        self.img_ = ImageTk.PhotoImage(Image.open("login.png"))
        Label(frame, image=self.img_, bg=config.COLOR_PRIMARY).pack(pady=0)

        f1 = Frame(self.root)
        f1.place(x=150, y=310)
        Label(f1, text="A/c number ", font=("", 25, 'bold'), bg=config.COLOR_PRIMARY, fg=config.COLOR_SECONDARY).pack(side='left')
        self.login_entry = Entry(f1, width=14, justify="right", font=("", 25, 'bold'))
        self.login_entry.pack(side='right')
        self.login_entry.focus()

        f2 = Frame(self.root)
        f2.place(x=150, y=370)
        Label(f2, text="Password    ", font=("", 25, 'bold'), bg=config.COLOR_PRIMARY, fg=config.COLOR_SECONDARY).pack(side='left')
        self.psw_entry = Entry(f2, width=14, justify="right", font=("", 25, 'bold'), bg='snow')
        self.psw_entry.pack(side='right')
        self.psw_entry.config(show='*')

        f3 = Frame(self.root, bg=config.COLOR_PRIMARY)
        f3.place(x=200, y=430)
        Button(f3, text="Submit", bg="green", font=("", 18), fg="white", command=self._handle_login).pack(side='right', padx=(70, 0))
        Button(f3, text="Clear", bg="red", fg="white", font=("", 18), command=self._clear_fields).pack(side='left')

        f4 = Frame(self.root, bg=config.COLOR_PRIMARY)
        f4.place(x=180, y=500)
        registration = Label(
            f4,
            text="Create a New Account  >>> SIGNUP",
            bg=config.COLOR_PRIMARY,
            fg='white',
            font=('courier', 10, 'bold', 'italic', 'underline')
        )
        registration.pack(pady=15)
        registration.bind('<Button-1>', self._open_registration)

    def _handle_login(self):
        account_number = self.login_entry.get().strip()
        pin = self.psw_entry.get().strip()

        try:
            self.current_user = self.auth_service.login(account_number, pin)
            MessageDialog.show_info(f"{config.BANK_SHORT} | SUCCESS", "Login Successful!")
            self._open_service_window()
        except (AuthenticationError, ValidationError) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)
            self._clear_fields()
        except AtmException as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)

    def _clear_fields(self):
        self.login_entry.delete(0, END)
        self.psw_entry.delete(0, END)
        self.login_entry.focus()

    def _open_registration(self, event=None):
        self.root.destroy()
        from signup_app import RegistrationWindow
        root = Tk()
        app = RegistrationWindow(root)

    def _open_service_window(self):
        self.root.withdraw()
        ServiceWindow(self.root, self.current_user, self.transaction_service, self.account_service)


class ServiceWindow:
    count = 0

    def __init__(self, parent, user_data: dict, transaction_service: TransactionService, account_service: AccountService):
        self.parent = parent
        self.user_data = user_data
        self.transaction_service = transaction_service
        self.account_service = account_service

        self.user_win = Toplevel(parent)
        self.user_win.config(bg=config.COLOR_SECONDARY)
        self.user_win.title(f"{config.BANK_SHORT} | SERVICE")
        self.user_win.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+380+140")
        self.user_win.wm_maxsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.user_win.wm_minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self._create_service_ui()
        self.user_win.protocol("WM_DELETE_WINDOW", self._handle_exit)

    def _create_service_ui(self):
        Label(
            self.user_win,
            text="SERVICE",
            font=('arial', 30, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(side='top', pady=(40, 40), fill='x', ipady=10)

        Label(
            self.user_win,
            text=f"Hello, {self.user_data['name'].capitalize()}",
            font=('arial', 28, 'bold'),
            bg=config.COLOR_SECONDARY,
            fg='orange'
        ).pack(side='top', pady=20)

        f1_ = Frame(self.user_win, bg=config.COLOR_SECONDARY)
        f1_.pack(side='top')
        Button(
            f1_,
            text='Withdraw',
            width=15,
            font=('arial', 15, 'bold'),
            command=self._withdraw,
            bg='#3C4048',
            fg='white',
            activebackground='green'
        ).pack(side='left', padx=(110, 50), pady=(30, 20))
        Button(
            f1_,
            text='Balance',
            bg='#3C4048',
            width=15,
            font=('arial', 15, 'bold'),
            command=self._show_balance,
            fg='white'
        ).pack(side='right', padx=(50, 110), pady=(30, 20))

        f2_ = Frame(self.user_win, bg=config.COLOR_SECONDARY)
        f2_.pack(side='top')
        Button(
            f2_,
            text='Pinchange',
            bg='#3C4048',
            width=15,
            font=('arial', 15, 'bold'),
            command=self._pin_change,
            fg='white'
        ).pack(side='left', padx=(110, 50), pady=20)
        Button(
            f2_,
            text='Deposit',
            bg='#3C4048',
            width=15,
            font=('arial', 15, 'bold'),
            command=self._deposit,
            fg='white'
        ).pack(side='right', padx=(50, 110), pady=20)

        f3_ = Frame(self.user_win, bg=config.COLOR_SECONDARY)
        f3_.pack(side='top')
        Button(
            f3_,
            text='Send',
            bg='#3C4048',
            width=15,
            font=('arial', 15, 'bold'),
            command=self._transfer,
            fg='white'
        ).pack(side='left', padx=(110, 50), pady=(20, 80))
        Button(
            f3_,
            text='Exit',
            bg='red',
            width=15,
            font=('arial', 15, 'bold'),
            command=self._handle_exit,
            fg='white'
        ).pack(side='right', padx=(50, 110), pady=(20, 80))

    def _withdraw(self):
        self.user_win.withdraw()
        WithdrawWindow(
            self.user_win,
            self.user_data,
            self.transaction_service,
            lambda: self._return_to_service()
        )

    def _deposit(self):
        self.user_win.withdraw()
        DepositWindow(
            self.user_win,
            self.user_data,
            self.transaction_service,
            lambda: self._return_to_service()
        )

    def _show_balance(self):
        try:
            balance = self.account_service.get_balance(self.user_data['id'])
            confirm = ConfirmDialog.ask_yes_no(
                f"{config.BANK_SHORT} | BALANCE",
                f"Account: {self.user_data['account_number']}\n\n"
                f"Name: {self.user_data['name'].capitalize()}\n\n"
                f"Balance: ₹ {balance:.2f}\n\n"
                f"Last Checked: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Click YES to keep showing, NO to return"
            )
            if not confirm:
                self._return_to_service()
        except AtmException as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)

    def _pin_change(self):
        self.user_win.withdraw()
        PinChangeWindow(
            self.user_win,
            self.user_data,
            self.auth_service,
            lambda: self._return_to_service()
        )

    def _transfer(self):
        self.user_win.withdraw()
        TransferWindow(
            self.user_win,
            self.user_data,
            self.transaction_service,
            lambda: self._return_to_service()
        )

    def _return_to_service(self):
        self.user_data['balance'] = self.account_service.get_balance(self.user_data['id'])
        self.user_win.deiconify()

    def _handle_exit(self):
        self.user_win.destroy()
        self.parent.deiconify()
        self.parent.focus()


class WithdrawWindow:
    def __init__(self, parent, user_data: dict, transaction_service: TransactionService, on_success):
        self.parent = parent
        self.user_data = user_data
        self.transaction_service = transaction_service
        self.on_success = on_success
        self.window = Toplevel(parent)
        self._create_ui()

    def _create_ui(self):
        self.window.title(f"{config.BANK_SHORT} | WITHDRAW")
        self.window.config(bg=config.COLOR_SECONDARY)
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+380+140")

        Label(
            self.window,
            text='WITHDRAW',
            font=('', 30, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(side='top', fill='x', pady=50)

        Label(
            self.window,
            text=' Enter Amount ',
            font=('', 15, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(pady=(50, 30), padx=285)

        Label(
            self.window,
            text=' NOTE: Enter amounts in multiples of 100 (100, 200, 500, 2000) ',
            font=('', 15, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(pady=(20, 50))

        f1 = Frame(self.window, bg=config.COLOR_SECONDARY)
        f1.pack()
        self.amount_entry = Entry(f1, width=10, font=('', 30, 'bold'), bg='white', fg='grey10', justify='center')
        self.amount_entry.pack(side='left')
        self.amount_entry.focus()
        Label(f1, text=" ₹ ", fg='green', font=('', 30, 'bold'), bg='grey10').pack(side='right')

        f2 = Frame(self.window, bg=config.COLOR_SECONDARY)
        f2.pack()
        Button(
            f2,
            text='Cancel',
            font=('', 15, 'bold'),
            bg='red',
            fg='white',
            command=self._cancel
        ).pack(side='left', pady=30, padx=100)
        Button(
            f2,
            text='Clear',
            font=('', 15, 'bold'),
            bg='red',
            fg='white',
            command=lambda: self.amount_entry.delete(0, END)
        ).pack(side='left')
        Button(
            f2,
            text='Submit',
            font=('', 15, 'bold'),
            bg='green',
            fg='white',
            command=self._handle_withdraw
        ).pack(side='right', padx=100)

    def _handle_withdraw(self):
        amount = self.amount_entry.get().strip()
        if not amount:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Please enter an amount")
            return

        try:
            amount_int = int(amount)
        except ValueError:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Invalid amount entered")
            self.amount_entry.delete(0, END)
            return

        try:
            confirm = ConfirmDialog.ask_yes_no(
                f"{config.BANK_SHORT} | CONFIRM",
                f"Confirm withdrawal of ₹{amount_int}?"
            )
            if not confirm:
                self.amount_entry.delete(0, END)
                return

            result = self.transaction_service.withdraw(self.user_data['id'], amount_int)
            MessageDialog.show_info(
                f"{config.BANK_SHORT} | SUCCESS",
                f"Withdrawal successful!\n\nAmount: ₹{amount_int}\nBalance: ₹{result['new_balance']:.2f}"
            )
            self.window.destroy()
            self.on_success()
        except (ValidationError, InsufficientFundsError) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)
            self.amount_entry.delete(0, END)
        except (ValueError, Exception) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Invalid amount entered")
            self.amount_entry.delete(0, END)

    def _cancel(self):
        self.window.destroy()
        self.on_success()


class DepositWindow:
    def __init__(self, parent, user_data: dict, transaction_service: TransactionService, on_success):
        self.parent = parent
        self.user_data = user_data
        self.transaction_service = transaction_service
        self.on_success = on_success
        self.window = Toplevel(parent)
        self._create_ui()

    def _create_ui(self):
        self.window.title(f"{config.BANK_SHORT} | DEPOSIT")
        self.window.config(bg=config.COLOR_SECONDARY)
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+380+140")

        Label(
            self.window,
            text=' DEPOSIT ',
            font=('', 30, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(side='top', fill='x', pady=50)

        Label(
            self.window,
            text=' Enter Amount ',
            font=('', 20, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(pady=10, padx=260)

        Label(
            self.window,
            text=' NOTE: Enter amounts in multiples of 100 (100, 200, 500, 2000) ',
            font=('', 15, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(pady=(20, 50))

        entry_frame = Frame(self.window, bg=config.COLOR_SECONDARY)
        entry_frame.pack()
        self.amount_entry = Entry(entry_frame, width=10, font=('', 30, 'bold'), bg='white', fg='grey10', justify='center')
        self.amount_entry.pack(pady=40, side='left')
        self.amount_entry.focus()
        Label(entry_frame, text=" ₹ ", fg='green', font=('', 30, 'bold'), bg='grey10').pack(side='right')

        btn_frame = Frame(self.window, background=config.COLOR_SECONDARY)
        btn_frame.pack()
        Button(
            btn_frame,
            text='Cancel',
            font=('', 15, 'bold'),
            bg='red',
            fg='white',
            command=self._cancel
        ).pack(side='left', padx=50)
        Button(
            btn_frame,
            text='Clear',
            font=('', 15, 'bold'),
            bg='red',
            fg='white',
            command=lambda: self.amount_entry.delete(0, END)
        ).pack(side='left', padx=30)
        Button(
            btn_frame,
            text='Submit',
            font=('', 15, 'bold'),
            bg='green',
            fg='white',
            command=self._handle_deposit
        ).pack(side='right', padx=50)

    def _handle_deposit(self):
        amount = self.amount_entry.get().strip()
        if not amount:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Please enter an amount")
            return

        try:
            amount_int = int(amount)
        except ValueError:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Invalid amount entered")
            self.amount_entry.delete(0, END)
            return

        try:
            confirm = ConfirmDialog.ask_yes_no(
                f"{config.BANK_SHORT} | CONFIRM",
                f"Confirm deposit of ₹{amount_int}?"
            )
            if not confirm:
                self.amount_entry.delete(0, END)
                return

            result = self.transaction_service.deposit(self.user_data['id'], amount_int)
            MessageDialog.show_info(
                f"{config.BANK_SHORT} | SUCCESS",
                f"Deposit successful!\n\nAmount: ₹{amount_int}\nNew Balance: ₹{result['new_balance']:.2f}"
            )
            self.window.destroy()
            self.on_success()
        except (ValidationError, Exception) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", str(e))
            self.amount_entry.delete(0, END)

    def _cancel(self):
        self.window.destroy()
        self.on_success()


class PinChangeWindow:
    def __init__(self, parent, user_data: dict, auth_service: AuthService, on_success):
        self.parent = parent
        self.user_data = user_data
        self.auth_service = auth_service
        self.on_success = on_success
        self.window = Toplevel(parent)
        self._create_ui()

    def _create_ui(self):
        self.window.title(f"{config.BANK_SHORT} | PIN CHANGE")
        self.window.config(bg=config.COLOR_SECONDARY)
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+380+140")

        Label(
            self.window,
            text='PIN CHANGE',
            font=("", 30, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(side='top', fill='x', pady=50)

        f = Frame(self.window, bg=config.COLOR_SECONDARY)
        f.pack()

        f1 = Frame(f, bg=config.COLOR_SECONDARY)
        f1.pack(side='left')
        Label(f1, text='Enter Old PIN    ', font=('', 15, 'bold'), bg='grey20', fg='white').pack(padx=(50, 0), pady=21)
        Label(f1, text='New PIN  ', font=('', 15, 'bold'), bg='grey20', fg='white').pack(padx=(50, 0), pady=21)
        Label(f1, text='Confirm PIN     ', font=('', 15, 'bold'), bg='grey20', fg='white').pack(padx=(50, 0), pady=21)

        f2 = Frame(f, bg=config.COLOR_SECONDARY)
        f2.pack(side='right')
        self.old_pin = Entry(f2, width=7, font=('', 18, 'bold'))
        self.old_pin.pack(padx=(0, 412), pady=20)
        self.old_pin.focus()
        self.old_pin.config(show='*')

        self.new_pin = Entry(f2, width=7, font=('', 18, 'bold'))
        self.new_pin.pack(padx=(0, 412), pady=20)
        self.new_pin.config(show='*')

        self.confirm_pin = Entry(f2, width=7, font=('', 18, 'bold'))
        self.confirm_pin.pack(padx=(0, 412), pady=20)
        self.confirm_pin.config(show='*')

        b_f = Frame(self.window, bg=config.COLOR_SECONDARY)
        b_f.pack(pady=52)

        Button(
            b_f,
            text='Confirm',
            font=('', 15, 'bold'),
            bg='green',
            fg='white',
            command=self._handle_change
        ).pack(side='right', pady=20, padx=80)

        Button(
            b_f,
            text='Clear',
            font=('', 15, 'bold'),
            bg='red',
            fg='white',
            command=self._clear_fields
        ).pack(side='left', pady=20, padx=80)

        Button(
            b_f,
            text='Cancel',
            font=('', 15, 'bold'),
            bg='red',
            fg='white',
            command=self._cancel
        ).pack(side='right', pady=20)

    def _handle_change(self):
        old_pin = self.old_pin.get().strip()
        new_pin = self.new_pin.get().strip()
        confirm_pin = self.confirm_pin.get().strip()

        if not old_pin or not new_pin or not confirm_pin:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "All fields are required")
            return

        if new_pin != confirm_pin:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "New PINs do not match")
            self._clear_fields()
            return

        try:
            self.auth_service.change_pin(self.user_data['id'], old_pin, new_pin)
            MessageDialog.show_info(f"{config.BANK_SHORT} | SUCCESS", "PIN changed successfully!")
            self.window.destroy()
            self.on_success()
        except (AuthenticationError, ValidationError) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)
            self._clear_fields()

    def _clear_fields(self):
        self.old_pin.delete(0, END)
        self.new_pin.delete(0, END)
        self.confirm_pin.delete(0, END)
        self.old_pin.focus()

    def _cancel(self):
        self.window.destroy()
        self.on_success()


class TransferWindow:
    def __init__(self, parent, user_data: dict, transaction_service: TransactionService, on_success):
        self.parent = parent
        self.user_data = user_data
        self.transaction_service = transaction_service
        self.on_success = on_success
        self.window = Toplevel(parent)
        self._create_ui()

    def _create_ui(self):
        self.window.title(f"{config.BANK_SHORT} | TRANSFER")
        self.window.config(bg=config.COLOR_SECONDARY)
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+380+140")

        Label(
            self.window,
            text='TRANSFER',
            font=('', 30, 'bold'),
            bg='grey20',
            fg='white'
        ).pack(fill='x', pady=50)

        f_1 = Frame(self.window, bg=config.COLOR_SECONDARY)
        f_1.pack(pady=30)
        Label(f_1, text='Recipient A/C  ', bg='grey10', fg="white", font=('', 15, 'bold')).pack(side='left', padx=(50, 0))
        self.recipient_entry = Entry(f_1, width=12, font=('', 16, 'bold'))
        self.recipient_entry.pack(side='right', padx=(0, 400))
        self.recipient_entry.focus()

        f_2 = Frame(self.window, bg=config.COLOR_SECONDARY)
        f_2.pack(pady=30)
        Label(f_2, text='Confirm A/C  ', bg='grey10', fg="white", font=('', 15, 'bold')).pack(side='left', padx=(50, 0))
        self.confirm_entry = Entry(f_2, width=12, font=('', 16, 'bold'))
        self.confirm_entry.pack(side='right', padx=(0, 400))

        f_3 = Frame(self.window, bg=config.COLOR_SECONDARY)
        f_3.pack(pady=30)
        Label(f_3, text='Amount  ', bg='grey10', fg="white", font=('', 15, 'bold')).pack(side='left', padx=(50, 0))
        self.amount_entry = Entry(f_3, width=12, font=('', 16, 'bold'))
        self.amount_entry.pack(side='right', padx=(0, 400))

        f_4 = Frame(self.window, bg=config.COLOR_SECONDARY)
        f_4.pack()
        Button(
            f_4,
            text='Send',
            bg='green',
            fg='white',
            font=('', 15, 'bold'),
            command=self._handle_transfer
        ).pack(side='right', padx=80, pady=50)
        Button(
            f_4,
            text='Clear',
            bg='red',
            fg='white',
            font=('', 15, 'bold'),
            command=self._clear_fields
        ).pack(side='left', padx=80, pady=50)
        Button(
            f_4,
            text='Cancel',
            bg='red',
            fg='white',
            font=('', 15, 'bold'),
            command=self._cancel
        ).pack(pady=50)

    def _handle_transfer(self):
        recipient = self.recipient_entry.get().strip()
        confirm_acct = self.confirm_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not recipient or not confirm_acct or not amount:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "All fields are required")
            return

        if recipient != confirm_acct:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Account numbers do not match")
            self._clear_fields()
            return

        try:
            amount_int = int(amount)
        except ValueError:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Invalid amount")
            self._clear_fields()
            return

        try:
            confirm_dialog = ConfirmDialog.ask_yes_no(
                f"{config.BANK_SHORT} | CONFIRM",
                f"Transfer ₹{amount_int} to account {recipient}?"
            )
            if not confirm_dialog:
                self._clear_fields()
                return

            result = self.transaction_service.transfer(
                self.user_data['id'],
                recipient,
                amount_int
            )
            MessageDialog.show_info(
                f"{config.BANK_SHORT} | SUCCESS",
                f"Transfer successful!\n\n"
                f"Amount: ₹{amount_int}\n"
                f"To: {result['recipient']}\n"
                f"Balance: ₹{result['new_balance']:.2f}"
            )
            self.window.destroy()
            self.on_success()
        except (ValidationError, InvalidAccountError, InsufficientFundsError) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)
            self._clear_fields()
        except ValueError:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", "Invalid amount")
            self._clear_fields()

    def _clear_fields(self):
        self.recipient_entry.delete(0, END)
        self.confirm_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        self.recipient_entry.focus()

    def _cancel(self):
        self.window.destroy()
        self.on_success()


if __name__ == '__main__':
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()