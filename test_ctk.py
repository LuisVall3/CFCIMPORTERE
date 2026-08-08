import customtkinter as ctk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("500x300")

label = ctk.CTkLabel(
    app,
    text="PRUEBA CUSTOM TKINTER",
    width=300,
    height=50
)

label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

app.mainloop()