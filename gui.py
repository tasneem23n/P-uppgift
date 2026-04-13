import tkinter as tk
from tkinter import messagebox, simpledialog

# ============================
#   CLASS: Contact
# ============================

class Contact:
    """
    Represents a contact in the phonebook.

    Input:
        first_name (str)
        last_name (str)
        phone (str)
        email (str)
        address (str)

    Output:
        Contact object with cleaned fields
    """

    def __init__(self, first_name, last_name, phone, email, address):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.address = address.strip()

    def matches(self, search_term):
        """
        Input: search_term (str)
        Output: True if search term matches first or last name
        """
        s = search_term.lower()
        return s in self.first_name.lower() or s in self.last_name.lower()

    def to_file_format(self):
        """
        Output: A single line string for saving to file
        Format: first;last;phone;email;address
        """
        return f"{self.first_name};{self.last_name};{self.phone};{self.email};{self.address}"


# ============================
#   FILE HANDLING
# ============================

def read_contacts_from_file(file_name):
    """
    Input: file_name (str)
    Output: list of Contact objects
    """
    contacts = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 5:
                    contacts.append(Contact(*parts))
    except FileNotFoundError:
        print("No contact file found. Starting empty.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    """
    Input: list of Contact objects, file_name (str)
    Output: writes all contacts to file
    """
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================
#   GUI APPLICATION
# ============================

class PhonebookGUI:
    """
    Creates the GUI and handles all user interactions.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Phonebook GUI")
        self.root.geometry("650x450")
        self.root.configure(bg="#eef3ff")

        self.FILE = "contacts.txt"
        self.contacts = read_contacts_from_file(self.FILE)

        # Listbox to display contacts
        self.listbox = tk.Listbox(root, width=80, height=15)
        self.listbox.pack(pady=10)

        # Buttons
        frame = tk.Frame(root, bg="#eef3ff")
        frame.pack()

        tk.Button(frame, text="Add", width=12, command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Update", width=12, command=self.update_contact).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Remove", width=12, command=self.remove_contact).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Search", width=12, command=self.search_contact).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Show All", width=12, command=self.load_contacts).grid(row=0, column=4, padx=5)

        self.load_contacts()

    def load_contacts(self):
        """
        Loads all contacts into the listbox.
        Input: none
        Output: updates listbox
        """
        self.listbox.delete(0, tk.END)
        for c in sorted(self.contacts, key=lambda x: (x.last_name.lower(), x.first_name.lower())):
            self.listbox.insert(
                tk.END,
                f"{c.first_name} {c.last_name} | {c.phone} | {c.email} | {c.address}"
            )

    def add_contact(self):
        """
        Adds a new contact.
        Input: user dialog boxes
        Output: new contact saved to file
        """
        first = simpledialog.askstring("First name", "Enter first name:")
        if not first: return

        last = simpledialog.askstring("Last name", "Enter last name:")
        if not last: return

        phone = simpledialog.askstring("Phone", "Enter phone number:")
        if not phone: return

        email = simpledialog.askstring("Email", "Enter email:") or ""
        address = simpledialog.askstring("Address", "Enter address:") or ""

        self.contacts.append(Contact(first, last, phone, email, address))
        write_contacts_to_file(self.contacts, self.FILE)
        self.load_contacts()

    def update_contact(self):
        """
        Updates selected contact.
        Input: selected listbox item + user dialogs
        Output: updated contact saved to file
        """
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Error", "Select a contact first.")
            return

        c = self.contacts[index[0]]

        new_first = simpledialog.askstring("First name", "Enter new first name:", initialvalue=c.first_name)
        if not new_first: return

        new_last = simpledialog.askstring("Last name", "Enter new last name:", initialvalue=c.last_name)
        if not new_last: return

        new_phone = simpledialog.askstring("Phone", "Enter new phone:", initialvalue=c.phone)
        if not new_phone: return

        new_email = simpledialog.askstring("Email", "Enter new email:", initialvalue=c.email) or ""
        new_address = simpledialog.askstring("Address", "Enter new address:", initialvalue=c.address) or ""

        c.first_name = new_first
        c.last_name = new_last
        c.phone = new_phone
        c.email = new_email
        c.address = new_address

        write_contacts_to_file(self.contacts, self.FILE)
        self.load_contacts()

    def remove_contact(self):
        """
        Removes selected contact.
        Input: selected listbox item
        Output: contact removed from file
        """
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Error", "Select a contact first.")
            return

        c = self.contacts[index[0]]

        if messagebox.askyesno("Confirm", f"Remove {c.first_name} {c.last_name}?"):
            self.contacts.remove(c)
            write_contacts_to_file(self.contacts, self.FILE)
            self.load_contacts()

    def search_contact(self):
        """
        Searches for contacts by first or last name.
        Input: search term from user
        Output: popup with results
        """
        term = simpledialog.askstring("Search", "Enter name:")
        if not term: return

        matches = [c for c in self.contacts if c.matches(term)]

        if not matches:
            messagebox.showinfo("Search result", "No contacts found.")
            return

        result = "\n".join(
            f"{c.first_name} {c.last_name} | {c.phone} | {c.email} | {c.address}"
            for c in matches
        )
        messagebox.showinfo("Search result", result)


# ============================
#   RUN GUI
# ============================

if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookGUI(root)
    root.mainloop()
