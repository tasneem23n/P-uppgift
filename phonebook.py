import os

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
        A Contact object with cleaned fields
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
        print("Ingen kontaktfil hittades. Börjar med tom lista.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    """
    Input: contacts (list of Contact), file_name (str)
    Output: writes all contacts to file
    """
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================
#   PHONEBOOK FUNCTIONS
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
#   REGISTER HANDLING (B-NIVÅ)
# ============================

def choose_register():
    """
    Lets the user choose or create a register.
    Output: filename (str)
    """

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
#   MAIN MENU
# ============================

def main():
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
        print("6. Byt register (B-nivå)")
        print("7. Avsluta")

        choice = input("Välj ett alternativ: ")

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
            print("Ogiltigt val, försök igen.")


if __name__ == "__main__":
    main()
