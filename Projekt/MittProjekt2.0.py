import os
import random


class Main:         # Här skapar jag min huvudclass, detta kommer även att bli min enda class
    username = None     # Denna använder jag för att skapa användarnamn och lösenord för registrering
    password = None

    def __init__(self):
            self.username = Main.username
            self.password = Main.password

    def create_username(self, uname):
        self.username = uname

    def create_password(self, pw):
        self.password = pw

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password


menuLoop = True
# Menu start
while menuLoop:
    print('Welcome to NackaCasino!')    # Här startar programmet med en loop där man får logga in eller registrera sig
    print('[1] Login')
    print('[2] Register')
    menuChoice = (input('>>'))
    if menuChoice == '1':
        menuLogin = input('Please enter your Username:\n>>')
        count = 0
        for items in os.listdir():  # Här kollar den igenom alla items i den lokala katalogen
            if menuLogin+'.txt' == items:   # Om någon av dessa är samma som användarnamnet går den vidare
                menuPassword = input('Please enter your Password:\n>>')
                userlength = len(menuLogin)     # Här skapar jag nya variablar med längden på username och lösenord
                passlength = len(menuPassword)
                with open(menuLogin + '.txt', 'r') as Password:
                    Password.seek(userlength + 2)   # Här använder jag seek med användarnamnet för att komma till lösenord i filen
                    lines = Password.readline()
                    newlines = lines.replace('\n', '')  # Här tar jag bort newline för att det inte har med lösenordet att göra.
                    if newlines == menuPassword:    # Om newlines är rätt lösenord kommer man in.
                        print('Welcome', menuLogin)
                        menuLoop = False
                    else:
                        print('INVALID PASSWORD')
            elif menuLogin+'.txt' != items:  # Om användarnamnet inte stämmer med något i katalogen hamnar man här.
                count += 1
                if count == len(os.listdir()):
                    print('The username is not registered!')

    elif menuChoice == '2': # Detta är menyn för registrering
        menuRegisterUser = input('Please enter a Username:\n>>')
        count = 1
        for items in os.listdir():  # Här söker den igenom den lokala katalogen som innan
            if items == menuRegisterUser+'.txt':  # Om användarnamnet redan finns kan man inte skapa det.
                print('Username already taken')
            elif items != menuRegisterUser+'.txt' and count == len(os.listdir()): # Countern här är för att gå igenom alla filer i katalogen
                print('Username NOT taken')
                user = Main()           # Här använder jag min Main class
                user.create_username(menuRegisterUser)  # Här använder jag funktionen create_username för att skapa användaren
                menuRegisterPw = input('Please enter a Password:\n>>')
                user.create_password(menuRegisterPw)    # Samma som ovan fast för lösenord
                print('You have succesfully registered', user.get_username(), 'to the database.\n'
                      'You got 1000 free credits. Login to use them!')
                with open('Users.txt', 'a+') as registerUser:  # Här sparar jag det som tidigare skrivits in i en textfil
                    registerUser.write(user.get_username()+'\n')    # Skriver användare i textfil på rad 1
                    registerUser.write(user.get_password()+'\n')    # Skriver användare i textfil på rad 2
                    registerUser.write('1000')                         # Skriver balance på rad 3.

                os.rename('Users.txt', user.get_username()+'.txt')  # Döper om textfilen till användarnamnet.
            elif items != menuRegisterUser+'.txt':
                count += 1  # Här ändras countern med +1, denna används ovanför som beskrivet

    else:
        print('Please choose a correct alternative')


# ----- FUNKTIONER FÖR BLACK JACK ------ #
def deal(deck): # Detta är deal funkttionen
    hand = []    # Här skapas en tom lista som heter hand
    for i in range(2):  # Eftersom man får två kort i början är rangen (2)
        random.shuffle(deck)  # Här tar vi en random.shuffle för att blanda om bland allt i deck. deck ligger nedanför innuti en loop för att korten aldrig ska ta slut.
        card = deck.pop()   # Här använer jag pop för ta ett kort ur listan deck.
        if card == 11:
            card = "J"  # Eftersom kort 11,12,13 och 14 är J Q K A i en kortlek döper jag om dessa här.
        if card == 12:
            card = "Q"
        if card == 13:
            card = "K"
        if card == 14:
            card = "A"
        hand.append(card)   # Här lägger jag till kortet i listan hand
    return hand # Sedan returnerar vi listan hand


def total(hand):    # Denna funktionen är för att räkna ut totalen av handen.
    total = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":  # Om kortet är J Q K , är dessa värda 10, och inte 11, 12, 13 som deras kortnummer är
            total += 10
        elif card == "A":   # Om kortet är A ändrar jag värde här beroende på om totalen på handen är högre eller lika med 11.
            if total >= 11:  # Eftersom A i BlackJack kan ha värdet 11 eller 1.
                total += 1
            else:
                total += 11  # Om totalen på handen är lägre än 11 får A värdet 11.
        else:
            total += card  # Om kortet inte är J Q K A så läggs vädet direkt på totalen.
    return total  # Sedan returnerar vi totalen.


