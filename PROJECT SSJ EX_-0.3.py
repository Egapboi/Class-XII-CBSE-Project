#IMPORTED MODULES                FUNCTIONS USED FROM THE MODULE

import sys                                  # ——> sys.exit("")                ["" is a string]
import random                           # ——> random.randint(x,y)                [x and y are integers]
import mariadb as m    # ——> m.connect(host="", user="", password="", database="")    ,    db.cursor()






#REGISTER / LOGIN / DELETE / UPDATE ACCOUNT
def Accounts(Choice):
    while True:
        try:
            DB = m.connect(
                host="localhost",
                user="root",
                password="sunil09",
                database="ss_jewellery"
            )
            DB_cursor = DB.cursor()
                    
            Client_Name = CVU(Choice)
            Client_ID = CVID(Choice)
            Client_Password = CVP(Choice)
            
            if Choice == 1:
                if Login_var == '1':
                    Register_query = "INSERT INTO CUSTOMERS VALUES (%s,%s,%s,now())"    #(Name, ID, Password, Registration_Date_&_Time)
                elif Login_var == '3':
                    Register_query = "INSERT INTO STAFFS VALUES (%s,%s,%s,now())"
                elif Login_var == '4':
                    Register_query = "INSERT INTO ADMINS VALUES (%s,%s,%s,now())"
                DB_cursor.execute(Register_query, (Client_Name, Client_ID, Client_Password))
                DB.commit()
            
            elif Choice == 2:
                if Login_var == '1':
                    Check_query = "SELECT Name FROM CUSTOMERS WHERE ID = %s and Password = %s"
                elif Login_var == '2':
                    Check_query = "SELECT Name FROM STAFFS WHERE ID = %s and Password = %s"
                elif Login_var == '3':
                    Check_query = "SELECT Name FROM ADMINS WHERE ID = %s and Password = %s"
                elif Login_var == '4':
                    Check_query = "SELECT Name FROM CEO WHERE ID = %s and Password = %s"
                DB_cursor.execute(Check_query, (Client_ID, Client_Password))
                result = DB_cursor.fetchone()
    
                if result:
                    Name_var = result[0]
                    if Name_var == Client_Name:
                        print("\n", "LOGIN SUCCESSFUL! Welcome back", Name_var, "\n")
                        
                        if Login_var in ['1','4']:
                            if Login_var == '1':
                                Login_query = "INSERT INTO CUSTOMER_LOGIN_HISTORY (Name, ID, Login_Time) VALUES (%s,%s,now())"
                            elif Login_var == '4':
                                Login_query = "INSERT INTO CEO_LOGIN_HISTORY (Name, ID , Login_Time) VALUES (%s,%s,now())"
                            DB_cursor.execute(Login_query , (Client_Name ,Client_ID))
                            DB.commit()
                        
                        elif Login_var in ['2','3']:
                            Client_deal_no = input("Enter DEALERSHIP NUMBER : ")
                            if Login_var == '2':
                                Login_query = "INSERT INTO STAFF_LOGIN_HISTORY (Dealership_No, Name, ID, Login_Time) VALUES (%s,%s,%s,now())"
                            elif Login_var == '3':
                                Login_query = "INSERT INTO ADMIN_LOGIN_HISTORY (Dealership_No, Name, ID, Login_Time) VALUES (%s,%s,%s,now())"
                            DB_cursor.execute(Login_query , (Client_deal_no, Client_Name ,Client_ID))
                            DB.commit()
                    else:
                        print("\n","NAME IS DIFFERENT","\n")
                
                else:
                    print("Invalid NAME or LOGIN ID or PASSWORD. Please try again.\n")
                    EOC()
                    continue
            
            elif Choice in [3, 4]:
                if Login_var == '2':
                    Check_query = "SELECT Name FROM CUSTOMERS WHERE ID = %s and Password = %s"
                elif Login_var == '3':
                    Check_query = "SELECT Name FROM STAFFS WHERE ID = %s and Password = %s"
                elif Login_var == '4':
                    Check_query = "SELECT Name FROM ADMINS WHERE ID = %s and Password = %s"
                DB_cursor.execute(Check_query, (Client_ID, Client_Password))
                result = DB_cursor.fetchone()
    
                if result:
                    Name_var = result[0]
            
                    if Choice == 3:
                        if Login_var == '2':
                            Delete_query = "DELETE FROM CUSTOMERS WHERE ID = %s"
                        elif Login_var == '3':
                            Delete_query = "DELETE FROM STAFFS WHERE ID = %s"
                        elif Login_var == '4':
                            Delete_query = "DELETE FROM ADMINS WHERE ID = %s"
                        DB_cursor.execute(Delete_query, (Client_ID,))
                        DB.commit()
                        print("DETAILS REMOVED SUCCESSFULLY","\n")
                    
                    elif Choice == 4:
                        while True :
                            print("What would you like to UPDATE?")
                            print("Enter 1 for NAME")
                            print("Enter 2 for ID")
                            print("Enter 3 for Password")
                            Update_var = input("Enter your choice here : ")
                            if Update_var in ["1","2","3"]:
                                Login_Dict = {1:"CUSTOMERS", 2:"STAFFS", 3:"ADMINS"}
                                Table = Login_Dict[(int(Login_var)-1)]
                                if Update_var == "1":
                                    New_Name = CVU(1)
                                    Update_query = ("UPDATE %s " % Table) + "SET NAME = %s  WHERE ID = %s"
                                    Para = (New_Name, Client_ID)
                                elif Update_var == "2":
                                    New_ID = CVID(1)
                                    Update_query = ("UPDATE %s " % Table) + "SET ID = %s WHERE ID = %s "
                                    Para = (New_ID, Client_ID)
                                elif Update_var == "3":
                                    New_Password = CVP(1)
                                    Update_query = ("UPDATE %s " % Table) + "SET Password = %s WHERE ID = %s "
                                    Para = (New_Password, Client_ID)
                                DB_cursor.execute(Update_query, Para)
                                DB.commit()
                                print("DETAILS UPDATED SUCCESSFULLY","\n")
                                break
                    
                            else:
                                print("\n","INVALID INPUT","\n")
                                continue

                else:
                    print("Invalid NAME or LOGIN ID or PASSWORD. Please try again.\n")
                    EOC()
                    continue


        except m.Error as error1:
            print("Database error occurred:", error1, "\n")
            EOC()
            
        except Exception as error2:
            print("Unexpected error:", error2, "\n")
            EOC()

        else:
            if Choice == 2:
                print("You have successfully LOGGED IN","\n")
                Client_Data = [Client_Name, Client_ID, Client_Password]
                return Client_Data
            return

        finally:
            if 'DB_cursor' in locals():                #locals() → dictionary which includes all variables and their respective value created in the present code
                DB_cursor.close()
            if 'DB' in locals() and DB is not None:                #HERE '.is_connected' verifies if DB is still connected or not
                DB.close()



