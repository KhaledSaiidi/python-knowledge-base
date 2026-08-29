from pathlib import Path

expenses_dir = Path(__file__).resolve().parent
expenses_path = expenses_dir / "expenses.txt"

def add_expense(amount: float, description: str):
    try:
        with open(expenses_path, 'a') as file:
            file.write(f"{amount}, {description}\n")
            print(f"Added expense: ${amount} for ${description}")
    except Exception as e:
        print(f"An error occured: {e}")

def view_expenses():
    total = 0
    try:
        with open(expenses_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                amount, description = line.strip().split(",")
                print(f"{amount}, {description}")
                total += float(amount)
                print(f"Total Expenses: ${total}")
    except Exception as e:
        print(f"An error occured: {e}")

def main():
    while True:
        print("\nSimple Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            try:
                amount = float(input("Enter expense amount: $"))
                description = input("Enter expense description: ")
                add_expense(amount, description)
            except ValueError:
                print("Please enter a valid number for the amount.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
