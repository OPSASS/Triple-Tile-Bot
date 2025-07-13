import customtkinter as ctk
import tkinter as tk


class Notification(ctk.CTkToplevel):
    def __init__(self, master, message="Thông báo", duration=3000, border_color="gray", border_width=2):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0)

        # Border bằng frame bên ngoài
        self.border_frame = ctk.CTkFrame(
            self, corner_radius=8, border_color=border_color, border_width=border_width)
        self.border_frame.pack(padx=1, pady=1)

        # Nội dung thông báo
        self.label = ctk.CTkLabel(
            self.border_frame, text=message, padx=15, pady=0)
        self.label.pack()

        self.update_idletasks()
        w = self.label.winfo_reqwidth()
        h = self.label.winfo_reqheight() - 12
        x = self.winfo_screenwidth() // 2 - w // 2
        y = 24
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Hiệu ứng fade-in
        self.fade_in()

        # Đặt thời gian hiển thị, sau đó fade-out rồi đóng
        self.after(duration, self.fade_out)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.1
            self.attributes("-alpha", alpha)
            self.after(30, self.fade_in)

    def fade_out(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.1
            self.attributes("-alpha", alpha)
            self.after(30, self.fade_out)
        else:
            self.destroy()
