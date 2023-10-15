# Use it for Enter Tasks, Adds Skills and their Progress

import sqlite3
import re
import os

class User():
    """
    Login and register
    """        
    # To connect to database
    database = sqlite3.connect("SkillsApp")
    create_data = database.cursor()
    create_data = create_data.execute("create table if not exists 'User' (Email text , Name text, Skills text, Progress interger) ")

    def __init__(self): 
        
        pass

    def true_syntex_of_Email(self):
        """
        Log in, register, and correct the account pattern
        """

        Email = input("Enter Your Email: ").strip()
        Name = input("Enter Your Name: ").strip().capitalize()
        create_data = self.database.cursor() 
                        # xx00@xx00.yy
        if re.search(r"[a-z0-9]+(\@)[a-z]+(\.)[a-z]+",Email) and re.search(r"[A-z0-9]+", Name):
            create_data.execute("select Email, Name from User where Email = ? and Name = ?", (Email, Name))
            exists_user = create_data.fetchone()

            # Email has not same pattern
            if exists_user == None:
                # if you new User
                create_data.execute("insert into User (Email, Name) values (?, ?)", (Email, Name))
                print("Your Account Added")

            else:
                # if you User
                print("You are Member")
            return Email, Name

        else:
            # if entered incorrect value
            print("Entered Value Is Not Valid")
            return self.true_syntex_of_Email()

