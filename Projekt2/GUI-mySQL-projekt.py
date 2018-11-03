from tkinter import *
from tkinter import ttk
import random
import pymysql

# Här nedanför skapar jag en anslutning till min databasserver.
# Jag använder paketet PyMySQL eftersom jag tycker att det fungerar väldigt bra.

db = pymysql.connect(host='localhost',
                                 user='DITT ANVÄNDARNAMN',
                                 password='DITT LÖSENORD',
                                 db='DIN DATABAS NAMN')
connection = db.cursor()

# Här skapar jag instansen för huvudfönstret där man sedan kommer kunna logga in
loginWindow = Tk()


# Detta är en funktion för som används för att ändra värdet i Username fältet.
# Om man inte har skrivit in något där så tar den bort allt för att man ska kunna skriva in något.
# Om man redan har ändrat värdet i entryt och man går tillbaka så markeras allt istället.
def deleteUserEntry(event):
    if userEntry.get() == 'Username':
        userEntry.delete(0, "end")
    else:
        userEntry.selection_range(0, END)


# Det här funktionen gör precis samma som ovan, men för Lösenords-entryt
def deletePassEntry(event):
    if passEntry.get() == 'Password':
        passEntry.delete(0, "end")
    else:
        passEntry.selection_range(0, END)


# Den här funktionen används för att stänga ner programmet om man trycker på QUIT
def closeLoginAttempt():
    loginWindow.destroy()


# Den här funktionen används när man trycker på Login. Den tar värdena från Username och Password entries
# och kollar sedan om dessa stämmer överens med värden från databasen.
# Om det inte stämmer överens så skrivs ett felmeddelande ut på skärmen
# Om man loggar in har jag lagt in en withdraw på det fönstret för att sedan kunna hämta upp det senare igen.
# När man loggar in körs alltså funktionen loggedin() som skapar ett nytt fönster.
def trytologin(self=None):
    with db.cursor() as login:
        login.execute(
            "SELECT username, password FROM users WHERE username = %s AND password = %s",
            (userEntry.get(),
             passEntry.get())
        )
        authorize = login.rowcount
        if authorize != 0:
            loginWindow.withdraw()
            loggedin()
        else:
            wrongLogin.set('Incorrect Username/Password')


# Den här funktionen tar hand om utloggning. Om man loggar ut stängs fönstret och den hämtar även upp
# inloggningsfönstret som tidigare blivit withdrawat. Detta med deiconify.
def logout():
    window.destroy()
    loginWindow.deiconify()


# Den här funktionen används när en användare försöker byta användarnamn och/eller lösenord.
# Den kollar värdena på entries för att sedan kolla med värden i databasen.
# Om tex ett användarnamn redan finns som man försöker byta till får man ut ett felmeddelande.
def changeuserdetails():
    with db.cursor() as changeuser:
        changeuser.execute(
            "SELECT username, password FROM users WHERE username = %s AND password = %s",
            (userEntry.get(),
             entry3.get())
        )
        authorize = changeuser.rowcount
        if authorize != 0:
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s", (entry1.get(),)
                )
                doesexist = cursor.rowcount
            if doesexist == 0:
                with db.cursor() as cursor:
                    cursor.execute(
                        "UPDATE users SET username=%s, password=%s WHERE username=%s AND password =%s",
                        (entry1.get(), entry2.get(), userEntry.get(), entry3.get())
                    )
                    db.commit()
                errormessage("Username and/or Password changed!")
            elif userEntry.get() == entry1.get():
                with db.cursor() as cursor:
                    cursor.execute(
                        "UPDATE users SET username=%s, password=%s WHERE username=%s AND password =%s",
                        (entry1.get(), entry2.get(), userEntry.get(), entry3.get())
                    )
                    db.commit()
                errormessage("Password has been changed!")
            else:
                errormessage("Username already exists!")
        else:
            errormessage("Incorrect Password!")


# Den här funktionen använder jag för att skriva ut felmeddelande i fönstret 'window'
# Funktionen används på flera ställen för att kunna ändra värdet på meddelandet som skrivs ut.
def errormessage(asdasd):
    errormsg = Label(window)
    errormsg.config(text=asdasd, width=35)
    errormsg.grid(row=6, column=0, sticky=E, columnspan=2)


