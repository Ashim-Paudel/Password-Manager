from tkinter import *                # for whole UI creation
from tkinter import messagebox       # for pop-up boxes
import string                        # for ascii letters and digits
import pyperclip                     # for copying generated password immediately
import json                          # for handling of json data files
import random                
from encryption import *

class PasswordManager:
    # ---------------------- UI ----------------- #
    def __init__(self, current_username):
        self.current_username = current_username        # this is used to display the current user name.
        self.window = Tk()
        self.window.title("Password Mana-Generator")
        self.window.config(padx=50, pady=50)
        self.window.iconbitmap("images/app_icon.ico")
        self.window.resizable(0, 0)

        self.admin_label = Label(text=f"Greetings {decrypt(self.current_username)} !", font=("Courier", 15, 'bold'), relief='groove', width=28)
        self.admin_label.grid(row=1, column=1, columnspan=3)
        self.window.rowconfigure(1, pad=20)

        # adding required picture for attractive looks
        self.canvas = Canvas(width=200, height=200)
        pass_gen_img = PhotoImage(file="images/password_manager_image.png")
        self.canvas.create_image(100, 100, image=pass_gen_img)
        self.canvas.grid(row=0, column=2)

        # labels
        self.website_label = Label(text="Website :")
        self.website_label.grid(row=2, column=1)

        self.email_label = Label(text="Email/Username :")
        self.email_label.grid(row=3, column=1)

        self.password_label = Label(text="Password :")
        self.password_label.grid(row=4, column=1)


        # entry fields
        self.website_entry = Entry(width=36, relief="solid")
        self.website_entry.grid(row=2, column=2)
        self.website_entry.focus()

        self.email_entry = Entry(width=55, relief="solid")
        self.email_entry.grid(row=3, column=2, columnspan=2)

        self.password_entry = Entry(width=36, relief="solid")
        self.password_entry.grid(row=4, column=2)


        # button fields
        self.generate_button = Button(text="Generate Password",
                                cursor="hand2", relief="groove", command=self.generate_random_password)
        self.generate_button.grid(row=4, column=3)

        self.add_button = Button(text="Add", cursor="hand2",
                            relief="groove", width=46, command=self.save_password)
        self.add_button.grid(row=5, column=2, columnspan=2)

        self.search_button = Button(text="Search", cursor="hand2", relief="groove", width=14, command=self.search_website)
        self.search_button.grid(row=2, column=3)

        self.window.mainloop()


    def generate_random_password(self):       # function to generate random password of 10 character length
        characters = list("#@!%$&*_?")
        alpha_lower = list(string.ascii_lowercase)
        alpha_upper = list(string.ascii_uppercase)
        nums = list(string.digits)

        for items in [characters, alpha_lower, alpha_upper, nums]:     # create a list of all characters and shuffle it
            random.shuffle(items)

        password_list = list(
            alpha_lower[:3]+alpha_upper[:3]+nums[:3]+characters[:3])  # including 3 characters from each
        random.shuffle(password_list)
        final_password = ''.join(ch for ch in password_list[:10])  # slicing only 10 characters from shuffled list
        self.password_entry.delete(0, END)
        self.password_entry.insert(END, final_password)

        pyperclip.copy(final_password)     # copy that generated password directly to clipboard



    # -------------- password saving mechanism ----------- #
    def save_password(self):       # function to add (password, username and website name) to a json file
        # getting strings from entry fields
        user_website = self.website_entry.get()
        user_email = self.email_entry.get()
        user_password = self.password_entry.get()

        # checking if the respective strings are of valid length (>0)
        if len(user_website) == 0 or len(user_email) == 0 or len(user_password) == 0:
            messagebox.showerror(
                title="Error !!!", message="It seems than one or more fields are left empty.")    # message box to show warning

        else:
            # if everything is okay, then start to write in a file
            entry_field_data = {
            user_website.capitalize(): {
                "E-mail": encrypt(user_email),
                "Password": encrypt(user_password)
            }
            }     # a sample nested dictionary for getting the entry filed datas

            try:
                data_file = open(f"{self.current_username}passwords.json", "r")                # try to open file in read mode
            except FileNotFoundError:                                  # if file doesn't exist
                data_file = open(f"{self.current_username}passwords.json", "w")                # open in write mode
                json.dump(entry_field_data, data_file, indent=4)       # dump all the data to json file
            else:                                                      # if file can be opened in read mode
                old_data = json.load(data_file)                        # load inital data in file to a variable
                old_data.update(entry_field_data)                      # update initial file data with entry filed datas

                with open(f"{self.current_username}passwords.json", "w") as data_file:         # again open file in write mode and dump all data
                    json.dump(old_data, data_file, indent=4)

            finally:
                data_file.close()                                      # close the file
        
                for items in self.website_entry, self.email_entry, self.password_entry:
                    items.delete(0, END)                               # deleting all the entry filed datas after saving


    # ---------------- Search Mechanism ------------ #
    def search_website(self):                                         # function to search saved password by website name
        website_name = self.website_entry.get()

        try:        # try to open file in read mode
            with open(f"{self.current_username}passwords.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:            # in case the file is not created yet!
            messagebox.showerror(title="", message="You have not stored any data yet!!! ")
        else:
            if len(website_name)!=0:       # if website name field isnot empty yet
                website_name = website_name.capitalize()   # avoid case error
                try:
                    website_data = data[website_name]
                    message_to_show = f'''
                    E-mail/ Username : {decrypt(website_data['E-mail'])}
                    Password : {decrypt(website_data["Password"])}
                    '''
                    pyperclip.copy(decrypt(website_data["Password"]))  # instantly copy that website password 
                    
                    messagebox.showinfo(title=website_name, message=message_to_show) # show all data in dialogue box
                except KeyError:
                    messagebox.showerror(title="No Data Found", message=f"There is no any data to show for {website_name}")
            else: # if website entry field is entered
                messagebox.showwarning(title='Empty Field', message='Please enter website name to show info. ')


if __name__ == "__main__":
    ashim = encrypt("Ashim")
    PasswordManager(ashim)
