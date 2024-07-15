import customtkinter
import ModificationClass
import Process

class App(customtkinter.CTk):
    def __init__(self, mod_object_list):
        # Налаштування вікна
        super().__init__()

        self.title("Конструктор перекладу 0.3.2")
        self.geometry('415x580')
        self.minsize(415, 580)
        self.maxsize(415, 580)
        self.configure()

        # Сітка
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Рамка списку модів
        self.ModListFrame = customtkinter.CTkScrollableFrame(self)
        self.ModListFrame.configure(corner_radius=0, width=400)
        self.ModListFrame.grid(row=1, column=0, padx=0, pady=0, sticky="wens")

        for i, mod_object in enumerate(mod_object_list):
            self.ModLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.ModLabel.configure(text=mod_object.get_attribute('Name'))
            self.ModLabel.bind('<Double-Button-1>', lambda event, idx=i: self.clickable(event, idx))
            self.ModLabel.grid(row=i+2, column=0, padx=10, pady=0, sticky="w")

    def clickable(self, event, idx):
        print(f'Натиснуто {mod_object_list[idx].get_attribute('Name')}')
        Process.run(modification=mod_object_list[idx].get_attribute('RootPath'),
                    mod_name=mod_object_list[idx].get_attribute('Name'))


mod_object_list = ModificationClass.create_mod_list(path_294100=ModificationClass.search_294100_folder())

app = App(mod_object_list)
app.mainloop()