#CREATE/CHECK VALID USERNAME
def CVU(Choice_U):
    while True:
        if Choice_U == 1:
            print("PLEASE enter THE REAL FULL NAME","\n")
            
        elif Choice_U in [2,3,4]:
            pass
        
        Username = input("Enter USERNAME : ")
        print("\n","\n")
                                
        count_alpha_Username = 0
        count_space_Username = 0
        for i in Username:
            if i.isalpha():
                count_alpha_Username += 1
            if i.isspace():
                count_space_Username += 1
                                
        if len(Username) == count_alpha_Username + count_space_Username and count_alpha_Username >= 2 :
            return Username
        else :
            print("INVALID INPUT","\n","\n")
            continue



#CREATE/CHECK VALID PASSWORD
def CVP(Choice_P):
    while True:
        if Choice_P == 1:
            print("Enter your PASSWORD with the GIVEN INSTRUCTIONS :","\n")
            print("PASSWORD must contain AT LEAST 5 ALPHABETS")
            print("PASSWORD must contain AT LEAST 2 DIGITS ")
            print("PASSWORD must contain AT LEAST 1 SPECIAL CHARACTER")
            print("PASSWORD SHOULD NOT CONTAIN ANY SPACES")
            print("LENGTH of the PASSWORD MUST BE AT LEAST 8 CHARACTERS and LESS THAN 30 CHARACTERS LONG","\n")
            Password = input("Enter LOGIN PASSWORD : ")
            print()
        elif Choice_P in [2,3,4]:
            Password = input("Enter LOGIN PASSWORD : ")
            print()
        
        if 30 >= len(Password) >= 8:
            count_alpha = 0
            count_digit = 0
            count_special = 0
            count_space = 0
        
            for i in Password:
                if i.isalpha():
                    count_alpha += 1
                elif i.isdigit():
                    count_digit += 1
                elif i.isspace():
                    count_space += 1
                else :
                    count_special += 1
                                
            if count_alpha >= 5 and count_digit >= 2 and count_special >= 1 and count_space == 0:
                break
            else:
                print("INVALID PASSWORD","\n")
                             
        else:
            if len(Password) < 8:
                print("LENGTH of GIVEN PASSWORD is SHORTER than 8 CHARACTERS","\n")
                continue
            elif len(Password) > 30:
                print("LENGTH of GIVEN PASSWORD is LONGER than 30 CHARACTERS","\n")
                continue
                        
    while True:
        PC = input("Enter the PASSWORD AGAIN for CONFIRMATION : ")
        print()
                            
        if Password == PC:
             return Password
        else :
            print("Please enter the NEW PASSWORD CORRECTLY","\n")
            continue



#CREATE/CHECK VALID ID
def CVID(Choice_ID):
    
    if Choice_ID == 1:
        while True:
            ID = random.randint(10000000, 20000000)
            Login_Dict = {"1":"CUSTOMERS", "2":"STAFFS", "3":"ADMINS", "4":"CEO"}
            Table = Login_Dict[Login_var]
            try:
                DB = m.connect(
                    host="localhost",
                    user="root",
                    password="sunil09",
                    database="ss_jewellery"
                )
                DB_cursor = DB.cursor()
                Query = ("SELECT ID FROM %s" % Table)
                DB_cursor.execute(Query)
                ID_Data = DB_cursor.fetchall()
                
            except m.Error as error1:
                print("Database error occurred:", error1, "\n")
                EOC()
            except Exception as error2:
                print("Unexpected error:", error2, "\n")
                EOC()
            
            else :
                ID_found = 0
                for Existing_ID in ID_Data :
                    if Existing_ID[0] == ID:
                        ID_found +=1
                        break
            
            finally :
                if 'DB_cursor' in locals():
                    DB_cursor.close()
                if 'DB' in locals() and DB is not None:
                    DB.close()
            
            if ID_found == 1:
                print("\n","ID ALREADY EXISTS","\n","RETRYING FOR ANOTHER ID","\n")
                continue
                
            else :
                print("Your ID is :",ID)
                return ID
    
    elif Choice_ID in [2,3,4]:
        while True :
            try :
                ID = int(input("Enter the ID for VALIDIFICATION : "))
            except :
                print("INVALID ID","\n")
            else :
                if len(str(ID)) == 8 and str(ID)[0] == "1":
                    print("\n","The given ID has VALID FORMAT","\n")
                    return ID



def VIEW_ALL_CLIENTS(View_Choice, Client_ID):
    while True:
        try:
            DB = m.connect(
                host="localhost",
                user="root",
                password="sunil09",
                database="ss_jewellery"
            )
            DB_cursor = DB.cursor()
            
            View_Dict = {1:"CUSTOMERS", 2:"STAFFS", 3:"ADMINS"}
            Table = View_Dict[View_Choice]
            Query = ("SELECT * FROM %s " % Table)
            DB_cursor.execute(Query)
            All_Data = DB_cursor.fetchall()
            print("="*80,"\n")
            for Records in All_Data:
                for Value in Records:
                    print(Value, end = " | ")
                print()
            print("="*80,"\n")
        
        except m.Error as error1:
            print("Database error occurred:", error1, "\n")
            Client_EOC(Client_ID)
            
        except Exception as error2:
            print("Unexpected error:", error2, "\n")
            Client_EOC(Client_ID)
        
        else:
            break
            
        finally :
            if 'DB_cursor' in locals():
                DB_cursor.close()
            if 'DB' in locals() and DB is not None:
                DB.close()





#LOGOUT FUNCTION
def LOGOUT(Client_ID):
    DB = m.connect(
        host="localhost",
        user="root",
        password="sunil09",
        database="ss_jewellery"
    )
    DB_cursor = DB.cursor()
    
    if Login_var == '1':
        Logout_query = "UPDATE CUSTOMER_LOGIN_HISTORY SET Logout_Time = now() WHERE ID = %s"
    elif Login_var == '2':
        Logout_query = "UPDATE STAFF_LOGIN_HISTORY SET Logout_Time = now() WHERE ID = %s"
    elif Login_var == '3':
        Logout_query = "UPDATE ADMIN_LOGIN_HISTORY SET Logout_Time = now() WHERE ID = %s"
    elif Login_var == '4':
        Logout_query = "UPDATE CEO_LOGIN_HISTORY SET Logout_Time = now() WHERE ID = %s"
    else:
        print("Unexpected Outcome")
    
    DB_cursor.execute(Logout_query , (Client_ID,))
    DB.commit()
    DB_cursor.close()
    DB.close()



#EXIT OR CONTINUE
def EOC():
    while True:
        exit_var = input("Enter 0 to EXIT THE PORTAL        OR        Enter 1 to CONTINUE : ")
        print()
        if exit_var in ['0','1']:
            if exit_var == '1':
                break
            else :
                sys.exit("THANKS FOR VISITING")
        else :
            print("INVALID INPUT","\n")



