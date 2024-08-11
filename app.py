import os
import sys
import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog  



error_codes = {11:"Flash error",12:"Ram Eroor",13:"Config error",14:"Slave error",16:"Winc error",17:"Keypad error",18:"Sound error",
               19:"Init error",20:"BT not connected",21:"SSID not found",22:"WIFI error",23:"Tab error",24:"RTC error",30:"Taring error",
               31:"Stabilisation error",32:"Range error",34:"Tilt error",42:"Watchdog reset",70:"Taring success",80:"Plank validation i2c error",
               81:"Plank validation unauthorised plank",82:"Plank validation invalid plank number",83:"Plank validation serial number mismatch"}

undetected = 0
generated_text = ""



def epoch_to_datetime(epoch_time: int) -> str:
    mytimestamp = datetime.datetime.fromtimestamp(epoch_time - 19800)
    datetime_str = mytimestamp.strftime("%d - %m - %Y  %H : %M : %S")
    return datetime_str

def convert_to_hex(string: str) -> str:
    hex_string = ""
    for char in string:
        hex_string += hex(ord(char))[2:].zfill(2)
    return hex_string

def process_file()-> None:
    global treeview
    global generated_text
    global undetected
    file_path = tk.filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        clear_tree()
        encodings = ["utf-8", "latin-1"] 
        data = None
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    data = file.read()
                    if(data==""):
                        top = tk.Toplevel()
                        top.geometry("300x200")
                        top.maxsize(300,200)
                        top.title("ERROR")
                        top.grab_set()
                        label=tk.Label(top, text= "FILE EMPTY", font=("Times", "22", "bold"))
                        label.place(x=50,y=50)
                break
            except UnicodeDecodeError:
                continue
        a = []
        for i in range(len(data)):
            hex_text = convert_to_hex(data[i])
            a.append(hex_text)
        e = 0
        generated_text = ""
        generated_text += "   Time" + " "*28 +"Event Code" + " "*26 + "Event Description\n"
        generated_text += "--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        for i in range(len(data)):
            if e == len(data):
                break
            br = a[e:4+e]
            ar = list(reversed(br))
            time = "".join(ar)
            d = int(time, 16)
            try:
                if(i%2==0 or i==0):
                    generated_text += f" {d}           |              {int(a[4+e],16)}               |                 {error_codes[int(a[4+e],16)]}\n"
                    generated_text += "--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                    treeview.insert('', 'end', text=str(i+1), values=(d,epoch_to_datetime(d), int(a[4+e],16), error_codes[int(a[4+e],16)]),tags=('evenrow',))
                else:
                    generated_text += f" {d}           |              {int(a[4+e],16)}               |                 {error_codes[int(a[4+e],16)]}\n"
                    generated_text += "--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                    treeview.insert('', 'end', text=str(i+1), values=(d,epoch_to_datetime(d), int(a[4+e],16), error_codes[int(a[4+e],16)]),tags=('oddrow',))       
            except:
                undetected+=1
            e = 4+e+1
    print(undetected)

def download()-> None:
    global generated_text
    file = tk.filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt")
    if(generated_text!=""):   
        with open(f"{file}","w") as f:
            f.write(generated_text)
    else:
        top=tk.Toplevel()
        top.geometry("350x200")
        top.grab_set()
        top.title("ERROR")
        top.maxsize(300,200)
        label=tk.Label(top, text= "File empty", font=("Times", "22", "bold"))
        label.place(x=50,y=50)

def clear_tree()-> None:
    global treeview
    treeview.delete(*treeview.get_children())

class main(tk.Tk):

    def __init__(self):
        #initialization
        super().__init__()
        self.geometry("900x600")
        self.minsize(800,600)  
        self.title("Error Log")

        #body
        style=ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview.Heading",background="#7ea8f8",foreground="black",font=("Franklin Gothic Medium", 11))
        style.configure("Treeview",background="white",foreground="black",rowheight=35,font=("arial", 10))

        #columview init and config
        global treeview
        treeview=ttk.Treeview(self)
        treeview = ttk.Treeview(self, columns=("Column 1", "Column 2", "Column 3","Column 4"))
        treeview.tag_configure('oddrow', background='#ffffff')
        treeview.tag_configure('evenrow', background='#f1f1f1')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        treeview.grid(row=0, column=0, sticky="nsew",padx=10,pady=25)
        scrollbar.grid(row=0, column=1, sticky="ns",rowspan=2)

        #column init
        treeview.column("#0", anchor=tk.CENTER,width=100,stretch=tk.NO)
        treeview.column("#1", anchor=tk.CENTER)
        treeview.column("#2", anchor=tk.CENTER)
        treeview.column("#3", anchor=tk.CENTER)
        treeview.column("#4", anchor=tk.W)

        #column heading
        treeview.heading('#0', text='Sl.No')
        treeview.heading('#1', text='Epoch Time')
        treeview.heading('#2', text='Date & Time')
        treeview.heading('#3', text='Event Code')
        treeview.heading('#4', text='Event Description',anchor=tk.W)

        #grid config
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #add widgets
        button1 = ttk.Button(self, text="Select File", command=process_file)
        button1.grid(row=1, column=0,pady=10,padx=250,sticky="w")
        button2=ttk.Button(self,text="Download",command=download)
        button2.grid(row=1, column=0,pady=10,padx=250,sticky="e")
        label=tk.Label(self,text="Undetected logs:",font=("Times New Roman", "10", "bold"))
        label.grid(row=1,column=0,pady=10,padx=5,sticky="w")
        label=tk.Label(self,text=undetected,font=("Times New Roman", "10", "bold"))
        label.grid(row=1,column=0,pady=10,padx=100,sticky="w")

#mainloop
if __name__ == "__main__":
    main().mainloop()
