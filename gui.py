import tkinter as tk
from tkinter import messagebox, simpledialog

# ============================
#   CLASS: Contact
# ============================

class Contact:
    # This class represents ONE contact (name, phone, info)
    def __init__(self, name, phone, info):
        # strip() removes extra spaces
        self.name = name.strip()
        self.phone = phone.strip()
        self.info = info.strip()

    # Used when searching for a name
    def matches(self, search_term):
        # Case-insensitive search
        return search_term.lower() in self.name.lower()

    # Format used when saving to file
    def to_file_format(self):
        return f"{self.name};{self.phone};{self.info}"


# ============================
#   FILE HANDLING
# ============================

def read_contacts_from_file(file_name):
    # Reads contacts from a text file and returns a list of Contact objects
    contacts = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                # Remove newline and split by ;
                parts = line.strip().split(";")
                if len(parts) == 3:
                    # Create a Contact object from the line
                    contacts.append(Contact(*parts))
    except FileNotFoundError:
        # If file doesn't exist, start with empty list
        print("No contact file found. Starting empty.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    # Saves all contacts to a file
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================
#   GUI APPLICATION
# ============================

class PhonebookGUI:
    # This class creates the entire GUI window and handles all button actions
    def __init__(self, root):
        self.root = root
        self.root.title("Phonebook GUI")  # Window title
        self.root.geometry("550x420")     # Window size
        self.root.configure(bg="#eef3ff") # Background color

        self.FILE = "contacts.txt"        # File where contacts are stored
        self.contacts = read_contacts_from_file(self.FILE)

        # ----------------------------
        # Listbox (shows all contacts)
        # ----------------------------
        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(pady=10)

        # ----------------------------
        # Buttons (Add, Update, etc.)
        # ----------------------------
        frame = tk.Frame(root, bg="#eef3ff")
        frame.pack()

        # Each button calls a function when clicked
        tk.Button(frame, text="Add", width=12, command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Update", width=12, command=self.update_contact).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Remove", width=12, command=self.remove_contact).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Search", width=12, command=self.search_contact).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Show All", width=12, command=self.load_contacts).grid(row=0, column=4, padx=5)

        # Load contacts into the listbox when the program starts
        self.load_contacts()

    # ----------------------------
    # Load all contacts into listbox
    # ----------------------------
    def load_contacts(self):
        self.listbox.delete(0, tk.END)  # Clear listbox
        # Sort contacts alphabetically by name
        for c in sorted(self.contacts, key=lambda x: x.name.lower()):
            self.listbox.insert(tk.END, f"{c.name} ({c.phone}) – {c.info}")

    # ----------------------------
    # Add a new contact
    # ----------------------------
    def add_contact(self):
        # Ask user for contact details
        name = simpledialog.askstring("Name", "Enter name:")
        if not name:
            return
        phone = simpledialog.askstring("Phone", "Enter phone:")
        if not phone:
            return
        info = simpledialog.askstring("Info", "Extra info:") or ""

        # Add to list
        self.contacts.append(Contact(name, phone, info))
        write_contacts_to_file(self.contacts, self.FILE)
        self.load_contacts()

    # ----------------------------
    # Update selected contact
    # ----------------------------
    def update_contact(self):
        index = self.listbox.curselection()  # Get selected item
        if not index:
            messagebox.showwarning("Error", "Select a contact first.")
            return

        contact = self.contacts[index[0]]

        # Ask user for new values (pre-filled with old values)
        new_name = simpledialog.askstring("New name", "Enter new name:", initialvalue=contact.name)
        if not new_name:
            return
        new_phone = simpledialog.askstring("New phone", "Enter new phone:", initialvalue=contact.phone)
        if not new_phone:
            return
        new_info = simpledialog.askstring("New info", "Enter new info:", initialvalue=contact.info) or ""

        # Update contact
        contact.name = new_name
        contact.phone = new_phone
        contact.info = new_info

        write_contacts_to_file(self.contacts, self.FILE)
        self.load_contacts()

    # ----------------------------
    # Remove selected contact
    # ----------------------------
    def remove_contact(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Error", "Select a contact first.")
            return

        contact = self.contacts[index[0]]

        # Confirm deletion
        if messagebox.askyesno("Confirm", f"Remove {contact.name}?"):
            self.contacts.remove(contact)
            write_contacts_to_file(self.contacts, self.FILE)
            self.load_contacts()

    # ----------------------------
    # Search for a contact
    # ----------------------------
    def search_contact(self):
        term = simpledialog.askstring("Search", "Enter name:")
        if not term:
            return

        # Find all matching contacts
        matches = [c for c in self.contacts if c.matches(term)]

        if not matches:
            messagebox.showinfo("Search result", "No contacts found.")
            return

        # Show results in a popup
        result = "\n".join(f"{c.name} ({c.phone}) – {c.info}" for c in matches)
        messagebox.showinfo("Search result", result)


# ============================
#   RUN GUI
# ============================

if __name__ == "__main__":
    root = tk.Tk()          # Create main window
    app = PhonebookGUI(root) # Create GUI app
    root.mainloop()         # Start GUI loop (keeps window open)
