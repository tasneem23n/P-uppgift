import os   # Används för att lista filer och hantera registerfiler

# ============================================================
#   KLASS: Contact – representerar en kontakt i registret
# ============================================================

class Contact:
    def __init__(self, first_name, last_name, phone, email, address):
        # Sparar alla fält och tar bort extra mellanslag
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.address = address.strip()

    def matches(self, search_term):
        """
        Returnerar True om söktermen matchar för- eller efternamn.
        Sökningen är skiftlägesokänslig.
        """
        s = search_term.lower()
        return s in self.first_name.lower() or s in self.last_name.lower()

    def to_file_format(self):
        """
        Returnerar kontaktens data i ett format som kan sparas i fil.
        Format: förnamn;efternamn;telefon;email;adress
        """
        return f"{self.first_name};{self.last_name};{self.phone};{self.email};{self.address}"


# ============================================================
#   FILHANTERING – läsa och skriva registerfiler
# ============================================================

def read_contacts_from_file(file_name):
    """
    Läser in kontakter från en textfil och returnerar en lista av Contact-objekt.
    Om filen inte finns skapas en tom lista.
    """
    contacts = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")  # Delar upp raden vid ;
                if len(parts) == 5:              # Kontrollerar att alla fält finns
                    contacts.append(Contact(*parts))
    except FileNotFoundError:
        print("Ingen kontaktfil hittades. Börjar med tom lista.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    """
    Skriver alla kontakter till filen.
    Varje kontakt sparas på en egen rad.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================================================
#   TERMINALFUNKTIONER – funktioner för användarens menyval
# ============================================================

def add_contact(contacts):
    """
    Lägger till en ny kontakt baserat på användarens input.
    """
    print("\n--- Lägg till kontakt ---")
    first = input("Förnamn: ")
    last = input("Efternamn: ")
    phone = input("Mobilnummer: ")
    email = input("E-post: ")
    address = input("Adress: ")

    contacts.append(Contact(first, last, phone, email, address))
    print("Kontakt tillagd!")


def show_contacts(contacts):
    """
    Visar alla kontakter i registret.
    """
    print("\n--- Alla kontakter ---")
    if not contacts:
        print("Inga kontakter sparade.")
        return

    for c in contacts:
        print(f"{c.first_name} {c.last_name} | {c.phone} | {c.email} | {c.address}")


def search_contact(contacts):
    """
    Söker efter kontakter baserat på namn.
    """
    term = input("\nSök efter namn: ")
    matches = [c for c in contacts if c.matches(term)]

    if not matches:
        print("Inga kontakter hittades.")
        return

    print("\n--- Sökresultat ---")
    for c in matches:
        print(f"{c.first_name} {c.last_name} | {c.phone} | {c.email} | {c.address}")


def remove_contact(contacts):
    """
    Tar bort en kontakt baserat på namn.
    Tar bort första matchande kontakt.
    """
    term = input("\nAnge namn på kontakt att ta bort: ")
    for c in contacts:
        if c.matches(term):
            contacts.remove(c)
            print("Kontakt borttagen.")
            return
    print("Ingen kontakt hittades.")


def update_contact(contacts):
    """
    Uppdaterar en befintlig kontakt.
    Tomt fält innebär att det gamla värdet behålls.
    """
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


# ============================================================
#   REGISTERHANTERING – B-nivå
# ============================================================

def choose_register():
    """
    Låter användaren välja eller skapa ett register (fil).
    Returnerar filnamnet.
    """
    print("\n===== REGISTERHANTERING =====")
    print("1. Välj befintligt register")
    print("2. Skapa nytt register")

    choice = input("Val: ")

    if choice == "1":
        # Lista alla .txt-filer i mappen
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
        open(filename, "w").close()   # Skapar en tom fil
        print(f"Register '{filename}' skapat!")
        return filename

    else:
        print("Ogiltigt val.")
        return choose_register()


# ============================================================
#   MAIN – kör hela terminalprogrammet
# ============================================================

def main():
    """
    Huvudfunktionen som kör hela programmet.
    Hanterar meny, registerbyte och sparande.
    """
    print("Välkommen till telefonregistret!")

    # Låter användaren välja eller skapa ett register
    file_name = choose_register()

    # Läser in alla kontakter från filen
    contacts = read_contacts_from_file(file_name)

    # Huvudmeny-loop
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
            write_contacts_to_file(contacts, file_name)  # Spara innan byte
            file_name = choose_register()                # Välj nytt register
            contacts = read_contacts_from_file(file_name)
        elif choice == "7":
            write_contacts_to_file(contacts, file_name)  # Spara innan avslut
            print("Programmet avslutas.")
            break
        else:
            print("Ogiltigt val, försök igen.")


# ============================================================
#   STARTAR PROGRAMMET
# ============================================================

if __name__ == "__main__":
    main()   # Kör huvudprogrammet
