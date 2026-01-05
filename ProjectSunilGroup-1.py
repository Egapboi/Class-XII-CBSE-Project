from rich.console import Console
from rich.table import Table 
import mariadb as con
from datetime import datetime, timedelta
import random as rand
import re
import os
from dotenv import load_dotenv
load_dotenv()
console= Console()

console.print('[grey93]-[grey89]-[grey85]-[grey82]-[grey78]-[grey74]-[grey70]-[grey66]-[grey62]-[grey58]-[grey54]-[grey50]-[grey46]-[grey42]-[grey39]-[grey35]-[grey30]-[grey27]-[grey23]-[grey19]-[grey15]-[grey11]-[grey7]-[grey3]-[/grey3]Welcome to [magenta3]Track[/magenta3][red3]It[/red3][grey3]-[/grey3][grey7]-[grey11]-[grey15]-[grey19]-[grey23]-[grey27]-[grey30]-[grey35]-[grey39]-[grey42]-[grey46]-[grey50]-[grey54]-[grey58]-[grey62]-[grey66]-[grey70]-[grey74]-[grey78]-[grey82]-[grey85]-[grey89]-[grey93]-[/grey93]')

console.print("""Wanna exit real quick?
Just type [light_goldenrod1]'-1'[/light_goldenrod1]!""")

def db_connection():
    return con.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "TrackIt"))

def exit(input_para):
    try:
        if int(input_para)==-1:
            console.print('[bright_red]EXITING...')
            return True
        else:
            return False
    except ValueError:
        return False

def choose():
    while 1:
        choose_table= Table(title='Choose your user type')
        choose_table.add_column('Enter', justify='center')
        choose_table.add_column('User Type', justify='center', style='yellow')
        choose_table.add_row('1', 'User')
        choose_table.add_row('2', 'Admin')
        choose_table.add_row('3', 'Delivery Man')
        console.print(choose_table)
        try:
            choose_type=input("Enter 1 | 2 | 3 : ")
            if exit(choose_type):
                choose()
                return
            elif choose_type not in ['1','2','3']:
                console.print('[bright_red]Invalid choice given, retry.[/bright_red]')
                continue
            elif choose_type=='1':
                normal_user_choose()
                break
            elif choose_type=='2':
                admin_login()
                break
            elif choose_type=='3':
                delivery_man_login()
                break
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue

#########################################normal user###############################################################################################################################################################################################################
def normal_user_choose():
    while 1:
        normal_user_choice=input("""Already have an account?
Enter 1 for login 
    or   
Don't have an account? 
Sign up for a new account by entering 2:  
""")
        if exit(normal_user_choice):
                choose()
                return
        try:
            if normal_user_choice.lower()in ['1', 'login', 'log in']:
                normal_user_login()
                break
            elif normal_user_choice.lower() in ['2', 'sign up', 'signup']:
                normal_user_signup()
                break
            else:
                console.print('[bright_red]Invalid choice given, retry.[/bright_red]')
                continue
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
        
def normal_user_signup():
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try:
            email_signup=input('Enter your email: ')
            if exit(email_signup):
                choose()
                return
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_signup):
                console.print('[bright_red]Invalid email format! Please enter a valid email.[/bright_red]')
                continue

            cur.execute("select count(*) from normal_user_data where email=%s", (email_signup,))
            if cur.fetchone()[0] > 0:
                console.print('[bright_red]Email is already registered, retry.[/bright_red]')
                continue
            
            name_signup=input('Enter your name: ')
            if exit(name_signup):
                choose()
                return
            state=input('Enter your state: ')
            if exit(state):
                choose()
                return
            city=input('Enter your city: ')
            if exit(city):
                choose()
                return
            password_signup=''
            while 1:
                password_signup_temp=input('Enter your password: ')
                if exit(password_signup_temp):
                    choose()
                    return
                reenter_password_temp=input('Re-enter your password: ')
                if exit(reenter_password_temp):
                    choose()
                    return
                elif password_signup_temp==reenter_password_temp:
                    password_signup=reenter_password_temp
                    break
                else:
                    console.print("[bright_red]Password doesn't match, retry.[/bright_red]")
                    continue
            cur.execute("insert into normal_user_data (Name, state, city, password, email) values (%s, %s, %s, %s, %s)",(name_signup, state, city, password_signup, email_signup))
            connect.commit()
            console.print('[green]Account created successfully![/green]')
            normal_user_login()
            return
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
    cur.close()
                
