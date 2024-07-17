import customtkinter
import ModificationClass
import Process

class App(customtkinter.CTk):
    def __init__(self, mod_object_list):
        super().__init__()
        self.title('Конструктор перекладу')
        self.geometry('800x600')
        # self.minsize(415, 580)
        # self.maxsize(415, 580)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)
        # self.grid_columnconfigure(1, weight=0)


        # Пошуковий рядок
        self.SearchBar = customtkinter.CTkEntry(self)
        self.SearchBar.configure(corner_radius=0, placeholder_text='Пошук за назвою', height=30)
        self.SearchBar.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.SearchBar.bind('<KeyRelease>', self.search_modifications)

        # Рамка списку модифікацій
        self.ModListFrame = customtkinter.CTkScrollableFrame(self)
        self.ModListFrame.configure(corner_radius=0)
        self.ModListFrame.grid(row=1, column=0, padx=0, pady=0, sticky="wens")

        # Кнопка налаштувань
        self.SettingButton = customtkinter.CTkButton(self)
        self.SettingButton.configure(corner_radius=0, text='Налаштування', height=40, fg_color='slate gray', hover_color='SlateGray3')
        self.SettingButton.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        # Кнопка Discord
        self.SettingButton = customtkinter.CTkButton(self)
        self.SettingButton.configure(corner_radius=0, text='DC', width=40, height=40, fg_color='RoyalBlue4', hover_color='RoyalBlue3')
        self.SettingButton.grid(row=2, column=0, padx=150, pady=5, sticky='e')

        # Рядок шляху збереження
        self.InputPath = customtkinter.CTkEntry(self)
        self.InputPath.configure(corner_radius=0,
                                 placeholder_text='Вкажіть шлях до теки зберігання та натисніть Enter',
                                 height=30)
        self.InputPath.grid(row=2, column=0, padx=(5, 200), pady=0, sticky="we")
        self.InputPath.bind('<Return>', self.input_path)
        self.savePath = str()

        self.update_mod_list(mod_object_list)

    def search_modifications(self, event):
        search_text = self.SearchBar.get().strip().lower()
        filtered_mods = []
        for mod_object in mod_object_list:
            mod_name = mod_object.get_attribute('Name').lower()
            if search_text in mod_name:
                filtered_mods.append(mod_object)
        self.update_mod_list(filtered_mods)

    def update_mod_list(self, mod_object_list):
        element_number = 0

        for widget in self.ModListFrame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()
        for i, mod_object in enumerate(mod_object_list):
            self.ModLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.ModLabel.configure(text=mod_object.get_attribute('Name'), font=("Helvetica", 18, "normal"))
            self.ModLabel.grid(row=2*i, column=0, padx=10, pady=0, sticky="w")
            self.ModLabel.bind('<Double-Button-1>', lambda event, idx=element_number: self.start_event(event, idx))
            element_number += 1

    def input_path(self, event):
        self.InputPath.configure(text_color='Gray')
        self.savePath = self.InputPath.get()

    def start_event(self, event, idx):
        mod_name = mod_object_list[idx].get_attribute('Name')
        print(f'Натиснуто {mod_name}')
        Process.run(modification=mod_object_list[idx].get_attribute('RootPath'),
                    mod_name=mod_name, save_path=self.savePath)


mod_object_list = ModificationClass.create_mod_list(path_294100=ModificationClass.search_294100_folder())

customtkinter.set_default_color_theme('blue')
app = App(mod_object_list)
app.mainloop()
