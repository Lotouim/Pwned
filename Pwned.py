import requests
import hashlib
from art import text2art
from termcolor import colored
import os
import argparse
import random 
import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk
from tkinter import filedialog
import subprocess



def clearConsole():
    return os.system("cls" if os.name in ("nt", "dos") else "clear")

clearConsole()


parser = argparse.ArgumentParser(description="Check if a password has been compromised.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-p", "--password", type=str, help="the password to check")
group.add_argument("-e", "--explication", action="store_true", help="usage's explication")
group.add_argument("-f", "--file", type = str, help="the path to the file containing passwords")
group.add_argument("-g", "--generate", action="store_true", help="generate a random password")
group.add_argument("-b", "--botdiscord", action="store_true", help="start discord'bot")
group.add_argument("-wizard", "--wizard", action="store_true", help="Graphic prob")
args = parser.parse_args()

def check_password(password):
    sha_password = hashlib.sha1(password.encode()).hexdigest()
    sha_prefix = sha_password[:5]
    sha_postfix = sha_password[5:].upper()

    url = "https://api.pwnedpasswords.com/range/" + sha_prefix

    try:
        response = requests.get(url)

        pwnd_dict = {}
        pwnd_list = response.text.split("\r\n")
        for pwnd_pass in pwnd_list:
            pwnd_hash = pwnd_pass.split(":")
            pwnd_dict[pwnd_hash[0]] = pwnd_hash[1]

        if sha_postfix in pwnd_dict.keys():
            return int(pwnd_dict[sha_postfix])
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print("\033[91mErreur de connexion au service Pwned Passwords :", e, "\033[0m")
        return -1

