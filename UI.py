import customtkinter
import Main


class ModList(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.name = Main.ModNames
        self.identifier = Main.ModId
        self.mod_list = []

        for i, (name, identifier) in enumerate(zip(self.name, self.identifier)):
            mod_name = customtkinter.CTkLabel(self, text=name)
            mod_name.configure(font=("Arial", 25))
            mod_name.bind("<Double-Button-1>", self.clickable)
            mod_name.grid(row=i * 2, column=0, padx=10, pady=0, sticky="w")
            self.mod_list.append(mod_name)

            mod_id = customtkinter.CTkLabel(self, text=f"ID - {identifier}")
            mod_id.configure(font=("Arial", 15), text_color="Gray")
            mod_id.bind("<Double-Button-1>", self.copy)
            mod_id.grid(row=i * 2 + 1, column=0, padx=10, pady=0, sticky="w")
            self.mod_list.append(mod_id)

    def clickable(self, event):
        print("Натиснуто")

    def copy(self, event):
        pass


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
        self.SearchString.configure(width=400, height=35, corner_radius=0, fg_color="#2b2d30", border_color="", font=("Arial", 15), placeholder_text="Пошук")
        self.SearchString.grid(row=0, column=0, padx=10, pady=10, sticky="ens")

        self.mod_list_frame = ModList(self.ModListFrame)
        self.mod_list_frame.configure(fg_color="#1e1f22", corner_radius=0)
        self.mod_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")


app = App()
app.mainloop()