#EOC FOR LOGGID IN CLIENT
def Client_EOC(Client_ID):
    while True:
        Client_exit_var = input("Enter 0 to EXIT THE PORTAL        OR        Enter 1 to CONTINUE : ")
        print()
        if Client_exit_var in ['0','1']:
            if Client_exit_var == '1':
                break
            else :
                LOGOUT(Client_ID)
                sys.exit("You have successfully LOGGED OUT\nTHANKS FOR VISITING")
        else :
            print("INVALID INPUT","\n")





#VIEWING FUNCTIONS FOR CUSTOMER
def VIEW_Jewellery(Customer_ID):
    while True:
        print("What TYPE of JEWELLERY are you looking for :", "\n")
        print("Enter -1 to GO BACK ")
        print("Enter 0 to LOGOUT and exit the PORTAL")
        print("Enter 1 to look fo RINGS")
        print("Enter 2 to look for PENDANTS")
        print("Enter 3 to look for CHAINS")
        print("Enter 4 to look for NECKLACES")
        print("Enter 5 to look for BRACELETS")
        print("Enter 6 to look for EARINGS","\n")
        
        View_var = input("Enter your choice here : ")
        print("")
        
        if View_var in ['-1','0','1','2','3','4','5','6']:
            
            if View_var == "-1":
                print("You have successfully RETURNED to CUSTOMER OPTIONS INTERFACE","\n","\n","\n")
                Materials = 0
                break
            
            elif View_var == "0":
                LOGOUT(Customer_ID)
                sys.exit("You have successfully LOGGED OUT\n\nTHANKS FOR VISITING")
            
            else :
                View_Dict = {"1":"RINGS" , "2":"PENDANTS" , "3":"CHAINS" , "4":"NECKLACES" , "5":"BRACELETS" , "6":"EARINGS"}
                Materials = Material(Customer_ID)
                View_var_table = View_Dict[View_var]

                if Materials == 0:
                    continue
                
                elif len(Materials) == 1 :
                    Material_var = Materials[0]
                    View_Query = "SELECT * FROM JEWELLERIES WHERE TYPE = %s AND MATERIAL IN (%s)"
                    Data = Jewellery_View(Materials, View_Query, View_var_table, Material_var)
                        
                else :
                    Material_var = str(Materials)
                    View_Query = "SELECT * FROM JEWELLERIES WHERE TYPE = %s " + ("AND MATERIAL IN %s" % Material_var)
                    Data = Jewellery_View(Materials, View_Query, View_var_table, Material_var)
        
        else :
            print("INVALID INPUT","\n")
            continue


    if View_var == "-1":
        pass
    
    elif View_var in ['1','2','3','4','5','6'] and Materials != 0:
        while True:
            print("What would you like to do now ?")
            print("Enter -1 to GO BACK ")
            print("Enter 0 to LOGOUT and exit the PORTAL")
            print("Enter 1 to BOOK VIA CODE")
            print("Enter 2 to SORT and VIEW","\n")
            
            View2_var = input("Enter your choice here : ")
            if View2_var in ['-1','0','1','2']:
                
                if View2_var == "-1":
                    print("You have successfully RETURNED to CUSTOMER OPTIONS INTERFACE","\n","\n","\n")
                    break
                
                elif View2_var == "0":
                    LOGOUT(Customer_ID)
                    sys.exit("You have successfully LOGGED OUT\n\nTHANKS FOR VISITING")
                
                elif View2_var == "1":
                    BOOK(Customer_ID, Data)
                
                elif View2_var == "2":
                    while True:
                        print("Select your SORT TYPE :")
                        print("Enter 1 to SORT BY PRICE INCREASING")
                        print("Enter 2 to SORT BY PRICE DECREASING")
                        
                        Sort_var = input("Enter your choice here : ")
                        if Sort_var in ['1','2']:
                            Sort_Dict = {"1":" ORDER BY PRICE", "2":" ORDER BY PRICE DESC"}
                            Sort_Query = View_Query + Sort_Dict[Sort_var]
                            Data = Jewellery_View(Materials, Sort_Query, View_var_table, Material_var)
    
                        else :
                            print("INVALID INPUT","\n")
                            continue

            else :
                print("INVALID INPUT","\n")
                continue




def Material(Customer_ID):
    while True:
        print("Select number of Materials :")
        print("Enter -1 to GO BACK ")
        print("Enter 0 to LOGOUT and exit the PORTAL")
        print("Enter 1 for Viewing Items of ALL MATERIALS")
        print("Enter 2 for Viewing Item for an INDIVIDUAL MATERIAL")
        print("Enter 3 for Viewing Items of Multiple MATERIALS")
        
        Material_Nos = input("Enter your choice here : ")
        if Material_Nos in ['-1','0','1','2','3']:
            
            if Material_Nos == "-1":
                print("You have successfully RETURNED to JEWELLERY OPTIONS INTERFACE\n\n\n")
                return 0
            
            elif Material_Nos == "0":
                LOGOUT(Customer_ID)
                sys.exit("You have successfully LOGGED OUT\n\nTHANKS FOR VISITING")
            
            elif Material_Nos == "1":
                return ("Gold","Diamond","Silver","Emerald","Ruby","Blue Sapphire","Yellow Sapphire","Pink Sapphire","White Sapphire")
            
            else :
                while True:
                    print("Select from given MATERIAL TYPES :","\n")
                    print("Enter -1 to GO BACK ")
                    print("Enter 0 to LOGOUT and exit the PORTAL")
                    print("Enter 1 for Gold:")
                    print("Enter 2 for Diamond")
                    print("Enter 3 for Silver")
                    print("Enter 4 for Emerald")
                    print("Enter 5 for Ruby")
                    print("Enter 6 for Blue Sapphire")
                    print("Enter 7 for Yellow Sapphire")
                    print("Enter 8 for Pink Sapphire")
                    print("Enter 9 for White Sapphire","\n")
                    print("                        If you want to VIEW items for INDIVIDUAL MATERIAL then JUST ENTER THEIR RESPECTIVE NUMBER")
                    print("                                                                                            OR")
                    print("If you want to VIEW items for MULTIPLE MATERIALS then ENTER THEIR RESPECTIVE NUMBERS IN THE FOLLWING MANNER :- a b c","\n")
                    Material_input = input("Enter your Decision : ")
                    Material_Dict = {"1":"Gold" , "2":"Diamond" , "3":"Silver" , "4":"Emerald" , "5":"Ruby" , "6":"Blue Sapphire" , "7":"Yellow Sapphire" , "8":"Pink Sapphire" , "9":"White Sapphire"}
                    
                    if Material_Nos == "2":
                        if Material_input in ['-1','0','1','2','3','4','5','6','7','8','9']:
                            
                            if Material_input == "-1":
                                print("You have successfully RETURNED to SORT OUT OPTIONS INTERFACE","\n","\n","\n")
                                break
                                    
                            elif Material_input == "0":
                                LOGOUT(Customer_ID)
                                sys.exit("You have successfully LOGGED OUT\n\nTHANKS FOR VISITING")
                            
                            else :
                                return (Material_Dict[Material_input],)
                            
                        else :
                            print("INVALID INPUT","\n")
                            continue
                            
                    elif Material_Nos == "3":
                        
                        if Material_input == "-1":
                            print("You have successfully RETURNED to SORT OUT OPTIONS INTERFACE","\n","\n","\n")
                            break
                                
                        elif Material_input == "0":
                            LOGOUT(Customer_ID)
                            sys.exit("You have successfully LOGGED OUT\n\nTHANKS FOR VISITING")
                        
                        else:
                            Nos_split = Material_input.split()
                            Nos_Length = 0
                            Nos_List = []
                            for i in Nos_split:
                                if i in ['1','2','3','4','5','6','7','8','9'] and Nos_split.count(i) == 1 :
                                    Nos_Length += 1
                                    Nos_List.append(Material_Dict[i])
                            if len(Nos_split) == Nos_Length:
                                return tuple(Nos_List)
                            else :
                                print("INVALID INPUT","\n")
                                continue
                        
        else :
            print("INVALID INPUT","\n")
            continue