class GraphUser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PWNED?")
        self.root.configure(bg='#000000')
        self.root.geometry("1200x800")
        self.cool = ttk.Frame(self.root)

        self.notebook = ttk.Notebook(self.cool)

        style = ttk.Style()
        style.configure("Custom.TFrame", background ='black')

        self.tab1 = ttk.Frame(self.notebook, height = 660, style = "Custom.TFrame")
        self.tab2 = ttk.Frame(self.notebook, height = 660, style = "Custom.TFrame")
        self.tab3 = ttk.Frame(self.notebook, height = 660, style = "Custom.TFrame")
        self.notebook.add(self.tab1, text="                                                    Generate safe password                                         ")
        self.notebook.add(self.tab2, text="                                                    Test file passwords                                            ")
        self.notebook.add(self.tab3, text="                                                    Test a single password                                         ")
        self.ExitButton = ttk.Button(self.root, command = self.root.destroy, text = 'QUIT').grid(row = 2)
        self.notebook.grid()
        self.cool.grid(row = 1)
        self.entry = ttk.Entry(self.tab1)
        self.ValeurEntre = ttk.Label(self.tab1, text="Please enter a password length : ", background = "black", foreground = "white", font=("Castellar", 15))
        self.CheckMyPwd = ttk.Label(self.tab3, text = "", foreground = "white", background ="black")
        self.SecondPageFrame =ttk.Frame(self.tab2, width = 500, height = 300, style = 'Custom.TFrame', padding ="5")
        self.ResultFrame = tk.Listbox(self.SecondPageFrame, height = 20, width = 60, background = 'black', foreground = 'black', font =('Helvetica', 12))
        self.ErrorInOpeningFile = ttk.Label(self.SecondPageFrame, text = "")
        self.Bienvenue()
        self.PremierePage()
        self.SecondPage()
        self.ThirdPage()
    def Bienvenue(self):
        self.Bienvenue = ttk.Frame(self.root, style = "Custom.TFrame", height = 60, width = 1200)
        self.WelcomeText = ttk.Frame(self.Bienvenue, style = "Custom.TFrame", height = 60, width = 1200)
        self.WelcomeLabel = ttk.Label(self.WelcomeText, text='Welcome to PWNED?', foreground='blue', font=("Castellar", 24), background= 'black').grid()
        self.WelcomeLabel2 = ttk.Label(self.WelcomeText, text='Has your password ever been compromised ?', foreground='red', font=("Castellar", 19), background = 'black').grid()
        self.Bienvenue.grid(row = 0)
        self.WelcomeText.grid(row = 0)

    def PremierePage(self):
        ttk.Label(self.tab1, text="Wanna get a safer password ? ", font=("Helvetica", 20, 'bold'), foreground = 'red', background ="black").grid(column = 0, pady = 20, padx = 400,row = 0, columnspan = 3)
        try:
            image = Image.open("./Images/PasswordStrength.png")
            ImageFrame = ttk.Frame(self.tab1, width = 450,style = "Custom.TFrame")
            resized_image = image.resize((450,450))
            photo = ImageTk.PhotoImage(resized_image)
            label = ttk.Label(ImageFrame, image=photo, background = 'black')
            label.photo = photo
            label.grid(column = 0)
            self.ValeurEntre.grid(column = 1)
            self.entry.grid(column = 1, row = 3)
            self.entry.bind("<Return>", self.GeneratePassword)
            ImageFrame.grid(column = 0, row = 1, columnspan = 1, rowspan = 5)
        except:
            self.ValeurEntre.grid(pady = 50)
            self.entry.grid(padx = 550)
            self.entry.bind("<Return>", self.GeneratePassword)
    def SecondPage(self):
        ttk.Label(self.tab2, text = "Test multiple passwords in a file ?", foreground='red', font=("Castellar", 20), background = 'black').grid(padx = 360, pady = 20, row = 0, columnspan = 3)
        ttk.Label(self.tab2, text="Please make sure that passwords are set line on line in the text file", foreground='white', background='black', font=('Castellar', 16)).grid(row = 1, pady = 20, columnspan = 3)
        ReadFileButton = ttk.Button(self.SecondPageFrame, text ="Import file !", command= self.read_file) 
        ReadFileButton.grid(row = 0, padx = 400)
        self.SecondPageFrame.grid(row = 2, padx = 200)
        ttk.Label(self.SecondPageFrame, text ="Please wait, 12 passwords/s", foreground ="white", background = 'black').grid(pady = 10, row = 3)

    def ThirdPage(self):
        ttk.Label(self.tab3, text="Is your password enough secured ? ", foreground= 'red', font=('Helvetica', 20), background='black').grid(row = 0,padx = 400,pady = 20) 
        ttk.Label(self.tab3, text="Having a secured password is very important \n            because of BRUTEFORCING.\n       If it's too weak, anyone can guess it \n                      with a computer.\n     Many have already been compromised.\n                    What about yours ?", foreground = "white", background='black', font=('Helvetica', 15)).grid(padx = 400, pady = 20)
        ttk.Label(self.tab3, text ="TEST MY PASSWORD", background = 'black', foreground = 'white',font=('Helvetica', 20)).grid(padx = 400, pady = 20)
        self.entry2 = ttk.Entry(self.tab3)
        self.entry2.grid(padx = 400, pady = 50)
        self.entry2.bind("<Return>", self.CheckMyPassword)
        self.CheckMyPwd.grid(padx = 400, pady = 90)

    def GeneratePassword(self, event):
        value = event.widget.get()
        if value.isalpha() or int(value) <= 1 or int(value) >= 25:
            self.ValeurEntre.configure(text = "Enter an integer number between 1-25 please : ", foreground = 'red')
            return 0
        else:
            while True:
                mdp_generate = ""
                for i in range(int(value)):
                    caracter = chr(random.randint(32, 126))
                    mdp_generate += caracter
                compromised_count = check_password(mdp_generate)
                if compromised_count == 0:
                    self.ValeurEntre.configure(text = "Password generated : {}".format(mdp_generate), foreground = 'green')
                    return 0
    def CheckMyPassword(self, event):
        passed = str(event.widget.get())
        compromised_count2 = check_password(passed)
        if compromised_count2 > 0:
            self.CheckMyPwd.configure(text = "Your password has been compromised {} times !".format(compromised_count2), foreground = 'red', background = 'black',font=('Helvetica', 15))
            return 0
        else:
            self.CheckMyPwd.configure(text = "Your password has never been found : Greatings !", foreground = 'green', background = 'black',font=('Helvetica', 15))
            return 0
    def read_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if file_path:
            self.ResultFrame.delete(0, tk.END)
            self.ResultFrame.grid(row = 2)
            count = 0
            with open(file_path, 'r') as file:
                lines = file.readlines()
            for line in lines:
                check = 25-len(line)
                compromised_count3 = check_password(line[:-1])
                if compromised_count3 > 0:
                    self.ResultFrame.insert(tk.END, "{}".format(line)+check*" "+"<compromised {} times>".format(compromised_count3))
                    self.ResultFrame.itemconfig(count, bg='red')
                else:
                    self.ResultFrame.insert(tk.END, line)
                    self.ResultFrame.itemconfig(count, bg='green')
                count+= 1
            file.close()
        else:
            self.ErrorInOpeningFile.configure(text = "Error in opening text file.", foreground = 'red', font = ('Helvetica', 15))


    def start(self):
        self.root.mainloop()  

