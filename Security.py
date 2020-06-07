from Interface import *
from Database import *
import os
import getpass

adminEmail = '1'#'admin@fe.co.uk'
adminPassword = '2'#'admin'

def login():
    while 1 == 1:
        os.system('clear')
        print('Welcome to FirstEuropean management system ver 2.9.1\n')

        # get username and password
        email = ''
        email = input('Your email please: ')
        while email == '':
            email = input('Invalid email, please enter a valid email: ')

        password = ''
        password = getpass.getpass('Your password please: ')
        while password == '':
            password = getpass.getpass('Invalid password, please enter a valid password: ')

        # get database ready
        init_database()
        
        # check if admin has logged in
        if (email == adminEmail) & (password == adminPassword):
            print('\nYou have logged in as Admin. Welcome.\n')
            main_admin_menu()
        else:
            
            # check if courier has logged in
            try:
                connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM couriers WHERE Email=%s AND Password=%s", (email, password))
                courier = cursor.fetchall()
                connection.commit()
                connection.close()
            except:
                input('Error, could not verify identity, continue (y): ')
                continue
            
            if courier[0] is None:
                input('Error, invalid email/password, continue (y): ')
                continue
            else:
                print('\nYou have logged in as ',(courier[0])[7], '. Welcome.\n')
                main_courier_menu(str((courier[0])[0]))