def Jewellery_View(Materials, View_Query, View_var_table, Material_var):
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
                    
        if len(Materials) == 1 :
            DB_cursor.execute(View_Query, (View_var_table, Material_var))
            Data = DB_cursor.fetchall()
            print("BOOKING CODE | JEWELLERY TYPE | MATERIAL | WEIGHT |  PRICE  |     DESCRIPTION     ")
            for record in Data :
                print("|   ", record[0], "   |   ", record[1], "   | ", record[2], " | ", record[3], " |", record[4], "| ", record[5], "|")
            print("\n", "ADDITIONAL CHARGES ARE NOT INCLUDED", "\n")
            return Data

        else :
            DB_cursor.execute(View_Query, (View_var_table,))
            Data = DB_cursor.fetchall()
            print("BOOKING CODE | JEWELLERY TYPE | MATERIAL | WEIGHT |     PRICE     |     DESCRIPTION     ")
            for record in Data :
                print("|   ", record[0], "   |   ", record[1], "   | ", record[2], " | ", record[3], " |", record[4], "| ", record[5], "|")
            print("\n", "ADDITIONAL CHARGES ARE NOT INCLUDED", "\n")
            return Data

    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
                
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def BOOK(Customer_ID, Data):
    while True :
        try :
            Book_Code = int(input("Enter the BOOKING CODE to BOOK THE RESPECTIVE JEWELLERY : "))
        except :
            print("INVALID CODE","\n")
        else :
            if len(str(Book_Code)) == 4:
                found = 0
                
                for J_Code in Data:
                    if J_Code[0]==Book_Code:
                        found +=1
                        Record = J_Code
                        break
                
                if found == 1 :
                    while True :
                        print("NOW CONFIRM YOUR BOOKING BY TYPING 'YES'")
                        print("                                OR")
                        print("   CANCEL THE BOOKING BY TYPING 'NO'","\n")
                        YN_var = input("TYPE HERE : ")
                        
                        if YN_var in ["YES","NO"] :
                            if YN_var == "YES":
                                print("\n", "Please provide th following information CORRECTLY in order to continue your BOOKING","\n")
                                
                                while True :
                                    
                                    try :
                                        Ph_no = int(input("Please provide us YOUR 10 digit phone / mobile number : "))
                                    except :
                                        print("INVALID INPUT","\n")
                                    else :
                                        if len(str(Ph_no)) == 10 :
                                            if str(Ph_no)[0] in ['6','7','8','9']:
                                                print(Ph_no)
                                                break
                                            else :
                                                print("INVALID PHONE NO.", "\n")
                                                continue
                                        else :
                                            print("INVALID PHONE NO.","\n")
                                            continue
                                
                                while True :
                                    Address = input("Also provide us  YOUR ADDRESS in the FOLLOWING MANNER :- SECTOR/AREA, CITY/TOWN/VILLAGE , DISTRICT , STATE :")
                                    if len(Address) >= 20 :
                                        print(Address)
                                        break
                                    else :
                                        print("INVALID INPUT","\n")
                                                                
                                try:
                                    DB = m.connect(
                                        host="localhost",
                                        user="root",
                                        password="sunil09",
                                        database="ss_jewellery"
                                    )
                                    DB_cursor = DB.cursor()
                                   
                                    Query = "INSERT INTO BOOKINGS VALUES (%s,%s,%s,%s,now())"
                                    DB_cursor.execute(Query, (Customer_ID, Book_Code, Ph_no, Address))
                                    DB.commit()
                                    
                                    
                                    J_details = Record[2] + " " + Record[1]
                                    Weight = Record[3]
                                    Rate = round(Record[4]/Record[3], 2)
                                    Amount = Record[4]
                                    Making_Charges = round(Record[4]*0.2, 2)
                                    CGST = round(Record[4]*0.015, 2)
                                    SGST = round(Record[4]*0.015, 2)
                                    Total_Amount = Amount + Making_Charges + CGST + SGST
                                    Bill = ("=============================================\nCUSTOMER ID :-               %s\nJEWELLERY DESCRIPTION :-     %s\nGROSS WEIGHT :-              %s grams\nRATE PER GRAM :-             %s Rs/g\nAMOUNT :-                    %s\nMAKING CHARGES :-            %s\nCGST 1.5%% :-                %s\nSGST 1.5%% :-                %s\nTOTAL AMOUNT :-              %s\n=============================================" % (Customer_ID, J_details, Weight, Rate, Amount, Making_Charges, CGST, SGST, Total_Amount))
                                    
                                    
                                    Table = "CHAT" + Customer_ID
                                    DB_cursor.execute("SHOW TABLES")
                                    Tables = DB_cursor.fetchall()
                                    
                                    if (Table,) in Tables:
                                        query = ("INSERT INTO %s VALUES" % Table) + "(%s)"
                                        DB_cursor.execute(query, (Bill,))
                                        DB.commit()
                                    
                                    else :
                                        query1 = ("CREATE TABLE %s(CHATS TEXT)" % Table)
                                        DB_cursor.execute(query1)
                                        DB.commit()
                                        query2 = ("INSERT INTO %s VALUES" % Table) + "(%s)"
                                        DB_cursor.execute(query2, (Bill,))
                                        DB.commit()
                                
                                    
                                except m.Error as error1:
                                    print("Database error occurred:", error1, "\n")
                                except Exception as error2:
                                    print("Unexpected error:", error2, "\n")
                                
                                else :
                                    print("\n","YOU HAVE SUCCESSFULLY BOOKED THE JEWELLERY")
                                    print("CHECK OUT YOUR CHATBOX TO SEE YOUR INITIAL BILL")
                                    print("YOUR BOOKING WILL BE CONFIRMED WITHIN THE NEXT 24 HOURS VIA CALL","\n")
                                    break
                                
                                finally :
                                    if 'DB_cursor' in locals():
                                        DB_cursor.close()
                                    if 'DB' in locals() and DB is not None:
                                        DB.close()
                                
                            
                            else:
                                print("THE BOOKING HAS SUCCESSFULLY CANCELLED","\n")
                                break
                            
                        else :
                            print("INVALID STATEMENT","\n")     

                else :
                    print("Given Code could not be FOUND or INCORRECT code is given","\n")
                    continue
                
                break
            else :
                print("INVALID CODE","\n")
                continue



