from Database import *

menuOptions = {
    'Main':[ "Manage customers", "Manage couriers", "Manage reports" , "Manage parcels", "Exit"],
    'Customers':["View all customers", "Search customers", "Add new customers","Modify existing customers", "Remove existing customers", "Return"],
    'Couriers':["View all couriers", "Search couriers", "Add new couriers","Modify existing couriers", "Remove existing couriers", "Return"],
    'Parcels':["View all parcels", "View undelivered parcels", "Add new parcels","Modify existing parcels", "Remove existing parcels", "Return"],
    'Reports': [ "Generate profit/loss reports", "Return"],
    'MainCourier':[ "Get parcel list", "View undelivered parcels", "Modify parcel status", "Set all parcels as delivered", "Exit"]
   }

# item type: 0 = customer, 1 = courier, 2 = parcel

# displays a menu/submenu
def display_menu(menuChoice):
    count = 1
    for items in menuOptions[menuChoice]:
        tempStr = str(count)+ '. ' + items
        print(tempStr)
        count += 1

# displays the main menu for the admin
def main_admin_menu():
    userChoice = ''
    while userChoice != '5':
        display_menu('Main')
        userChoice = input('Select option: ')
        if userChoice == '1':
            customers_menu()
        elif userChoice == '2':
            couriers_menu()
        elif userChoice == '3':
            reports_menu
        elif userChoice == '4':
            parcels_menu()

# displays the options for the master data menu
def customers_menu():
    userChoice = ''
    while userChoice != '6':
       display_menu('Customers')
       userChoice = input('Select option: ')
       if userChoice == '1':
           view_all_users(0)
       elif userChoice == '2':
           search_users(0)
       elif userChoice == '3':
           add_user(0)
       elif userChoice == '4':
           modify_user(0)
       elif userChoice == '5':
           remove_user(0)
        
# displays the options for the jobs
def couriers_menu():
    userChoice = ''
    while userChoice != '6':
        display_menu('Couriers')
        userChoice = input('Select option: ')
        if userChoice == '1':
            view_all_users(1)
        elif userChoice == '2':
            search_users(1)
        elif userChoice == '3':
            add_user(1)
        elif userChoice == '4':
            modify_user(1)
        elif userChoice == '5':
            remove_user(1)

# displays the options for the customers within the master data
def parcels_menu():
    userChoice = ''
    while userChoice != '6':
        display_menu('Parcels')
        userChoice = input('Select option: ')
        if userChoice == '1':
            view_parcels(0)
            view_parcels(1)
        elif userChoice == '2':
            view_parcels(0)
        elif userChoice == '3':
            add_parcel()
        elif userChoice == '4':
            modify_parcel()
        elif userChoice == '5':
            remove_parcel()
    
# displays the options for the couriers
def reports_menu():
    userChoice = ''
    while userChoice != '2':
        display_menu('Reports')
        userChoice = input('Select option: ')
        if userChoice == '1':
            pass

# displays the menu for couriers company
def main_courier_menu(courierID):
    userChoice = ''
    while userChoice != '5':
        display_menu('MainCourier')
        userChoice = input('Select option: ')
        if userChoice == '1':
            print_list_item(2, search_parcel('Courier', courierID))
        elif userChoice == '2':
            print_list_item(2, search_undelivered_parcel(courierID))
        elif userChoice == '3':
            modify_parcel_status(int(courierID))
        elif userChoice == '4':
            set_parcel_status_delivered(int(courierID))