import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

APPNAME = 'Fancy lil\' Text Editor'

root = Tk()
root.title(APPNAME)
root.option_add('*tearOff', FALSE)
root.geometry('800x500')
root.minsize(22*12,100)

KAROLISICON = PhotoImage(file='res/karolis.png')
NEWICON = PhotoImage(file='res/new.png')
OPENICON = PhotoImage(file='res/open.png')
SAVEICON = PhotoImage(file='res/save.png')
SAVEASICON = PhotoImage(file='res/saveas.png')
CUTICON = PhotoImage(file='res/cut.png')
COPYICON = PhotoImage(file='res/copy.png')
PASTEICON = PhotoImage(file='res/paste.png')
UNDOICON = PhotoImage(file='res/undo.png')
REDOICON = PhotoImage(file='res/redo.png')
FINDICON = PhotoImage(file='res/find.png')
SELECTALLICON = PhotoImage(file='res/selectall.png')
HELPICON = PhotoImage(file='res/help.png')

showinbar = IntVar()
darktheme = IntVar()
showinbar.set(1)
darktheme.set(0)

shortcutbar = Frame(root, height=25, bg='gainsboro', relief='ridge')
shortcutbar.pack(expand=NO, fill=X)

textpad = Text(root, undo=True)
scroll = Scrollbar(textpad, cursor='arrow')

scroll.config(command=textpad.yview)
scroll.pack(side=RIGHT, fill=Y)
textpad.configure(yscrollcommand=scroll.set)
textpad.pack(expand=YES, fill=BOTH)

