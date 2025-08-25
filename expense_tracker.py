from expense import Expense
import expense


def main():
    print("Running Expense Tracker")
    expense_file_name="track.csv"
    budget=2000
    # get user input 
    expense=get_user_experience()
    






    # write their expense to a file
    save_expense_to_file(expense,expense_file_name)



    # read file and summarixe
    summarize_expense(expense_file_name,budget)

    


def get_user_experience():
    print("getting user experiense")
    Expense_name=input("enter expense Name  : ")
    Expense_amount=float(input("enter expense Amount  : "))
    print(f"YOU entered UR expense name  :{Expense_name}  {Expense_amount}")

    expense_categories=[
        "Food",
        "Home",
        "Work",
        "fun"

    ]
    while True:
        print("Select a category :")
        for i,expenses_name in enumerate(expense_categories):
            print(f"{i+1} .{expenses_name}")

        value_range=f"[1 - {len(expense_categories)}]"
        selected_index=int(input(f"enter a category number {value_range}:"))-1

        if selected_index in range(len(expense_categories)):
                selected_category=expense_categories[selected_index]
                new_expense=Expense(name=Expense_name,category=selected_category,amount=Expense_amount)
                return new_expense
        else:
                print("invalid Category")
    
def save_expense_to_file(expense,expense_file_name):
    print(f"Saving User Expense{expense}to {expense_file_name}")
    with open(expense_file_name,"a") as f:
         f.write(f"{expense.name},{expense.amount},{expense.category}\n")
         
def summarize_expense(expense_file_name,budget):
    print("Summarizing user experiense")
    expenses:list[Expense]=[]
    with open(expense_file_name,"r") as f:
         lines=f.readlines()
         for line in lines:
              expense_name,expense_amount,expense_category=line.strip().split(",")
              print(expense_name,expense_category,expense_amount)
              line_expense=Expense(
                   name=expense_name,  amount=float(expense_amount), category=expense_category
              )
              print(line_expense)
              expenses.append(line_expense)
    
    amount_by_category={}
    for expense in expenses:
         key=expense.category
         if key in amount_by_category:
            amount_by_category  [key] += expense.amount
         else:
              amount_by_category  [key] = expense.amount
    print(" Expenses By Category :")
    for key,amount in amount_by_category.items():
         print(f" {key}: $ {amount:.2f}")
        
    total_spent=sum([x.amount for x in expenses])
    print(f"you have spent ${total_spent:.2f} this month")

    remaining_budget= budget-total_spent
    print(f"Total budget remaining {remaining_budget:.2f}")

import datetime
import calendar

def get_remaining_days_in_month():
    today = datetime.date.today()
    total_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = total_days - today.day
    return remaining_days

print(f"Remaining days in this month: {get_remaining_days_in_month()}")


         
         

if __name__=="__main__":
     main()