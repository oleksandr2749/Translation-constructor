import customtkinter
import ModificationClass


class App(customtkinter.CTk):
    def __init__(self, mod_object_list):
        # Налаштування вікна
        super().__init__()

        self.title("Конструктор перекладу")
        self.geometry("800x600")
        #self.minsize(420, 600)
        #self.maxsize(420, 600)
        self.configure()

        # Сітка
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Рамка списку модів
        self.ModListFrame = customtkinter.CTkScrollableFrame(self)
        self.ModListFrame.configure(corner_radius=0)
        self.ModListFrame.grid(row=1, column=0, padx=0, pady=0, sticky="wens")

        # Рядок пошуку
        self.SearchString = customtkinter.CTkEntry(self)
        self.SearchString.configure(width=400, height=35, corner_radius=0, font=("Arial", 15), placeholder_text="Пошук")
        self.SearchString.grid(row=0, column=0, padx=10, pady=10, sticky="wn")

        for i, mod_object in enumerate(mod_object_list):
            self.ModLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.ModLabel.configure(text=mod_object.return_name())
            self.ModLabel.bind("<Double-Button-1>", lambda event, idx=i: self.clickable(event, idx))
            self.ModLabel.grid(row=i+1, column=0, padx=10, pady=0, sticky="w")

    def clickable(self, event, idx):
        print(f'Натиснуто {mod_object_list[idx].return_name()}')


mod_object_list = ModificationClass.create_mod_object_list()

app = App(mod_object_list)
app.mainloop()
