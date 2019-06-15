import tkinter as tk
import os
import csv
import subprocess as sp
from BasicKeyLogger import KeyLogger
from Plots import PlotCreate
from tkinter import messagebox
import connector
import sha1
import fernetAES
import user
from cryptography.fernet import InvalidToken

try:
    connection = connector.connection()  # Creates DB Connection Module
except Exception as e:
    print(e)
    print("Failed to create Server Connection")
    messagebox.showerror("Failed To connect",
                         "Failed to Create Server Connection \nThe program will terminate")
    exit(1)
current_user = user.User()  # Creates Global User Obj for later use

LARGE_FONT = ("Verdana", 12)
HEIGHT = 580
WIDTH = 500
dirName = "Results"
# define test modes
test1 = 1
test1Phase2Var = 11
test2 = 2
normalMode = 3
# graph mode
file = 0
server = 1
# Buffer overflow limit
overFlow_limit = 80


class TremorSecApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("TremorSec")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (AgreementPage, UserLogin, OptionsWindow, Stats, StartStop, Test1, Test2, Test1Phase2, SignUp):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(AgreementPage)

    def show_frame(self, cont):
        name = self.frames[cont].winfo_name()
        # Checks if the window required is option window and done_test1 declared and set to TRUE
        # Meaning the user finished the first test1 and the button should be disabled
        if self.frames[cont].winfo_name() == '!optionswindow' and 'done_test1' in globals() and done_test1 is True:
            frame = self.frames[cont]
            frame.Test1Button.config(state=tk.DISABLED)
        # Same for test No 2
        if self.frames[cont].winfo_name() == '!optionswindow' and 'done_test2' in globals() and done_test2 is True:
            frame = self.frames[cont]
            frame.Test2Button.config(state=tk.DISABLED)
        if self.frames[cont].winfo_name() == '!optionswindow' and 'done_tests' not in globals():
            frame = self.frames[cont]
            frame.StatsButton.config(state=tk.DISABLED)
        # If the user finished both tests => checks the length of the reasultsFile.csv
        if (self.frames[cont].winfo_name() == '!optionswindow' and 'done_tests' in globals() and done_tests is True) or (self.frames[cont].winfo_name() == '!optionswindow' and 'done_test1' in globals() and done_test1 is True and 'done_test2' in globals() and done_test2 is True):
            frame = self.frames[cont]
            frame.Test1Button.config(state=tk.DISABLED)
            frame.Test2Button.config(state=tk.DISABLED)
            frame.StatsButton.config(state=tk.ACTIVE)
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
                    "The user agrees to the term of use.\n"
                    + "User know that the app is working with key logger that \nlogging all of his key stroks\n"
                    + "Saves locally all the data and encrypts the data.\n"
                    + "Some data sent to the remote server that contains only \nthe statistical value.")
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

        self.entry_username = LimEntry(frame)
        self.entry_password = LimEntry(frame, show="*")

        self.label_username.grid(row=1)
        self.label_password.grid(row=2)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.logbtn = tk.Button(frame, text="Login", command=lambda: self._login_btn_clicked(controller))
        self.logbtn.grid(columnspan=2)

        self.logbtn = tk.Button(frame, text="Sign Up", command=lambda: controller.show_frame(SignUp))
        self.logbtn.grid(columnspan=2)

        frame.place(relx=0.17, rely=0.3)

    def _login_btn_clicked(self, controller):
        userDb = connection.readUsers()  # Load all user Data base as Dictionary
        username = self.entry_username.get()
        password = self.entry_password.get()
        local_Sha = sha1.shaControl(password)  # Creates Sha1 Module
        local_Sha.sha1()  # Converts the password to Hash

        global done_tests  # For disabling the buttons if user finished the tests

        if username in userDb:  # Checks if username in DB
            if userDb[username][0] == local_Sha.password:  # Compares 2 passwords
                messagebox.showinfo("Login info", "Welcome " + username)
                # Checks if resultfile.csv exists, if not creates one and write in the first line the username
                first_entrance_bit = False
                exists = os.path.isfile("resultsFile.csv")
                if not exists:
                    resultfile = open("resultsFile.csv", 'a+')
                    fileWriter = csv.writer(resultfile)
                    fileWriter.writerow(["User info: ", username])
                    resultfile.close()
                    first_entrance_bit = True
                if userDb[username][2] is not None:
                    KL.set_User(username, userDb[username][1], fernetAES.fernet_Encryption(userDb[username][2].encode()))  # Sets the KeyLogger with values: UserName, User Server Id, Fernet Key class
                    current_user.user_name = username
                    current_user.user_server_id = userDb[username][1]
                    current_user.fernet_class = fernetAES.fernet_Encryption(userDb[username][2].encode())
                    if not exists:
                        current_user.fernet_class.encrypt_file("resultsFile.csv")
                    elif first_entrance_bit is False:
                        try:
                            current_user.fernet_class.decrypt_file("resultsFile.csv")
                            try:
                                with open("resultsFile.csv", "r") as file2:
                                    data = file2.read()
                                    data = data.split(',')  # len 11 - The length of the file if user finished both tests
                                    if len(data) is 11:
                                        done_tests = True
                            finally:
                                current_user.fernet_class.encrypt_file("resultsFile.csv")
                        except InvalidToken:
                            messagebox.showerror("Bad User", "User does not match the current machine \nThe Program will end \nEnter with correct User")
                            exit(1)
                else:
                    KL.set_User(username, userDb[username][1])
                controller.show_frame(OptionsWindow)
            else:
                messagebox.showerror("Login error", "Incorrect username or password")
        else:
            messagebox.showerror("Login error", "Incorrect username or password")


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        frame = tk.Frame(self)

        self.label_username = tk.Label(frame, text="Username")
        self.label_password = tk.Label(frame, text="Password")
        self.label_email = tk.Label(frame, text="Email")

        self.entry_username = LimEntry(frame)
        self.entry_password = LimEntry(frame, show="*")
        self.entry_email = LimEntry(frame)

        self.label_username.grid(row=1)
        self.label_password.grid(row=2)
        self.label_email.grid(row=3)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        self.entry_email.grid(row=3, column=1)

        self.logbtn = tk.Button(frame, text="Sign Up", command=lambda: self._login_btn_clicked(controller))
        self.logbtn.grid(columnspan=2)

        self.backButton = tk.Button(frame, text="Back", command=lambda: controller.show_frame(UserLogin))
        self.backButton.grid(columnspan=2)
        frame.place(relx=0.17, rely=0.3)

    def _login_btn_clicked(self, controller):
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        userDb = connection.readUsers()  # Load all user Data base as Dictionary
        if username == '' or password == '' or email == '':
            messagebox.showerror("Sing Up", "ERROR All Fields Required")
        elif username not in userDb:  # checks if userName already exists
            # TODO: check for user inputs and breakpoints
            usr = user.User()
            usr.user_name = username
            usr.email = email
            self.pop = Verification_PopUp(self.parent, usr.check())
            self.parent.wait_window(self.pop.top)
            if self.pop.ok_bit is True:
                if connection.signUp_User(username, password, email):
                    messagebox.showinfo("Sing Up", "Added New User: " + username)
                    controller.show_frame(UserLogin)
                else:
                    messagebox.showerror("Sing Up", "ERROR Adding new user")
            else:
                messagebox.showerror("Sing Up", "ERROR \nWrong Verification Code \nTry Again")
        else:
            messagebox.showerror("Sing Up", "ERROR User Name Already Exists")


