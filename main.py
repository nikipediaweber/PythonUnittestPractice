from crm_usermanagement import AngemeldeterUser, UnregistrierterUser, Hersteller, Produkt, IAngemeldeterUser, IProduktService, IHerstellerInterface, ISystemZugriff, Mensch
from productbackend import ProductList
from usermanagement import UserManagement, SimpleUserInterface, SimpleProductService


def main():
    # Erstelle die benötigten Services
    product_list : IHerstellerInterface = ProductList()
    product_service : IProduktService = SimpleProductService(product_list)
    user_interface : IAngemeldeterUser = SimpleUserInterface()
    Systemzugriff : ISystemZugriff = UserManagement(user_interface, product_service)



    # Registriere einen neuen User
    unregistered_user = UnregistrierterUser()
    registration_success = unregistered_user.registrierenUser(Systemzugriff, "MaxMustermann", "maxmustermacnn@gmail.com")
    if registration_success:
        print("User successfully registered.")
    else:
        print("User registration failed.")

    # Logge den User ein
    logged_in_user = Systemzugriff.login("MaxMustermann")
    if logged_in_user:
        print(f"User {logged_in_user.getName()} logged in.")
    else:
        print("Login failed.")      

    # Erstelle einen Hersteller
    hersteller_interface = product_list  # Verwende die ProductList als Hersteller-Interface
    unregistered_user2 = UnregistrierterUser()
    registration_success2 = unregistered_user2.registrierenHersteller(Systemzugriff, "Siemens", "verkauf@siemens.com")
    if registration_success2:
        print("Hersteller successfully registered.")
    else:
        print("Hersteller registration failed.")    

    
    # Veröffentliche ein Produkt
    logged_in_hersteller = Systemzugriff.login("Siemens")

    if logged_in_hersteller:
        print(f"Hersteller {logged_in_hersteller.getName()} was logged in.")
        neues_produkt = Produkt("Waschmaschine", "Siemens Waschmaschine Modell X100", "Waschmaschine mit 8kg Fassungsvermögen, Energieeffizienzklasse A+++")
        hersteller_interface.veroeffentlicheProdukt(logged_in_hersteller.getName(), neues_produkt)
        print(f"Produkt {neues_produkt.name} veröffentlicht.")
    else:
        print("Hersteller login failed.")   

    # Liste alle Produkte
    alle_produkte = product_list.get_all_products()
    print("Alle Produkte im System:")
    for produkt, hersteller in alle_produkte:
        print(f"- {produkt.getName()}: {produkt.getBeschreibung()} (Hersteller: {hersteller})")

   #Produkte von user aus abrufen
    if isinstance(logged_in_user, AngemeldeterUser):
        produkte = logged_in_user.holeProdukte()
        print(f"Produkte für {logged_in_user.getName()}:")
        for produkt, hersteller in alle_produkte:
            print(f"- {produkt.getName()}: {produkt.getBeschreibung()} (Hersteller: {hersteller})")
    else:
        print("Nur angemeldete User können Produkte abrufen.")  

if __name__ == "__main__":
    main()