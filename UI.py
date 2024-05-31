import customtkinter
import Main


class ModList(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.name = Main.get_mod_names()
        print(self.name)
        self.mod_list = []

        for i, name in enumerate(self.name):
            mod_name = customtkinter.CTkLabel(self, text=name)
            mod_name.configure(font=("Arial", 20))
            mod_name.bind("<Double-Button-1>", self.clickable)
            mod_name.grid(row=i, column=0, padx=10, pady=(0, 5), sticky="w")
            self.mod_list.append(mod_name)

    def clickable(self, event):
        print("Натиснуто")

    def copy(self, event):
        self.clipboard_clear()
        self.clipboard_append(event.widget.cget("text").replace("id-", ""))


class App(customtkinter.CTk):
    def __init__(self):
        # Налаштування вікна
        super().__init__()
        self.title("Конструктор перекладу")
        self.geometry("800x600")
        self.minsize(420, 600)
        self.maxsize(420, 600)
        self.configure()
        #self.config(bg="#1f1f1f")

        # Сітка
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Вікно списку модів
        self.ModListFrame = customtkinter.CTkFrame(self)
        self.ModListFrame.configure(fg_color="#1e1f22", corner_radius=0)
        self.ModListFrame.grid(row=0, column=1, padx=0, pady=0, sticky="ens")
        # Рядок пошуку в списку моодів
        self.SearchString = customtkinter.CTkEntry(self.ModListFrame)
        self.SearchString.configure(width=400, height=35, corner_radius=0, fg_color="#2b2d30", border_color="", font=("Arial", 15), placeholder_text="Пошук (назва, автор, айді)")
        self.SearchString.grid(row=0, column=0, padx=10, pady=10, sticky="ens")

        self.mod_list = ModList(self.ModListFrame)
        self.mod_list.configure(height=500, fg_color="#1e1f22", corner_radius=0)
        self.mod_list.grid(row=1, column=0, padx=10, pady=10, sticky="we")


app = App()
app.mainloop()

