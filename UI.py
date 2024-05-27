import customtkinter


class ModLisn(customtkinter.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = values
        self.labels = []

        for i, value in enumerate(self.values):
            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i, column=0, padx=10, sticky="w")
            label.bind("<Double-Button-1>", self.clickable)
            self.labels.append(label)

    def clickable(self, event):
        print("Настинуто")


class App(customtkinter.CTk):
    def __init__(self, title, size, mod_names):
        # Налаштування вікна
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.maxsize(size[0], size[1])
        self.config(bg="#1f1f1f")
        self.modNames = mod_names

        # Сітка
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Елементи вікна
        # Вікно списку модів
        self.ModListFrame = customtkinter.CTkFrame(self, corner_radius=0)
        self.ModListFrame.grid(row=0, column=1, padx=0, pady=0, sticky="ens")
        # Рядок пошуку в списку моодів
        self.SearchString = customtkinter.CTkEntry(self.ModListFrame, width=400, corner_radius=0, placeholder_text="Пошук")
        self.SearchString.grid(row=0, column=0, padx=10, pady=10, sticky="ens")
        # Список модів
        self.ModList = ModLisn(self.ModListFrame, values=self.modNames)
        self.ModList.configure(fg_color="transparent", height=540)
        self.ModList.grid(row=1, column=0, sticky="wne")

        # Запуск
        self.mainloop()
