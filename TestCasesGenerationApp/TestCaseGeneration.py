import time
from tkinter import *
from tkinter import filedialog, messagebox
import webbrowser
from threading import Thread
import threading
from tkinter.ttk import Progressbar
from SDK import TestCasesGenerator

# Required in order to add data files to Windows executable
import sys, os

path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

window, canvas = None, None
input_path, output_path, dur_key_entry, input_path_entry, output_path_entry = "", "", "", "", ""
finished = threading.Event()

def fun():
    print("Test fun")

def btn_clicked():
    global window, canvas, input_path, output_path, dur_key_entry

    def check_if_finished():
        if finished.is_set():
            finished.clear()
            print("Process finished!")
            messagebox.showinfo(title="Success", message="Output file saved successfully!")
            # window.destroy()
            canvas1.destroy()
            show_home_screen_again()
        else:
            window.after(1000, check_if_finished)
    dur_key = dur_key_entry.get()

    if not input_path:
        messagebox.showerror(title="Invalid path",
                             message="Enter a valid input file")
    elif not dur_key:
        messagebox.showerror(title="Empty Fields",
                             message="Please enter total duration for generating new test cases")
    elif not output_path:
        messagebox.showerror(title="Invalid path",
                             message="Enter a valid output path")
    else:
        output_path += "/" + input_path.split('/')[-1].split('.')[0] + ".txt"
        canvas.destroy()
        canvas1 = Canvas(
            window,
            bg="#ffffff",
            height=519,
            width=862,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        # Text for processing
        canvas1.create_text(337, 230, text="Processing the audio...", fill="#515486", font=("Arial-BoldMT", int(12.0)))
        # Progress bar
        progress = Progressbar(window, orient=HORIZONTAL,
                               length=400, mode='indeterminate')
        window.update_idletasks()
        progress.place(x=260, y=250)
        progress.start()

        thread = Thread(target=fun, args=(input_path, dur_key, output_path, finished))
        thread.start()
        canvas1.pack(expand=True, fill=BOTH)
        window.after(1000, check_if_finished)
        window.mainloop()


def select_input_path(event):
    global input_path, input_path_entry

    input_path = filedialog.askopenfilename(filetypes=(("CSV Files", ".csv"), ("All Files", "*.*")))
    input_path_entry.delete(0, END)
    input_path_entry.insert(0, input_path)


def select_output_path(event):
    global output_path, output_path_entry

    output_path = filedialog.askdirectory()
    output_path_entry.delete(0, END)
    output_path_entry.insert(0, output_path)


def live_demo_link_clicked(event):
    url = "http://testifytech.ml"
    webbrowser.open_new(url)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = Label(f, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)

    return label


def show_home_screen():
    global window, canvas, input_path_entry, dur_key_entry, output_path_entry
    window = Tk()
    logo = PhotoImage(file='images/logo.png')
    window.call('wm', 'iconphoto', window._w, logo)
    window.title("Test cases Generator")

    window.geometry("862x519")
    window.configure(bg="#3A7FF6")
    canvas = Canvas(window, bg="#3A7FF6", height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
    canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

    text_box_bg = PhotoImage(file=f"images/TextBox_Bg.png")
    inputFilePath_entry_img = canvas.create_image(650.5, 147.5, image=text_box_bg)
    dur_key_entry_img = canvas.create_image(650.5, 240.5, image=text_box_bg)
    outoutFilePath_entry_img = canvas.create_image(650.5, 319.5, image=text_box_bg)

    input_path_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    input_path_entry.place(x=490.0, y=117 + 35, width=321.0, height=35)
    input_path_entry.bind("<1>", select_input_path)
    input_path_entry.focus()

    dur_key_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    dur_key_entry.place(x=490.0, y=210 + 35, width=321.0, height=35)

    output_path_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    output_path_entry.place(x=490.0, y=279 + 35, width=321.0, height=35)
    output_path_entry.bind("<1>", select_output_path)

    canvas.create_text(583.5, 50.0, text="Enter the details", fill="#515486", font=("Arial-BoldMT", int(22.0)))
    canvas.create_text(519.0, 136.0, text="Input File", fill="#515486", font=("Arial-BoldMT", int(13.0)))
    canvas.create_text(581.5, 218.5, text="Enter duration (in minutes)", fill="#515486", font=("Arial-BoldMT", int(13.0)))
    canvas.create_text(532.5, 300.5, text="Output Folder", fill="#515486", font=("Arial-BoldMT", int(13.0)))

    title = Label(text="Test cases Generator", bg="#3A7FF6", fg="white", font=("Arial-BoldMT", int(20.0)))
    title.place(x=27.0, y=120.0)

    info_text = Label(text="Test cases Generator preprocesses\n"
                           "input data and uses GPT-2 model to \n"
                           "generate novel test cases after\n"
                           "training model.\n\n",
                      bg="#3A7FF6", fg="white", justify="left", font=("Georgia", int(16.0)))

    info_text.place(x=27.0, y=200.0)

    live_demo_link = Label(text="Click here for more details", bg="#3A7FF6", fg="white", cursor="hand2")
    live_demo_link.place(x=27, y=385)
    live_demo_link.bind('<Button-1>', live_demo_link_clicked)

    generate_btn_img = PhotoImage(file="./images/generate.png")
    generate_btn = Button(image=generate_btn_img, borderwidth=0, highlightthickness=0, command=btn_clicked,
                          relief="flat")

    generate_btn.place(x=557, y=375, width=180, height=55)

    window.resizable(False, False)
    window.mainloop()


def show_home_screen_again():
    global window, canvas, lang_clicked, input_path_entry, sub_key_entry, location_entry, output_path_entry

    canvas = Canvas(window, bg="#3A7FF6", height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
    canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

    text_box_bg = PhotoImage(file=f"images/TextBox_Bg.png")
    inputFilePath_entry_img = canvas.create_image(650.5, 147.5, image=text_box_bg)
    dur_key_entry_img = canvas.create_image(650.5, 240.5, image=text_box_bg)
    outoutFilePath_entry_img = canvas.create_image(650.5, 319.5, image=text_box_bg)

    input_path_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    input_path_entry.place(x=490.0, y=117 + 35, width=321.0, height=35)
    input_path_entry.bind("<1>", select_input_path)
    input_path_entry.focus()

    dur_key_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    dur_key_entry.place(x=490.0, y=210 + 35, width=321.0, height=35)

    output_path_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    output_path_entry.place(x=490.0, y=279 + 35, width=321.0, height=35)
    output_path_entry.bind("<1>", select_output_path)

    canvas.create_text(583.5, 50.0, text="Enter the details", fill="#515486", font=("Arial-BoldMT", int(22.0)))
    canvas.create_text(519.0, 136.0, text="Input File", fill="#515486", font=("Arial-BoldMT", int(13.0)))
    canvas.create_text(581.5, 218.5, text="Enter duration (in minutes)", fill="#515486",
                       font=("Arial-BoldMT", int(13.0)))
    canvas.create_text(532.5, 300.5, text="Output Folder", fill="#515486", font=("Arial-BoldMT", int(13.0)))

    title = Label(text="Test cases Generator", bg="#3A7FF6", fg="white", font=("Arial-BoldMT", int(20.0)))
    title.place(x=27.0, y=120.0)

    info_text = Label(text="Test cases Generator preprocesses\n"
                           "input data and uses GPT-2 model to \n"
                           "generate novel test cases after\n"
                           "training model.\n\n",
                      bg="#3A7FF6", fg="white", justify="left", font=("Georgia", int(16.0)))

    info_text.place(x=27.0, y=200.0)

    live_demo_link = Label(text="Click here for more details", bg="#3A7FF6", fg="white", cursor="hand2")
    live_demo_link.place(x=27, y=385)
    live_demo_link.bind('<Button-1>', live_demo_link_clicked)

    generate_btn_img = PhotoImage(file="./images/generate.png")
    generate_btn = Button(image=generate_btn_img, borderwidth=0, highlightthickness=0, command=btn_clicked,
                          relief="flat")

    generate_btn.place(x=557, y=375, width=180, height=55)

    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    show_home_screen()
