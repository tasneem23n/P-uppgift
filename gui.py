import tkinter as tk
from tkinter import messagebox, simpledialog

# ============================
#   CLASS: Contact
# ============================

class Contact:
    def __init__(self, name, phone, info):
        self.name = name.strip()
        self.phone = phone.strip()
        self.info = info.strip()

    def matches(self, search_term):
        return search_term.lower() in self.name.lower()

    def to_file_format(self):
        return f"{self.name};{self.phone};{self.info}"


# ============================
#   FILE HANDLING
# ============================

def read_contacts_from_file(file_name):
    contacts = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 3:
                    contacts.append(Contact(*parts))
    except FileNotFoundError:
        print("No contact file found. Starting empty.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================
#   GUI APPLICATION
# ============================

class PhonebookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Phonebook GUI")
        self.root.geometry("550x420")
        self.root.configure(bg="#eef3ff")

        self.FILE = "contacts.txt"
        self.contacts = read_contacts_from_file(self.FILE)

        # Listbox
        self.listbox = tk.Listbox(root, width=60, height=15)
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
        self.listbox.delete(0, tk.END)
        for c in sorted(self.contacts, key=lambda x: x.name.lower()):
            self.listbox.insert(tk.END, f"{c.name} ({c.phone}) – {c.info}")

    def add_contact(self):
        name = simpledialog.askstring("Name", "Enter name:")
        if not name:
            return
        phone = simpledialog.askstring("Phone", "Enter phone:")
        if not phone:
            return
        info = simpledialog.askstring("Info", "Extra info:") or ""

        self.contacts.append(Contact(name, phone, info))
        write_contacts_to_file(self.contacts, self.FILE)
        self.load_contacts()

    def update_contact(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Error", "Select a contact first.")
            return

        contact = self.contacts[index[0]]

        new_name = simpledialog.askstring("New name", "Enter new name:", initialvalue=contact.name)
        if not new_name:
            return
        new_phone = simpledialog.askstring("New phone", "Enter new phone:", initialvalue=contact.phone)
        if not new_phone:
            return
        new_info = simpledialog.askstring("New info", "Enter new info:", initialvalue=contact.info) or ""

        contact.name = new_name
        contact.phone = new_phone
        contact.info = new_info

        write_contacts_to_file(self.contacts, self.FILE)
        self.load_contacts()

    def remove_contact(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Error", "Select a contact first.")
            return

        contact = self.contacts[index[0]]

        if messagebox.askyesno("Confirm", f"Remove {contact.name}?"):
            self.contacts.remove(contact)
            write_contacts_to_file(self.contacts, self.FILE)
            self.load_contacts()

    def search_contact(self):
        term = simpledialog.askstring("Search", "Enter name:")
        if not term:
            return

        matches = [c for c in self.contacts if c.matches(term)]

        if not matches:
            messagebox.showinfo("Search result", "No contacts found.")
            return

        result = "\n".join(f"{c.name} ({c.phone}) – {c.info}" for c in matches)
        messagebox.showinfo("Search result", result)


# ============================
#   RUN GUI
# ============================

if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookGUI(root)
    root.mainloop()
