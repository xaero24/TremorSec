import tkinter as tk
from tkinter import messagebox
LARGE_FONT = ("Verdana", 12)
HEIGHT = 580
WIDTH = 500


class TremorSecApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("TremorSec")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (AgreementPage, UserLogin, OptionsWindow, Stats):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(AgreementPage)

    def show_frame(self, cont):
        if cont == UserLogin:
            self.geometry('{}x{}'.format(300, 300))
        frame = self.frames[cont]
        frame.tkraise()


class AgreementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = controller
        self.parent.geometry('{}x{}'.format(HEIGHT, WIDTH))

        # # Creates the Window Size
        # canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH)
        # canvas.pack()

        # Inside frame
        frame = tk.Frame(self)
        frame.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.9)

        # ScrollBar for the agreement text box
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text object for agreement text
        text = tk.Text(frame, yscrollcommand=scrollbar.set)
        text.insert(tk.INSERT,
                    "Check\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\n123123123\n")
        text.pack(side=tk.TOP)
        scrollbar.config(command=text.yview)  # Setting the scroll bar for the box

        checkVar = tk.IntVar()  # Check box variable

        # Continue Button
        cont = tk.Button(frame, text="Continue", command=lambda: controller.show_frame(UserLogin), state=tk.DISABLED)  # Lambda function move to user login window
        cont.pack(side=tk.BOTTOM)

        def changeButtonStatus():
            print("Check Box Status:" + cont.cget('state'))
            if cont.cget('state') == 'disabled':
                cont.config(state=tk.ACTIVE)
            else:
                cont.config(state=tk.DISABLED)

        # Check Box button
        agree = tk.Checkbutton(frame, text="I have read and ACCEPT", variable=checkVar, onvalue=1, offvalue=0,
                               command=changeButtonStatus)
        agree.pack(side=tk.BOTTOM)


class UserLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame = tk.Frame(self)

        self.label_username = tk.Label(frame, text="Username")
        self.label_password = tk.Label(frame, text="Password")

        self.entry_username = tk.Entry(frame)
        self.entry_password = tk.Entry(frame, show="*")

        self.label_username.grid(row=1)
        self.label_password.grid(row=2)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.logbtn = tk.Button(frame, text="Login", command=lambda: self._login_btn_clicked(controller))
        self.logbtn.grid(columnspan=2)

        frame.place(relx=0.17, rely=0.3)

    def _login_btn_clicked(self, controller):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)

        if username == "tzvi" and password == "1234":
            messagebox.showinfo("Login info", "Welcome Tzvi")
            controller.show_frame(OptionsWindow)
        else:
            messagebox.showerror("Login error", "Incorrect username")


class OptionsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame = tk.Frame(self)
        self.StatsButton = tk.Button(frame, text="View Stats", command=lambda: controller.show_frame(Stats))
        self.StatsButton.pack(padx=10, pady=10)
        # TODO: Add graphs and stats later after we get data

        self.SendToBack = tk.Button(frame, text="Send to Background")
        self.SendToBack.pack(padx=10, pady=10)
        # TODO: Add functionality - send to background work

        self.DiasbleExit = tk.Button(frame, text="Disable and Exit", command=lambda: disableAndExit())
        self.DiasbleExit.pack(padx=10, pady=10)

        frame.place(relx=0.28, rely=0.2)

        def disableAndExit():
            # TODO: Disable key logger
            print("Exit")
            exit()


class Stats(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        test = tk.Label(self, text="Stat Window")
        test.pack()
        backButton = tk.Button(self, text="Back", command=lambda: controller.show_frame(OptionsWindow))
        backButton.pack(side=tk.BOTTOM)


app = TremorSecApp()
app.mainloop()

# #####Previous Version - Meantime Stayes as Comments#########
# HEIGHT = 580
# WIDTH = 500
#
# root = tk.Tk()
# root.resizable(False, False)
# root.title('Tremor Sec')
#
# # Centering the Window on screen
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
#
# x_cordinate = int((screen_width/2) - (HEIGHT/2))
# y_cordinate = int((screen_height/2) - (HEIGHT/2))
#
# root.geometry("{}x{}+{}+{}".format(HEIGHT, HEIGHT, x_cordinate, y_cordinate))
#
# # Creates the Window Size
# canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
# canvas.pack()
#
# # Inside frame with background color
# frame = tk.Frame(root)
# frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.78)
#
# # ScrollBar for the agreement text box
# scrollbar = tk.Scrollbar(frame)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#
# # Text object for agreement text
# text = tk.Text(frame, yscrollcommand=scrollbar.set)
# text.insert(tk.INSERT, "Check\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\nCheck\n123123123\n")
# text.pack(side=tk.TOP)
# scrollbar.config(command=text.yview)  # Setting the scroll bar for the box
#
# checkVar = tk.IntVar()  # Check box variable
#
#
# def agreementCheckBox():
#     print("Entered Function")
#     msg = messagebox.showinfo("Test", "User Login")
#
#
# # Continue Button
# cont = tk.Button(frame, text="Continue", command=agreementCheckBox, state=tk.DISABLED)
# cont.pack(side=tk.BOTTOM)
#
#
# def changeButtonStatus():
#     print("Check Box Status:" + cont.cget('state'))
#     if cont.cget('state') == 'disabled':
#         cont.config(state=tk.ACTIVE)
#     else:
#         cont.config(state=tk.DISABLED)
#
#
# # Check Box button
# agree = tk.Checkbutton(frame, text="I have read and ACCEPT", variable=checkVar, onvalue=1, offvalue=0, command=changeButtonStatus)
# agree.pack(side=tk.BOTTOM)
#
# root.mainloop()
#