def CHATBOX(Customer_Name, Customer_ID):
    while True :
        print("What would you like to do ?")
        print("Enter -1 to GO BACK ")
        print("Enter 0 to LOGOUT and exit the PORTAL")
        print("Enter 1 to SEE All YOUR CHATS AT ONCE")
        print("Enter 2 to RAISE A REQUEST IN THE 'HELP BOX'")
        
        Chat_var = input("Enter your choice here : ")
        print("")
        if Chat_var in ['-1','0','1','2']:
            
            if Chat_var == "-1":
                print("You have successfully RETURNED to CUSTOMER OPTIONS INTERFACE","\n","\n","\n")
                break
            
            elif Chat_var == "0":
                LOGOUT(Customer_ID)
                sys.exit("You have successfully LOGGED OUT\n\nTHANKS FOR VISITING")
            
            elif Chat_var =="1" :
                print("Here is all of your CHATS with our AGENT :")
                
                try:
                    DB = m.connect(
                        host="localhost",
                        user="root",
                        password="sunil09",
                        database="ss_jewellery"
                    )
                    DB_cursor = DB.cursor()
                        
                    Table = "CHAT" + Customer_ID
                    DB_cursor.execute("SHOW TABLES")
                    Tables = DB_cursor.fetchall()
                    
                    if (Table,) not in Tables:
                        Query1 = ("CREATE TABLE %s" % Table) + "(CHATS TEXT)"
                        DB_cursor.execute(Query1)
                        DB.commit()
                    else: 
                        Query = ("SELECT * FROM %s" % Table)
                        DB_cursor.execute(Query)
                        Chat_Data = DB_cursor.fetchall()
                        print("==================================================","\n","\n")
                        for chat_record in Chat_Data :
                            print(chat_record[0], "==================================================","\n","\n")
                        
                except m.Error as error1:
                    print("Database error occurred:", error1, "\n")
                    Client_EOC(Customer_ID)
                
                except Exception as error2:
                    print("Unexpected error:", error2, "\n")
                    Client_EOC(Customer_ID)
                                
                finally :
                    if 'DB_cursor' in locals():
                        DB_cursor.close()
                    if 'DB' in locals() and DB is not None:
                        DB.close()
            
            elif Chat_var =="2" :
                W_HelpBox(Customer_Name, Customer_ID)
        
        else :
            print("INVALID INPUT","\n")



#WRITE A REQUEST IN HELP BOX (FOR CUSTOMER)
def W_HelpBox(Customer_Name, Customer_ID):
    while True:
        Help_comment = input("Enter your REQUEST within 500 letters : ")
        if len(Help_comment) == 0:
            print("WHY ENTER WITHOUT TYPING ANYTHING ?","\n")
        elif 0 < len(Help_comment) <= 500:
            break
        else:
            print("REQUEST IS TOO LONG","\n")
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
        
        Table = "CHAT" + Customer_ID
        DB_cursor.execute("SHOW TABLES")
        Tables = DB_cursor.fetchall()
        
        if (Table,) not in Tables:
            Query = ("CREATE TABLE %s" % Table) + "(CHATS TEXT)"
            DB_cursor.execute(Query)
            DB.commit()
        
        Query1 = ("INSERT INTO %s" % Table) + " VALUES (%s)"
        DB_cursor.execute(Query1, (Help_comment,))
        DB.commit()
        Query2 = "INSERT INTO HELP_BOX VALUES (%s, %s, %s, now())"
        DB_cursor.execute(Query2, (Customer_Name, Customer_ID, Help_comment))
        DB.commit()
        print("\n","THE REPLY OF YOUR REQUEST WILL BE SENT TO YOUR CHATBOX WITHIN 7 BUISNESS DAYS","THANKS FOR REACHING OUT","\n")
        
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
        
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()





def Jewellery_Type():
    while True:
        print("What is the TYPE of JEWELLERY :", "\n")
        print("Enter 1 fo RINGS")
        print("Enter 2 for PENDANTS")
        print("Enter 3 for CHAINS")
        print("Enter 4 for NECKLACES")
        print("Enter 5 for BRACELETS")
        print("Enter 6 for EARINGS","\n")
        
        J_Type = input("Enter your choice here : ")
        print("")
        
        if J_Type in ['1','2','3','4','5','6']:
            J_Dict = {"1":"RINGS" , "2":"PENDANTS" , "3":"CHAINS" , "4":"NECKLACES" , "5":"BRACELETS" , "6":"EARINGS"}
            return J_Dict[J_Type]
       
        else :
            print("\n","INVALID INPUT","\n")
            continue



def Material_Type():
    while True:
        print("Select from given MATERIAL TYPES :","\n")
        print("Enter 1 for Gold:")
        print("Enter 2 for Diamond")
        print("Enter 3 for Silver")
        print("Enter 4 for Emerald")
        print("Enter 5 for Ruby")
        print("Enter 6 for Blue Sapphire")
        print("Enter 7 for Yellow Sapphire")
        print("Enter 8 for Pink Sapphire")
        print("Enter 9 for White Sapphire","\n")
        
        M_Type = input("Enter your choice here : ")
        if M_Type in ['1','2','3','4','5','6','7','8','9']:
            M_Dict = {"1":"Gold" , "2":"Diamond" , "3":"Silver" , "4":"Emerald" , "5":"Ruby" , "6":"Blue Sapphire" , "7":"Yellow Sapphire" , "8":"Pink Sapphire" , "9":"White Sapphire"}
            return M_Dict[M_Type]
       
        else :
            print("\n","INVALID INPUT","\n")
            continue



def Jewellery_Weight():
    while True:
        try:
            J_Weight = round(float(input("Enter WEIGHT of the Jewellery : ")),2)
        except:
            print("\n","INVALID INPUT","\n")
        else:
            if 1000 >= J_Weight >= 0.5 :
                return J_Weight
            else:
                print("\n","INVALID INPUT","\n")



def Jewellery_Price():
    while True:
        try:
            J_Price = round(float(input("Enter PRICE of the Jewellery : ")),2)
        except:
            print("\n","INVALID INPUT","\n")
        else:
            if 10000000 >= J_Price >= 500 :
                return J_Price
            else:
                print("\n","INVALID INPUT","\n")



