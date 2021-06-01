from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from numpy import *
import time


class Plots(Frame):
    '''class for all widgets at the right
    side of the window'''

    def __init__(self, master=None):
        '''Takes optional argument master,
        initalize frame instance, master,
        functions that create canvas and widgets.'''
        Frame.__init__(self, master)
        Pack.config(self)
        self.master = master
        self.createWidgets()

    def quit(self):
        '''end program'''
        import sys;
        sys.exit()

    def createWidgets(self):
        '''create widgets and place them
        with gird() :
        >label above entry space for title of plot and axis description (desc_label)
        >entry space for those values (desc_entry)
        >quit button'''
        self.title_lbl = Label(self, text="tytuł rysunku")
        self.title_lbl.grid(row=0, column=0)
        self.x_lbl = Label(self, text="etykieta osi x")
        self.x_lbl.grid(row=0, column=1)
        self.y_lbl = Label(self, text="etykieta osi y")
        self.y_lbl.grid(row=0, column=2)
        self.title_entry = Entry(self)
        self.title_entry.grid(row=1, column=0)
        self.x_entry = Entry(self)
        self.x_entry.grid(row=1, column=1)
        self.y_entry = Entry(self)
        self.y_entry.grid(row=1, column=2)
        self.createCanvas()
        self.QUIT = Button(self, text='KONIEC', command=self.quit)
        self.QUIT.grid(row=4, column=2)

    def createCanvas(self):
        '''create blank canvas an place it
        using gird()'''
        self.figure = Figure(figsize=(7, 7), dpi=75)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=2,column=0, columnspan=3)

    def clear_canvas(self):
        '''close fig and delete all instances on canvas'''
        try:
            plt.close(self.figure)
            self.canvas.get_tk_widget().delete("all")
        except:
            pass

    def draw_on_Canvas(self, f, x_lims, y_lims, legend, save):
        '''takes arguments f-list of funcions, x_lims - limes for x axis
        in form of min,max; y_lims - limes fo y axis in the same form
        and c - value of the check button.
        Destory previous canvas and figure, then:
        >get descripion from desc_entry and splits it
        >split x_lims and y_lims to lists
        >create a new figure
        >create list of x values based on x_lim if possible
        (default - 100 values between 0 and 10)
        >plot functions using eval() function and dictionary of math functions
        if possible, if not plot text "Niewłaściwy wzór funkcji"
        >set tile nad labels if possible
        >creates canvas instance'''
        # clear canvas and figure
        self.clear_canvas()

        # create figure
        self.figure = Figure(figsize=(7, 7), dpi=75)
        self.ax = self.figure.add_subplot(111)

        #set x lims
        try:
            self.x_lim_list = x_lims.split(",")
            self.ax.set_xlim([float(self.x_lim_list[0]), float(self.x_lim_list[1])])
        except:
            pass

        #set y lims
        try:
            self.y_lim_list = y_lims.split(",")
            self.ax.set_ylim([float(self.y_lim_list[0]), float(self.y_lim_list[1])])
        except:
            pass

        #set xs according to x lims if possible
        try:
            x = linspace(float(self.x_lim_list[0]),
                                  float(self.x_lim_list[1]),
                                  round((float(self.x_lim_list[1]) - float(self.x_lim_list[0]))*100))
        except:
            x = linspace(0, 10, 100)

        try:
            # read functions
            for i in range(len(f)):
                self.ys = eval(f[i].replace("^","**"))
                self.ax.plot(x, self.ys)

            # set tile and labels
            self.ax.set_title(self.title_entry.get())
            self.ax.set_xlabel(self.x_entry.get())
            self.ax.set_ylabel(self.y_entry.get())

            # add legend
            if legend:
                self.ax.legend(f)


        except:
            self.ax.set_xlim([0, 15])
            self.ax.set_ylim([0, 15])
            self.ax.text(1, 8, "Nieprawidłowy wzór funckji", fontsize=15, color='red')

        # create canvas with plot
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=2,column=0, columnspan=3)

        if save:
            self.figure.savefig("wykres" + str(time.time()) + ".png")


