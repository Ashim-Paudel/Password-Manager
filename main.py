# ------------ IMPORTS ------------- #
from tkinter import *
from tkinter import messagebox
import json
from password_manager import PasswordManager
from encryption import *

# ------------ Login System Class ------------- #
class LogInSystem:

    def __init__(self):
        self.admin = ''
        self.window = Tk()                   # creating non-resizable window
        self.window.title("Password Manager-LogIn System")
        self.window.config(padx=50, pady=50)
        self.window.iconbitmap("images/app_icon.ico")
        self.window.resizable(0,0)
        
        # login_section_text
        self.login_sys_label = Label(text="LogIn System", font=("Courier", 20, "bold"))
        self.login_sys_label.grid(row=1, column=1, columnspan=3)
        self.window.rowconfigure(1, pad=50)

        # username and password label section
        self.username_label = Label(text="Username  :  ")
        self.username_label.grid(row=2, column=1)

        self.password_label = Label(text="Password   :  ")
        self.password_label.grid(row=3, column=1)

        # entry field
        self.username_entry = Entry(width=40, relief='solid')
        self.username_entry.grid(row=2, column=2, columnspan=2)
        self.username_entry.focus()                              # setting focus to username entry field

        self.password_entry = Entry(width=40, relief='solid', show="*")
        self.password_entry.grid(row=3, column=2, columnspan=2)

        # buttons
        self.login_button = Button(text="Login", relief="groove", cursor='hand2', command=self.login_action)
        self.login_button.grid(row=4, column=1)

        self.register_button = Button(text="Register", relief='groove', cursor="hand2", command=self.register)
        self.register_button.grid(row=4, column=3)
        self.window.rowconfigure(4, pad=30)


        self.window.mainloop()                

    def login_action(self):                    # logging in for the user
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.is_valid():
            try:                          # trying to open file in read mode if possible
                with open("user_data.json", 'r') as file:   
                    old_data = json.load(file)
            except FileNotFoundError:    # if file doesn't exist, then move to register
                if messagebox.askokcancel(title='', message="No users have been registered yet! \n Register now? "):
                    self.register()
                    self.delete_field()
            else:
                try:     # searching for the username and password in the data file
                    individual_data = old_data[f"user_{encrypt(username)}"]
                except KeyError:
                    if messagebox.askokcancel(title='', message='''You are not registered yet!!! \n Register now?'''):
                        self.register()      # if the user is not registered , asking for register
                else:
                    if username == decrypt(individual_data['name']) and password == decrypt(individual_data['password']):
                        self.admin = encrypt(username.capitalize())
                        self.window.destroy()
                        PasswordManager(self.admin)
                    else:
                        messagebox.showerror(title='Error', message="Incorrect username or password!!! ")
                        self.password_entry.delete(0, END)      
    
    def register(self):            # function to register for new user
        username = self.username_entry.get()
        password = self.password_entry.get()
        new_user_data = {f"user_{encrypt(username)}":{"name":encrypt(username), "password":encrypt(password)}}

        if self.is_valid():
            try:
                with open("user_data.json", 'r') as file:
                    old_data = json.load(file)
                    old_data.update(new_user_data)       
            except:
                with open("user_data.json", 'w') as file:
                    json.dump(new_user_data, file, indent=4)
                    self.delete_field()         
            else:
                if f"user_{encrypt(username)}" in old_data.keys():
                    messagebox.showerror(title="User Already Exists", message=f"The user '{username}', you are trying to register already exists.")
                else:
                    with open("user_data.json", 'w') as file:
                        json.dump(old_data, file, indent=4)
                    self.delete_field()      

    def is_valid(self):       # function to check none of the entry field are left empty 
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == '' or password == '':
            messagebox.showerror(title="Empty fields", message="It seems that one or more fields are left empty. ")
            return False
        else:
            return True

    def delete_field(self):        #this will delete the entry field data
        for items in [self.username_entry, self.password_entry]:
            items.delete(0, END)


if __name__ == "__main__":
    LogInSystem()
