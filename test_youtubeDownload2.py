from pytube import YouTube, Playlist
import tkinter as tk

from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import font
from tkinter import filedialog

from tkinter import ttk
import os
from time import sleep
from threading import Thread

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.master.geometry('800x500')
        self.master.title('Youtube Downloader')
        self.master.resizable(False, False)

        self.iconfile = "./YT.ico"
        self.master.iconbitmap(default=self.iconfile)
        self.create_widgets()

    def create_widgets(self):
        # Font
        self.font01 = font.Font(family='Helvetica', size=15, weight='normal')
        self.font02 = font.Font(family='Helvetica', size=15, weight='bold')
        self.font03 = font.Font(family='Helvetica', size=30, weight='bold')

        # Menu
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Exit', command=self._quit)
        self.menu_bar.add_cascade(label='File', menu='self.file_menu')

        # Add another help menu
        # Display messagebox when clicked
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='About', command=self._msgBox)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        # Main Label
        self.lbl_main = ttk.Label(self.master, text='Youtube Downloader', font=self.font03)

        self.lbl_main.place(relx=0.25, rely=0.02)

        # Frame: URL Input From, Downloader Folder
        self.frame_form = tk.Label(self.master)
        self.frame_form.place(relx=0.01, rely=0.25, height=400, width=780)

        # URL Input Form
        self.lbl_URL = ttk.Label(self.frame_form, text='URL')
        self.lbl_URL.configure(font=self.font01)
        self.lbl_URL.grid(column=0, row=0, padx=20, pady=20)

        self.URL_name = tk.StringVar()

        self.ent_URL = ttk.Entry(self.frame_form, textvariable=self.URL_name)
        self.ent_URL.configure(width=35, font=self.font01)
        self.ent_URL.grid(column=1, row=0, padx=20, pady=20)
        self.ent_URL.focus()

        # Download Folder
        self.Folder_name = tk.StringVar()

        self.lbl_folder = ttk.Label(self.frame_form, text='URL')
        self.lbl_folder.configure(font=self.font01)
        self.lbl_folder.grid(column=0, row=0, padx=20, pady=20)

        self.ent_Folder = ttk.Entry(self.frame_form, textvariable=self.Folder_name)
        self.ent_Folder.configure(width=35, font=self.font01)
        self.ent_Folder.grid(column=1, row=1, padx=20, pady=20)

        self.btn_Folder = tk.Button(self.frame_form, text='Set Folder Path')
        self.btn_Folder.configure(font=self.font02)
        self.btn_Folder.grid(column=2, row=1, padx=20, pady=20, sticky=tk.W + tk.E)
        self.btn_Folder.configure(command=self._get_Folder_Path)

        # Start Button
        self.btn_Start = tk.Button(self.frame_form, text='Start')
        self.btn_Start.configure(font=self.font02)
        self.btn_Start.grid(column=1, row=2, padx=20, pady=20, sticky=tk.W + tk.E)
        self.btn_Start.configure(command=self.click_me)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.frame_form, orient='horizontal', length=286, mode='determinate')
        self.progress_bar.grid(column=1, row=3, padx=20, pady=12, sticky=tk.W + tk.E)

    # Create Callback Functions

    # python treading to prevent GUI freezing
    def click_me(self):
        self.create_thread()

    def create_thread(self):
        self.run_thread = Thread(target=self.method_in_a_thread)
        self.run_thread.start()
        print(self.run_thread)

    def method_in_a_thread(self):
        print('New Thread is Running')
        self.get_youtube(self.URL_name.get(), self.Folder_name.get())

    # Display a Message Box
    def _msgBox(self):
        msg.showinfo('Program Information', 'Youtube Downloader with Tkinter')

    # Youtube download function
    def get_youtube(self, y_url, download_folder):
        # Youtube Instance
        yt = YouTube(y_url)
        yt.streams.filter(progressive=True, subtype='mp4').get_highest_resolution().download(download_folder)

        # progress bar
        self.progress_bar['maximum'] = 100

        for i in range(101):
            sleep(0.05)
            self.progress_bar['value'] = i
            self.progress_bar.update()

    # Exit GUI cleanly
    def _quit(self):
        self.master.quit()
        self.master.destroy()
        exit()

    # Get Folder Path
    def _get_Folder_Path(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        folder_Path = filedialog.askdirectory(initialdir=iDir)

        self.Folder_name.set(folder_Path)

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__== '__main__':
    main()