def Jewellery_Details():
    while True:
        J_Details = input("Enter your DETAILS within 100 letters : ")
        if len(J_Details) == 0:
            print("WHY ENTER WITHOUT TYPING ANYTHING ?","\n")
        elif 8 < len(J_Details) <= 100:
            return J_Details
        elif len(J_Details) < 8:
            print("DETAILS ARE TOO SHORT","\n")
        elif len(J_Details) > 100:
            print("DETAILS ARE TOO LONG","\n")



def Add_Jewellery():
    print("Provide the details asked to ADD NEW JEWELLERY ITEM")
    
    J_Type = Jewellery_Type()
    M_Type = Material_Type()
    J_Weight = Jewellery_Weight()
    J_Price = Jewellery_Price()
    J_Details = Jewellery_Details()
    
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
            
        Query1 = "SELECT ID FROM JEWELLERIES"
        DB_cursor.execute(Query1)
        Data = DB_cursor.fetchall()
            
        List_J_ID = []
        for Records in Data:
            List_J_ID.append(Records[0])
        while True:
            J_ID = random.randint(1000, 9999)
            if J_ID in List_J_ID:
                continue
            else:
                break
            
        J_Data = (J_ID, J_Type, M_Type, J_Weight, J_Price, J_Details)
        Query2 = "INSERT INTO JEWELLERIES VALUES (%s, %s, %s, %s, %s, %s)"
        DB_cursor.execute(Query2, J_Data)
        DB.commit()
        print("\n","YOU ADDED THE JEWELLERY SUCCESSFULLY","\n")
            
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
            
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def VIEW_ALL_JEWELLERIES():
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
        Query = "SELECT * FROM JEWELLERIES ORDER BY TYPE"
        DB_cursor.execute(Query)
        Data = DB_cursor.fetchall()
        print("="*80,"\n")
        print("BOOKING CODE | JEWELLERY TYPE | MATERIAL | WEIGHT |  PRICE  |     DESCRIPTION     ")
        for record in Data :
            print("|   ", record[0], "   |   ", record[1], "   | ", record[2], " | ", record[3], " |", record[4], "| ", record[5], "|")
        print("="*80,"\n")
        
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
            
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def Remove_Jewellery():
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
        
        
        Query1 = "SELECT ID FROM JEWELLERIES"
        DB_cursor.execute(Query1)
        Data = DB_cursor.fetchall()
            
        List_J_ID = []
        for Records in Data:
            List_J_ID.append(str(Records[0]))
        while True:
            J_ID = input("Enter the JEWELLERY ID : ")
            if J_ID in List_J_ID:
                print("ID FOUND","\n")
                break
            else:
                print("IINVALID ID or ID NOT FOUND","\n")
                continue
                
        Query2 = "DELETE FROM JEWELLERIES WHERE ID = %s"
        DB_cursor.execute(Query2, (int(J_ID,)))
        DB.commit()
        print("\n","YOUR HAVE REMOVED THE JEWELLEY  SUCCESSFULLY","\n")
        
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
        
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def Update_Jewellery(Staff_ID):
                    
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
            
        Query1 = "SELECT ID FROM JEWELLERIES"
        DB_cursor.execute(Query1)
        Data = DB_cursor.fetchall()
            
        List_J_ID = []
        for Records in Data:
            List_J_ID.append(str(Records[0]))
        while True:
            J_ID = input("Enter the JEWELLERY ID : ")
            if J_ID in List_J_ID:
                print("ID FOUND","\n")
                break
            else:
                print("IINVALID ID or ID NOT FOUND","\n")
                continue
        
        while True :
            print("What would you like to UPDATE?")
            print("Enter -1 to STOP Updating")
            print("Enter 1 for Jewellery Type")
            print("Enter 2 for Material Type")
            print("Enter 3 for Weight of the Jewellery")
            print("Enter 4 for Price of the Jewellery")
            print("Enter 5 for Details of the Jewellery","\n")
            
            Update_J_var = input("Enter your choice here : ")
            if Update_J_var in ['-1','1','2','3','4','5']:
                
                if Update_J_var == "-1":
                    break
                
                elif Update_J_var == "1":
                    Column = "Type"
                    Value = Jewellery_Type()
                    
                elif Update_J_var == "2":
                    Column = "Material"
                    Value = Material_Type()
                    
                elif Update_J_var == "3":
                    Column = "Weight"
                    Value = Jewellery_Weight()
                    
                elif Update_J_var == "4":
                    Column = "Price"
                    Value = Jewellery_Price()
                    
                elif Update_J_var == "5":
                    Column = "Details"
                    Value = Jewellery_Details()
                    
                Query = ("UPDATE JEWELLERIES SET %s " % Column) + "= %s WHERE ID = %s"
                DB_cursor.execute(Query, (Value, int(J_ID)))
                DB.commit()
                print("\n","YOU HAVE UPDATED THE JEWELLERY SUCCESSFULLY","\n")
            
            else:
                print("\n","INVALID INPUT","\n")
                continue
            
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
        Client_EOC(Staff_ID)
        
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
        Client_EOC(Staff_ID)
            
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def VIEW_ALL_REQUESTS():
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
        Query = "SELECT * FROM HELP_BOX"
        DB_cursor.execute(Query)
        Data = DB_cursor.fetchall()
        print("Customer_Name    |    Customer_ID    |    Help_comment","\n")
        for record in Data :
            print("|  ", record[0], " |  ", record[1], "  | ", record[2], "  |")
        print()
        
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
            
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def Staff_ReplyBox():
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
        
        Query1 = "SELECT ID FROM HELP_BOX"
        DB_cursor.execute(Query1)
        C_ID = DB_cursor.fetchall()
        
        while True:
            print("Enter Customer ID for Replying to a Request")
            Customer_ID = CVID(2)
            if (Customer_ID,) in C_ID:
                break
            else:
                print("\n","ID NOT FOUND","\n")
                continue
        
        while True:
            Reply_comment = input("Enter your REPLY within 500 letters : ")
            if len(Reply_comment) == 0:
                print("WHY ENTER WITHOUT TYPING ANYTHING ?","\n")
            elif 0 < len(Reply_comment) <= 500:
                break
            else:
                print("REPLY IS TOO LONG","\n")
                
        Reply_comment = "AGENT :\n" + Reply_comment
        Table = "CHAT" + Customer_ID
        Query2 = ("INSERT INTO %s" % Table) + " VALUES (%s)"
        DB_cursor.execute(Query2, (Reply_comment,))
        DB.commit()
        print("\n","YOU HAVE REPLIED SUCCESSFULLY","\n")
        
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
        
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def Staff_Delete_Requests():
    try:
        DB = m.connect(
            host="localhost",
            user="root",
            password="sunil09",
            database="ss_jewellery"
        )
        DB_cursor = DB.cursor()
        
        Query1 = "SELECT ID FROM CUSTOMERS"
        DB_cursor.execute(Query1)
        C_ID = DB_cursor.fetchall()
        
        while True:
            print("Enter Customer ID to Delete COMPLETED REQUESTS")
            Customer_ID = CVID(2)
            if (Customer_ID,) in C_ID:
                break
            else:
                print("\n","ID NOT FOUND","\n")
                continue
                
        Query = "DELETE FROM HELP_BOX WHERE CUSTOMER_ID = %s"
        DB_cursor.execute(Query, (Customer_ID,))
        DB.commit()
        print("\n","YOUR HAVE REMOVED THE REQUEST SUCCESSFULLY","\n")
        
    except m.Error as error1:
        print("Database error occurred:", error1, "\n")
    except Exception as error2:
        print("Unexpected error:", error2, "\n")
        
    finally :
        if 'DB_cursor' in locals():
            DB_cursor.close()
        if 'DB' in locals() and DB is not None:
            DB.close()