class Verification_PopUp(tk.Frame):
    def __init__(self, parent, verifier=None):
        tk.Frame.__init__(self, parent)
        self.verifier = verifier
        top = self.top = tk.Toplevel(parent)
        self.l = tk.Label(top, text="Enter Verification Code")
        self.l.pack()
        self.e = LimEntry(top)
        self.e.pack()
        self.b = tk.Button(top, text='Ok', command=self.cleanup)
        self.b.pack()
        self.ok_bit = False

    def cleanup(self):
        value = self.e.get()
        try:
            value = int(value)
            if value == self.verifier:
                self.ok_bit = True
        except ValueError:
            messagebox.showerror("ERROR", "Input Number should be only Numbers.")
        self.top.destroy()


class OptionsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame = tk.Frame(self)

        self.KeyLoggerButton = tk.Button(frame, text="Key Logger", command=lambda: controller.show_frame(StartStop))
        self.KeyLoggerButton.pack(padx=10, pady=10)

        self.Test1Button = tk.Button(frame, text="Test 1", command=lambda: controller.show_frame(Test1))
        self.Test1Button.pack(padx=10, pady=10)

        self.Test2Button = tk.Button(frame, text="Test 2", command=lambda: controller.show_frame(Test2))
        self.Test2Button.pack(padx=10, pady=10)

        self.StatsButton = tk.Button(frame, text="View Stats", command=lambda: controller.show_frame(Stats))
        self.StatsButton.pack(padx=10, pady=10)

        self.DisableExit = tk.Button(frame, text="Disable and Exit", command=lambda: disableAndExit())
        self.DisableExit.pack(padx=10, pady=10)

        frame.place(relx=0.28, rely=0.1)

        def disableAndExit():
            print("Exit")
            exit()