def anothercard(hand):  # Denna funktionen är om man vill ta ett till kort
    card = deck.pop()   # Vi tar helt enkelt ett nytt kort ur listan deck och sparar det i variabeln card
    if card == 11:  # Samma procedur här som ovan, om kortet är 11,12,13,14 skrivs J Q K A ut istället
        card = "J"
    if card == 12:
        card = "Q"
    if card == 13:
        card = "K"
    if card == 14:
        card = "A"
    hand.append(card)  # Sedan lägger vi till variabeln card till hand.
    return hand     # Och vi returnerar sedan hand.


def wincoins():
    with open(menuLogin + '.txt',
              'w+') as checkBalance:  # Dessa ändrar värdet på credits i användarens textfil. Om man vinner får man mer credits, och om man förlorar tar den bort credits.
        newbalance = realbalance + bet
        checkBalance.seek(0)
        checkBalance.write(menuLogin + "\n")
        checkBalance.write(menuPassword + "\n")
        checkBalance.write(str(newbalance))


def losscoins():
    with open(menuLogin + '.txt', 'w+') as checkBalance:  # Dessa ändrar värdet på credits i användarens textfil. Om man vinner får man mer credits, och om man förlorar tar den bort credits.
        newbalance = realbalance - bet
        checkBalance.seek(0)
        checkBalance.write(menuLogin + "\n")
        checkBalance.write(menuPassword + "\n")
        checkBalance.write(str(newbalance))


def score(dealer_hand, player_hand):  # Här kommer funktinen som skriver ut resultatet beroende på händerna.
    if total(player_hand) == 21:
        print("The dealer has", *dealer_hand, "for a total of " + str(total(dealer_hand)))
        print("You have", *player_hand, "for a total of " + str(total(player_hand)))
        print("Congratulations! You got a Blackjack!")
        print("You win", bet, "\n")
        wincoins()
    elif total(dealer_hand) == 21:
        print("The dealer has", *dealer_hand, "for a total of " + str(total(dealer_hand)))
        print("You have", *player_hand, "for a total of " + str(total(player_hand)))
        print("Sorry, you lose. The dealer got a blackjack. You lost", bet, "\n")
        losscoins()
    elif total(player_hand) > 21:
        print("The dealer has", *dealer_hand, "for a total of " + str(total(dealer_hand)))
        print("You have", *player_hand, "for a total of " + str(total(player_hand)))
        print("Sorry. You busted. You lost", bet, "\n")
        losscoins()
    elif total(dealer_hand) > 21:
        print("The dealer has", *dealer_hand, "for a total of " + str(total(dealer_hand)))
        print("You have", *player_hand, "for a total of " + str(total(player_hand)))
        print("Dealer busts. You win", bet, "\n")
        wincoins()
    elif total(player_hand) < total(dealer_hand):
        print("The dealer has", *dealer_hand, "for a total of " + str(total(dealer_hand)))
        print("You have", *player_hand, "for a total of " + str(total(player_hand)))
        print("The dealer has a higher hand, you lost", bet, "\n")
        losscoins()
    elif total(player_hand) > total(dealer_hand):
        print("The dealer has", *dealer_hand, "for a total of " + str(total(dealer_hand)))
        print("You have", *player_hand, "for a total of " + str(total(player_hand)))
        print("Congratulations. Your hand is higher then the dealer. You win", bet, "\n")
        wincoins()


def depositmoremoney(amount):  # Här är funktionen för att lägga till mer credits till sitt konto
    with open(menuLogin + '.txt') as checkBalance:
        checkBalance.seek(userlength + passlength + 2)
        balancebeforedeposit = checkBalance.read()  # Först öppnar den filen och läser in hur mycket credits som fanns innan
    balancebeforedeposit1 = int(balancebeforedeposit)
    with open(menuLogin + '.txt', 'w+') as depositmoney:
        depositmoney1 = balancebeforedeposit1 + amount  # Sedan skriver den om filen med användarnamn och lösenord.
        depositmoney.seek(0)                            # Och lägger sedan in gamla summan + amount till kontot.
        depositmoney.write(menuLogin + "\n")
        depositmoney.write(menuPassword + "\n")
        depositmoney.write(str(depositmoney1))


