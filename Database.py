import pymysql
import warnings
from Interface import *
        
# userType: 1 = courier, 0 = customer
# parcelType: 0 = undelivered, 1 = delivered

# database details
dbHostname= 'localhost'
dbUsername = 'root'
dbPassword = ''
dbName = 'FirstEuropean'

# database table headers
dbHeaders = {
    'Customers':["Name", "Address1", "Address2", "Town", "PostCode", "Telephone", "Email"],
    'Couriers':["Name", "Address1", "Address2", "Town", "PostCode", "Telephone", "Email", "Payrate", "Password"],
    'Parcels':["Weight", "Width", "Length", "Height", "Customer", "Address1", "Address2", "Town", "PostCode", "Telephone", "Courier", "Status", "DeliveryDate", "Price"]
    }


# courier: set parcel status as delivered to all parcels
def set_parcel_status_delivered(courierID):
    if courierID < 0:
        print('Invalid arguments for set_parcel_status_delivered')
        return
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("UPDATE parcels SET Status=1 WHERE (Courier=%s AND Status=0)", (str(courierID)))
        connection.commit()
        connection.close()
    except:
        print('Error, could not change parcel status from database')
    input('Do you wish to continue? (y): ')

# courier: modify parcels status
def modify_parcel_status(courierID):
    if courierID < 0:
        print('Invalid arguments for modify_parcel_status')
        return
    # display parcels to select from
    print_list_item(2, search_parcel('Courier', str(courierID)))
    parcelID = -1
    parcelID = int(input('Parcel ID to modify: '))
    while parcelID < 0:
        parcelID = int(input('Invalid selection, input valid parcel ID to modify: '))
    newValue = input('Please input the new status: ')
    # write to database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("UPDATE parcels SET Status=%s WHERE ID=%s", ((newValue, str(parcelID))))
        connection.commit()
        connection.close()
    except:
        print('Error, could not change parcel status from database')
    input('Do you wish to continue? (y): ')
    
# display item details
def print_single_item(itemType, item):
    # Validate arguments
    if itemType not in range(-1, 3):
        print('Error, invalid arguments for print_single_item')
        return
    if item == None:
        print('Error, invalid item to print in print_single_item')
        return
    print('<--------------->')
    try:
        print('ID: ' + str(item[0]))
        for i in range(0, len(item)):
            if itemType == 0:
                print((dbHeaders['Customers'])[i] + ': ' + str(item[i+1]))
            elif itemType == 1:
                if i != 8:
                    print((dbHeaders['Couriers'])[i] + ': ' + str(item[i+1]))
            elif itemType == 2:
                print((dbHeaders['Parcels'])[i] + ': ' + str(item[i+1]))
    except:
        pass
        #print('Error, could not print items')

def print_list_item(itemType, itemList):
    if itemType not in range(-1, 3):
        print('Error, invalid arguments for print_list_item')
        return
    if itemList == None:
        print('Error, invalid itemList to print in print_list_item')
        return 
    try:
        print('\n')
        for i in range(0, len(itemList)):
            print_single_item(itemType, itemList[i])    
        print('<--------------->')
        print('\n')
    except:
        pass
        #print('Error, could not print item list')

    
# displays a header
def display_header(headerChoice):
    count = 1
    for items in dbHeaders[headerChoice]:
        tempStr = str(count)+ '. ' + items
        print(tempStr)
        count += 1

