import os   # Importerar os-modulen för att kunna lista filer och hantera flera register


# ============================
#   KLASS: Contact
# ============================

class Contact:
    """
    Representerar en kontakt i telefonregistret.
    """

    def __init__(self, first_name, last_name, phone, email, address):
        self.first_name = first_name.strip()   # Sparar förnamn utan extra mellanslag
        self.last_name = last_name.strip()     # Sparar efternamn
        self.phone = phone.strip()             # Sparar mobilnummer
        self.email = email.strip()             # Sparar e-post
        self.address = address.strip()         # Sparar adress

    def matches(self, search_term):
        """
        Returnerar True om söktermen matchar för- eller efternamn.
        """
        s = search_term.lower()
        return s in self.first_name.lower() or s in self.last_name.lower()

    def to_file_format(self):
        """
        Returnerar en rad som kan sparas i en textfil.
        Format: förnamn;efternamn;telefon;email;adress
        """
        return f"{self.first_name};{self.last_name};{self.phone};{self.email};{self.address}"


# ============================
#   FILHANTERING
# ============================

def read_contacts_from_file(file_name):
    """
    Läser in kontakter från en fil och returnerar en lista av Contact-objekt.
    """
    contacts = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")   # Delar upp raden vid ;
                if len(parts) == 5:               # Kontrollerar att alla fält finns
                    contacts.append(Contact(*parts))
    except FileNotFoundError:
        print("Ingen kontaktfil hittades. Börjar med tom lista.")
    return contacts


def write_contacts_to_file(contacts, file_name):
    """
    Skriver alla kontakter till filen.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(c.to_file_format() + "\n")


# ============================
#   KONTAKTFUNKTIONER
# ============================

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


# ============================
#   REGISTERHANTERING (B-NIVÅ)
# ============================

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


def main():
    # Skriver ut en välkomsttext när programmet startar
    print("Välkommen till telefonregistret!")

    # Låter användaren välja eller skapa ett register (fil)
    file_name = choose_register()

    # Läser in alla kontakter från den valda filen
    contacts = read_contacts_from_file(file_name)

    # Startar huvudloopen (menyn körs om och om igen tills användaren avslutar)
    while True:
        print("\n===== TELEFONREGISTER =====")
        print(f"Aktiva registret: {file_name}")  # Visar vilket register som används
        print("1. Visa alla kontakter")
        print("2. Lägg till kontakt")
        print("3. Uppdatera kontakt")
        print("4. Ta bort kontakt")
        print("5. Sök kontakt")
        print("6. Byt register (B-nivå)")
        print("7. Avsluta")

        # Användaren väljer ett menyval
        choice = input("Välj ett alternativ: ")

        # Kör rätt funktion beroende på val
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
            # Sparar nuvarande register innan byte
            write_contacts_to_file(contacts, file_name)

            # Låter användaren välja ett nytt register
            file_name = choose_register()

            # Läser in kontakter från det nya registret
            contacts = read_contacts_from_file(file_name)

        elif choice == "7":
            # Sparar innan programmet avslutas
            write_contacts_to_file(contacts, file_name)
            print("Programmet avslutas.")
            break  # Avslutar loopen och programmet

        else:
            print("Ogiltigt val, försök igen.")


if __name__ == "__main__":
    main()