# Logged in Menu start
menuUserLoop = True
while menuUserLoop:
    print('What would your like to do?\n'  # Här startar loopen när man loggat in
          '[1] Play Black Jack\n'
          '[2] Deposit money\n'
          '[3] Check balance\n'
          '[4] Check Black Jack Rules\n')
    menuUserInput = input('>>')
    if menuUserInput == '1':
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4  # Här skapas listan för alla korten som sedan används i funktionerna ovan
            print('Welcome to BlackJack')
            with open(menuLogin + '.txt') as checkBalance:
                checkBalance.seek(userlength + passlength + 2)
                balance = checkBalance.read()
                print('Your balance: ' + balance + '\n') # Här skriver den ut credits för att man ska veta hur mycket man har att betta
            realbalance = int(balance)
            try:
                bet = int(input('How much do you want to bet?\n>>'))
                if bet <= realbalance:  # Om bettet är mindre eller lika med beloppet man har så går det igenom
                    dealer_hand = deal(deck) # Här använder vi funktionen deal för att lägga till kort till dealern
                    player_hand = deal(deck) # Här använder vi funktionen deal för att lägga till kort till playern
                    while bet:
                        print('The dealer is showing: ' + str(dealer_hand[0])) # Här visar vi ett av korten som dealern har fått
                        print('You have:', *player_hand, 'which is ' + str(total(player_hand))) # Här visar vi vilka kort som spelaren har fått och även vad summan av korten är.
                        yourChoice = input('Do you want to:\n[1]Hit\n[2]Stand\n>>') # Här får man välja om man är nöjd eller om man vill ta ett till kort.
                        if yourChoice == "1":
                            anothercard(player_hand)  # Här använder vi funktionen som lägger till ett kort till handen
                            while total(player_hand) < 21:  # Så länge spelarens hand är längre än 21 så får man ta ett till kort.
                                print('You got a :', player_hand[-1]) # Här använer vi [-1] för att skriva ut vad spelaren fick för kort
                                print('You now got :', total(player_hand))  # Och här skriver vi ut vad spelaren har för total
                                hitorstand = input('Do you want to:\n[1]Hit\n[2]Stand?\n>>') # Här får man välja om man fortfarande vill ta ett till kort eller inte
                                if hitorstand == "1" and total(player_hand) != 21:
                                    anothercard(player_hand)
                                    continue
                                if hitorstand == "2" and total(player_hand) != 21:  # Om man väljer att stanna stå breakar vi loopen.
                                    print('You chose to stand.')
                                    break
                            if total(player_hand) < 22:  # Om spelarens hand är lägre än 22
                                while total(dealer_hand) < 17:  # Så får dealern dra kort så länge handen är lägre än 17
                                    anothercard(dealer_hand)
                                score(dealer_hand, player_hand)  # Vi printar sedan ut poängen med funktionen score
                                break
                            else:
                                score(dealer_hand, player_hand)  # Om spelarens hand är hägre än 22 så drar inte dealern några kort utan poängen printas ut istället
                                break
                        elif yourChoice == "2":  # Om man väljer att stanna direkt.
                            while total(dealer_hand) < 17:  # Och om dealerns hand är lägre än 17 så kommer dealern dra kort.
                                anothercard(dealer_hand)
                            score(dealer_hand, player_hand)
                            break
                else:
                    print('You dont have enough money!')
            except:
                print('You can only bet money, not textlines...')
    elif menuUserInput == '2':  # Här nedan använder vi funktionen för att lägga till credits.
        print('Here you can deposit more money.\n'
              'You can only deposit 1000 more credits at a time.\n'
              'How much would you like to deposit?')
        try:
            depositamounth = int(input('>>'))
            if depositamounth <= 1000:
                print('You made a deposit of', depositamounth)
                print('Dont spend it all in one bet!')
                depositmoremoney(depositamounth)
            else:
                print('You cant deposit that amount right now.')
        except:
            print('You can only deposit money, not textstrings....')
    elif menuUserInput == '3':
        with open(menuLogin + '.txt') as checkBalance:
            checkBalance.seek(userlength+passlength+2)
            balance = checkBalance.read()
        print('Your balance: ' + balance + '\n')

    elif menuUserInput == '4': # Här har jag skrivit in alla regler för blackjack
        print('Black Jack Rules:\n'
              'In black Jack the goal is to hit 21 or get as close to as possible\n'
              'The game start by giving you two cards and the dealer shows one.\n'
              'You then have the option to get another card (hit) or stand.\n'
              'If you chose to hit:\n'
              'You get another card and the option to hit again or stand.\n'
              'You may hit as many times as you like, but if you exceed 21 your auto lose.\n'
              'If you chose to stand:\n'
              'The dealer shows her next card, if the dealer has 17 or higher she must stand.\n'
              'If the dealer shows 16 or lower she must draw cards until she gets greater than 17 or busts.\n'
              'Do not spend money you cannot afford losing.\n')
        # Check Rules
    else:
        print('Please choose a correct alternative')