infobar = Label(textpad, text='Line: 1 | Column: 0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

menubar = Menu(root)
root['menu'] = menubar

class shortcutbutton():
    def __init__(self, icon, command):
        self.icon = icon
        self.cmd = command
        self.toolbar = Button(shortcutbar, image=self.icon, command=self.cmd)
        self.toolbar.image = self.icon
        self.toolbar.pack(side=LEFT)

def action(action):
    textpad.event_generate(action)
    update_line_number()

def new_file():
    global filename
    root.title('Untitled'+' - '+APPNAME)
    filename = None
    textpad.delete(1.0, END)
    update_line_number()

def open_file():
    global filename
    filename = filedialog.askopenfilename(defaultextension='.txt',
               filetypes=[('All Files', '*.*'), ('Text Documents', '.txt')])
    if filename == '':
        filename = None
    else:
        root.title(os.path.basename(filename)+' - '+APPNAME)
        textpad.delete(1.0, END)
        with open(filename, 'r') as fh:
            textpad.insert(1.0, fh.read())
    update_line_number()

def save():
    global filename
    try:
        with open(filename, 'w') as f:
            letter = textpad.get(1.0, 'end')
            f.write(letter)
    except:
        save_as()

def save_as():
    try:
        f = filedialog.asksaveasfilename(initialfile='Untitled.txt',
            defaultextension='.txt', filetypes=[('All Files', '*.*'),
                                          ('Text Documents', '.txt')])
        with open(f, 'w') as fh:
            textoutput = textpad.get(1.0, END)
            fh.write(textoutput)
        root.title(os.path.basename(filename)+' - '+APPNAME)
    except:
        pass

def tofind():
    fwindow = Toplevel(root)
    fwindow.title('Find')
    fwindow.geometry('262x65+{}+{}'.format(root.winfo_x()+70, root.winfo_y()+200))
    fwindow.transient(root)
    fwindow.resizable(FALSE,FALSE)
    Label(fwindow, text='Find all:').grid(row=0, column=0, sticky='e')
    v = StringVar()
    e = Entry(fwindow, width=25, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    e.focus_set()
    c = IntVar()
    Checkbutton(fwindow, text='Ignore Case', variable=c).grid(row=1, column=1,
                sticky='e', padx=2, pady=2)
    Button(fwindow, text='Find All', underline=0,
    command = lambda: search_for(v.get(), c.get(), textpad, fwindow, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)

    def close_search():
        textpad.tag_remove('match', '1.0', END)
        fwindow.destroy()

    fwindow.protocol('WM_DELETE_WINDOW', close_search)    

def search_for(needle, cssnstv, textpad, fwindow, e):
    textpad.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textpad.search(needle, pos, nocase=cssnstv,
            stopindex=END)
            if not pos:
                break
            lastpos = '%s+%dc' % (pos, len(needle))
            textpad.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
    textpad.tag_config('match', foreground='red', background='yellow')
    e.focus_set()
    fwindow.title('{} matches found'.format(count))

def select_all():
    textpad.tag_add('sel', '1.0', 'end-1c')

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    else:
        infobar.pack_forget()

def update_line_number():
    currline, curcolumn = textpad.index(INSERT).split('.')
    infobar.config(text='Line: {} | Column: {}'.format(currline, curcolumn))

def theme():
    if darktheme.get():
        textpad.config(bg='gray16', fg='#FFFFFF')
        shortcutbar['bg'] = 'gray56'
        infobar['bg'] = 'gray56'
    else:
        textpad.config(bg='#FFFFFF', fg='#000000')
        shortcutbar['bg'] = 'gainsboro'
        infobar['bg'] = 'SystemMenu'

def about():
    messagebox.showinfo(message='Message', title='All hail Karolis')

def hilfe():
    h = Toplevel(root)
    h.title('Pomoc')
    h.geometry('262x100+{}+{}'.format(int(root.winfo_screenwidth()-262)//2,
                                      int(root.winfo_screenheight()-100)//2))
    h.resizable(width=False, height=False)
    frame = Frame(h)
    frame.pack()
    Label(frame, image=KAROLISICON).pack()
    Label(frame, text='You jokin\', peasant?').pack()
    Button(frame, text="Quit", command=h.destroy).pack()

def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)

def exit_msg():
    if messagebox.askokcancel('Quit', 'Do you really want to quit?'):
        root.destroy()

root.protocol('WM_DELETE_WINDOW', exit_msg)

menu_file = Menu(menubar, tearoff=0)
newmenu = Menu(menu_file)
menu_file.add_command(label='New', compound=LEFT, image=NEWICON, accelerator='Ctrl+N', command=new_file)
menu_file.add_command(label='Open', compound=LEFT, image=OPENICON, accelerator='Ctrl+O', command=open_file)
menu_file.add_separator()
menu_file.add_command(label='Save', compound=LEFT, image=SAVEICON, accelerator='Ctrl+S', command=save)
menu_file.add_command(label='Save as...', compound=LEFT, image=SAVEASICON, accelerator='Ctrl+Shift+S', command=save_as)
menu_file.add_separator()
menu_file.add_command(label='Close', accelerator='Ctrl+W')
menu_file.add_separator()
menu_file.add_command(label='Exit', command=exit_msg)
menubar.add_cascade(menu=menu_file, label=' File ')

menu_edit = Menu(menubar, tearoff=0)
menu_edit.add_command(label='Undo', compound=LEFT, image=UNDOICON,
                      accelerator='Ctrl+Z', command=lambda: action('<<Undo>>'))
menu_edit.add_command(label='Redo', compound=LEFT, image=REDOICON,
                      accelerator='Ctrl+Y', command=lambda: action('<<Redo>>'))
menu_edit.add_separator()
menu_edit.add_command(label='Copy', compound=LEFT, image=COPYICON, accelerator='Ctrl+C', command=lambda: action('<<Copy>>'))
menu_edit.add_command(label='Cut', compound=LEFT, image=CUTICON, accelerator='Ctrl+X', command=lambda: action('<<Cut>>'))
menu_edit.add_command(label='Paste', compound=LEFT, image=PASTEICON, accelerator='Ctrl+V', command=lambda: action('<<Paste>>'))
menu_edit.add_separator()
menu_edit.add_command(label='Find', compound=LEFT, image=FINDICON, accelerator='Ctrl+F', command=tofind)
menu_edit.add_separator()
menu_edit.add_command(label='Select all', compound=LEFT, image=SELECTALLICON, accelerator='Ctrl+A',
                      command=select_all)
menubar.add_cascade(menu=menu_edit, label=' Edit ')

menu_view = Menu(menubar, tearoff=0)
menu_view.add_checkbutton(label='Show Index Bar', variable=showinbar, command=show_info_bar)
menu_view.add_checkbutton(label='Dark Theme', variable=darktheme, command=theme)
menubar.add_cascade(menu=menu_view, label='View')

menu_about = Menu(menubar, tearoff=0)
menu_about.add_command(label='About', command=about)
menu_about.add_separator()
menu_about.add_command(label='Help', compound=LEFT, image=HELPICON, command=hilfe)
menubar.add_cascade(menu=menu_about, label=' About ')

cmenu = Menu(textpad)
cmenu.add_command(label='Copy', compound=LEFT, command=lambda: action('<<Copy>>'))
cmenu.add_command(label='Cut', compound=LEFT, command=lambda: action('<<Cut>>'))
cmenu.add_command(label='Paste', compound=LEFT, command=lambda: action('<<Paste>>'))
cmenu.add_command(label='Undo', compound=LEFT, command=lambda: action('<<Undo>>'))
cmenu.add_command(label='Redo', compound=LEFT, command=lambda: action('<<Redo>>'))
cmenu.add_separator()
cmenu.add_command(label='Select All', command=select_all)

newbutton = shortcutbutton(NEWICON, new_file)
openbutton = shortcutbutton(OPENICON, open_file)
savebutton = shortcutbutton(SAVEICON, save)
saveasbutton = shortcutbutton(SAVEASICON, save_as)
cutbutton = shortcutbutton(CUTICON, command=lambda: action('<<Cut>>'))
copyebutton = shortcutbutton(COPYICON, command=lambda: action('<<Copy>>'))
pastebutton = shortcutbutton(PASTEICON, command=lambda: action('<<Paste>>'))
undobutton = shortcutbutton(UNDOICON, command=lambda: action('<<Undo>>'))
redobutton = shortcutbutton(REDOICON, command=lambda: action('<<Redo>>'))
findbutton = shortcutbutton(FINDICON, tofind)
selectallbutton = shortcutbutton(SELECTALLICON, select_all)
about = shortcutbutton(HELPICON, about)

textpad.bind('<Any-KeyPress>', lambda e: update_line_number())
textpad.bind('<Button-1>', lambda e: update_line_number())
textpad.bind('<Button-3>', popup)
textpad.bind('<Control-N>', lambda e: new_file())
textpad.bind('<Control-n>', lambda e: new_file())
textpad.bind('<Control-O>', lambda e: open_file())
textpad.bind('<Control-o>', lambda e: open_file())
textpad.bind('<Control-S>', lambda e: save())
textpad.bind('<Control-s>', lambda e: save())
textpad.bind('<Control-Shift-S>', lambda e: save_as())
textpad.bind('<Control-Shift-s>', lambda e: save_as())
textpad.bind('<Control-A>', lambda e: select_all())
textpad.bind('<Control-a>', lambda e: select_all())
textpad.bind('<Control-F>', lambda e: tofind())
textpad.bind('<Control-f>', lambda e: tofind())

root.mainloop()

