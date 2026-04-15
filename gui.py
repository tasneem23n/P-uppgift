import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# ============================
#   KLASS: Contact
# ============================

class Contact:
    def __init__(self, first_name, last_name, phone, email, address):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.address = address.strip()

    def matches(self, search_term):
        s = search_term.lower()
        return s in self.first_name.lower() or s in self.last_name.lower()

    def to_file_format(self):
        return f"{self.first_name};{self.last_name};{self.phone};{self.email};{self.address}"


# ============================
#   FILHANTERING
# ============================

def read_contacts_from_file(file_name):
    contacts = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 5:
                    contacts.append(Contact(*parts))
    except FileNotFoundError:
        print("Ingen kontaktfil hittades. Börjar med tom lista.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================
#   KONTAKTFUNKTIONER
# ============================

def add_contact(contacts):
    print("\n--- Lägg till kontakt ---")
    first = input("Förnamn: ")
    last = input("Efternamn: ")
    phone = input("Mobilnummer: ")
    email = input("E-post: ")
    address = input("Adress: ")

    contacts.append(Contact(first, last, phone, email, address))
    print("Kontakt tillagd!")


def show_contacts(contacts):
    print("\n--- Alla kontakter ---")
    if not contacts:
        print("Inga kontakter sparade.")
        return

    for c in contacts:
        print(f"{c.first_name} {c.last_name} | {c.phone} | {c.email} | {c.address}")


def search_contact(contacts):
    term = input("\nSök efter namn: ")
    matches = [c for c in contacts if c.matches(term)]

    if not matches:
        print("Inga kontakter hittades.")
        return

    print("\n--- Sökresultat ---")
    for c in matches:
        print(f"{c.first_name} {c.last_name} | {c.phone} | {c.email} | {c.address}")


def remove_contact(contacts):
    term = input("\nAnge namn på kontakt att ta bort: ")
    for c in contacts:
        if c.matches(term):
            contacts.remove(c)
            print("Kontakt borttagen.")
            return
    print("Ingen kontakt hittades.")


def update_contact(contacts):
    term = input("\nAnge namn på kontakt att uppdatera: ")

    for c in contacts:
        if c.matches(term):
            print("Lämna tomt för att behålla gamla värdet.")

            c.first_name = input(f"Förnamn ({c.first_name}): ") or c.first_name
            c.last_name = input(f"Efternamn ({c.last_name}): ") or c.last_name
            c.phone = input(f"Mobilnummer ({c.phone}): ") or c.phone
            c.email = input(f"E-post ({c.email}): ") or c.email
            c.address = input(f"Adress ({c.address}): ") or c.address

            print("Kontakt uppdaterad!")
            return

    print("Ingen kontakt hittades.")


# ============================
#   REGISTERHANTERING (B-NIVÅ)
# ============================

def choose_register():
    print("\n===== REGISTERHANTERING =====")
    print("1. Välj befintligt register")
    print("2. Skapa nytt register")

    choice = input("Val: ")

    if choice == "1":
        files = [f for f in os.listdir() if f.endswith(".txt")]
        if not files:
            print("Inga register hittades.")
            return choose_register()

        print("\nTillgängliga register:")
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")

        index = int(input("Välj register: ")) - 1
        return files[index]

    elif choice == "2":
        name = input("Namn på nytt register (utan .txt): ")
        filename = name + ".txt"
        open(filename, "w").close()
        print(f"Register '{filename}' skapat!")
        return filename

    else:
        print("Ogiltigt val.")
        return choose_register()


# ============================
#   GUI-FUNKTIONER
# ============================

def gui_show_contacts(contacts):
    window = tk.Toplevel()
    window.title("Alla kontakter")

    tree = ttk.Treeview(window, columns=("Förnamn", "Efternamn", "Telefon", "E-post", "Adress"), show="headings")
    tree.pack(fill="both", expand=True)

    for col in ("Förnamn", "Efternamn", "Telefon", "E-post", "Adress"):
        tree.heading(col, text=col)

    for c in contacts:
        tree.insert("", "end", values=(c.first_name, c.last_name, c.phone, c.email, c.address))


def gui_add_contact(contacts, file_name):
    window = tk.Toplevel()
    window.title("Lägg till kontakt")

    labels = ["Förnamn", "Efternamn", "Telefon", "E-post", "Adress"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0)
        entry = tk.Entry(window)
        entry.grid(row=i, column=1)
        entries[label] = entry

    def save():
        first = entries["Förnamn"].get()
        last = entries["Efternamn"].get()
        phone = entries["Telefon"].get()
        email = entries["E-post"].get()
        address = entries["Adress"].get()

        contacts.append(Contact(first, last, phone, email, address))
        write_contacts_to_file(contacts, file_name)
        messagebox.showinfo("Klar", "Kontakt tillagd!")
        window.destroy()

    tk.Button(window, text="Spara", command=save).grid(row=len(labels), column=0, columnspan=2)


def gui_search_contact(contacts):
    term = simpledialog.askstring("Sök", "Ange namn att söka efter:")
    if not term:
        return

    results = [c for c in contacts if c.matches(term)]

    if not results:
        messagebox.showinfo("Resultat", "Inga kontakter hittades.")
        return

    gui_show_contacts(results)


def gui_main():
    file_name = choose_register()
    contacts = read_contacts_from_file(file_name)

    root = tk.Tk()
    root.title("Telefonregister GUI")

    tk.Button(root, text="Visa alla kontakter", width=30,
              command=lambda: gui_show_contacts(contacts)).pack(pady=5)

    tk.Button(root, text="Lägg till kontakt", width=30,
              command=lambda: gui_add_contact(contacts, file_name)).pack(pady=5)

    tk.Button(root, text="Sök kontakt", width=30,
              command=lambda: gui_search_contact(contacts)).pack(pady=5)

    tk.Button(root, text="Avsluta", width=30,
              command=root.destroy).pack(pady=5)

    root.mainloop()


# ============================
#   HUVUD-MAIN SOM KÖR ALLT
# ============================

def main_terminal():
    print("Välkommen till telefonregistret!")
    file_name = choose_register()
    contacts = read_contacts_from_file(file_name)

    while True:
        print("\n===== TELEFONREGISTER =====")
        print(f"Aktiva registret: {file_name}")
        print("1. Visa alla kontakter")
        print("2. Lägg till kontakt")
        print("3. Uppdatera kontakt")
        print("4. Ta bort kontakt")
        print("5. Sök kontakt")
        print("6. Byt register")
        print("7. Avsluta")

        choice = input("Val: ")

        if choice == "1":
            show_contacts(contacts)
        elif choice == "2":
            add_contact(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            remove_contact(contacts)
        elif choice == "5":
            search_contact(contacts)
        elif choice == "6":
            write_contacts_to_file(contacts, file_name)
            file_name = choose_register()
            contacts = read_contacts_from_file(file_name)
        elif choice == "7":
            write_contacts_to_file(contacts, file_name)
            print("Programmet avslutas.")
            break
        else:
            print("Ogiltigt val.")


# ============================
#   STARTA PROGRAMMET
# ============================

if __name__ == "__main__":
    mode = input("Skriv 'gui' för GUI eller 'terminal' för terminalversion: ")

    if mode.lower() == "gui":
        gui_main()
    else:
        main_terminal()
