from tkinter import *
from tkinter import ttk, messagebox
from typing import Optional, Callable
import config


class InputField:
    def __init__(
        self,
        parent: Widget,
        width: int = 20,
        font: tuple = ('', 12),
        show: Optional[str] = None,
        justify: str = 'left'
    ):
        self.entry = Entry(
            parent,
            width=width,
            font=font,
            bg='white',
            fg='black',
            justify=justify
        )
        if show:
            self.entry.config(show=show)

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)

    def place(self, **kwargs):
        self.entry.place(**kwargs)

    def get(self) -> str:
        return self.entry.get()

    def delete(self, start: int = 0, end: int = END):
        self.entry.delete(start, end)

    def insert(self, index: int, text: str):
        self.entry.insert(index, text)

    def focus(self):
        self.entry.focus()

    def config(self, **kwargs):
        self.entry.config(**kwargs)

    def bind(self, sequence: str, func: Callable):
        self.entry.bind(sequence, func)

    @property
    def widget(self):
        return self.entry


class StyledButton:
    def __init__(
        self,
        parent: Widget,
        text: str,
        command: Callable,
        bg: str = config.COLOR_SUCCESS,
        fg: str = 'white',
        width: int = 12,
        font: tuple = ('', 12, 'bold')
    ):
        self.button = Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            width=width,
            font=font,
            relief='raised',
            bd=2
        )

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def place(self, **kwargs):
        self.button.place(**kwargs)

    def config(self, **kwargs):
        self.button.config(**kwargs)

    def state(self, state: str):
        self.button.config(state=state)

    @property
    def widget(self):
        return self.button


class MessageDialog:
    @staticmethod
    def show_error(title: str, message: str):
        messagebox.showerror(title, message)

    @staticmethod
    def show_info(title: str, message: str):
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning(title: str, message: str):
        messagebox.showwarning(title, message)


class ConfirmDialog:
    @staticmethod
    def ask_yes_no(title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)

    @staticmethod
    def ask_ok_cancel(title: str, message: str) -> bool:
        return messagebox.askokcancel(title, message)

    @staticmethod
    def ask_yes_no_cancel(title: str, message: str) -> Optional[bool]:
        return messagebox.askyesnocancel(title, message)