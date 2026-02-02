from abc import ABC, abstractmethod
from typing import Protocol

#Interfaces:
class ISystemZugriff(Protocol):
    def registrierenuser(self, UnregistrierterUser) -> None: ...
    def registrierenhersteller(self, UnregistrierterUser) -> None: ...
    def login(self, userdata) -> None: ...

class IAngemeldeterUser(Protocol): # Nachrichtenfunktionalität
    def sendeNachricht(self, user, empfaenger, text) -> None: ...
    def leseNachrichten(self, user) -> None: ...

class IHerstellerInterface(Protocol):
    def veroeffentlicheProdukt(self, username, Produkt) -> None: ...

class IProduktService(Protocol):
    def getProduktId(self, hersteller) -> None: ...
    def getProducts(self) -> None: ...

#Abstrakte Klassen:
class Mensch(ABC):
    pass

class AngemeldeterUser(Mensch):
    def __init__(self, name, mail, user_interface: IAngemeldeterUser, product_service: IProduktService):
        self.name = name
        self.email = mail
        self.UserInterface = user_interface
        self.ProduktService = product_service

    
    def getName(self):
        return self.name
    
    
    def getEmail(self):
        return self.email
    
    def sendeNachricht(self, empfaenger, text):
        self.UserInterface.sendeNachricht(self, empfaenger, text)
   
    def leseNachrichten(self):
        self.UserInterface.leseNachrichten(self)
    
    def holeProdukte(self):
        return self.ProduktService.getProducts()

class UnregistrierterUser(Mensch):
    #def __init__(self, name, mail):
    #    self.name = name
    #    self.email = mail
    
    def registrierenUser(self, systemZugriff: ISystemZugriff, name, email):
        """Erstellt einen konkreten User (z.B. StandardUser)"""
        return systemZugriff.registrierenuser(name, email)
    def registrierenHersteller(self, systemZugriff: ISystemZugriff, name, email):
        """Erstellt einen konkreten User (z.B. StandardUser)"""
        return systemZugriff.registrierenhersteller(name, email)


class Hersteller(AngemeldeterUser):
    def __init__(self, name, mail, user_interface: IAngemeldeterUser, product_service: IProduktService, hersteller_interface: IHerstellerInterface):
        super().__init__(name, mail, user_interface, product_service)
        self.HerstellerInterface = hersteller_interface
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def produktVeroeffentlichen(self, Produkt):
        self.HerstellerInterface.veroeffentlicheProdukt(self.name, Produkt)

class Produkt:
    def __init__(self, produktId, name, beschreibung):
        self.produktId = produktId
        self.name = name
        self.beschreibung = beschreibung
    
    def getProduktId(self):
        return self.produktId
    
    def getName(self):
        return self.name
    
    def getBeschreibung(self):
        return self.beschreibung


