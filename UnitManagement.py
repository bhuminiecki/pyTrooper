from PyQt5.QtWidgets import *

from BuildingForm import BuildingForm
from BuildingPreview import BuildingPreview
from VehicleForm import VehicleForm
from VehiclePreview import VehiclePreview
from Utilities import set_info_tab, create_table
from connector import Connector

# GUI
# app = QApplication([])

budynki = [["AB3", "Wychodek"], ["DG2", "Toaleta"], ["BG7", "Urynał"], ["QV1", "Ubikacja"], ["HU1", "Kibel"]]
oficerowie = [["Stasiek", "Dupas", "9450245291"], ["Krzysiek", "Kasztan", "9150258790"],
              ["Wiechu", "Szachista", "5540235263"]]
pojazdy = [["1", "Maluch"], ["2", "BMW"], ["3", "Silvia"], ["4", "Corolla"], ["5", "Rudy"], ["6", "Jagdpanzer"],
           ["7", "Rower"], ["8", "Turbosmiglowiec"]]


class UnitManagement(QTabWidget):
    def __init__(self, id_jednostki):
        global budynki, oficerowie, pojazdy
        super().__init__()
        self.unit_id = id_jednostki
        self.setWindowTitle("Zarządzanie jednostką")
        self.setMinimumSize(400, 350)
        self.infoTab = set_info_tab(id_jednostki)
        self.insertTab(0, self.infoTab, "Ogólne")
        self.listTab1 = None
        self.refresh_buildings()
        self.listTab2 = None
        self.refresh_vehicles()
        self.listTab3 = None
        self.refresh_officers()
        self.addWindow = None
        self.previewWindow = None
        self.setCurrentIndex(0)

    def refresh_buildings(self):
        self.removeTab(1)
        self.listTab1 = self.create_list_tab(["Oznaczenie", "Rola"],
                                             Connector.get_filtered("budynki", ["oznaczenie", "rola_budynku"],
                                                                    " WHERE id_jednostki = " + self.unit_id), "budynki")
        self.insertTab(1, self.listTab1, "Budynki")
        self.setCurrentIndex(1)

    def refresh_vehicles(self):
        self.removeTab(2)
        self.listTab2 = self.create_list_tab(["ID", "Producent", "Model"], Connector.get_filtered("pojazdy", ["id_pojazdu", "producent", "model"],
                                                                                     " WHERE id_jednostki = " + self.unit_id), "pojazdy")
        self.insertTab(2, self.listTab2, "Pojazdy")
        self.setCurrentIndex(2)

    def refresh_officers(self):
        self.removeTab(3)
        self.listTab3 = self.create_list_tab(["Imię", "Nazwisko", "PESEL"],
                                             Connector.get_filtered("oficerowie", ["imie", "nazwisko", "pesel"],
                                                                    " WHERE id_jednostki = " + self.unit_id), "oficerowie")
        self.insertTab(3, self.listTab3, "Oficerowie")
        self.setCurrentIndex(3)

    def create_list_tab(self, column_names, items, type):
        tab = QWidget()
        layout = QVBoxLayout()

        tabela = create_table(column_names, items)
        # lista = QListWidget()
        # for item in items:
        #    lista.addItem(item)
        # layout.addWidget(lista)
        layout.addWidget(tabela)

        buttons = QGroupBox("Zarządzanie")
        boxLayout = QHBoxLayout()
        addButton = QPushButton("Dodaj")
        rmvButton = QPushButton("Usuń")
        editButton = QPushButton("Edytuj")
        boxLayout.addWidget(addButton)
        boxLayout.addWidget(rmvButton)
        boxLayout.addWidget(editButton)
        buttons.setLayout(boxLayout)

        # addButton.clicked.connect(show_add_windows(type, id))
        if type == "budynki":
            addButton.clicked.connect(self.add_building)
            rmvButton.clicked.connect(self.delete_buildings)
            self.tabela_budynki = tabela
            self.tabela_budynki.cellDoubleClicked.connect(self.building_preview)
        if type == "pojazdy":
            addButton.clicked.connect(self.add_vehicle)
            rmvButton.clicked.connect(self.delete_vehicles)
            self.tabela_pojazdy = tabela
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vehicle_preview)

        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def add_building(self):
        self.addWindow = BuildingForm(self.unit_id)
        self.addWindow.commited.connect(self.refresh_buildings)
        self.addWindow.show()

    def add_vehicle(self):
        self.addWindow = VehicleForm(self.unit_id, "Dostępny")
        self.addWindow.commited.connect(self.refresh_vehicles)
        self.addWindow.show()

    def delete_buildings(self):
        selection = self.tabela_budynki.selectedItems()
        if selection:
            res = []
            for x in selection:
                res.append(self.tabela_budynki.item(x.row(), 0).text())
            res = list(dict.fromkeys(res))
            Connector.delete_items("budynki", res, "oznaczenie", str)
            self.refresh_buildings()

    def delete_vehicles(self):
        selection = self.tabela_pojazdy.selectedItems()
        if selection:
            res = []
            for x in selection:
                res.append(self.tabela_pojazdy.item(x.row(), 0).text())
            res = list(dict.fromkeys(res))
            Connector.delete_items("pojazdy", res, "id_pojazdu", int)
            self.refresh_vehicles()

    def building_preview(self, rowid):
        item = self.tabela_budynki.item(rowid, 0)
        self.previewWindow = BuildingPreview(item.text())
        self.previewWindow.show()

    def vehicle_preview(self, rowid):
        item = self.tabela_pojazdy.item(rowid, 0)
        self.previewWindow = VehiclePreview(item.text())
        self.previewWindow.show()
