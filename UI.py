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
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        self.label_list = list()

        # Рядок пошуку
        self.SearchBar = customtkinter.CTkEntry(self)
        self.SearchBar.configure(corner_radius=0, placeholder_text='Пошук за назвою', height=30)
        self.SearchBar.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.SearchBar.bind('<KeyRelease>', lambda event: self.search_modifications(event, self.label_list))

        # Рамка списку модифікацій
        self.ModListFrame = customtkinter.CTkScrollableFrame(self)
        self.ModListFrame.configure(corner_radius=0)
        self.ModListFrame.grid(row=1, column=0, padx=5, pady=5, sticky="wens")

        # Нижня рамка
        self.BottomFrame = customtkinter.CTkFrame(self)
        self.BottomFrame.configure(corner_radius=0)
        self.BottomFrame.grid(row=2, column=0, padx=5, pady=5, sticky="wens")
        self.BottomFrame.grid_columnconfigure(index=0, weight=1)
        # self.BottomFrame.grid_columnconfigure(index=0, weight=1)

        # Кнопка налаштувань
        self.SettingButton = customtkinter.CTkButton(self.BottomFrame)
        self.SettingButton.configure(corner_radius=0, text='Налаштування')
        self.SettingButton.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка Discord
        self.SettingButton = customtkinter.CTkButton(self.BottomFrame)
        self.SettingButton.configure(corner_radius=0, text='DC',
                                     fg_color='RoyalBlue4',
                                     hover_color='RoyalBlue3',
                                     width='30')
        self.SettingButton.grid(row=0, column=2, padx=5, pady=5)

        # Кнопка відображення автора
        self.AutorButton = customtkinter.CTkButton(self.BottomFrame)
        self.AutorButton.configure(corner_radius=0, text='А', width='30')
        self.AutorButton.grid(row=0, column=1, padx=5, pady=5)

        # Рядок шляху збереження
        self.InputPath = customtkinter.CTkEntry(self.BottomFrame)
        self.InputPath.configure(corner_radius=0,
                                 placeholder_text='Вкажіть шлях до теки зберігання та натисніть Enter')
        self.InputPath.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.InputPath.bind('<Return>', self.input_path)
        self.savePath = str()

        for i, mod_object in enumerate(mod_object_list):
            self.ModLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.ModLabel.configure(text=mod_object.get_attribute('Name'), font=("Helvetica", 18, "normal"))
            self.ModLabel.bind('<Double-Button-1>', self.start_event)
            self.ModLabel.bind('<Button-1>', self.print_text)
            self.label_list.append(self.ModLabel)
            print(f'Створено об\'єкт {self.ModLabel.cget('text')}')

        self.list_update(self.label_list)

    def search_modifications(self, event, testlist):
        searchtestlist = list()
        print(id(searchtestlist))
        print('пишу')
        for mod in testlist:
            mod.grid_forget()
        for i, mod in enumerate(testlist):
            if self.SearchBar.get().strip().lower() in mod.cget('text').strip().lower():
                searchtestlist.append(mod)
        if searchtestlist:
            self.list_update(searchtestlist)

    def list_update(self, testlist):
        print(f'\nВикликано функцію list_update\n')
        for i, mod in enumerate(testlist):
            mod.grid(row=i, column=0, padx=5, pady=0, sticky="w")
            print(f'До списку додано {mod.cget('text')}')

    def print_text(self, event):
        print(event.widget.cget('text'))

    def input_path(self, event):
        self.InputPath.configure(text_color='Gray')
        self.savePath = self.InputPath.get()

    def start_event(self, event):
        print(f'Натиснуто {None}')
        Process.run(modification=None, save_path=self.savePath)

mod_object_list = ModificationClass.create_mod_list(path_294100=ModificationClass.search_294100_folder())

customtkinter.set_default_color_theme('blue')
app = App(mod_object_list)
app.mainloop()