def show_orders_user(show_orders_var, email_login, password_login):
    connect = db_connection()

    cur=connect.cursor()
    cur.execute("select * from orders where id=%s", (show_orders_var,))
    user_order_data = cur.fetchall()
    connect.commit()
    user_order_data_table = Table(title='Your Order Data', style='blue')
    user_order_data_table.add_column('Order ID', justify='center')
    user_order_data_table.add_column('Item', justify='center', style='green1')
    user_order_data_table.add_column('Ordered On', justify='center', style='green1')
    user_order_data_table.add_column('Expected Delivery Date', justify='center')
    user_order_data_table.add_column('Delivery Status', justify='center')
    user_order_data_table.add_column('Item Price in ₹', justify='center')
    for i in user_order_data:
        order_date_temp = i[2].strftime("%Y-%m-%d")
        exp_delivery_date_temp = i[3].strftime("%Y-%m-%d")
        user_order_data_table.add_row(
            str(i[0]), i[1], order_date_temp, exp_delivery_date_temp, i[6], str(i[5])
        )
    console.print(user_order_data_table)
    return
    cur.close()
    

def get_delivery_status(specific_user_order_data, user_city):
    connect = db_connection()

    cur=connect.cursor()
    cur.execute('select item_name from order_items')
    order_items_names = []
    for i in cur.fetchall():
        order_items_names.append(i[0])
    cur.execute('select item_manu from order_items')
    order_items_locations = [] 
    for i in cur.fetchall():
        order_items_locations.append(i[0])
    random_city_pool = [
        "Delhi", "Nagpur", "Raipur", "Kolkata", "Ranchi", "Patna",
        "Lucknow", "Hyderabad", "Chennai", "Jaipur", "Pune", "Ahmedabad"
    ]

    today = datetime.now().date()

    for order in specific_user_order_data:
        order_id, _, delivery_date = order

        cur.execute('select item from orders where order_id=%s', (order_id,))
        user_item = cur.fetchone()
        if not user_item:
            continue
        item_name = user_item[0]
        manf_city = order_items_locations[order_items_names.index(item_name)]
        diff_days = (delivery_date - today).days
        if diff_days in range(7, 10):
            status = f"In Warehouse {manf_city}"
        elif diff_days == 6:
            status = f"Out of Shipping, {rand.choice(random_city_pool)}"
        elif diff_days in range(2, 6):
            status = f"Shipping, {rand.choice(random_city_pool)}"
        elif diff_days == 1:
            status = f"Out of Delivery {user_city}"
        elif diff_days <= 0:
            status = "Delivered"
        else:
            status = "Pending"
        cur.execute('update orders set delivery_status=%s where order_id=%s', (status, order_id,))
    connect.commit()
    cur.close()

def normal_user_order(user_order_var):
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try:
            console.print("[cyan]1. List All Items\n2. Search Item[/cyan]")
            search_choice = input("Enter choice (1/2): ")
            if exit(search_choice):
                choose()
                return

            if search_choice == '2':
                search_term = input("Enter search term: ")
                if exit(search_term):
                    choose()
                    return
                query="select item_name, item_price, item_manu from order_items where item_name like %s"
                params=('%'+search_term+'%',)
            else:
                query="select item_name, item_price, item_manu from order_items"
                params=()

            cur.execute(query, params)
            items = cur.fetchall()
            
            if not items:
                console.print("[yellow]No items found.[/yellow]")
                continue

            order_items_names = [i[0] for i in items]
            order_items_prices = [i[1] for i in items]
            order_items_locations = [i[2] for i in items]

            cur.execute('select city from normal_user_data where id=%s',(user_order_var,))
            current_city_of_user=cur.fetchone()
            connect.commit()
            order_item_table=Table(title='List of Items to Order', style='blue')
            order_item_table.add_column('Enter', justify='center')
            order_item_table.add_column('Item Name', justify='center', style='green1')
            order_item_table.add_column('Price (₹)', justify='center')
            count1=0
            for name, price in zip(order_items_names, order_items_prices):
                count1+=1
                order_item_table.add_row(str(count1), name, str(price))
            console.print(order_item_table)
            choose_order_no=int(input('Which item do you want to order? '))
            if exit(choose_order_no):
                choose()
                return
            elif choose_order_no-1 in range(len(order_items_locations)):
                item_chose=[order_items_names[choose_order_no-1], order_items_prices[choose_order_no-1], order_items_locations[choose_order_no-1]]
                initial_date=datetime.now().date()
                initial_date_str=str(initial_date)
                expected_date=initial_date+timedelta(days=rand.randint(7,9))
                expected_date_str=str(expected_date)
                
                cur.execute("select man_id from delivery_men_data")
                all_men = []
                for m in cur.fetchall():
                    all_men.append(m[0])
                available_men = []
                
                for man_id in all_men:
                    cur.execute("select count(*) from orders where delivery_man_id=%s and exp_delivery_date=%s", (man_id, expected_date))
                    count = cur.fetchone()[0]
                    if count < 20:
                        available_men.append(man_id)
                
                if available_men:
                    assigned_man_id = rand.choice(available_men)
                else:
                    assigned_man_id = None
                
                cur.execute("insert into orders (item, order_date, id, price, exp_delivery_date, delivery_status, delivery_man_id) values (%s, %s, %s, %s, %s, %s, %s)",
                            (item_chose[0], initial_date, user_order_var, item_chose[1], expected_date, 'Pending', assigned_man_id))
                connect.commit()
                if assigned_man_id:
                    console.print(f"[green]Order placed and assigned to delivery agent ID {assigned_man_id}.[/green]")
                else:
                    console.print("[yellow]Order placed but delivery agent assignment pending (capacity full).[/yellow]")
                return
            else:
                console.print('[bright_red]Invalid choice given, retry.[/bright_red]')
                continue
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
    cur.close()
            
            
