from tkinter import *
from tkinter import messagebox

from services import AuthService
from utils import ValidationError, DuplicateAccountError, AtmException
from ui import MessageDialog, ConfirmDialog
import config


class RegistrationWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.auth_service = AuthService()
        self._setup_window()
        self._create_ui()

    def _setup_window(self):
        self.root.title(f"{config.BANK_SHORT} | Account Registration")
        self.root.config(bg=config.COLOR_PRIMARY)
        self.root.iconbitmap(r'atm.ico')
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
        ).pack(pady=(40, 10), fill=X)

        Label(
            self.root,
            text="CREATE NEW ACCOUNT",
            bg=config.COLOR_SECONDARY,
            font=("rockwell", 20, "bold"),
            fg='grey10',
            justify='center'
        ).pack(pady=10, fill=X, ipady=10)

        self.t_frame = LabelFrame(
            self.root,
            text="  User Details >> ",
            bg=config.COLOR_PRIMARY,
            font=('', 15, 'italic', 'bold'),
            fg=config.COLOR_SECONDARY
        )
        self.t_frame.pack(ipadx=15)

        self._create_form_fields()
        self._create_buttons()
        self._create_login_link()

    def _create_form_fields(self):
        self.f1 = Frame(self.t_frame, bg=config.COLOR_PRIMARY)
        self.f1.pack(pady=(30, 20))

        Label(
            self.f1,
            text="Account Number ",
            bg=config.COLOR_SECONDARY,
            font=('', 15, 'bold')
        ).pack(side='left')

        self.num_entry = Entry(self.f1, font=('', 17, 'bold'), width=8, justify='center')
        self.num_entry.pack(side='left')
        self.num_entry.insert(0, self.auth_service.user_repo.get_next_account_number())
        self.num_entry.config(state='readonly')

        self.name_entry = Entry(self.f1, font=('', 17, 'bold'), width=15)
        self.name_entry.focus()
        self.name_entry.pack(side='right')

        Label(
            self.f1,
            text="User Name ",
            bg=config.COLOR_SECONDARY,
            font=('', 15, 'bold')
        ).pack(side='right', padx=(30, 0))

        self.f2 = Frame(self.t_frame, bg=config.COLOR_PRIMARY)
        self.f2.pack(pady=15)

        Label(
            self.f2,
            text="Password ",
            bg=config.COLOR_SECONDARY,
            font=('', 15, 'bold')
        ).pack(side='left')

        self.psw_entry = Entry(self.f2, font=('', 17, 'bold'), width=8, show='*')
        self.psw_entry.pack(side='left')

        self.crf_psw_entry = Entry(self.f2, font=('', 17, 'bold'), width=8, show='*')
        self.crf_psw_entry.pack(side='right')

        Label(
            self.f2,
            text="Confirm Password ",
            bg=config.COLOR_SECONDARY,
            font=('', 15, 'bold')
        ).pack(side='right', padx=(110, 0))

        self.f3 = Frame(self.t_frame, bg=config.COLOR_PRIMARY)
        self.f3.pack(pady=20)

        Label(
            self.f3,
            text="Initial Balance ",
            bg=config.COLOR_SECONDARY,
            font=('', 15, 'bold')
        ).pack(side='left')

        self.blnc_entry = Entry(self.f3, font=('', 17, 'bold'), width=8, justify='center')
        self.blnc_entry.pack(side='left')

        Label(
            self.f3,
            text=" ₹ (Min: 100) ",
            bg=config.COLOR_PRIMARY,
            fg=config.COLOR_SECONDARY,
            font=('', 12, 'bold')
        ).pack(side='left', padx=(10, 0))

    def _create_buttons(self):
        b_frame = Frame(self.root, bg=config.COLOR_PRIMARY)
        b_frame.pack(pady=(20, 10))

        Button(
            b_frame,
            text="Save",
            bg="green",
            font=("", 18),
            fg="white",
            command=self._handle_registration
        ).pack(side=RIGHT, padx=(70, 0), ipadx=10)

        Button(
            b_frame,
            text="Reset",
            bg="red",
            fg="white",
            font=("", 18),
            command=self._reset_fields
        ).pack(side=LEFT, ipadx=10)

    def _create_login_link(self):
        bottom4 = Frame(self.root, bg=config.COLOR_PRIMARY)
        bottom4.pack(pady=10)

        registration = Label(
            bottom4,
            text="Already have an account  >>> LOGIN",
            bg=config.COLOR_PRIMARY,
            fg='white',
            font=('courier', 10, 'bold', 'italic', 'underline')
        )
        registration.pack()
        registration.bind('<Button-1>', self._open_login)

    def _handle_registration(self):
        name = self.name_entry.get().strip()
        pin = self.psw_entry.get().strip()
        confirm_pin = self.crf_psw_entry.get().strip()
        balance_str = self.blnc_entry.get().strip()

        if not name or not pin or not confirm_pin or not balance_str:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ALERT", "All fields are required")
            return

        try:
            balance = float(balance_str)
        except ValueError:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ALERT", "Please enter a valid balance amount")
            return

        try:
            result = self.auth_service.register(name, pin, confirm_pin, balance)

            confirm = ConfirmDialog.ask_yes_no(
                f"{config.BANK_SHORT} | CONFIRM",
                f"Save account details?\n\n"
                f"Account No: {result['account_number']}\n"
                f"Name: {result['name']}\n"
                f"Initial Balance: ₹{result['balance']}"
            )

            if confirm:
                MessageDialog.show_info(
                    f"{config.BANK_SHORT} | SUCCESS",
                    f"Account created successfully!\n\n"
                    f"Account Number: {result['account_number']}\n"
                    f"Name: {result['name']}\n\n"
                    f"Please remember your account number and PIN."
                )
                self._reset_fields()
                self.num_entry.config(state='normal')
                self.num_entry.delete(0, END)
                self.num_entry.insert(0, self.auth_service.user_repo.get_next_account_number())
                self.num_entry.config(state='readonly')

        except (ValidationError, DuplicateAccountError) as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ALERT", e.message)
        except AtmException as e:
            MessageDialog.show_error(f"{config.BANK_SHORT} | ERROR", e.message)

    def _reset_fields(self):
        self.name_entry.delete(0, END)
        self.psw_entry.delete(0, END)
        self.crf_psw_entry.delete(0, END)
        self.blnc_entry.delete(0, END)
        self.name_entry.focus()

    def _open_login(self, event=None):
        self.root.destroy()
        from main import LoginWindow
        root = Tk()
        app = LoginWindow(root)


if __name__ == '__main__':
    root = Tk()
    app = RegistrationWindow(root)
    root.mainloop()