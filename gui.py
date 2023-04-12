from tkinter import Tk, BOTH, EW, BooleanVar

from tkinter.ttk import Frame, Button, Style, Label, Checkbutton
from tkinter.filedialog import askopenfile
from os import path

from api_worker import APIworker


class GUI(Frame):
 
    _style: Style
    _document_label: Label
    _document_button: Button
    _document_path: str
    _csv_label: Label
    _csv_button: Button
    _csv_path: str
    _paragraph_checkbutton: Checkbutton
    _picture_caption_checkbutton: Checkbutton
    _paragraph_checkbutton_var: BooleanVar
    _picture_caption_checkbutton_var: BooleanVar
    _table_caption_checkbutton_var: BooleanVar
    _api_worker: APIworker


    def __init__(self):
        super().__init__()
        self.__init_ui()
 
    def __init_ui(self):
        self.master.title("GUI Client")
        self.pack(fill=BOTH, expand=True)
        self.__init_style()
        self.__init_upload_buttons()
        self.__init_checkbuttons()
        self.__init_submit_button()
        self._document_path = None
        self._csv_path = None
        self._api_worker = APIworker()
        
    def __init_style(self):
        self._style = Style()
        self._style.theme_use("alt")

        self._style.configure(
            'TCheckbutton',
            focuscolor=self.master.cget("background"))
        self._style.configure(
            'TCheckbutton',
            activebackground=self.master.cget("background"))
        self._style.configure(
            'TCheckbutton',
            background=self.master.cget("background"))

        self._style.configure(
            'TLabel',
            focuscolor=self.master.cget("background"))
        self._style.configure(
            'TLabel',
            activebackground=self.master.cget("background"))
        self._style.configure(
            'TLabel',
            background=self.master.cget("background"))

        self._style.configure(
            'TButton',
            focuscolor=self.master.cget("background"))
        self._style.configure(
            'TButton',
            activebackground=self.master.cget("background"))
        self._style.configure(
            'TButton',
            background=self.master.cget("background"))
        
    def __init_checkbuttons(self):
        self._paragraph_checkbutton_var = \
            BooleanVar(value=False)
        self._picture_caption_checkbutton_var = \
            BooleanVar(value=False)
        self._table_caption_checkbutton_var = \
            BooleanVar(value=False)
        self._paragraph_checkbutton = \
            Checkbutton(
                self, text='Paragraph', 
                variable=self._paragraph_checkbutton_var, 
                onvalue=True, offvalue=False, padding=5)
        self._paragraph_checkbutton.grid(row=4, column=0, sticky=EW)
        self._picture_caption_checkbutton = \
            Checkbutton(
                self, text='Picture caption',
                variable=self._picture_caption_checkbutton_var,
                onvalue=True, offvalue=False, padding=5)
        self._picture_caption_checkbutton.grid(row=4, column=1,
                                               sticky=EW)
        self._table_caption_checkbutton = \
            Checkbutton(
                self, text='Table caption', 
                variable=self._table_caption_checkbutton_var, 
                onvalue=True, offvalue=False, padding=5,)
        self._table_caption_checkbutton.grid(row=4, column=2,
                                             sticky=EW)

    def __init_upload_buttons(self):
        self._document_label = \
            Label(self, text="Input docx document", padding=5)
        self._document_label.grid(
            row=0, column=0, columnspan=3, sticky=EW)
        self._document_button = \
            Button(self, text="Choose docx", padding=5)
        self._document_button.configure(
            command=lambda: self.__on_button_click("choose_docx"))
        self._document_button.grid(
            row=1, column=0, columnspan=3, sticky=EW)

        self._csv_label = \
            Label(self, text="Input csv file", padding=5)
        self._csv_label\
            .grid(row=2, column=0, columnspan=3, sticky=EW)
        self._csv_button = \
            Button(self, text="Choose csv", padding=5)
        self._csv_button.configure(
            command=lambda: self.__on_button_click("choose_csv"))
        self._csv_button\
            .grid(row=3, column=0, columnspan=3, sticky=EW)

    def __init_submit_button(self):
        submit_button: Button = \
            Button(self, text="Submit", padding=5)
        submit_button.configure(
            command=lambda: self.__on_button_click("submit"))
        submit_button.grid(row=5, column=0, columnspan=3, 
                           sticky=EW, pady=1)
        
    def __get_query_component(self) -> str:
        query_component: str = "?"
        if self._paragraph_checkbutton_var.get():
            query_component = \
                query_component + "text-paragraph-fix=true"
        if self._picture_caption_checkbutton_var.get():
            query_component = \
                query_component + "picture-caption-fix"
        if self._table_caption_checkbutton_var.get():
            query_component = \
                query_component + "table-caption-fix"
        return query_component

    def __submit(self):
        query_component: str = self.__get_query_component()
        full_doc_path: str = self._document_path
        full_dic_path: str = self._csv_path
        self._api_worker \
            .get_files(full_doc_path, full_dic_path, query_component)
        self._api_worker \
            .replace_fields_in_document(full_doc_path, 
                                        full_dic_path, 
                                        query_component)        
        self._document_path = None
        self._document_label.configure(text="Input docx document")
        self._csv_path = None
        self._csv_label.configure(text="Input csv file")

    def __on_button_click(self, button_name: str):
        if button_name == "submit":
            self.__submit()
        elif button_name == "choose_docx":
            path_wrapper = \
                askopenfile(mode='r', 
                            filetypes=[('docx files', '*.docx')])
            if path_wrapper != None:
                self._document_path = path_wrapper.name
                self._document_label\
                    .configure(text=self._document_path)
        elif button_name == "choose_csv":
            path_wrapper = \
                askopenfile(mode='r', 
                            filetypes=[('CSV files', '*.csv')])
            if path_wrapper != None:
                self._csv_path = path_wrapper.name
                self._csv_label.configure(text=self._csv_path)