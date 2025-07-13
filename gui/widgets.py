import customtkinter as ctk


def create_button(master, text, command=None, **kwargs):
    return ctk.CTkButton(master, text=text, command=command, **kwargs)


def create_label(master, text, size=12, weight="normal", **kwargs):
    return ctk.CTkLabel(master, text=text, font=ctk.CTkFont(size=size, weight=weight), **kwargs)


def create_frame(master, **kwargs):
    return ctk.CTkFrame(master, **kwargs)


def create_textbox(master, height=100, **kwargs):
    return ctk.CTkTextbox(master, height=height, **kwargs)
