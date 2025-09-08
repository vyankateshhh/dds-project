# Node for Linked List
class BookNode:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True
        self.next = None


# Linked List for Book Inventory
class BookInventory:
    def __init__(self):
        self.head = None

    def add_book(self, title, author):
        new_book = BookNode(title, author)
        new_book.next = self.head
        self.head = new_book

    def search(self, keyword):
        results = []
        current = self.head
        while current:
            if keyword.lower() in current.title.lower() or keyword.lower() in current.author.lower():
                results.append((current.title, current.author, "Available" if current.available else "Borrowed"))
            current = current.next
        return results

    def get_book(self, title):
        current = self.head
        while current:
            if current.title.lower() == title.lower():
                return current
            current = current.next
        return None

    def display_books(self):
        current = self.head
        books = []
        while current:
            books.append((current.title, current.author, "Available" if current.available else "Borrowed"))
            current = current.next
        return books


# Stack for Undo Actions
class ActionStack:
    def __init__(self):
        self.stack = []

    def push(self, action, book):
        self.stack.append((action, book))

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None


# Main E-Library System
class ELibrary:
    def __init__(self):
        self.inventory = BookInventory()
        self.undo_stack = ActionStack()

    def borrow_book(self, title):
        book = self.inventory.get_book(title)
        if book and book.available:
            book.available = False
            self.undo_stack.push("borrow", book)
            return f"You borrowed '{book.title}'"
        return "Book not available or does not exist."

    def return_book(self, title):
        book = self.inventory.get_book(title)
        if book and not book.available:
            book.available = True
            self.undo_stack.push("return", book)
            return f"You returned '{book.title}'"
        return "Book was not borrowed or does not exist."

    def undo(self):
        last_action = self.undo_stack.pop()
        if not last_action:
            return "No actions to undo."
        action, book = last_action
        if action == "borrow":
            book.available = True
            return f"Undo: Returned '{book.title}'"
        elif action == "return":
            book.available = False
            return f"Undo: Borrowed '{book.title}'"

    def search_books(self, keyword):
        return self.inventory.search(keyword)

    def show_inventory(self):
        return self.inventory.display_books()


# ------------------ Demo ------------------
if __name__ == "__main__":
    lib = ELibrary()
    
    # Add books
    lib.inventory.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    lib.inventory.add_book("1984", "George Orwell")
    lib.inventory.add_book("To Kill a Mockingbird", "Harper Lee")

    print("📚 Library Inventory:")
    print(lib.show_inventory())

    print("\n🔎 Search for 'George':")
    print(lib.search_books("George"))

    print("\n➡️ Borrowing '1984':")
    print(lib.borrow_book("1984"))
    print(lib.show_inventory())

    print("\n↩️ Undo last action:")
    print(lib.undo())
    print(lib.show_inventory())

    print("\n⬅️ Returning '1984':")
    print(lib.return_book("1984"))
    print(lib.show_inventory())

    print("\n↩️ Undo last action:")
    print(lib.undo())
    print(lib.show_inventory())