class Stats(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        test = tk.Label(self, text="Stat Window")
        test.pack()
        plot = PlotCreate(file)
        tButton = tk.Button(self, text="Show Graph", command=lambda: PlotCreate.createPlot(plot, current_user))
        tButton.pack(pady=30)
        plotServer = PlotCreate(server)
        tButton = tk.Button(self, text="Show Graph from server", command=lambda: PlotCreate.createPlot(plotServer, current_user))
        tButton.pack(pady=30)
        backButton = tk.Button(self, text="Back", command=lambda: controller.show_frame(OptionsWindow))
        backButton.pack(side=tk.BOTTOM)


class StartStop(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        test = tk.Label(self, text="Key Logger")
        test.pack()

        # Create target Directory if don't exist
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        else:
            print("Directory ", dirName, " already exists")

        if not os.path.exists(dirName + "/ResultsCsv"):
            os.mkdir(dirName + "/ResultsCsv")
            print("Directory ", dirName + "/ResultsCsv", " Created ")
        else:
            print("Directory ", dirName + "/ResultsCsv", " already exists")

        if not os.path.exists(dirName + "/Encrypted"):
            os.mkdir(dirName + "/Encrypted")
            print("Directory ", dirName + "/Encrypted", " Created ")
        else:
            print("Directory ", dirName + "/Encrypted", " already exists")

        # exists = os.path.isfile(dirName + "AvgSpeeds.txt")
        # if not exists:
        #     open(dirName + "/AvgSpeeds.txt", 'a').close()

        self.canvas = tk.Canvas(self, width=31, height=31)
        self.indicator = self.canvas.create_oval(1, 1, 30, 30, outline="#000000", fill="#dd0d0d", width=2)

        backButton = tk.Button(self, text="Back", command=lambda: controller.show_frame(OptionsWindow))

        KeyLoggerButton = tk.Button(self, text="Start", command=lambda: self.startKeyLoggerNormal())
        KeyLoggerButton.pack(padx=10, pady=10)

        instructions = tk.Label(self,
                                text="As you press start the Key Logger will start working. \nThe app will be suspended. \nTo stop recording press ESC")
        instructions.pack()

        self.canvas.pack()

        KeyLoggerButton.pack(side=tk.TOP)
        backButton.pack(side=tk.BOTTOM)

    def startKeyLoggerNormal(self):
        self.canvas.itemconfig(self.indicator, fill="#38ce0a")
        self.update()
        KL.activateKeyLogger(normalMode)
        self.canvas.itemconfig(self.indicator, fill="#ef0404")
        self.update()


class Test1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        test = tk.Label(self, text="Test1")
        test.pack()

        self.canvas = tk.Canvas(self, width=31, height=31)
        self.indicator = self.canvas.create_oval(1, 1, 30, 30, outline="#000000", fill="#dd0d0d", width=2)

        instructions = tk.Label(self,
                                text="This is the First test to check for baseline."
                                     + "\nPlease press buttons: a & p  \n"
                                     + "Press the keys with one hand of your'e choosing \n"
                                     + "rapidly as fast as you can for 15 sec \n"
                                     + "The test will begin when you press START"
                                     + "\n\nNOTE: the app will suspend during the time of the test")

        instructions.pack()
        openButton = tk.Button(self, text="Open input NotePad", command=lambda: openFiles())
        openButton.pack(padx=10, pady=10)

        # KeyLoggerButton = tk.Button(self, text="Start", command=lambda: KL.activateKeyLogger(test1))
        KeyLoggerButton = tk.Button(self, text="Start", command=lambda: self.activation())
        KeyLoggerButton.pack()

        self.canvas.pack()

        backButton = tk.Button(self, text="Continue to second phase", command=lambda: openFiles(1))
        backButton.pack(padx=10, pady=15)

        def openFiles(back=None):
            if back is None:
                self.s = sp.Popen(['notepad', "input.txt"])
            if back is 1:
                try:
                    self.s.terminate()
                except Exception:
                    pass
                finally:
                    controller.show_frame(Test1Phase2)

    def activation(self):
        self.canvas.itemconfig(self.indicator, fill="#38ce0a")
        self.update()
        KL.activateKeyLogger(test1)
        self.canvas.itemconfig(self.indicator, fill="#ef0404")
        self.update()
        messagebox.showinfo("Times Up !!", "Times Up !! Continue")


class Test1Phase2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        test = tk.Label(self, text="Test1 Phase2")
        test.pack()

        self.canvas = tk.Canvas(self, width=31, height=31)
        self.indicator = self.canvas.create_oval(1, 1, 30, 30, outline="#000000", fill="#dd0d0d", width=2)

        instructions = tk.Label(self,
                                text="This is the First test to check for baseline."
                                     + "\nPlease press buttons: a & p  \n"
                                     + "Press the keys with both hands \n"
                                     + "rapidly as fast as you can for 15 sec \n"
                                     + "The test will begin when you press START"
                                     + "\n\nNOTE: the app will suspend during the time of the test")

        instructions.pack()

        openButton = tk.Button(self, text="Open input NotePad", command=lambda: openFiles())
        openButton.pack(padx=10, pady=10)

        KeyLoggerButton = tk.Button(self, text="Start", command=lambda: self.activation())
        KeyLoggerButton.pack(padx=10, pady=10)

        self.canvas.pack()

        backButton = tk.Button(self, text="Back", command=lambda: openFiles(1))
        backButton.pack(side=tk.BOTTOM)

        def openFiles(back=None):
            if back is None:
                self.s = sp.Popen(['notepad', "input.txt"])
            if back is 1:
                try:
                    self.s.terminate()
                except Exception:
                    pass
                finally:
                    controller.show_frame(OptionsWindow)

    def activation(self):
        self.canvas.itemconfig(self.indicator, fill="#38ce0a")
        self.update()
        KL.activateKeyLogger(test1Phase2Var)
        global done_test1
        done_test1 = True
        self.canvas.itemconfig(self.indicator, fill="#ef0404")
        self.update()
        messagebox.showinfo("Times Up !!", "Times Up !! Continue")


class Test2(tk.Frame):
    def __init__(self, parent, controller):
        self.f = None
        self.s = None
        tk.Frame.__init__(self, parent)
        test = tk.Label(self, text="Test2")
        test.pack()

        self.canvas = tk.Canvas(self, width=31, height=31)
        self.indicator = self.canvas.create_oval(1, 1, 30, 30, outline="#000000", fill="#dd0d0d", width=2)

        instructions = tk.Label(self,
                                text="This is the Second test \n"
                                + "In this test youll have to type a text as fast as you can\n"
                                + "And we will measure the average type speed \n"
                                + "NOTE: The app suspends when the test is running. \n")

        instructions.pack()

        openButton = tk.Button(self, text="Open files", command=lambda: openFiles())
        openButton.pack(padx=10, pady=10)

        KeyLoggerButton = tk.Button(self, text="Start", command=lambda: self.activationTest2())
        KeyLoggerButton.pack(padx=10, pady=10)

        self.canvas.pack()

        backButton = tk.Button(self, text="Back", command=lambda: openFiles(1))
        backButton.pack(side=tk.BOTTOM)

        def openFiles(back=None):
            if back is None:
                self.s = sp.Popen(['notepad', "textsource.txt"])
                self.f = sp.Popen(['notepad', "writetest.txt"])
            if back is 1:
                try:
                    self.f.terminate()
                    self.s.terminate()
                except Exception:
                    pass
                finally:
                    controller.show_frame(OptionsWindow)

    def activationTest2(self):
        self.canvas.itemconfig(self.indicator, fill="#38ce0a")
        self.update()
        KL.activateKeyLogger(test2)
        global done_test2
        done_test2 = True
        self.canvas.itemconfig(self.indicator, fill="#ef0404")
        self.update()


class LimEntry(tk.Entry):
    """
    Limit Entry input at Entry boxes - To prevent Buffer Overflow
    Var input_Limit => Upper limit input
    """
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        vcmd = (self.register(self.on_validate), "%P")
        self.configure(validate="key", validatecommand=vcmd)
        self.input_Limit = overFlow_limit  # The variable to determine the upper limit at input Box

    def disallow(self):
        self.bell()
        messagebox.showerror("Buffer OverFlow",
                             "Buffer Over-Flow Change input")

    def on_validate(self, new_value):
        try:
            if new_value.strip() == "":
                return True
            if len(new_value) > self.input_Limit:
                self.disallow()
                return False
        except ValueError:
            self.disallow()
            return False

        return True


KL = KeyLogger()
app = TremorSecApp()
app.mainloop()