# Denna funktionen används för att hämta alla användare som finns sparade i databasen.
# Alla användare sparas senare ned i en lista som används i en OptionMenu längre ned.
def getExistingUsers(event=None):
    with db.cursor() as getall:
        getall.execute(
            "SELECT username FROM users"
        )
        allusers = getall.fetchall()
        global listusers
        listusers = []
        for all in allusers:
            for users in all:
                listusers.append(users)


# Den här funktionen används för att skriva ut användarnamn och lösenord på en användare som man har valt
# i OptionMenyn. När man väljer en användare i listan så hämtar den värdena från databasen.
# Sedan lägger den in värdena i en lista. Med indexnummer hämtas sedan värdena från listan och skrivs ut
# i rätt entrybox.
def plantuserdetails(event):
    nameEntry1.delete(0, END)
    passEntry1.delete(0, END)
    with db.cursor() as getall:
        getall.execute(
            "SELECT username, password, isadmin FROM users WHERE username=%s", (cUserString.get(),)
        )
        allusers = getall.fetchall()
        global userinfo
        userinfo = []
        for all in allusers:
            for users in all:
                userinfo.append(users)
        nameEntry1.insert(END, userinfo[0])
        passEntry1.insert(END, userinfo[1])
        adminVar.set(userinfo[2])


# Den här funktionen är för för att ändra värdena på en användare i Admin Panelen.
# Först kollar den om användarnamnet finns, om det finns så går det inte att ändra till det namnet.
# Om användarnamnet finns och det är samma som man valt i listan, så går det dock att ändra lösenord och adminstatus.
def edituser():
    with db.cursor() as changeuser:
        changeuser.execute(
            "SELECT username FROM users WHERE username = %s",
            (nameEntry1.get(),)
        )
        authorize = changeuser.rowcount
        print(authorize)
        if authorize == 0:
            with db.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username=%s, password=%s, isadmin=%s WHERE username=%s",
                    (nameEntry1.get(), passEntry1.get(), adminVar.get(), cUserString.get())
                )
                db.commit()
                updateoptionmenu()
                adminPanelMessage("Userdetails changed!")
        elif nameEntry1.get() == cUserString.get():
            with db.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username=%s, password=%s, isadmin=%s WHERE username=%s",
                    (nameEntry1.get(), passEntry1.get(), adminVar.get(), cUserString.get())
                )
                db.commit()
                updateoptionmenu()
                adminPanelMessage("Userdetails changed!")
        else:
            adminPanelMessage("Username already exists!")


# Den här funktionen är för att skapa en ny användare.
# Här kollar den precis som i de andra funktionerna om användaren redan finns.
# Om användaren inte finns så skapas en användare med det användarnamnet, lösenordet och adminstatus.
def createNewUser():
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s", (newUserEntry.get(),)
        )
        doesexist = cursor.rowcount
    if doesexist == 0:
        with db.cursor() as cursor:
            sql = "INSERT INTO `users` (`username`,`password`, `isadmin`, `ipadress`) " \
                  "VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (newUserEntry.get(), newPassEntry.get(), newAdminVar.get(), 0))
            db.commit()
            newUserMessage('User Created!')
            updateoptionmenu()
    else:
        newUserMessage('Username already exists!')


# Den här funktionen är för att ta bort en användare.
# Den tar helt enkelt värdet från den man valt i listan och sedan raderar den från tabeln.
def deleteuser():
    with db.cursor() as cursor:
        cursor.execute(
            "DELETE FROM users WHERE username=%s", (nameEntry1.get(),)
        )
        db.commit()
        adminPanelMessage("User deleted!")
        updateoptionmenu()


# Den här funktionen är för att skriva ut ett meddelande när man skapar en ny användare i Admin Panel
def newUserMessage(asdasd):
    errormsg = Label(page1)
    errormsg.config(text=asdasd, width=24)
    errormsg.grid(row=7, column=0, sticky=W, columnspan=2)


# Den här funktionen är för att skriva u ett meddelande när man gör något i Admin Panel i fliken Edit User.
def adminPanelMessage(asdasd):
    errormsg = Label(page2)
    errormsg.config(text=asdasd, width=24)
    errormsg.grid(row=7, column=1, sticky=E, columnspan=2)