def Staff_CHATBOX():
    while True:
        print("What would you like to do :")
        print("Enter -1 to GO BACK")
        print("Enter 1 for VIEWING ALL REQUESTS")
        print("Enter 2 for REPLYING TO CUSTOMERS")
        print("Enter 3 for MARKING REQUEST COMPLETION","\n")
        SC_var = input("Enter your choice here : ")
        
        if SC_var in ['-1','1','2','3']:
            if SC_var == "-1":
                break
            elif SC_var == "1":
                VIEW_ALL_REQUESTS()
            elif SC_var == "2":
                Staff_ReplyBox()
            elif SC_var == "3":
                Staff_Delete_Requests()
        
        else:
            print("\n","INVALID INPUT","\n")
            continue





def SSJ():
    global Login_var
    print("WELCOME TO SS JEWELLERY PORTAL","\n","\n","\n")
    while True:
        print("Who do you want to LOGIN AS","\n")
        
        print("Enter 0 to EXIT the PORTAL")
        print("Enter 1 for CUSTOMER")
        print("Enter 2 for STAFF")
        print("Enter 3 for ADMIN")
        print("Enter 4 for CEO","\n")
        
        Login_var = input("Enter your preference : ")
        print("\n","\n")
        
        if Login_var in ['0','1','2','3','4']:
            
            
            if Login_var == "0":
                sys.exit("THANKS FOR VISITING")
            
            elif Login_var == "1":
                while True:
                    print("What do you prefer : ","\n")
                    
                    print("Enter -1 to GO BACK to MAIN LOGIN INTERFACE")
                    print("Enter 0 to EXIT the PORTAL")
                    print("Enter 1 to LOGIN")
                    print("Enter 2 for REGISTRATION","\n")
                    
                    Customer_var = input("Enter your preference : ")
                    print("\n","\n")
                    
                    
                    if Customer_var  in ['-1','0','1','2'] :
                        
                        
                        if Customer_var == '-1':
                            print("You have successfully RETURNED to MAIN LOGIN INTERFACE","\n","\n","\n")
                            break
                        
                        
                        elif Customer_var == "0":
                            sys.exit("THANKS FOR VISITING")
                        
                        
                        elif Customer_var == "1":
                            Customer_Data = Accounts(2)
                            Customer_Name = Customer_Data[0]
                            Customer_ID = Customer_Data[1]
                            Customer_Password = Customer_Data[2]
                            
                            print("Welcome back ",Customer_Name,"\n")
                            while True:
                                print("So what would you like to do :", "\n")
                                print("Enter -1 to LOG OUT and GO BACK to CUSTOMER LOGIN INTERFACE")
                                print("Enter 0 to LOGOUT and exit the PORTAL")
                                print("Enter 1 to VIEW  and BOOK for Jewellery")
                                print("Enter 2 for writing a REQUEST in HELP BOX","\n")
                                
                                
                                OC_var = input("Enter your preference : ")
                                print("")
                                if OC_var in ['-1','0','1','2']:
                                    
                                    
                                    if OC_var == "-1":
                                        LOGOUT(Customer_ID)
                                        print("You have successfully LOGGED OUT and RETURNED to CUSTOMER LOGIN INTERFACE","\n","\n","\n")
                                        break
                                    
                                    
                                    elif OC_var == "0":
                                        LOGOUT(Customer_ID)
                                        sys.exit("You have successfully LOGGED OUT \n\nTHANKS FOR VISITING")
                                    
                                    
                                    elif OC_var == "1":
                                        Client_EOC(Customer_ID)
                                        VIEW_Jewellery(Customer_ID)
                                    
        
                                    elif OC_var == "2":
                                        Client_EOC(Customer_ID)
                                        CHATBOX(Customer_Name, Customer_ID)
                                        
                                else :
                                    print("INVALID INPUT","\n")
                            
                            
                        elif Customer_var == "2":
                            EOC()
                            print("Please provide the following necessary details for REGISTRATION : ","\n")
                            
                            Accounts(1)
                            print("\n","YOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY")
                            print("Now Please Login to your Account","\n")
                            Customer_Data = Accounts(2)
                            Customer_Name = Customer_Data[0]
                            Customer_ID = Customer_Data[1]
                            Customer_Password = Customer_Data[2]
                                                    
                            print("Welcome ",Customer_Name,"\n")
                            print("So what would you like to do :", "\n")
                            print("Enter -1 to LOG OUT and GO BACK to CUSTOMER LOGIN INTERFACE")
                            print("Enter 0 to LOGOUT and exit the PORTAL")
                            print("Enter 1 to VIEW  and BOOK for Jewellery")
                            print("Enter 2 for writing a REQUEST in HELP BOX","\n")
                            
                            
                            NC_var = input("Enter your preference : ")
                            print()
                            if NC_var in ['-1','0','1','2']:
                                
                                
                                if NC_var == "-1":
                                    LOGOUT(Customer_ID)
                                    print("You have successfully LOGGED OUT and RETURNED to CUSTOMER LOGIN INTERFACE","\n","\n","\n")
                                    break
                                
                                
                                elif NC_var == "0":
                                    LOGOUT(Customer_ID)
                                    sys.exit("You have successfully LOGGED OUT \n\nTHANKS FOR VISITING")
                                
                                
                                elif NC_var == "1":
                                    Client_EOC(Customer_ID)
                                    VIEW_Jewellery(Customer_ID)
                                
                                
                                elif NC_var == "2":
                                    Client_EOC(Customer_ID)
                                    CHATBOX(Customer_Name, Customer_ID)
                    
                    
                    else :
                        print("INVALID INPUT","\n")
            
            
            
            elif Login_var == "2":
                EOC()
                Staff_Data = Accounts(2)
                Staff_Name = Staff_Data[0]
                Staff_ID = Staff_Data[1]
                Staff_Password = Staff_Data[2]
    
                while True:
    
                    print("So what would you like to do :", "\n")
                    print("Enter -1 to LOGOUT and GO BACK to MAIN LOGIN INTERFACE")
                    print("Enter 0 to LOGOUT and exit the PORTAL")
                    print("Enter 1 for VIEWING ALL CUSTOMERS DETAILS")
                    print("Enter 2 for UPDATING CUSTOMER DETAILS")
                    print("Enter 3 for REMOVAL OF CUSTOMER")
                    print("Enter 4 for access REQUEST from HELP BOX")
                    print("Enter 5 for VIEWING ALL JEWELLERY DETAILS")
                    print("Enter 6 for UPDATING JEWELLERY DETAILS")
                    print("Enter 7 for REMOVAL OF JEWELLERY ITEM","\n")
                                
                                
                    Staff_var = input("Enter your preference : ")
                    print()
                    if Staff_var in ['-1','0','1','2','3','4','5','6','7']:
                            
                            
                        if Staff_var == "-1":
                            LOGOUT(Staff_ID)
                            print("You have successfully LOGGED OUT and RETURNED to MAIN  LOGIN INTERFACE","\n","\n","\n")
                            break
                                    
                        
                        elif Staff_var == "0":
                            LOGOUT(Staff_ID)
                            sys.exit("You have successfully LOGGED OUT \n\nTHANKS FOR VISITING")
                                
                        
                        elif Staff_var == "1":
                            Client_EOC(Staff_ID)
                            VIEW_ALL_CLIENTS(1, Staff_ID)
                        
                        
                        elif Staff_var == "2":
                            Client_EOC(Staff_ID)
                            print("\n","Please provide the details of the CUSTOMER for UPDATING","\n")
                            Accounts(4)
                    
                        
                        elif Staff_var == "3":
                            Client_EOC(Staff_ID)
                            print("\n","Please provide the details of the CUSTOMER for REMOVAL","\n")
                            Accounts(3)
                                        
    
                        elif Staff_var == "4":
                            Client_EOC(Staff_ID)
                            Staff_CHATBOX()
                                
    
                        elif Staff_var == "5":
                            Client_EOC(Staff_ID)
                            VIEW_ALL_JEWELLERIES()
                                    
    
                        elif Staff_var == "6":
                            Client_EOC(Staff_ID)
                            Update_Jewellery(Staff_ID)
    
    
                        elif Staff_var == "7":
                            Client_EOC(Staff_ID)
                            Remove_Jewellery()
                    
                    
                    else :
                        print("INVALID INPUT","\n")
             
             
             
            elif Login_var == "3":
                EOC()
                Admin_Data = Accounts(2)
                Admin_Name = Admin_Data[0]
                Admin_ID = Admin_Data[1]
                Admin_Password = Admin_Data[2]
                
                while True:
                    print("So what would you like to do :", "\n")
                    print("Enter -1 to LOGOUT and GO BACK to MAIN LOGIN INTERFACE")
                    print("Enter 0 to LOGOUT and exit the PORTAL")
                    print("Enter 1 for ADDING JEWELLERY ITEM")
                    print("Enter 2 for VIEWING ALL STAFF DETAILS")
                    print("Enter 3 for ADDING STAFF")
                    print("Enter 4 for REMOVAL OF STAFF")
                    print("Enter 5 for UPDATING STAFF DETAILS","\n")
                                
                                
                    Admin_var = input("Enter your preference : ")
                    print()
                    if Admin_var in ['-1','0','1','2','3','4','5']:
                                
                                
                        if Admin_var == "-1":
                            LOGOUT(Admin_ID)
                            print("You have successfully LOGGED OUT and RETURNED to MAIN LOGIN INTERFACE","\n","\n","\n")
                            break
                                    
                        
                        elif Admin_var == "0":
                            LOGOUT(Admin_ID)
                            sys.exit("You have successfully LOGGED OUT \n\nTHANKS FOR VISITING")
                                
                        
                        elif Admin_var == "1":
                            Client_EOC(Admin_ID)
                            Add_Jewellery()
                                    
                                    
                        elif Admin_var == "2":
                            Client_EOC(Admin_ID)
                            VIEW_ALL_CLIENTS(2, Admin_ID)
                        
                        
                        elif Admin_var == "3":
                            Client_EOC(Admin_ID)
                            print("\n","Please provide the details of the STAFF for REGISTRATION","\n")
                            Accounts(1)
                        
                        
                        elif Admin_var == "4":
                            Client_EOC(Admin_ID)
                            print("\n","Please provide the details of the STAFF for REMOVAL","\n")
                            Accounts(3)
                                
    
                        elif Admin_var == "5":
                            Client_EOC(Admin_ID)
                            print("\n","Please provide the details of the STAFF for UPDATING","\n")
                            Accounts(4)
    
    
                    else :
                        print("INVALID INPUT","\n")
    
    
    
            elif Login_var == "4":
                EOC()
                CEO_Data = Accounts(2)
                CEO_Name = CEO_Data[0]
                CEO_ID = CEO_Data[1]
                CEO_Password = CEO_Data[2]
                
                while True:
                    print("So what would you like to do :", "\n")
                    print("Enter -1 to LOGOUT and GO BACK to MAIN LOGIN INTERFACE")
                    print("Enter 0 to LOGOUT and exit the PORTAL")
                    print("Enter 1 for VIEWING ALL ADMIN DETAILS")
                    print("Enter 2 for ADDING ADMIN")
                    print("Enter 3 for REMOVAL OF ADMIN")
                    print("Enter 4 for UPDATING ADMIN  DETAILS","\n")
                                
                                
                    CEO_var = input("Enter your preference : ")
                    print()
                    if CEO_var in ['-1','0','1','2','3','4']:
                                
                        if CEO_var == "-1":
                            LOGOUT(CEO_ID)
                            break
                        
                        
                        elif CEO_var == "0":
                            LOGOUT(CEO_ID)
                            sys.exit("You have successfully LOGGED OUT \n\nTHANKS FOR VISITING")
                        
                        
                        elif CEO_var == "1":
                            Client_EOC(CEO_ID)
                            VIEW_ALL_CLIENTS(3, CEO_ID)
                        
                        
                        elif CEO_var == "2":
                            Client_EOC(CEO_ID)
                            print("\n","Please provide the details of the ADMIN for REGISTRATION","\n")
                            Accounts(1)
                        
                        
                        elif CEO_var == "3":
                            Client_EOC(CEO_ID)
                            print("\n","Please provide the details of the ADMIN for REMOVAL","\n")
                            Accounts(3)
                        
                        
                        elif CEO_var == "4":
                            Client_EOC(CEO_ID)
                            print("\n","Please provide the details of the ADMIN for UPDATING","\n")
                            Accounts(4)
                    
                    
                    else :
                            print("INVALID INPUT","\n")
    
    
        else :
            print("INVALID INPUT","\n")



if __name__ == "__main__":
    SSJ()