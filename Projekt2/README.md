Krav för att kunna använda programmet:
mySQL databasserver
pymysql paketet

För att kunna använda programmet följ hänvisningar:
Ändra följande rader (6-9):
db = pymysql.connect(host='localhost',
                                 user='DITT ANVÄNDARNAMN',
                                 password='DITT LÖSENORD',
                                 db='DIN DATABAS NAMN')
								 
DITT ANVÄNDARNAMN = ditt användarnamn till mySQL
DITT LÖSENORD = ditt lösenord till användaren
DIN DATABAS NAMN = namnet på din databas
Om du inte kör mySQL servern localt ändra även host.

För att kunna använda programmet behöver du även skapa en ny table.
Använd följande rader för att skapa det du behöver:

CREATE TABLE users (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
username varchar(255) COLLATE utf8_bin NOT NULL COMMENT 'Usernames', 
password varchar(255) COLLATE utf8_bin NOT NULL COMMENT 'Passwords', 
ipadress varchar(255) COLLATE utf8_bin NOT NULL COMMENT 'IP when signed up', 
isadmin int(11) NOT NULL COMMENT 'is admin')


För att kunna logga in behöver du skapa en användare.
Använd följande rad för att skapa en:
INSERT INTO users (id, username, password, ipadress, isadmin) VALUES (1, 'Admin', '123', '', 1)

När detta är gjort är det bara starta programmet och logga in med:
Användarnamn: Admin
Lösenord: 123