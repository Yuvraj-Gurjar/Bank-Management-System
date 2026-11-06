import json
import random
import string
from pathlib import Path

class Bank:
    # first create a dummy data
    database='data.json'  #path of the data
    data=[]
    try:
        if Path(database).exists:
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("No such files exist")
             
    except Exception as err:
        print(f"An exception occured as {err}")
         
    @staticmethod
    def __update():
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
    
    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spchr=random.choices("!@#$%^&*()",k=2)
        id=alpha+num+spchr
        random.shuffle(id)
        return "".join(id) #bcz it will give it as an object but we want string 
        
    def CreateAccount(self):
        info={
            "name":input("Tell me your name-:"),
            "age":int(input("Enter your age-:")),
            "email":input("Enter your email-:"),
            "pin":int(input("Enter your 4 digit pin-:")),
            "accountNo":Bank.__accountgenerate(),
            "balance":0
        }
        # first check the eligibility
        if info["age"]<18 or len(str(info["pin"]))!=4:
            print("Sorry you can not create your account")
        else:
            print("Account has been created successfully")
            for i in info:
                print(f"{i}:{info[i]}")
            print("please note down your account number")

            Bank.data.append(info)
            Bank.__update()

    def depositmoney(self):
        accnumber=input("Please tell me your account number-:")
        pin=int(input("Enter your pin-:"))
        
        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]

        if userdata==False:
            print("Sorry no data found")
        else:
            amount=int(input("how u want to deposit-:"))
            if amount>10000 or amount <0:
                print("Sorry the amount is too much u can only deposit below 10000 and above 0")
            else:
                userdata[0]['balance']+=amount
                Bank.__update()
                print("Amount deposited successfully")
            
    def withdrawmoney(self):
            accnumber=input("Please tell me your account number-:")
            pin=int(input("Enter your pin-:"))
            
            userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]
    
            if userdata==False:
                print("Sorry no data found")
            else:
                amount=int(input("how u want to withdraw-:"))
                if userdata[0]['balance']<amount:
                    print("Sorry u dont have enough balance to withdraw")
                    
                else:
                    userdata[0]['balance']-=amount
                    Bank.__update()
                    print("Amount withdrawn successfully")
    
    def showdetails(self):
        accnumber=input("Please tell me your account number-:")
        pin=int(input("Enter your pin-:"))

        userdata=[i for i in Bank.data if i['accountNo']==accnumber and i['pin']==pin]
        print("Your information are-:\n\n")
        for i in userdata[0]:
            print(f"{i}:{userdata[0][i]}")
            
    def updatedetails(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("no such user found ")
        
        else:
            print("you cannot change the age, account number, balance")

            print("Fill the details for change or leave it empty if no change")

            newdata = {
                "name": input("please tell new name or press enter : "),
                "email":input("please tell your new Email or press enter to skip :"),
                "pin": input("enter new Pin or press enter to skip: ")
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
            
            newdata['age'] = userdata[0]['age']

            newdata['accountNo'] = userdata[0]['accountNo']
            newdata['balance'] = userdata[0]['balance']
            
            if type(newdata['pin']) == str:
                newdata['pin'] = int(newdata['pin'])
            

            for i in newdata:
                 if newdata[i] == userdata[0][i]:
                     continue
                 else:
                     userdata[0][i] = newdata[i]

            Bank.__update()
            print("details updated successfully")
    
    def Delete(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("sorry no such data exist ")
        else:
            check = input("press y if you actually want to delete the account or press n")
            if check == 'n' or check == "N":
                print("bypassed")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully ")
                Bank.__update()
                   
user=Bank()

print("Press 1 for creating an Account")
print("Press 2 for Depositing the money in the bank")
print("Press 3 for withdraw the money")
print('Press 4 for details')
print("Press 5 for updating the details")
print("Press 6 for deleting your account")

check=int(input("tell your response-:"))

if check==1:
    user.CreateAccount()
if check==2:
    user.depositmoney()
if check==3:
    user.withdrawmoney()
if check==4:
    user.showdetails()
if check == 5:
    user.updatedetails()
if check == 6:
    user.Delete()