import Process
import ModificationClass
import tkinter
import customtkinter
import webbrowser
from PIL import Image
from pathlib import Path


class SearchBarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Рядок пошуку
        self.SearchBarColor = 'gray20'
        self.SearchBarTextColor = 'white'
        self.SearchBarFont = ('Open Sans', 18)
        self.grid_columnconfigure(index=3, weight=1)
        self.SearchLabel = customtkinter.CTkLabel(self,
                                                  corner_radius=0, fg_color=self.SearchBarColor, height=28,
                                                  font=self.SearchBarFont, text_color=self.SearchBarTextColor,
                                                  text=' Пошук за ')
        self.SearchLabel.grid(row=0, column=0, padx=(5, 0), pady=(5, 0))
        self.options = ["назвою", "авторством", "айді"]
        self.combobox = customtkinter.CTkComboBox(self,
                                                  corner_radius=0, border_width=0, width=140,
                                                  fg_color=self.SearchBarColor,
                                                  button_color='gray18',
                                                  font=self.SearchBarFont, text_color=self.SearchBarTextColor,
                                                  values=self.options,
                                                  dropdown_font=self.SearchBarFont,
                                                  dropdown_text_color=self.SearchBarTextColor,
                                                  state='readonly')
        self.combobox.grid(row=0, column=1, pady=(5, 0))
        self.SearchLabel2 = customtkinter.CTkLabel(self,
                                                   corner_radius=0, fg_color=self.SearchBarColor, height=28,
                                                   font=self.SearchBarFont, text_color=self.SearchBarTextColor,
                                                   text=' :')
        self.SearchLabel2.grid(row=0, column=2, pady=(5, 0))
        self.SearchBar = customtkinter.CTkEntry(self)
        self.SearchBar.configure(corner_radius=0, fg_color=self.SearchBarColor, border_width=0,
                                 font=self.SearchBarFont)
        self.SearchBar.grid(row=0, column=3, padx=(0, 5), pady=(5, 0), sticky='we')


class App(customtkinter.CTk):
    def __init__(self, mod_object_list):
        super().__init__()
        self.title('Конструктор перекладу')
        self.geometry('800x600')

        self.grid_rowconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        self.label_list = list()
        self.mod_label_map = {}

        # Клас рамки рядка пошуку
        self.SearchBar = SearchBarFrame(self)
        self.SearchBar.configure(corner_radius=0)
        self.SearchBar.grid(row=0, column=0, sticky='we')
        self.SearchBar.SearchBar.bind('<KeyRelease>', lambda event: self.search_modifications(event, self.label_list))

        # Рамка списку модифікацій
        self.ModListFrame = customtkinter.CTkScrollableFrame(self)
        self.ModListFrame.configure(corner_radius=0)
        self.ModListFrame.grid(row=1, column=0, sticky="wens")

        # Нижня рамка
        self.BottomFrame = customtkinter.CTkFrame(self)
        self.BottomFrame.configure(corner_radius=0, height=40)
        self.BottomFrame.grid(row=2, column=0, padx=0, pady=(5, 0), sticky="wens")

        # Рядок шляху збереження
        self.InputPath = customtkinter.CTkEntry(self.BottomFrame)
        self.InputPath.configure(corner_radius=0, fg_color='gray20', border_width=0, width=500,
                                 placeholder_text='Введіть шлях теки зберігання та натисніть Enter :', font=('Open Sans', 18))
        self.InputPath.place(relx=0.01, rely=0.5, anchor='w')
        self.InputPath.bind('<Return>', self.input_path)
        self.savePath = str()

        for i, mod_object in enumerate(mod_object_list):
            self.ModLabel = customtkinter.CTkLabel(self.ModListFrame)
            self.ModLabel.configure(text=mod_object.get_attribute('Name'), font=("Helvetica", 18, "normal"))
            self.ModLabel.bind('<Double-Button-1>', self.start_event)
            # self.ModLabel.bind('<Button-1>', self.print_text)
            self.label_list.append(self.ModLabel)
            self.mod_label_map[self.ModLabel.cget('text')] = mod_object
            # print(f'Створено об\'єкт {self.ModLabel.cget('text')}')

        # Поле Discord
        self.discord_logo = customtkinter.CTkImage(
            dark_image=Image.open('/home/oleksanlr/Завантажене/1611711962-discord-button.png'),
            light_image=Image.open('/home/oleksanlr/Завантажене/1611711962-discord-button.png'),
            size=(1, 1))
        self.discord_button = customtkinter.CTkButton(self, image=self.discord_logo,
                                                      text='',
                                                      hover=False,
                                                      width=150,
                                                      height=60,
                                                      corner_radius=0,
                                                      fg_color='gray17',
                                                      command=self.discord_button_event_click)
        # self.discord_button.place(relx=0.5, rely=0.5, anchor='center')
        self.resize_discord_logo()

        self.list_update(self.label_list)

    def search_modifications(self, event, testlist):
        searchtestlist = list()
        if self.SearchBar.combobox.get() == 'назвою':
            for mod in testlist:
                mod.grid_forget()
            for i, mod in enumerate(testlist):
                if self.SearchBar.SearchBar.get().strip().lower() in mod.cget('text').strip().lower():
                    searchtestlist.append(mod)
            if searchtestlist:
                self.list_update(searchtestlist)
        else:
            self.attention_color()

    def attention_color(self):
        self.SearchBar.combobox.configure(fg_color='gray30', button_color='gray40')
        self.after(500, self.reset_color)

    def reset_color(self):
        self.SearchBar.combobox.configure(fg_color='gray20', button_color='gray18')

    def list_update(self, testlist):
        # print(f'\nВикликано функцію list_update\n')
        for i, mod in enumerate(testlist):
            mod.grid(row=i, column=0, padx=5, pady=0, sticky="w")
            # print(f'До списку додано {mod.cget('text')}')

    def input_path(self, event):
        self.InputPath.configure(text_color='Gray')
        self.savePath = Path(self.InputPath.get())

    def start_event(self, event):
        # print(id(event.widget))
        # print(self.mod_label_map)
        # print(f'Натиснуто {event.widget.cget('text')}')
        Process.run(self.mod_label_map[event.widget.cget('text')], self.savePath)

    # Подія натискання на кнопку діскорд
    def discord_button_event_click(self):
        webbrowser.open('https://discord.gg/CdKquMvf9w')

    # Встановлює розмір зображення логотипа діскор
    def resize_discord_logo(self):
        self.discord_logo.configure(size=(self.discord_button.cget('width'), self.discord_button.cget('height')))


mod_object_list = ModificationClass.create_mod_list(path_294100=ModificationClass.search_294100_folder())
customtkinter.set_default_color_theme('blue')
app = App(mod_object_list)
app.mainloop()
