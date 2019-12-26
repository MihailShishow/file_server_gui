from http.server import HTTPServer, SimpleHTTPRequestHandler
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import os
from threading import Thread
import socket


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.directory = ''
        self.port = 0
        self.port_str = tk.StringVar()
        self.port_str.set('')
        self.server = None
        self.thread = None
        self.create_widgets()
        self.bind_events()

    def validate_port(self, input_str, action_type):
        if action_type == '1':
            if not input_str.isdigit():
                return False
            else:
                if int(input_str) >= 65536:
                    return False
        return True

    def create_widgets(self):
        self.winfo_toplevel().title("Simple Local File Hosting GUI")
        self.dir_select_btn = ttk.Button(self, text="Select Directory...")
        self.dir_lbl = ttk.Label(self, text='')
        self.port_lbl = ttk.Label(self, text="Port")
        self.port_edit = ttk.Entry(
            self, validate='key', textvariable=self.port_str)
        self.port_edit['validatecommand'] = (
            self.port_edit.register(self.validate_port), '%P', '%d')
        self.server_toggle_btn = ttk.Button(self, text="Start Server")
        self.server_toggle_btn['state'] = 'disabled'
        self.address_lbl = ttk.Label(
            self, text="http://{}:PORT".format(socket.gethostbyname(socket.gethostname())))

        self.dir_select_btn.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        self.dir_lbl.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        self.port_lbl.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
        self.port_edit.grid(row=1, column=1, padx=(
            10, 10), pady=(10, 10), sticky='ew')
        self.server_toggle_btn.grid(row=2, column=0, columnspan=2, padx=(
            12, 12), pady=(12, 12), sticky='nesw')
        self.address_lbl.grid(row=3, column=0, columnspan=2, padx=(
            10, 10), pady=(10, 10), sticky='nesw')

    def bind_events(self):
        self.dir_select_btn.bind("<Button-1>", self.event_select_dir)
        self.port_str.trace('w', self.event_set_port)
        self.port_edit.bind("<KeyRelease>", self.event_set_port)
        self.server_toggle_btn.bind("<Button-1>", self.event_start_server)

    def event_select_dir(self, event):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.dir_lbl['text'] = directory
            if self.port:
                self.server_toggle_btn['state'] = 'normal'
            else:
                self.server_toggle_btn['state'] = 'disabled'

    def event_set_port(self, *args):
        if len(self.port_str.get()):
            self.port = int(self.port_str.get())
            if self.directory:
                self.server_toggle_btn['state'] = 'normal'
            else:
                self.server_toggle_btn['state'] = 'disabled'
        else:
            self.server_toggle_btn['state'] = 'disabled'
            self.port = 0

    def event_start_server(self, event):
        os.chdir(self.directory)
        self.server = HTTPServer(
            ('0.0.0.0', self.port), SimpleHTTPRequestHandler)
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.start()
        print('STARTED')

        self.server_toggle_btn["text"] = 'Stop Server'
        self.server_toggle_btn.bind("<Button-1>", self.event_terminate_server)
        print('BOUND')

    def event_terminate_server(self, event):
        self.server.shutdown()
        self.thread.join()
        self.server_toggle_btn["text"] = 'Start Server'
        self.server_toggle_btn.bind("<Button-1>", self.event_start_server)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    style = ttk.Style()
    style.theme_use('clam')
    app.mainloop()