def init_database():
    warnings.filterwarnings("ignore")
    try:
        connection = pymysql.connect(host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS customers(ID INTEGER, Name VARCHAR(32), Address1 VARCHAR(32), Address2 VARCHAR(32), Town VARCHAR(32), PostCode VARCHAR(32), Telephone VARCHAR(32), Email VARCHAR(32));")
        cursor.execute("CREATE TABLE IF NOT EXISTS couriers(ID INTEGER, Name VARCHAR(32), Address1 VARCHAR(32), Address2 VARCHAR(32), Town VARCHAR(32), PostCode VARCHAR(32), Telephone VARCHAR(32), Email VARCHAR(32), Payrate FLOAT, Password VARCHAR(32));")
        cursor.execute("CREATE TABLE IF NOT EXISTS parcels(ID INTEGER, Weight FLOAT, Width FLOAT, Length FLOAT, Height FLOAT, CustomerID INTEGER, Address1 VARCHAR(32), Address2 VARCHAR(32), Town VARCHAR(32), PostCode VARCHAR(32), Telephone VARCHAR(32), Courier INTEGER, Status VARCHAR(32), DeliveryDate INTEGER, Price FLOAT);")
        connection.commit()
    except:
        print('Error, could not initialise database')
    finally:
        try:
            connection.close()
        except:
            pass
    
def modify_parcel():
    view_parcels(0)
    view_parcels(1)
    parcelID = -1
    parcelID = int(input('Parcel ID to modify: '))
    while parcelID < 0:
        parcelID = int(input('Invalid selection, input valid parcel ID to modify: '))
    display_header('Parcels')
    choice = 0
    choice = int(input('Select field to modify: '))
    while (choice < 0) | (choice > len(dbHeaders['Parcels'])):
        choice = int(input('Invalid selection, select a valid field to modify: '))
    newValue = input('Please input the new value: ')
    choice = choice - 1
    # write to database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM parcels WHERE ID=%s", (str(parcelID)))
        parcelData = cursor.fetchone();
        lst = list(parcelData)
        lst[choice] = newValue
        parcelData = tuple(lst)
        cursor.execute("UPDATE parcels SET " + (dbHeaders['Parcels'])[choice] + "=%s WHERE ID=%s", ((parcelData[choice], str(parcelID))))
        connection.commit()
        connection.close()
    except:
        print('Error, could not modify parcel from database')
    input('Do you wish to continue? (y): ')

def search_parcel(criteria, searchValue):
    # search database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM parcels WHERE " + criteria + "="+ searchValue)
        parcelData = cursor.fetchall()
        connection.commit()
        connection.close()
    except:
        input('Error, could not find parcel, continue (y)')
        return None
    return parcelData
        
def search_undelivered_parcel(courierID):
    # search database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM parcels WHERE (Courier=%s AND Status=0)", courierID)
        parcelData = cursor.fetchall()
        connection.commit()
        connection.close()
    except:
        input('Error, could not find parcel, continue (y)')
        return None
    return parcelData

def search_users(userType):
    # validate arguments
    if (userType != 1) & (userType != 0):
        print('Error, invalid modify_user arguments')
        return
    
    if userType == 0:
        display_header('Customers')
        choice = 0
        choice = int(input('Select criteria  by which to search customer: '))
        while (choice < 0) | (choice > len(dbHeaders['Customers'])):
            choice = int(input('Invalid selection, select a valid criteria: '))
    else:
        display_header('Couriers')
        choice = 0
        choice = int(input('Select criteria  by which to search courier: '))
        while (choice < 0) | (choice > len(dbHeaders['Couriers'])):
            choice = int(input('Invalid selection, select a valid criteria: '))
    searchValue = input('Search: ')
    choice = choice - 1
    # search database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        if (userType ==0):
            cursor.execute("SELECT * FROM customers WHERE " + (dbHeaders['Customers'])[choice] + "=%s", searchValue)
            userData = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM couriers WHERE " + (dbHeaders['Couriers'])[choice] + "=%s", searchValue)
            userData = cursor.fetchall()
        print_list_item(userType, userData)
        connection.commit()
        connection.close()
    except:
        if userType == 0:
            print('Error, could not find customer from database')
        else:
            print('Error, could not find courier from database')
    input('Do you wish to continue? (y): ')

def modify_user(userType):
    # validate arguments
    if (userType != 1) & (userType != 0):
        print('Error, invalid modify_user arguments')
        return
    
    view_all_users(userType)
    if userType == 0:
        userID = -1
        userID = int(input('Customer ID to modify: '))
        while userID < 0:
            userID = int(input('Invalid selection, input valid customer ID to modify: '))
        display_header('Customers')
        choice = 0
        choice = int(input('Select field to modify: '))
        while (choice < 0) | (choice > len(dbHeaders['Customers'])):
            choice = int(input('Invalid selection, select a valid field to modify: '))
    else:
        userID = -1
        userID = int(input('Courier ID to modify: '))
        while userID < 0:
            userID = int(input('Invalid selection, input valid courier ID to modify: '))
        print('\n')
        display_header('Couriers')
        choice = 0
        choice = int(input('Select field to modify: '))
        while (choice < 0) | (choice > len(dbHeaders['Couriers'])):
            choice = int(input('Invalid selection, select a valid field to modify: '))
    choice = choice - 1
    
    newValue = input('Please input the new value: ')
    
    # write to database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        if (userType ==0):
            cursor.execute("SELECT * FROM customers WHERE ID=%s", (str(userID)))
            userData = cursor.fetchone();
            lst = list(userData)
            lst[choice] = newValue
            userData = tuple(lst)
            cursor.execute("UPDATE customers SET " + (dbHeaders['Customers'])[choice] +"=%s\
            WHERE ID=%s", ((userData[choice], str(userID))))
        else:
            cursor.execute("SELECT * FROM couriers WHERE ID=%s", (str(userID)))
            userData = cursor.fetchone();
            lst = list(userData)
            lst[choice] = newValue
            userData = tuple(lst)
            cursor.execute("UPDATE couriers SET " + (dbHeaders['Couriers'])[choice] +"=%s\
            WHERE ID=%s", ((userData[choice], str(userID))))
        connection.commit()
        connection.close()
    except:
        if userType == 0:
            print('Error, could not modify customer from database')
        else:
            print('Error, could not modify courier from database')
    input('Do you wish to continue? (y): ')
    
def view_parcels(parcelType):
    if (parcelType != 1) & (parcelType != 0):
        print('Error, invalid view_parcels arguments')
        return
    # display parcels from database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM parcels WHERE Status=" + str(parcelType))
        parcelData = cursor.fetchall()
        print_list_item(2, parcelData)
        connection.commit()
        connection.close()
    except:
        print('Error, could not display parcels from the database')
    input('Do you wish to continue? (y): ')
    
def view_all_users(userType):
    if (userType != 1) & (userType != 0):
        print('Error, invalid view_all_users arguments')
        return
    # display users from database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        if userType == 0:
            cursor.execute("SELECT * FROM customers")
        else:
            cursor.execute("SELECT * FROM couriers")
        userData = cursor.fetchall()
        print_list_item(userType, userData)
        connection.commit()
        connection.close()
    except:
        if userType == 0:
            print('Error, could not display customers from the database')
        else:
            print('Error, could not display couriers from the database')
    input('Do you wish to continue? (y): ')

def remove_parcel():
    view_parcels(0)
    view_parcels(1)
    parcelID = input('Enter the parcel ID to be deleted: ')
    if input('Do you wish to delete this parcel? (y/n): ') != 'y':
        return
    # delete parcel from database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM parcels WHERE ID=%s", parcelID)
        connection.commit()
        connection.close()
    except:
        print('Error, could not delete parcel from database')
    input('Do you wish to continue? (y): ')

def add_parcel():
    print('Enter the below details to add a new parcel: ')
    # read parcel information
    weight = input('Weight: ')
    width = input('Width: ')
    length = input('Length: ')
    height = input('Height: ')
    view_all_users(0)
    name = input('Select the CustomerID from above: ')
    address1 = input('Delivery address 1: ')
    address2 = input('Address 2: ')
    town = input('Town: ')
    postcode = input('PostCode: ')
    telephone = input('Telephone Number: ')
    status = 0
    deliveryDate = 0
    view_all_users(1)
    courierID = input('From the list above, select the courier ID: ')
    price = input('Price: ')
    if input('Do you wish to add this parcel? (y/n): ') != 'y':
        return
    # add parcel to database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName)
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(ID) FROM parcels")
        nextRow = cursor.fetchone()
        cursor.execute("SELECT * FROM couriers WHERE ID=%s", (courierID))
        courierData = cursor.fetchone()
        if nextRow[0] is None:
            parcelID = 0
        else:
            parcelID = nextRow[0] + 1
        if ((courierData[5])[0] != postcode[0]) | ((courierData[5])[1] != postcode[1]):
            print('Error, the courier does not cover this area')
        else:
            sql = "INSERT INTO parcels(ID, Weight, Width, Length, Height, CustomerID, Address1, Address2, Town, PostCode, Telephone, Courier, Status, DeliveryDate, Price)\
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(parcelID, weight, width, length, height, name, address1, address2, town, postcode, telephone, courierID, status, deliveryDate, price))
        connection.commit()
        connection.close()
    except:
        print('Error, could not add parcel to the database')
    input('Do you wish to continue? (y): ')

# remove a customer/courier from database
def remove_user(userType):
    if (userType != 1) & (userType != 0):
        print('Error, invalid add_user arguments')
        return
    if userType == 0:
        userID = input('Enter the customer ID to be deleted: ')
    else:
        userID = input('Enter the courier ID to be deleted: ')
    
    if userType == 0:
        if input('Do you wish to delete this customer? (y/n): ') != 'y':
            return
    else:
        if input('Do you wish to delete this courier? (y/n): ') != 'y':
            return
    # delete user from database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName )
        cursor = connection.cursor()
        if userType == 0:
            cursor.execute("DELETE FROM customers WHERE ID=%s", userID)
        else:
            cursor.execute("DELETE FROM couriers WHERE ID=%s", userID)
        connection.commit()
        connection.close()
    except:
        if userType == 0:
            print('Error, could not delete customer from database')
        else:
            print('Error, could not delete courier from database')
    input('Do you wish to continue? (y): ')

# add new customer/courier to the database
def add_user(userType):
    if (userType != 1) & (userType != 0):
        print('Error, invalid add_user arguments')
        return
    if userType == 0:
        print('Enter the below details to add a new customer: ')
    else:
        print('Enter the below details to add a new courier: ')
    # read user information
    name = input('Name: ')
    address1 = input('Address 1: ')
    address2 = input('Address 2: ')
    town = input('Town: ')
    postcode = input('PostCode: ')
    telephone = input('Telephone Number: ')
    email = input('Email: ')
    if userType != 0:
        payrate = input('Payrate per parcel: ')
        password = input('Password: ')
    if userType == 0:
        if input('Do you wish to add this customer? (y/n): ') != 'y':
            return
    else:
        if input('Do you wish to add this courier? (y/n): ') != 'y':
            return
    # add user to database
    try:
        connection = pymysql.connect( host = dbHostname, user = dbUsername, passwd = dbPassword, db = dbName)
        cursor = connection.cursor()
        if userType == 0:
            cursor.execute("SELECT MAX(ID) FROM customers")
        else:
            cursor.execute("SELECT MAX(ID) FROM couriers")

        nextRow = cursor.fetchone()
        if nextRow[0] is None:
            userID = 0
        else:
            userID = nextRow[0] + 1
        if userType == 0:
            sql = "INSERT INTO customers(ID, Name, Address1, Address2, Town, PostCode, Telephone, Email )\
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(userID, name, address1, address2, town, postcode, telephone, email))
        else:
            sql = "INSERT INTO couriers(ID, Name, Address1, Address2, Town, PostCode, Telephone, Email, Payrate, Password)\
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(userID, name, address1, address2, town, postcode, telephone, email, payrate, password))
        connection.commit()
        connection.close()
    except:
        if userType == 0:
            print('Error, could not add customer to the database')
        else:
            print('Error, could not add courier to the database')
    input('Do you wish to continue? (y): ')
