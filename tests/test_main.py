# tests/test_main.py
import unittest

from crm_usermanagement import UnregistrierterUser, AngemeldeterUser, Produkt
from productbackend import ProductList
from usermanagement import UserManagement, SimpleUserInterface, SimpleProductService


class TestMainFlowAndEdgeCases(unittest.TestCase):
    def setUp(self):
        self.product_list = ProductList()
        self.product_service = SimpleProductService(self.product_list)
        self.user_interface = SimpleUserInterface()
        self.systemzugriff = UserManagement(self.user_interface, self.product_service)

    # -------------------------
    # Basisszenarien (wie main)
    # -------------------------

    def test_register_user_and_login(self):
        unregistered = UnregistrierterUser()
        ok = unregistered.registrierenUser(
            self.systemzugriff, "MaxMustermann", "maxmustermacnn@gmail.com"
        )
        self.assertTrue(ok)
        self.assertEqual(len(self.systemzugriff.users), 1)

        acc = self.systemzugriff.login("MaxMustermann")
        self.assertIsInstance(acc, AngemeldeterUser)
        self.assertEqual(acc.getName(), "MaxMustermann")
        self.assertEqual(acc.getEmail(), "maxmustermacnn@gmail.com")

    def test_register_hersteller_and_login(self):
        unregistered = UnregistrierterUser()
        ok = unregistered.registrierenHersteller(
            self.systemzugriff, "Siemens", "verkauf@siemens.com"
        )
        self.assertTrue(ok)
        self.assertEqual(len(self.systemzugriff.herstellers), 1)

        acc = self.systemzugriff.login("Siemens")
        self.assertEqual(acc.getName(), "Siemens")
        self.assertEqual(acc.getEmail(), "verkauf@siemens.com")

    def test_publish_and_list_products(self):
        UnregistrierterUser().registrierenHersteller(
            self.systemzugriff, "Siemens", "verkauf@siemens.com"
        )
        hersteller_acc = self.systemzugriff.login("Siemens")

        produkt = Produkt(
            "Waschmaschine",
            "Siemens Waschmaschine Modell X100",
            "Waschmaschine mit 8kg Fassungsvermögen, Energieeffizienzklasse A+++",
        )
        self.product_list.veroeffentlicheProdukt(hersteller_acc.getName(), produkt)

        alle_produkte = self.product_list.get_all_products()
        self.assertEqual(len(alle_produkte), 1)

        stored = alle_produkte[0]
        self.assertIs(stored[0], produkt)         # Produktobjekt
        self.assertEqual(stored[1], "Siemens")    # Herstellername

    def test_user_can_fetch_products_via_product_service(self):
        UnregistrierterUser().registrierenUser(
            self.systemzugriff, "MaxMustermann", "maxmustermacnn@gmail.com"
        )
        user_acc = self.systemzugriff.login("MaxMustermann")
        self.assertIsInstance(user_acc, AngemeldeterUser)

        produkt = Produkt("P1", "Waschmaschine X100", "Beschreibung")
        self.product_list.veroeffentlicheProdukt("Siemens", produkt)

        produkte = user_acc.holeProdukte()
        self.assertIsInstance(produkte, list)
        self.assertEqual(len(produkte), 1)

        p, h = produkte[0]
        self.assertEqual(p.getProduktId(), "P1")
        self.assertEqual(h, "Siemens")

    def test_login_unknown_user_raises(self):
        with self.assertRaises(ValueError):
            self.systemzugriff.login("does_not_exist")

    # -------------------------
    # Edge cases (zusätzlich)
    # -------------------------

    def test_login_is_case_and_whitespace_insensitive(self):
        UnregistrierterUser().registrierenUser(
            self.systemzugriff, "MaxMustermann", "max@a.de"
        )

        # Durch _normalize_name: strip + casefold -> sollte matchen
        acc = self.systemzugriff.login("  maxmustermann  ")
        self.assertEqual(acc.getName(), "MaxMustermann")

        acc2 = self.systemzugriff.login("MAXMUSTERMANN")
        self.assertEqual(acc2.getEmail(), "max@a.de")

    def test_login_prefers_hersteller_over_user_on_same_username(self):
        # gleicher Username in beiden Listen: _find_account_by_username prüft Hersteller zuerst
        UnregistrierterUser().registrierenUser(self.systemzugriff, "ACME", "user@acme.de")
        UnregistrierterUser().registrierenHersteller(self.systemzugriff, "ACME", "sales@acme.de")

        acc = self.systemzugriff.login("acme")  # case-insensitive
        # Muss aus herstellers-Liste kommen (Email aus Hersteller-Registrierung)
        self.assertEqual(acc.getEmail(), "sales@acme.de")

    def test_user_duplicate_registration_does_not_append_second_time(self):
        unregistered = UnregistrierterUser()

        ok1 = unregistered.registrierenUser(self.systemzugriff, "Max", "max@a.de")
        self.assertTrue(ok1)
        self.assertEqual(len(self.systemzugriff.users), 1)

        ok2 = unregistered.registrierenUser(self.systemzugriff, "Max", "max@a.de")
        # In deinem aktuellen Code ist ok2 bei Duplikat wahrscheinlich None (kein return),
        # aber entscheidend: die Liste darf nicht wachsen.
        self.assertNotEqual(ok2, True)
        self.assertEqual(len(self.systemzugriff.users), 1)

    def test_user_duplicate_by_email_does_not_append(self):
        unregistered = UnregistrierterUser()

        self.assertTrue(unregistered.registrierenUser(self.systemzugriff, "Max", "dup@a.de"))
        self.assertEqual(len(self.systemzugriff.users), 1)

        ok2 = unregistered.registrierenUser(self.systemzugriff, "Andere", "dup@a.de")
        self.assertNotEqual(ok2, True)
        self.assertEqual(len(self.systemzugriff.users), 1)

    def test_hersteller_duplicate_registration_does_not_append_second_time(self):
        unregistered = UnregistrierterUser()

        ok1 = unregistered.registrierenHersteller(self.systemzugriff, "Siemens", "verkauf@siemens.com")
        self.assertTrue(ok1)
        self.assertEqual(len(self.systemzugriff.herstellers), 1)

        ok2 = unregistered.registrierenHersteller(self.systemzugriff, "Siemens", "verkauf@siemens.com")
        self.assertNotEqual(ok2, True)
        self.assertEqual(len(self.systemzugriff.herstellers), 1)

    def test_login_empty_or_none_username_raises(self):
        with self.assertRaises(ValueError):
            self.systemzugriff.login("")

        with self.assertRaises(ValueError):
            self.systemzugriff.login(None)  # normalize_name(None) -> "" -> nicht gefunden -> ValueError

    def test_productlist_empty_returns_empty(self):
        alle = self.product_list.get_all_products()
        self.assertIsInstance(alle, list)
        self.assertEqual(len(alle), 0)

    def test_productlist_multiple_products_preserve_order_and_structure(self):
        p1 = Produkt("P1", "Produkt 1", "Desc 1")
        p2 = Produkt("P2", "Produkt 2", "Desc 2")

        self.product_list.veroeffentlicheProdukt("H1", p1)
        self.product_list.veroeffentlicheProdukt("H2", p2)

        alle = self.product_list.get_all_products()
        self.assertEqual(len(alle), 2)

        # Struktur: jedes Element ist [Produkt, Hersteller]
        self.assertEqual(len(alle[0]), 2)
        self.assertEqual(len(alle[1]), 2)

        self.assertIs(alle[0][0], p1)
        self.assertEqual(alle[0][1], "H1")
        self.assertIs(alle[1][0], p2)
        self.assertEqual(alle[1][1], "H2")

    def test_product_service_returns_same_list_as_productlist(self):
        p = Produkt("P1", "Produkt 1", "Desc")
        self.product_list.veroeffentlicheProdukt("H1", p)

        fetched = self.product_service.getProducts()
        self.assertEqual(fetched, self.product_list.get_all_products())
        self.assertEqual(len(fetched), 1)


#if __name__ == "__main__":
#    unittest.main()