# Den här funktionen används för att uppdatera litan med användare så fort en ändring har gjorts.
def updateoptionmenu(event=None):
    getExistingUsers()
    cUser.set_menu(listusers[0], *listusers)
    plantuserdetails(None)
    adminPanelMessage("Userlist Updated!")


# Den här funktionen används för att kontrollera att en användare har admin status.
# Om användaren inte har det så får man ett felmeddelande.
# Om användaren är admin så skapas ett nytt fönster 'adminWindow'
def adminpanel():
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND isadmin =%s", (userEntry.get(), 1)
        )
        doesexist = cursor.rowcount
    if doesexist == 1:
        global adminWindow
        adminWindow = Tk()
        adminWindow.title('Admin Panel')
        # Här hittade jag en widget för ttk som gör det möjligt att ganska lätt skapa flikar.
        # Ref. http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Notebook.html
        # Med hjälp av länken ovan var det ganska smärtfritt att bygga upp två flikar med olika innehåll.
        flikar = ttk.Notebook(adminWindow)

        global page2, page1
        # Här skapar jag 2 stycken Frames som jag sedan lägger in i widgeten flikar(Notebook).
        page1 = ttk.Frame(flikar, width=300, height=300)
        page2 = ttk.Frame(flikar, width=300, height=300)
        # Här användare jag metoden .add för att Framesen skall läggas till.
        flikar.add(page1, text='New User')
        flikar.add(page2, text='Edit User')
        flikar.grid(column=0)
        # Här nedan följer alla knappar, entries, optionmenu, jag kommer att kommentera det mest väsentliga.
        # När jag skapar en knapp tex väljer jag helt enkelt i vilken flik den skall vara, page1 eller page2.
        createuserbutton = ttk.Label(page1, text="Create new User")
        createuserbutton.grid(row=0, column=0)
        global newUserEntry, newAdminVar, newPassEntry
        newUserEntry = ttk.Entry(page1)
        newPassEntry = ttk.Entry(page1, show="*")
        newUserButton = ttk.Button(page1, text="Create User", command=createNewUser)
        newUserLabel = ttk.Label(page1, text="Username:")
        newPassLabel = ttk.Label(page1, text="Password:")
        newAdminVar = IntVar(page1)
        newAdminCheck = Checkbutton(page1, text="Make Admin", variable=newAdminVar)
        newUserLabel.grid(row=3, column=0)
        newUserEntry.grid(row=3, column=1)
        newPassLabel.grid(row=4, column=0)
        newPassEntry.grid(row=4, column=1)
        newAdminCheck.grid(row=5, column=1)
        newUserButton.grid(row=6, column=1)

        edituserbutton = ttk.Label(page2, text="Edit existing User")
        edituserbutton.grid(row=0, column=1)
        chooseUser = ttk.Label(page2, text="Select a User:")
        chooseUser.grid(row=2, column=1)
        global cUserString, cUser
        cUserString = StringVar(adminWindow)
        # Här nedan skapar jag min OptionMenu, alltså min dropdown meny. I den lägger jag in listusers som jag får
        # från funktionen getExistingUsers, som initeras tidigare i funktionen loggedin lite längre ned.
        cUser = ttk.OptionMenu(page2, cUserString, listusers[0], *listusers, command=plantuserdetails)
        cUserString.set('Users:')
        cUser.grid(row=2, column=2)
        global nameEntry1, passEntry1, adminCheck
        nameEntry1 = ttk.Entry(page2)
        # I passEntry1 har jag lagt in en show="*" för att lösenordet man skriver in skall hållas dolt.
        passEntry1 = ttk.Entry(page2, show="*")
        global adminVar
        adminVar = IntVar(page2)
        adminCheck = Checkbutton(page2, text="Is Admin", variable=adminVar)
        applyButton = ttk.Button(page2, text="Apply", command=edituser)
        deleteUserButton = ttk.Button(page2, text="Delete User", command=deleteuser)
        nameEntryLabel = ttk.Label(page2, text="Username:")
        passEntryLabel = ttk.Label(page2, text="Password:")
        nameEntry1.grid(row=3, column=2)
        nameEntryLabel.grid(row=3, column=1)
        passEntry1.grid(row=4, column=2)
        passEntryLabel.grid(row=4, column=1, pady=5)
        adminCheck.grid(row=5, column=1, columnspan=2, padx=15, sticky=E)
        applyButton.grid(row=6, column=1, columnspan=2, padx=20, pady=5, sticky=E)
        deleteUserButton.grid(row=6, column=1, columnspan=2, padx=20, sticky=W)

        adminWindow.mainloop()
    else:
        errormessage("You are not Admin!")