def user_profile_edit(current_user_id, current_email, current_password):
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try: 
            password_for_edit=input('Enter your password: ')
            if exit(password_for_edit):
                choose()
                return
            cur.execute("SELECT password FROM normal_user_data WHERE id=%s",(current_user_id, ))
            current_user_password=cur.fetchone()
            connect.commit()
            if password_for_edit!=current_user_password[0]:
                console.print('[bright_red]Password does not match! Retry.[/bright_red]')
                continue
            else:
                user_profile_edit_table=Table(title='What do you want to edit?', style='yellow')
                user_profile_edit_table.add_column('Enter', justify='center')
                user_profile_edit_table.add_column('Change your', justify='center', style='blue')
                user_profile_edit_table.add_row('1', 'Name')
                user_profile_edit_table.add_row('2', 'Password')
                user_profile_edit_table.add_row('3', 'City')
                user_profile_edit_table.add_row('4', 'State')
                console.print(user_profile_edit_table)
                while 1: 
                    try: 
                        user_profile_edit_choose=int(input('Enter the choice 1 | 2 | 3 | 4: '))
                        if exit(user_profile_edit_choose):
                            choose()
                            return
                        elif user_profile_edit_choose not in [1,2,3,4]:
                            console.print('[bright_red]Invalid choice given, retry.[/bright_red]')
                            continue
                        else:
                            if user_profile_edit_choose==1:
                                while 1:
                                    try:
                                        change_name=input('What would you like to change your name to?')
                                        if exit(change_name):
                                            choose()
                                            return
                                        cur.execute('update normal_user_data set Name=%s where id=%s', (change_name, current_user_id))
                                        connect.commit()
                                        after_user_login(current_user_id, current_email, current_password)
                                        return
                                        break
                                    except ValueError:
                                        console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
                                        continue
                            elif user_profile_edit_choose==2:
                                while 1:
                                    try: 
                                        change_password=input('What would you like to change your password to?')
                                        if exit(change_password):
                                            choose()
                                            return
                                        cur.execute('update normal_user_data set password=%s where id=%s', (change_password, current_user_id))
                                        connect.commit()
                                        after_user_login(current_user_id, current_email, change_password)
                                        return
                                        break
                                    except ValueError:
                                        console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
                                        continue
                            elif user_profile_edit_choose==3:
                                while 1:
                                    try: 
                                        change_city=input('What would you like to change your city to?')
                                        if exit(change_city):
                                            choose()
                                            return
                                        cur.execute('update normal_user_data set city=%s where id=%s', (change_city, current_user_id))
                                        connect.commit()
                                        after_user_login(current_user_id, current_email, current_password)
                                        return
                                        break
                                    except ValueError:
                                        console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
                                        continue
                            elif user_profile_edit_choose==4:
                                while 1:
                                    try: 
                                        change_state=input('What would you like to change your state to?')
                                        if exit(change_state):
                                            choose()
                                            return
                                        cur.execute('update normal_user_data set state=%s where id=%s', (change_state, current_user_id))
                                        connect.commit()
                                        after_user_login(current_user_id, current_email, current_password)
                                        return
                                        break
                                    except ValueError:
                                        console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
                                        continue
                        after_user_login(current_user_id, current_email, current_password)
                        break
                    except ValueError:
                        console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
                        continue
            break  
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue 
    cur.close()
    