class Buttons(Frame):
    '''Handles and creates widgets
    on the left side of the window'''

    def __init__(self, master=None):
        '''takes optional argument master,
        initalize frame, master and function
        createWidgets()'''
        Frame.__init__(self, master)
        Pack.config(self)
        self.master = master
        self.createWidgets()

    def createWidgets(self):
        '''Create widgets:
        >label above entry space to enter functions' formulas separated by semicolon
        >entry space for those formulas (should be separeated by colon)
        > buttons of calculator, if clicked their text is added to entry space (b0-b13)
        >labels for x_lims and y_lims and entry spaces(e2,e3)
        >create checkbutton legend with value var
        (if checked add legend to the plot)
        >create checkbutton save with value var2
        (if checked save plot to .png file)
        and places them with grid()'''
        self.lbl1 = Label(self, text="Wpisz wzór funkcji")
        self.lbl1.grid(row=0, column=0, columnspan=7)
        self.e1 = Entry(self,width=75)
        self.e1.grid(row=1, column=0, columnspan=7)
        self.b0 = Button(self, text="CE", width=5, command=lambda: self.e1.delete(0, END))
        self.b0.grid(row=2, column=0)
        self.b1 = Button(self, text="(", width=5, command=lambda: self.show_press(self.b1))
        self.b1.grid(row=2, column=1)
        self.b2 = Button(self, text=")", width=5, command=lambda: self.show_press(self.b2))
        self.b2.grid(row=2, column=2)
        self.b3 = Button(self, text="sqrt", width=5, command=lambda: self.show_press(self.b3))
        self.b3.grid(row=2, column=3)
        self.b4 = Button(self, text="%", width=5, command=lambda: self.show_press(self.b4))
        self.b4.grid(row=2, column=4)
        self.b5 = Button(self, text="+", width=5, command=lambda: self.show_press(self.b5))
        self.b5.grid(row=2, column=5)
        self.b6 = Button(self, text="-", width=5, command=lambda: self.show_press(self.b6))
        self.b6.grid(row=2, column=6)
        self.b7 = Button(self, text="*", width=5, command=lambda: self.show_press(self.b7))
        self.b7.grid(row=3, column=0)
        self.b8 = Button(self, text="^", width=5, command=lambda: self.show_press(self.b8))
        self.b8.grid(row=3, column=1)
        self.b9 = Button(self, text="÷", width=5, command=lambda: self.show_press(self.b9))
        self.b9.grid(row=3, column=2)
        self.b10 = Button(self, text="sin", width=5, command=lambda: self.show_press(self.b10))
        self.b10.grid(row=3, column=3)
        self.b11 = Button(self, text="cos", width=5, command=lambda: self.show_press(self.b11))
        self.b11.grid(row=3, column=4)
        self.b12 = Button(self, text="tan", width=5, command=lambda: self.show_press(self.b12))
        self.b12.grid(row=3, column=5)
        self.b13 = Button(self, text="fabs", width=5, command=lambda: self.show_press(self.b13))
        self.b13.grid(row=3, column=6)

        self.xlims_lbl = Label(self, text="zakres osi X np. 0,10")
        self.xlims_lbl.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.e2 = Entry(self)
        self.e2.grid(row=5, column=0, columnspan=3, pady=5)
        self.ylims_lbl = Label(self, text="zakres osi Y np. 0,10")
        self.ylims_lbl.grid(row=4, column=4, columnspan=3, pady=5)
        self.e3 = Entry(self)
        self.e3.grid(row=5, column=4, columnspan=3, pady=5)

        self.var = IntVar()
        self.legend = Checkbutton(self, text="Legenda", variable=self.var)
        self.legend.grid(row=6, column=0, columnspan=2, pady=5)
        self.var2 = IntVar()
        self.save = Checkbutton(self, text="Zapisz wykres", variable=self.var2)
        self.save.grid(row=6, column=3, pady=5, columnspan=2)

    def show_press(self, b):
        '''takes argument b of type button
        nad insert it's text to entry space e1'''
        self.e1.insert(END, b['text'])

    def get_entry(self):
        ''''gets values from entry space e1'''
        return self.e1.get()