def Explain():
    print(colored(text2art("Pwned?"), "cyan"))
    print("Guide d'utilisation :\n")
    print("Syntaxe : python3 .\\Pwned.py [argument]\n")
    print("liste d'arguments : -p : permet de passer directement un mot de passe au programme")
    print("                         \033[92mExemple : python3 .\\fichier_de_test.py -p 'mdp'\n\033[0m")
    print("                    -f : permet de passer un fichier au programme en précisant son chemin d'accès afin de traiter\n                         plusieurs mots de passe")
    print("                         \033[92mExemple : python3 .\\fichier_de_test.py -f 'path_to_file'\n\033[0m")
    print("                    -g : permet de générer un mot de passe et de vérifier qu'il n'a pas fuité en le passant au programme")
    print("                         \033[92mExemple : python3 .\\fichier_de_test.py -g\n\033[0m")
    print("                    -b : permet de lancer le bot discord")
    print("                         \033[92mExemple : python3 .\\fichier_de_test.py -b\n\033[0m")
    print("                    -wizard : permet de lancer le programme en mode graphique")
    print("                         \033[92mExemple : python3 .\\fichier_de_test.py -wizard\n\033[0m")

def MyPassword(ThePassword):
    print(colored(text2art("Pwned?"), "cyan"))
    compromised_count = check_password(ThePassword)
    if compromised_count > 0:
        print("\033[91mLe mot de passe '{}' a été compromis {} fois. Il est recommandé de ne pas l'utiliser.\033[0m".format(args.password, compromised_count))
    else:
        print("\033[92mLe mot de passe n'a pas été trouvé. Vous pouvez l'utiliser.\033[0m")

def CheckFile(TheFilePath):
    try:
        print(colored(text2art("Pwned?"), "cyan"))
        ValidPasswd = []
        with open(TheFilePath, 'r') as f:
            passwords = f.readlines()
        for password in passwords:
            password = password.strip()
            compromised_count = check_password(password)
            if compromised_count > 0:
                print("\033[91mLe mot de passe '{}' a été compromis {} fois. Il est recommandé de ne pas l'utiliser.\033[0m".format(password, compromised_count))
            else:
                print("\033[92mLe mot de passe '{}' n'a pas été trouvé. Vous pouvez l'utiliser.\033[0m".format(password))
                ValidPasswd.append(password)
        print("\nValid password that can be used :",end='\n')
        for PasswdValid in ValidPasswd: 
            print("\033[92m                                 {}\033[0m".format(PasswdValid))
    except FileNotFoundError:
        print("\033[91mLe fichier spécifié n'a pas été trouvé.\033[0m")
        
def GenPassword():
    print(colored(text2art("Pwned?"), "cyan"))
    mdp_range = int(input("Quelle est la longueur du mot de passe que vous voulez générer : "))
    if mdp_range <= 0:
        print("\033[91mLa longueur du mot de passe doit etre superieur a 0.\033[0m")
        mdp_range = int(input("Quelle est la longueur du mot de passe que vous voulez générer : "))
    else:
        while True:
            mdp_generate = ""
            for i in range(mdp_range):
                caracter = chr(random.randint(32, 126))
                mdp_generate += caracter
            print(f"Le mot de passe généré est : {mdp_generate}")

            compromised_count = check_password(mdp_generate)
            if compromised_count > 0:
                print("\033[91mLe mot de passe '{}' a été compromis {} fois. Il est recommandé de ne pas l'utiliser.\033[0m".format(mdp_generate, compromised_count))
            else:
                print("\033[92mLe mot de passe n'a pas été trouvé. Vous pouvez l'utiliser.\033[0m")
                break


def main():
    if args.password:
        MyPassword(args.password)
    elif args.file:
        CheckFile(args.file)
    elif args.generate:
        GenPassword()
    elif args.explication:
        Explain()
    elif args.wizard:
        GraphUser().start()
    elif args.botdiscord:
        script_path = 'bot.py'
        subprocess.run(['python', script_path])
    else:
        Explain()

if __name__ == "__main__":
    main()