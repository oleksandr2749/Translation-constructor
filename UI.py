import customtkinter
import ModificationClass
import Process

class App(customtkinter.CTk):
    def __init__(self, mod_object_list):
        super().__init__()
        self.title("Конструктор перекладу 0.3.2")
        self.geometry('415x580')
        self.minsize(415, 580)
        self.maxsize(415, 580)
        self.configure()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Поле введення для пошуку
        self.search_entry = customtkinter.CTkEntry(self)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.search_entry.bind('<KeyRelease>', self.search_modifications)

        self.ModListFrame = customtkinter.CTkScrollableFrame(self)
        self.ModListFrame.configure(corner_radius=0, width=400)
        self.ModListFrame.grid(row=1, column=0, padx=0, pady=0, sticky="wens")

        self.update_mod_list(mod_object_list)

    def update_mod_list(self, mod_object_list):
        for widget in self.ModListFrame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        for i, mod_object in enumerate(mod_object_list):
            # Label для назви модифікації
            self.ModLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.ModLabel.configure(text=mod_object.get_attribute('Name'), font=("Helvetica", 18, "normal"))
            self.ModLabel.grid(row=2*i, column=0, padx=10, pady=0, sticky="w")

            # Label для автора модифікації
            self.AuthorLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.AuthorLabel.configure(text=mod_object.get_attribute('Author'), font=("Helvetica", 14, "normal"), text_color="gray")
            self.AuthorLabel.grid(row=2*i+1, column=0, padx=15, pady=(0, 10), sticky="w")

            # Binding для подвійного кліку на назву модифікації
            self.ModLabel.bind('<Double-Button-1>', lambda event, idx=i: self.clickable(event, idx))

    def search_modifications(self, event):
        search_text = self.search_entry.get().strip().lower()
        filtered_mods = []
        for mod_object in mod_object_list:
            mod_name = mod_object.get_attribute('Name').lower()
            if search_text in mod_name:
                filtered_mods.append(mod_object)
        self.update_mod_list(filtered_mods)

    def clickable(self, event, idx):
        mod_name = mod_object_list[idx].get_attribute('Name')
        print(f'Натиснуто {mod_name}')
        Process.run(modification=mod_object_list[idx].get_attribute('RootPath'),
                    mod_name=mod_name)


mod_object_list = ModificationClass.create_mod_list(path_294100=ModificationClass.search_294100_folder())

app = App(mod_object_list)
app.mainloop()