class MainWin(Tk):
    '''connect two frames and
    addtional functions as clear button,
    start button, help menu'''
    def __init__(self, master=None):
        '''initialize main window,
        mainWidget function and create_Menu
        function'''
        Tk.__init__(self, master)
        Tk.wm_title(self, "Rysowanie wykresów")
        self.menubar = Menu(self)
        self.mainWidgets()
        self.create_Menu()

    def mainWidgets(self):
        '''create instances of classes
        Plots and Buttons, start button connected to
        drawing() function and clear button connected
        to the clear() function'''
        self.window1 = Plots(self)
        self.window1.pack(side=RIGHT, fill=BOTH)
        self.window2 = Buttons(self)
        self.window2.pack(side=LEFT, fill=BOTH)
        self.start = Button(self.window2, text="Generuj wykres", command=self.drawing)
        self.start.grid(row=7, column=0, padx=5, pady=5, columnspan=2)
        self.clear_button = Button(self.window2, text="Wyczyść", command=self.clear)
        self.clear_button.grid(row=7, column=3, columnspan=2)

    def drawing(self):
        '''get values from entry spaces in both
        frames and draw plot using draw_on_Canvas
        function from window1'''
        functions = self.window2.get_entry()
        fun_list = functions.split(";")
        x_lims = self.window2.e2.get()
        y_lims = self.window2.e3.get()
        if_legend = self.window2.var.get()
        if_save = self.window2.var2.get()
        self.window1.draw_on_Canvas(fun_list, x_lims, y_lims, if_legend, if_save)

    def clear(self):
        '''clear all entry spaces, canvas,
        checkboxes'''
        self.window1.title_entry.delete(0, END)
        self.window1.x_entry.delete(0, END)
        self.window1.y_entry.delete(0, END)
        self.window2.e1.delete(0, END)
        self.window2.e2.delete(0, END)
        self.window2.e3.delete(0, END)
        self.window2.var.set(0)
        self.window2.var2.set(0)
        self.window1.clear_canvas()

    def create_Menu(self):
        '''create help menu with command 'opis działania'
         linked to HelpWidgets function'''
        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_command(label="Opis działania", command=self.HelpWidgets)
        self.menubar.add_cascade(label="Pomoc", menu=self.help)
        self.config(menu=self.menubar)

    def HelpWidgets(self):
        '''create label with help message
        and button exit to close help window'''
        self.helpwin = Toplevel(self)
        self.message ="""       Aplikacja pozwala na rysowanie wykresów funckji.
        W polu wpisz wzór funkcji dozwolone jest podanie więcej niż 
        jednego wzoru. Powinny one być oddzielone znakiem średnika .
        Oprócz funkcji widocznych w postaci kalkulatora obsługuje 
        także funckje dostępne w module numpy.
        Opcjonalnie można oddać opcje takie jak:
        > zakresy osi 0X, 0Y;
        > tytuł wykresu;
        > opisy osi 0X, 0y;
        > dodanie legendy;
        > zapisanie wykresu do pliku .png
        Przycisk generuj wykres uruchamia rysowanie, natomiast 
        wyczyść resetuje wszystkie pola."""
        self.help_lbl = Label(self.helpwin, text=self.message, justify=LEFT)
        self.help_lbl.pack()
        self.exit = Button(self.helpwin, text="KONIEC", command=self.helpwin.destroy)
        self.exit.pack()




if __name__ == "__main__":
    app = MainWin()
    app.mainloop()