class The_Operations(User):
    """
    The orders what you want to do  
    """
    database = User.database
    create_data = database.cursor()

    def __init__(self):
        
        # To bring Emil and Name from class User from method true_syntex_of_Email
        self.Email, self.Name = User.true_syntex_of_Email(self)
        self.create_data = The_Operations.database

    def get_option(self):
        """
        The order what you want to do
        """

        try:
            Opetion = str(input("""
    >>>>>>>>>>> What Do You Want To Do ?

                "s" => Show All Skills and Progress
                "a" => Add New Skill
                "u" => Update Progress of Skill
                "d" => Delete A Skill
                "ee" => Edit Email
                "i" => Show The Data Of Account
                "sw" => Switch Account
                "e" => Exist The App
                "du" => Delete Accout

    >>>>>>>>>>> Write Choose Option: """).lower().strip())    
            return Opetion
    
        except:
            # if you entered incorrect value
            print("You Entered Value Is Not Valid")
            return self.get_option()

    def Show_The_Data(self):
        """
        Show the Skills and Progress
        """
        num_skills = self.create_data.execute(f"select Skills, Progress from User where Email = ? and Name = ?", (self.Email, self.Name)).fetchall()

        if len(num_skills) > 0 and num_skills != None:

            print(f"\nYou Have {len(num_skills) - 1 } Skills")
            #   Skill => 90%
            for skill in num_skills:

                if skill[0] != None:
                    print(f"- {skill[0]} => {skill[1]}%")

                else:
                    continue
    
        else:
            # if you don't have any skill
            print("You Don't Have Any Skills")

    def Add_The_Data(self):
        """
        Add The Skills
        """
        try:     
            skill = str(input(f"Enter The Skill: ").capitalize().strip())
            progress = int(input(f"Enter The progress: "))

            is_skill_exists = self.create_data.execute("SELECT Skills FROM User WHERE Email = ? AND Name = ? AND Skills = ?", (self.Email, self.Name, skill)).fetchone()

            if is_skill_exists == None:

                self.create_data.execute(f"insert into User (Email, Name, Skills, Progress) values (?, ?, ?, ?)", (self.Email, self.Name, skill, progress))

                print("Skills Has Add")

                return self.database.commit()


            else:
                    # if you that Skill exists
                print("The Skill Is exists")
                opetion = input("""To Update This Skill Enter "u" To Back Write Anything: """)
                
                if opetion == "u":
                    # if you want to edit Progress that Skill
                    return self.Update_The_Data()

        except:
            # if you Entered in correct value
            print("\nYou Entered Value Is Not Valid")

    def Update_The_Data(self):
        """
        Edit Progress of Skill
        """
        try:
            skill = str(input("Enter The Skill What You Want Edit It ").capitalize().strip())
            new_progress = int(input("Enter The New Progress "))

            is_skill_exists = self.create_data.execute("SELECT Skills FROM User WHERE Email = ? AND Name = ? AND Skills = ?", (self.Email, self.Name, skill)).fetchone()

            if is_skill_exists != None:

                show_data = self.create_data.execute("update User set Progress = ? where Email = ? and Name = ? and Skills = ?  ", (new_progress, self.Email, self.Name, skill)).fetchall()
                
                if len(show_data) > 0 and show_data != None:
            
                    print(f"\nYou Have {len(show_data) - 1 } Skills")

                    for skill in show_data:
                            
                        if skill[0] != None:
                            print(f"- {skill[0]} => {skill[1]}%")

                        else:

                            continue

                else:
                    print("You Don't Have Any Skills")
                return self.database.commit()

            else:
                    # if you have that Skill
                print("The Skill Want To Edit Not Exists")        

        except:
            # if you Entered in correct value
            print("\nYou Entered Value Is Not Valid")
    
    def Delete_The_Data(self):
        """
        Delete Skill and That Progress
        """        
        try:
            delete_element = str(input("Enter The Skill What You Want Delete It ").capitalize().strip())
            is_skill_exists = self.create_data.execute("select Skills, Progress from User where Email = ? and Name = ? and Skills = ?", (self.Email, self.Name, delete_element)).fetchone()
            
            print(f"Will Delete Skill: {is_skill_exists[0]} and Progress: {is_skill_exists[1]}")
            
            # if Skill exists
            if is_skill_exists != None:
                
                self.create_data.execute("delete from User where Email = ? and Name = ? and Skills = ? ", (self.Email, self.Name, delete_element))
                
                print("The Skill Has Deleted")
                
                return self.database.commit()

            else:
                # if Skill not exists
                print("The Skill Not Exists")

        except:
            # if you Entered in correct value
            print("You Entered Value Is Not Valid")
            return self.Delete_The_Data()
                    
    def Update_The_Email(self):
        """
        To Edit The Account
        """
        try:

            New_Email = str(input("Enter Your New Email: ").strip())
            New_Name = str(input("Enter Your New Name: ").capitalize().strip())
                            # xx00@xx00.yy
            if re.search(r"[a-z0-9]+(\@)[a-z]+(\.)[a-z]+",New_Email) and re.search(r"[A-z0-9]+", New_Name):
                
                self.create_data.execute("update User set Email = ?, Name = ? where Email = ? and Name = ? ", (New_Email, New_Name, self.Email, self.Name))

                print(f"\n\nNew Email: {New_Email}\nNew Name: {New_Name}")
                # To save New Email and New Name
                return self.database.commit(), self.Show_All_Data()

            else:

                print("You Entered Value Is Not Valid")
                return self.Update_The_Email()

        except:
            self.Update_The_Email()

    def Show_All_Data(self):
        """
        To Show Email, Name, Skills and their Progress
        """
        # To show Email and Name
        print(f"\nYour Email: {self.Email}\nYour Name: {self.Name}")
        # To show Skills and Progress
        return self.Show_The_Data()

        def Switch_Account(self):
        '''
        Switch Account
        '''
                                                                       # Path python                                                   Name of File
        return self.database.commit(), self.database.close(), os.system(r"C:\Users\maham\AppData\Local\Programs\Python\Python311\python.exe Code0.py")
    
    def Exist(self):
        """
        Message to Exist from the app
        """
        print("\nAre You Want To Exist")
        opetion = input("""To Exist Write "e" To Back Write Anything: """)

        if opetion == "e":
            
            return self.database.commit(), self.database.close()

        else:
            
            return self.Operation()
    
    def Exist_The_App(self):
        """
        Exist from the app
        """
        # To save the data
        return self.database.commit(), self.database.close()

    def Operation(self):
        """
        To Choose the operation what you want to
        """
        Opetion = self.get_option()

        if Opetion == "s": 
            # Show All Skills and Progress
            print("\nYou Choose: Show All Skills and Progress ")
            return self.Show_The_Data(), self.Exist()

        elif Opetion == "a":
            # Add New Skill
            print("\nYou Choose: Add New Skill")
            return self.Add_The_Data(), self.Exist()

        elif Opetion == "d":
            # Delete A Skill
            print("\nYou Choose: Delete A Skill")
            return self.Delete_The_Data(), self.Exist()

        elif Opetion == "u":
            # Update Progress Of Skill
            print("\nYou Choose: Update Progress Of Skill")
            return self.Update_The_Data(), self.Exist()

        elif Opetion == "ee":
            # Update Email
            print("\nYou Choose: Update Email")
            return self.Update_The_Email(), self.Exist()

        elif Opetion == "du":
            # Delete Email
            print("\nYou Choose: Delete Email")
            return self.Delete_The_Account(), self.Exist()

        elif Opetion == "i":
            # Show All Data Of Account
            print("\nYou Choose: Show All Data Of Account")
            return self.Show_All_Data(), self.Exist()

        elif Opetion == "e":
            # Exist The App
            print("\nYou Choose: Exist The App >>>Bye")
            return self.Exist_The_App()

        elif Opetion == "sw":
            # Switch Account
            print("\nYou Choose: Switch Account\n")
            return self.Switch_Account()

        else:
            # if You Entered Value Is Not Valid
            print("You Entered Value Is Not Valid")
            return self.Exist()

The_Operation = The_Operations()
The_Operation.Operation()




















































