from tkinter import  *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from vector import *
from extract import *

LARGE_FONT = ("Verdana", 16)

image_path = "test"
db_path = 'pins.db'
db = None
#fig = plt.figure(figsize=(8,5) ,dpi=100)

class MainApp(Tk):
    currentFrame = None

    def __init__(self, *args, **kwargs):
        global db_path

        Tk.__init__(self, *args, **kwargs)
        
        Tk.wm_title(self, "KetokMagicHalal")
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True) 
        
        #container.grid_rowconfigure(0, weight = 1)
        #container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        for F in ([PageOne]):
            frame = F(container, self)
            self.frames[F] = frame
            frame.pack_forget()
            #frame.pack(side="top", fill = "both", expand = True)
        
        self.show_frame(PageOne)
        self.currentFrame.load_db(db_path)

    def show_frame(self, cont):
        if self.currentFrame is not None:
            self.currentFrame.pack_forget()
        self.currentFrame = self.frames[cont]
        self.currentFrame.pack(side=TOP, fill=BOTH, expand=True)
        
        
        
class PageOne(Frame):
    
    sub1 = None
    sub2 = None
    sub3 = None
    sub4 = None
    fig1 = None
    fig2 = None
    fig3 = None
    fig4 = None
    buttons = None
    canvas = None
    msg = None

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        global image_path
        label = ttk.Label(self, text="Ketok Magic Halal", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
            
            # def on_key_press(event):
            #     print("you pressed {}".format(event.key))
            #     key_press_handler(event, canvas, toolbar)
        
        self.buttons = Frame(self)
        self.buttons.pack(side = BOTTOM, expand = True, fill = BOTH)
        
        self.msg = StringVar()
        ttk.Label(self, textvariable=self.msg).pack(side = BOTTOM)
        self.msg.set('Welcome')

        self.canvas = Canvas(self, width=1280, height=600, borderwidth=4)
        self.canvas.pack(side = TOP, expand = True, fill = BOTH)
        
        button0 = ttk.Button(self.buttons, text="Pilih Gambar", command = lambda: self.SelectImage(controller))
        button0.pack(side = LEFT)

        button1 = ttk.Button(self.buttons, text="Update", command = lambda: self.draw_image())
        button1.pack(side = LEFT)
        
        button2 = ttk.Button(self.buttons, text="Match", command = lambda: self.matchs())
        button2.pack(side = LEFT)

    def draw_image(self):
        global image_path
        #img = mpimg.imread(image_path)
        print(image_path)

        # Subplot 1st row 2nd col
        # self.sub1 = fig.add_subplot(2, 3, 2)
        # plt.imshow(img)
        self.sub1 = ImageTk.PhotoImage(Image.open(image_path).resize((540, 540), Image.ANTIALIAS))
        if (self.fig1 is None):
            self.fig1 = self.canvas.create_image(0, 0, anchor = NW, image = self.sub1)
        else:
            self.canvas.itemconfig(self.fig1, image = self.sub1)
        # Subplot 2nd row 1st col
        # self.sub2 = fig.add_subplot(2, 3, 4)
        # plt.imshow(img)
        self.sub2 = ImageTk.PhotoImage(Image.open(image_path).resize((160, 160), Image.ANTIALIAS))
        if (self.fig2 is None):
            self.fig2 = self.canvas.create_image(560, 0, anchor = NW, image = self.sub2)
        else:
            self.canvas.itemconfig(self.fig2, image = self.sub2)
        

        # Subplot 2nd row 2nd col
        # self.sub3 = fig.add_subplot(2, 3, 5)
        # plt.imshow(img)
        self.sub3 = ImageTk.PhotoImage(Image.open(image_path).resize((160, 160), Image.ANTIALIAS))
        if (self.fig3 is None):
            self.fig3 = self.canvas.create_image(560, 180, anchor = NW, image = self.sub3)
        else:
            self.canvas.itemconfig(self.fig3, image = self.sub3)
        

        # Subplot 2nd row 3rd col
        # self.sub4 = fig.add_subplot(2, 3, 6)
        # plt.imshow(img)
        self.sub4 = ImageTk.PhotoImage(Image.open(image_path).resize((160, 160), Image.ANTIALIAS))
        if (self.fig4 is None):
            self.fig4 = self.canvas.create_image(560, 360, anchor = NW, image = self.sub4)
        else:
            self.canvas.itemconfig(self.fig4, image = self.sub4)
        

        #canvas = FigureCanvasTkAgg(fig, self)  # A tk.DrawingArea.
        #canvas.draw()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # toolbar = NavigationToolbar2Tk(canvas, window)
        # toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) 
    def SelectImage(self, controller):
        global image_path
        upload_img = filedialog.askopenfilename(initialdir = "./", title = "Select file", filetypes =  (("jpeg files","*.jpg"),("all files","*.*")))
        image_path = upload_img
        #controller.show_frame(PageOne)
        self.draw_image()
        self.msg.set('Opened %s.' %image_path.split('/')[-1])
        print(image_path)

    def load_db(self, path):
        global db
        if os.path.exists(path):
            dbfile = open('pins.db', 'rb')
            db = pickle.load(dbfile)
        else:
            self.msg.set('pins.db not found. Please run generate-pickle-file.py to generate it.')

    def matchs(self):
        global db
        global image_path
        #self.buttons.pack_forget()
        self.msg.set('Extracting %s...' %image_path.split('/')[-1])
        sim = 0
        name = ' '
        dsc = extractFeatures(image_path)
        for e in db:
            print('\rMatching: %s' %e, end='')
            k = db[e]
            x = calcCosineSimilarity(dsc, k)
            if x > sim:
                sim = x
                name = e
        #self.buttons.pack()
        self.msg.set('Match with: ' + name + ' (' + str(sim) + ') ')
if __name__ == '__main__':        
    app = MainApp()
    app.geometry("1280x720")
    app.mainloop()
        
        