# Här nedan följer konfigurationen för loginWindow, som alltså är första fönstret man ser när man startar
# programmet.
loginWindow.configure()
loginWindow.resizable(0, 0)
# Med .title kan jag bestämma vad titeln på fönstret skall vara.
loginWindow.title('Login to proceed...')
infolabel = Label(loginWindow, text="Hendrikx SQL Manager beta 0.35b")
infolabel.grid(row=0, column=0, columnspan=2)
userEntry = Entry(loginWindow)
userEntry.insert(0, 'Username')
userEntry.bind('<Button-1>', deleteUserEntry)
userEntry.bind('<Tab>', deletePassEntry)
userEntry.bind('<Return>', trytologin)
userEntry.grid(row=1, column=0, pady=10, padx=20, columnspan=2, ipadx=25)
passEntry = Entry(loginWindow, show="*")
passEntry.insert(0, 'Password')
passEntry.bind('<Return>', trytologin)
passEntry.bind('<Button-1>', deletePassEntry)
passEntry.grid(row=2, column=0, pady=10, padx=20, columnspan=2, ipadx=25)
loginButton1 = ttk.Button(loginWindow, text="Login", command=trytologin)
loginButton1.grid(row=3, column=0, sticky=E, padx=12, pady=10)
wrongLogin = StringVar()
minText = Label(loginWindow, textvariable=wrongLogin).grid(row=4, column=0, columnspan=2)
backButton = ttk.Button(loginWindow, text="Quit", command=closeLoginAttempt)
backButton.grid(row=3, column=1, sticky=W, padx=12)
backButton.bind('<Tab>', deleteUserEntry)


# Här skapas en ny funktion som skapar ett nytt fönster när man loggar in.
def loggedin():
    getExistingUsers()
    global window
    window = Tk()
    window.resizable(0, 0)
    window.title('Hendrikx SQL Mananger 1.0')
    window.configure()
    # Här har jag lagt protocol("WM_DELETE_WINDOW", quit), detta gör så att om jag stänger window med X knappen
    # så kommer den att stänga av programmet helt.
    window.protocol("WM_DELETE_WINDOW", quit)

    menuBar = Menu(window)
    window.config(menu=menuBar)
    filemenu = Menu(menuBar)
    menuBar.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Logout", command=logout)
    filemenu.add_command(label="Quit", command=quit)

    label3 = Label(window, text="Logged in as:")
    label4 = Label(window, text=userEntry.get())
    label0 = Label(window, text="Change User Details:")
    label1 = Label(window, text='New Username:')
    label2 = Label(window, text='New Password:')
    label5 = Label(window, text='Old Password:')
    global entry1, entry2, entry3
    entry1 = Entry(window)
    entry2 = Entry(window, show="*")
    entry3 = Entry(window, show="*")
    button1 = ttk.Button(window, text="Apply", command=changeuserdetails)
    button1.grid(row=5, column=1, sticky=W, padx=30, columnspan=2)
    entry1.grid(row=2, column=1, padx=10)
    entry2.grid(row=3, column=1, padx=10)
    label3.grid(row=0, column=0, padx=10)
    label4.grid(row=0, column=1)
    label0.grid(row=1, column=1)
    label1.grid(row=2, column=0, sticky=W, pady=5, padx=10)
    label2.grid(row=3, column=0, sticky=W, padx=10)
    label5.grid(row=4, column=0, pady=15, padx=10)
    entry3.grid(row=4, column=1)
    adminButton = ttk.Button(window, text="AdminPanel", command=adminpanel)
    adminButton.grid(row=5, column=0, sticky=W, padx=40, pady=10, columnspan=2)

    window.mainloop()


loginWindow.mainloop()
