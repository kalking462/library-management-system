import json
from datetime import datetime
import os

# ------------------- Library Class -------------------
class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.users = {}
        self.borrowed_books = {}
        self.transactions = []
        self.load_data()
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.books = data.get("books", [])
                self.users = data.get("users", {})
                self.borrowed_books = data.get("borrowed_books", {})
                self.transactions = data.get("transactions", [])
    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump({
                "books": self.books,
                "users": self.users,
                "borrowed_books": self.borrowed_books,
                "transactions": self.transactions
            }, file, indent=4)
    def add_user(self):
        user_id = input("Enter User ID: ")
        name = input("Enter User Name: ")
        if user_id in self.users:
            print("User ID already exists!")
        else:
            self.users[user_id] = name
            self.save_data()
            print(f"User '{name}' added successfully.")
    def add_book(self):
        title = input("Enter Book Title: ")
        author = input("Enter Author Name: ")
        subject = input("Enter Subject: ")
        isbn = input("Enter ISBN: ")
        quantity = int(input("Enter Quantity: "))
        book = {
            "title": title,
            "author": author,
            "subject": subject,
            "isbn": isbn,
            "quantity": quantity
        }
        self.books.append(book)
        self.save_data()
        print(f"Book '{title}' added successfully.")
    def show_books(self):
        if len(self.books) == 0:
            print("No books available.")
        else:
            print("\nAvailable Books:")
            for book in self.books:
                print(f"{book['title']} by {book['author']} | Subject: {book['subject']} | ISBN: {book['isbn']} | Quantity: {book['quantity']}")
            print()


    def borrow_book(self):
        title = input("Enter Book Title to Borrow: ")
        user_id = input("Enter Your User ID: ")
        if user_id not in self.users:
            print("User not found! Please register first.")
            return
        for book in self.books:
            if book["title"].lower() == title.lower() and book["quantity"] > 0:
                book["quantity"] -= 1
                self.borrowed_books[title] = user_id
                self.transactions.append({
                    "user_id": user_id,
                    "user_name": self.users[user_id],
                    "title": title,
                    "action": "borrowed",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                self.save_data()
                print(f"{self.users[user_id]} borrowed '{title}'.")
                return
        print("Book not available or out of stock!")

    
    def return_book(self):
        title = input("Enter Book Title to Return: ")
        user_id = input("Enter Your User ID: ")
        if title in self.borrowed_books and self.borrowed_books[title] == user_id:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    book["quantity"] += 1
                    break
            self.transactions.append({
                "user_id": user_id,
                "user_name": self.users[user_id],
                "title": title,
                "action": "returned",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            del self.borrowed_books[title]
            self.save_data()
            print(f"{self.users[user_id]} returned '{title}'.")
        else:
            print("This book was not borrowed by this user!")

    
    def show_transactions(self):
        if len(self.transactions) == 0:
            print("No transactions yet.")
        else:
            print("\nTransaction History:")
            for t in self.transactions:
                print(f"{t['time']} - {t['user_name']} ({t['user_id']}) {t['action']} '{t['title']}'")
            print()


def main():
    library = Library()
    while True:
        print("\n=== Library Menu ===")
        print("1. Add User")
        print("2. Add Book")
        print("3. Show Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Show Transactions")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            library.add_user()
        elif choice == "2":
            library.add_book()
        elif choice == "3":
            library.show_books()
        elif choice == "4":
            library.borrow_book()
        elif choice == "5":
            library.return_book()
        elif choice == "6":
            library.show_transactions()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
