from crm_usermanagement import AngemeldeterUser, UnregistrierterUser, IAngemeldeterUser, IProduktService, ISystemZugriff,Hersteller, Produkt
from productbackend import ProductList
from typing import Optional, Union

# Einfache Implementierung der benötigten Interfaces
class SimpleUserInterface:
    def sendeNachricht(self, user, empfaenger, text):
        print(f"Nachricht von {user.getName()} an {empfaenger}: {text}")
    
    def leseNachrichten(self, user):
        print(f"Nachrichten für {user.getName()} werden gelesen...")

class SimpleProductService:
    def __init__(self, productList: ProductList):
        self.productlist = productList

    def getProducts(self):
        return self.productlist.get_all_products()

class UserManagement:
    def __init__(self, userInterface : IAngemeldeterUser, productService : IProduktService):
        self.users: list[AngemeldeterUser] = []
        self.herstellers: list[Hersteller] = []
        self.userInterface = userInterface
        self.productService = productService

    Account = Union[AngemeldeterUser, Hersteller]

    def _normalize_name(self, s: str) -> str:
        return (s or "").strip().casefold()

    def _find_account_by_username(self, username: str) -> Optional[Account]:
        u = self._normalize_name(username)

        # 1) Hersteller prüfen
        for h in self.herstellers:
            if self._normalize_name(h.getName()) == u:
                return h

        # 2) normale User prüfen
        for usr in self.users:
            if self._normalize_name(usr.getName()) == u:
                return usr

        return None 

    def _user_exists(self, username: str, email: str) -> bool:
        """Prüft, ob Username ODER Email bereits vergeben ist."""
        u = (username or "").strip().casefold()
        e = (email or "").strip().casefold()

        for user in self.users:
            if user.getName().strip().casefold() == u:
                return True
            if user.getEmail().strip().casefold() == e:
                return True

        return False

    def _hersteller_exists(self, username: str, email: str) -> bool:
        """Prüft, ob Hersteller-Name ODER Email bereits vergeben ist."""
        u = (username or "").strip().casefold()
        e = (email or "").strip().casefold()

        for hersteller in self.herstellers:
            if hersteller.getName().strip().casefold() == u:
                return True
            if hersteller.getEmail().strip().casefold() == e:
                return True

        return False

    def registrierenuser(self, username, email):
            if not self._user_exists(username, email):  
                self.users.append(AngemeldeterUser(username, email, self.userInterface, self.productService))            
                print(f"User {username} registered.")
                return True
                print(f"User {username} already exists.")
                return False

    def deregistrierenuser(self, user):
        for user in self.users:    
            self.users.remove(user)
            print(f"User {user.username} removed.")
            return True
            print(f"User {username} does not exist.")
            return False
        
    def registrierenhersteller(self, username, email):
            if not self._hersteller_exists(username, email):  
                self.herstellers.append(AngemeldeterUser(username, email, self.userInterface, self.productService))            
                print(f"Hersteller {username} registered.")
                return True
                print(f"Hersteller {username} already exists.")
                return False

    def deregistrierenhersteller(self, hersteller):
        for hersteller in self.herstellers:    
            self.herstellers.remove(hersteller)
            print(f"Hersteller {hersteller.username} removed.")
            return True
            print(f"Hersteller {username} does not exist.")
            return False

    def login(self, username: str) -> Account:
        acc = self._find_account_by_username(username)
        if acc is None:
            raise ValueError("Username nicht gefunden")
        return acc
        
    def list_users(self):
        return self.users