def after_user_login(normal_user_id=None, email_login=None, password_login=None):
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        after_user_login_choose=Table(title='Enter 1 | 2 | 3]')
        after_user_login_choose.add_column('Enter', justify='center')
        after_user_login_choose.add_column('for', justify='center', style='blue')
        after_user_login_choose.add_row('1', 'Edit your profile')
        after_user_login_choose.add_row('2', 'Show profile info and your orders')
        after_user_login_choose.add_row('3', 'Order an item')
        console.print(after_user_login_choose)
        cur.execute("SELECT id, name, city, state FROM normal_user_data WHERE email=%s AND password=%s",(email_login, password_login))
        current_user_data=cur.fetchone()
        connect.commit()
        try:
            after_user_login_choice=int(input())
            if exit(after_user_login_choice):
                choose()
                return
            if after_user_login_choice==1:
                user_profile_edit(current_user_data[0], email_login, password_login)
            elif after_user_login_choice==2:
                cur.execute('select order_id, order_date, exp_delivery_date from orders where id=%s', (current_user_data[0],))
                specific_user_order_data=cur.fetchall()
                connect.commit()
                get_delivery_status(specific_user_order_data, current_user_data[2])
                console.print(f'Name: [chartreuse1]{current_user_data[1]}[/chartreuse1], ID: [chartreuse1]{current_user_data[0]}[/chartreuse1], State: [chartreuse1]{current_user_data[3]}[/chartreuse1], City: [chartreuse1]{current_user_data[2]}[/chartreuse1]')
                show_orders_user(current_user_data[0], email_login, password_login)
            elif after_user_login_choice==3:
                normal_user_order(current_user_data[0])
            else:
                console.print('[bright_red]Invalid choice given, retry.[/bright_red]')
                continue
        except ValueError as e:
            console.print(f'[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
    cur.close()
            
def normal_user_login():
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try:
            email_login=input('Enter your email ID: ')
            if exit(email_login):
                choose()
                return
            password_login=input('Enter your password: ')
            if exit(password_login):
                choose()
                return
            cur.execute("SELECT id, name FROM normal_user_data WHERE email=%s AND password=%s",(email_login, password_login))
            normal_user=cur.fetchone()
            connect.commit()
            if normal_user:
                normal_user_id, normal_user_name=normal_user
                console.print(f"WELCOME [green]{normal_user_name}[/green]!")
                after_user_login(normal_user_id, email_login, password_login)
                break
            else:
                console.print('[bright_red]Invalid email ID or password, retry.[/bright_red]')
                continue
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
    cur.close()
#########################################/normal user##############################################################################################################################################################################################################

#########################################admin#####################################################################################################################################################################################################################
def add_dman():
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try:
            dman_name_add=input('Enter the name of the delivery man: ')
            if exit(dman_name_add):
                choose()
                return
            dman_email_add=input('Enter your email: ')
            if exit(dman_email_add):
                choose()
                return
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", dman_email_add):
                console.print('[bright_red]Invalid email format! Please enter a valid email.[/bright_red]')
                continue

            

            if not re.match(r"[^@]+@[^@]+\.[^@]+", dman_email_add):
                console.print('[bright_red]Invalid email format! Please enter a valid email.[/bright_red]')
                continue

            cur.execute("select count(*) from delivery_men_data where man_email=%s", (dman_email_add,))
            if cur.fetchone()[0] > 0:
                console.print('[bright_red]Email is already registered as a Delivery Man, retry.[/bright_red]')
                continue
                return
            while 1:
                dman_password_add=input('Enter the password of the delivery man: ')
                if exit(dman_password_add):
                    choose()
                    return
                dman_password_temp=input('Renter the password: ')
                if exit(dman_password_temp):
                    choose()
                    return
                if dman_password_add == dman_password_temp:
                    break
                else:
                    console.print("[bright_red]Password doesn't match, retry.[/bright_red]")
            cur.execute("insert into delivery_men_data (man_name, man_email, man_password) values (%s,%s,%s)",(dman_name_add, dman_email_add, dman_password_add))
            connect.commit()
            console.print('[green]Delivery man added successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            break
    cur.close()

def remove_dman():
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try:
            dman_id_remove=int(input('Enter id of the delivery man you wanna remove: '))
            if exit(dman_id_remove):
                choose()
                return
            dman_password_remove=input('Enter password of the delivery man you wanna remove: ')
            if exit(dman_password_remove):
                choose()
                return

            cur.execute("select man_id from delivery_men_data where man_id=%s and man_password=%s", (dman_id_remove, dman_password_remove))
            if cur.fetchone():
                cur.execute("update orders set delivery_man_id=NULL where delivery_man_id=%s", (dman_id_remove,))
                connect.commit()
                
                cur.execute("delete from delivery_men_data where man_id=%s", (dman_id_remove,))
                console.print('[green]Delivery man removed successfully![/green]')
            else:
                console.print('[bright_red]Delivery man not found or credentials wrong![/bright_red]')
            connect.commit()
            return
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
    cur.close()

def assign_to_dman():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select order_id, item, delivery_status from orders where delivery_man_id is NULL and delivery_status!='Delivered'")
            orders = cur.fetchall()
            if not orders:
                console.print('[yellow]No pending orders to assign.[/yellow]')
                return
            
            table = Table(title="Pending Orders")
            table.add_column("Order ID", justify="center")
            table.add_column("Item", justify="center")
            table.add_column("Status", justify="center")
            for o in orders:
                table.add_row(str(o[0]), o[1], o[2])
            console.print(table)

            order_id = int(input("Enter Order ID to assign: "))
            if exit(order_id): 
                choose()
                return

            cur.execute("select man_id, man_name from delivery_men_data")
            men = cur.fetchall()
            if not men:
                console.print('[red]No delivery men available.[/red]')
                return

            dman_table = Table(title="Delivery Men")
            dman_table.add_column("ID", justify="center")
            dman_table.add_column("Name", justify="center")
            for m in men:
                dman_table.add_row(str(m[0]), m[1])
            console.print(dman_table)
            
            man_id = int(input("Enter Delivery Man ID: "))
            if exit(man_id): 
                choose()
                return

            cur.execute("update orders set delivery_man_id=%s where order_id=%s", (man_id, order_id))
            connect.commit()
            console.print('[green]Order assigned successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def remove_assign_dman():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select order_id, item, delivery_man_id from orders where delivery_man_id is NOT NULL")
            orders = cur.fetchall()
            if not orders:
                console.print('[yellow]No assigned orders found.[/yellow]')
                return

            table = Table(title="Assigned Orders")
            table.add_column("Order ID", justify="center")
            table.add_column("Item", justify="center")
            table.add_column("Delivery Man ID", justify="center")
            for o in orders:
                table.add_row(str(o[0]), o[1], str(o[2]))
            console.print(table)

            order_id = int(input("Enter Order ID to remove assignment: "))
            if exit(order_id): 
                choose()
                return
            
            cur.execute("update orders set delivery_man_id=NULL where order_id=%s", (order_id,))
            connect.commit()
            console.print('[green]Assignment removed successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def remove_user():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select ID, Name, email from normal_user_data")
            users = cur.fetchall()
            table = Table(title="Users")
            table.add_column("ID", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Email", justify="center")
            for u in users:
                table.add_row(str(u[0]), u[1], u[2])
            console.print(table)

            user_id = int(input("Enter User ID to remove: "))
            if exit(user_id): 
                choose()
                return
            
            cur.execute("delete from orders where ID=%s", (user_id,))
            connect.commit()
            
            cur.execute("delete from normal_user_data where ID=%s", (user_id,))
            if cur.rowcount > 0:
                console.print('[green]User removed successfully![/green]')
            else:
                console.print('[red]User not found.[/red]')
            connect.commit()
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def remove_user_order():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select order_id, item, ID from orders")
            orders = cur.fetchall()
            table = Table(title="All Orders")
            table.add_column("Order ID", justify="center")
            table.add_column("Item", justify="center")
            table.add_column("User ID", justify="center")
            for o in orders:
                table.add_row(str(o[0]), o[1], str(o[2]))
            console.print(table)

            order_id = int(input("Enter Order ID to remove: "))
            if exit(order_id): 
                choose()
                return
            
            cur.execute("delete from orders where order_id=%s", (order_id,))
            if cur.rowcount > 0:
                console.print('[green]Order removed successfully![/green]')
            else:
                console.print('[red]Order not found.[/red]')
            connect.commit()
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()


def edit_user_info():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select ID, Name, email, city, state from normal_user_data")
            users = cur.fetchall()
            table = Table(title="Users")
            table.add_column("ID", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Email", justify="center")
            for u in users:
                table.add_row(str(u[0]), u[1], u[2])
            console.print(table)

            user_id = int(input("Enter User ID to edit: "))
            if exit(user_id): 
                choose()
                return

            console.print("[cyan]1. Name\n2. City\n3. State\n4. Password[/cyan]")
            choice = int(input("What to edit? "))
            if exit(choice): 
                choose()
                return

            if choice == 1:
                new_val = input("Enter new Name: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update normal_user_data set Name=%s where ID=%s", (new_val, user_id))
            elif choice == 2:
                new_val = input("Enter new City: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update normal_user_data set city=%s where ID=%s", (new_val, user_id))
            elif choice == 3:
                new_val = input("Enter new State: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update normal_user_data set state=%s where ID=%s", (new_val, user_id))
            elif choice == 4:
                new_val = input("Enter new Password: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update normal_user_data set password=%s where ID=%s", (new_val, user_id))
            else:
                console.print("[red]Invalid choice[/red]")
                continue
            
            connect.commit()
            console.print('[green]User updated successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def add_item():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            name = input("Enter Item Name: ")
            if exit(name): 
                choose()
                return
            price = int(input("Enter Item Price: "))
            if exit(price): 
                choose()
                return
            manu = input("Enter Manufacturer: ")
            if exit(manu): 
                choose()
                return

            cur.execute("insert into order_items (item_name, item_price, item_manu) values (%s, %s, %s)", (name, price, manu))
            connect.commit()
            console.print('[green]Item added successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def remove_item():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select item_id, item_name, item_price from order_items")
            items = cur.fetchall()
            table = Table(title="Items")
            table.add_column("ID", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Price", justify="center")
            for i in items:
                table.add_row(str(i[0]), i[1], str(i[2]))
            console.print(table)

            item_id = int(input("Enter Item ID to remove: "))
            if exit(item_id): 
                choose()
                return
            
            cur.execute("delete from order_items where item_id=%s", (item_id,))
            if cur.rowcount > 0:
                console.print('[green]Item removed successfully![/green]')
            else:
                console.print('[red]Item not found.[/red]')
            connect.commit()
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def edit_item():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select item_id, item_name, item_price, item_manu from order_items")
            items = cur.fetchall()
            table = Table(title="Items")
            table.add_column("ID", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Price", justify="center")
            table.add_column("Manu", justify="center")
            for i in items:
                table.add_row(str(i[0]), i[1], str(i[2]), i[3])
            console.print(table)

            item_id = int(input("Enter Item ID to edit: "))
            if exit(item_id): 
                choose()
                return

            console.print("[cyan]1. Name\n2. Price\n3. Manufacturer[/cyan]")
            choice = int(input("What to edit? "))
            if exit(choice): 
                choose()
                return

            if choice == 1:
                new_val = input("Enter new Name: ")
                if exit(new_val): choose(); return
                cur.execute("update order_items set item_name=%s where item_id=%s", (new_val, item_id))
            elif choice == 2:
                new_val = int(input("Enter new Price: "))
                if exit(new_val): choose(); return
                cur.execute("update order_items set item_price=%s where item_id=%s", (new_val, item_id))
            elif choice == 3:
                new_val = input("Enter new Manufacturer: ")
                if exit(new_val): choose(); return
                cur.execute("update order_items set item_manu=%s where item_id=%s", (new_val, item_id))
            else:
                console.print("[red]Invalid choice[/red]")
                continue

            connect.commit()
            console.print('[green]Item updated successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def edit_order():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select order_id, item, delivery_status, exp_delivery_date from orders")
            orders = cur.fetchall()
            table = Table(title="Orders")
            table.add_column("ID", justify="center")
            table.add_column("Item", justify="center")
            table.add_column("Status", justify="center")
            table.add_column("Exp Date", justify="center")
            for o in orders:
                if o[3]:
                    exp_date = str(o[3])
                else:
                    exp_date = "N/A"
                table.add_row(str(o[0]), o[1], o[2], exp_date)
            console.print(table)

            order_id = int(input("Enter Order ID to edit: "))
            if exit(order_id): 
                choose()
                return

            console.print("[cyan]1. Status\n2. Expected Delivery Date (YYYY-MM-DD)[/cyan]")
            choice = int(input("What to edit? "))
            if exit(choice): 
                choose()
                return

            if choice == 1:
                new_val = input("Enter new Status: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update orders set delivery_status=%s where order_id=%s", (new_val, order_id))
            elif choice == 2:
                new_val = input("Enter new Date (YYYY-MM-DD): ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update orders set exp_delivery_date=%s where order_id=%s", (new_val, order_id))
            else:
                console.print("[red]Invalid choice[/red]")
                continue

            connect.commit()
            console.print('[green]Order updated successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()

def edit_dman():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            cur.execute("select man_id, man_name, man_email from delivery_men_data")
            men = cur.fetchall()
            table = Table(title="Delivery Men")
            table.add_column("ID", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Email", justify="center")
            for m in men:
                table.add_row(str(m[0]), m[1], m[2])
            console.print(table)

            man_id = int(input("Enter Delivery Man ID to edit: "))
            if exit(man_id): 
                choose()
                return

            console.print("[cyan]1. Name\n2. Email\n3. Password[/cyan]")
            choice = int(input("What to edit? "))
            if exit(choice): 
                choose()
                return

            if choice == 1:
                new_val = input("Enter new Name: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update delivery_men_data set man_name=%s where man_id=%s", (new_val, man_id))
            elif choice == 2:
                new_val = input("Enter new Email: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update delivery_men_data set man_email=%s where man_id=%s", (new_val, man_id))
            elif choice == 3:
                new_val = input("Enter new Password: ")
                if exit(new_val): 
                    choose()
                    return
                cur.execute("update delivery_men_data set man_password=%s where man_id=%s", (new_val, man_id))
            else:
                console.print("[red]Invalid choice[/red]")
                continue
            
            connect.commit()
            console.print('[green]Delivery Man updated successfully![/green]')
            return
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()


def see_dman_info():
    connect = db_connection()
    cur=connect.cursor()
    cur.execute("select * from delivery_men_data")
    men = cur.fetchall()
    table = Table(title="Delivery Men Info")
    table.add_column("ID", justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Email", justify="center")
    table.add_column("Password", justify="center")
    for m in men:
        table.add_row(str(m[0]), m[1], m[2], m[3])
    console.print(table)
    input("Press Enter to return...")
    cur.close()

def see_order_info():
    connect = db_connection()
    cur=connect.cursor()
    cur.execute("select * from orders")
    orders = cur.fetchall()
    table = Table(title="All Orders Info")
    table.add_column("Order ID", justify="center")
    table.add_column("Item", justify="center")
    table.add_column("Order Date", justify="center")
    table.add_column("Exp Date", justify="center")
    table.add_column("User ID", justify="center")
    table.add_column("Price", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("DMan ID", justify="center")
    
    for o in orders:
        if o[2]:
            o_date = str(o[2])
        else:
            o_date = "N/A"
        if o[3]:
            exp_date = str(o[3])
        else:
            exp_date = "N/A"
        if o[7] is not None:
            dman_id = str(o[7])
        else:
            dman_id = "Unassigned"
        table.add_row(str(o[0]), o[1], o_date, exp_date, str(o[4]), str(o[5]), o[6], dman_id)
    console.print(table)
    input("Press Enter to return...")
    cur.close()

def see_user_info():
    connect = db_connection()
    cur=connect.cursor()
    cur.execute("select * from normal_user_data")
    users = cur.fetchall()
    table = Table(title="All Users Info")
    table.add_column("Name", justify="center")
    table.add_column("ID", justify="center")
    table.add_column("Password", justify="center")
    table.add_column("City", justify="center")
    table.add_column("State", justify="center")
    table.add_column("Email", justify="center")
    
    for u in users:
        table.add_row(u[0], str(u[1]), u[2], u[3], u[4], u[5])
    console.print(table)
    input("Press Enter to return...")
    cur.close()

def after_admin_login(admin_id=None):
    while 1:
        after_admin_login_choose=Table(title='Choose What to Do')
        after_admin_login_choose.add_column('Enter',justify='center')
        after_admin_login_choose.add_column('Action', justify='center',style='cyan')
        after_admin_login_choose.add_row('1','Add a Delivery Man')
        after_admin_login_choose.add_row('2','Remove a Delivery Man')
        after_admin_login_choose.add_row('3','Assign Delivery to a Delivery Man')
        after_admin_login_choose.add_row('4','Remove Delivery from a Delivery Man')
        after_admin_login_choose.add_row('5','Remove a User')
        after_admin_login_choose.add_row('6',"Remove a User's Order")
        after_admin_login_choose.add_row('7',"Edit an User Info")
        after_admin_login_choose.add_row('8',"Add an Item")
        after_admin_login_choose.add_row('9',"Remove an Item")
        after_admin_login_choose.add_row('10','Edit an Item Info')
        after_admin_login_choose.add_row('11','Edit an Order Info')
        after_admin_login_choose.add_row('12','Edit a Delivery Man Info')
        after_admin_login_choose.add_row('13','See Delivery Man Info')
        after_admin_login_choose.add_row('14','See Order Info')
        after_admin_login_choose.add_row('15','See User Info')
        after_admin_login_choose.add_row('16','See Project Statistics')
        console.print(after_admin_login_choose)
        try:
            admin_choose=int(input('Enter a choice: '))
            if exit(admin_choose):
                choose()
                return
            elif admin_choose not in range(1,17):
                console.print('[bright_red]Invalid choice given, retry.[/bright_red]')
                continue
            elif admin_choose==1:
                add_dman()
            elif admin_choose==2:
                remove_dman()
            elif admin_choose==3:
                assign_to_dman()
            elif admin_choose==4:
                remove_assign_dman()
            elif admin_choose==5:
                remove_user()
            elif admin_choose==6:
                remove_user_order()
            elif admin_choose==7:
                edit_user_info()
            elif admin_choose==8:
                add_item()
            elif admin_choose==9:
                remove_item()
            elif admin_choose==10:
                edit_item()
            elif admin_choose==11:
                edit_order()
            elif admin_choose==12:
                edit_dman()
            elif admin_choose==13:
                see_dman_info()
            elif admin_choose==14:
                see_order_info()
            elif admin_choose==15:
                see_user_info()
            elif admin_choose==16:
                see_statistics()
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
                    
#########################################dman#####################################################################################################################################################################################################################
def after_dman_login(dman_id, dman_name):
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        console.print(f"\n[bold green]Welcome {dman_name}![/bold green]")
        try:
            cur.execute("""
                select order_id, item, exp_delivery_date, delivery_status, city, state 
                from orders natural join normal_user_data 
                where delivery_man_id = %s
            """, (dman_id,))
            orders = cur.fetchall()
            
            if not orders:
                console.print("[yellow]No orders assigned to you yet.[/yellow]")
            else:
                table = Table(title=f"Orders Assigned to {dman_name}")
                table.add_column("Order ID", justify="center")
                table.add_column("Item", justify="center")
                table.add_column("Exp Date", justify="center")
                table.add_column("Status", justify="center")
                table.add_column("City", justify="center")
                table.add_column("State", justify="center")
                
                for o in orders:
                    if o[2]:
                        exp_date = str(o[2])
                    else:
                        exp_date = "N/A"
                    table.add_row(str(o[0]), o[1], exp_date, o[3], o[4], o[5])
                console.print(table)
            
            console.print("\n[cyan]Press Enter to refresh/return or type '-1' to logout.[/cyan]")
            choice = input()
            if exit(choice):
                choose()
                return
        except ValueError:
            console.print('[bright_red]Enter a valid data, retrying...[/bright_red]')
            continue
    cur.close()

def see_statistics():
    connect = db_connection()
    cur=connect.cursor()
    cur.execute("select count(*) from normal_user_data")
    total_users = cur.fetchone()[0]
    cur.execute("select count(*) from delivery_men_data")
    total_dmen = cur.fetchone()[0]
    cur.execute("select count(*) from orders")
    total_orders = cur.fetchone()[0]
    cur.execute("select sum(price) from orders")
    total_revenue = cur.fetchone()[0]
    if total_revenue is None:
        total_revenue = 0
    table = Table(title="Project Statistics", style="bold magenta")
    table.add_column("Metric", justify="right", style="cyan")
    table.add_column("Value", justify="left", style="green")
    table.add_row("Total Users", str(total_users))
    table.add_row("Total Delivery Men", str(total_dmen))
    table.add_row("Total Orders", str(total_orders))
    table.add_row("Total Revenue", f"₹{total_revenue}")
    console.print(table)

    cur.execute("select u.city, count(*) from orders o, normal_user_data u where o.ID = u.ID group by u.city")
    city_stats = cur.fetchall()
    if city_stats:
        city_table = Table(title="Orders by City", style="bold yellow")
        city_table.add_column("City", justify="center")
        city_table.add_column("Orders", justify="center")
        for city, count in city_stats:
            city_table.add_row(city, str(count))
        console.print(city_table)

    input("Press Enter to return...")
    cur.close()

def delivery_man_login():
    connect = db_connection()
    cur=connect.cursor()
    while 1:
        try:
            dman_email=input('Enter your email: ')
            if exit(dman_email):
                choose()
                return
            dman_password=input('Enter your password: ')
            if exit(dman_password):
                choose()
                return
            
            cur.execute("select man_id, man_name from delivery_men_data where man_email=%s and man_password=%s", (dman_email, dman_password))
            dman = cur.fetchone()
            
            if dman:
                after_dman_login(dman[0], dman[1])
                break
            else:
                console.print('[bright_red]Invalid credentials, retry.[/bright_red]')
                continue
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()
#########################################/dman#####################################################################################################################################################################################################################


def admin_login():
    connect = db_connection()

    cur=connect.cursor()
    while 1:
        try:
            admin_email_login=input('Enter your email ID: ')
            if exit(admin_email_login):
                choose()
                return
            admin_password_login=input('Enter your password: ')
            if exit(admin_password_login):
                choose()
                return
            cur.execute("select admin_id, Name from admin_data where email=%s and password=%s",(admin_email_login, admin_password_login))
            admin=cur.fetchone()
            connect.commit()
            if admin:
                admin_id, admin_name=admin
                console.print(f"WELCOME [green]{admin_name}[/green]!")
                after_admin_login(admin_id)
                break
            else:
                console.print('[bright_red]Invalid credentials, retry.[/bright_red]')
                continue
        except ValueError:
            console.print('[bright_red]Invalid input, retrying...[/bright_red]')
            continue
    cur.close()
#########################################/admin#####################################################################################################################################################################################################################

choose()
