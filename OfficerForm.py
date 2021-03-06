from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector
from config import rx


class OfficerForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, pesel=None):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.oldPesel = pesel
        self.setWindowTitle("Formularz (oficer)")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        gap = QLabel()
        gap.setFixedHeight(1)
        disclaimer = QLabel('<i><font color="#707070">tekst</font> - pole nieobowiązkowe</i>')
        disclaimer.setAlignment(Qt.AlignRight)
        self.layout.addRow(gap)
        self.layout.addRow(disclaimer)
        self.setLayout(self.layout)
        self.setMinimumSize(280, 200)
        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.imie = QLineEdit()
        self.imie.setMaxLength(12)
        self.imie.setValidator(QRegExpValidator(QRegExp(rx)))
        self.nazwisko = QLineEdit()
        self.nazwisko.setMaxLength(20)
        self.nazwisko.setValidator(QRegExpValidator(QRegExp(rx)))
        self.data_ur = QLineEdit()
        self.data_ur.setInputMask("9999-99-99")
        self.wyznanie = QLineEdit()
        self.wyznanie.setMaxLength(15)
        self.wyznanie.setValidator(QRegExpValidator(QRegExp(rx)))
        self.grupa_krwi = QComboBox()
        self.grupa_krwi.addItems(Connector.get_enum("grupa_krwi_type"))
        self.ranga = QComboBox()
        rangi = Connector.get_table_data("rangi ORDER BY zold ASC", ["nazwa_rangi"])
        for i in range(len(rangi)):
            rangi[i] = rangi[i][0]
        self.ranga.addItems(rangi)
        self.budynek = QComboBox()
        filter = " WHERE id_jednostki = " + str(self.id_jednostki) + " ORDER BY oznaczenie ASC";
        budynki = Connector.get_filtered("budynki", ["oznaczenie"], filter)
        for i in range(len(budynki)):
            budynki[i] = budynki[i][0]
        self.budynek.addItems(budynki)
        if self.oldPesel is not None:
            oldData = Connector.get_record("oficerowie", ["imie", "nazwisko", "ranga", "data_ur", "grupa_krwi",
                                                          "wyznanie", "budynek"],
                                           self.oldPesel, "pesel", str)
            self.imie.setText(oldData[0])
            self.nazwisko.setText(oldData[1])
            self.pesel = QLabel(self.oldPesel)
            self.ranga.setCurrentText(oldData[2])
            self.data_ur.setText(str(oldData[3]))
            self.grupa_krwi.setCurrentText(oldData[4])
            self.wyznanie.setText(oldData[5])
            self.budynek.setCurrentText(oldData[6])
        else:
            self.pesel = QLineEdit()
            self.pesel.setMaxLength(11)
            self.pesel.setValidator(QRegExpValidator(QRegExp("\d{11}")))
        self.layout.addRow("Imię: ", self.imie)
        self.layout.addRow("Nazwisko: ", self.nazwisko)
        self.layout.addRow("PESEL: ", self.pesel)
        self.layout.addRow("Data urodzenia: ", self.data_ur)
        self.layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))
        self.layout.addRow("Grupa krwi: ", self.grupa_krwi)
        self.layout.addRow("Ranga: ", self.ranga)
        self.layout.addRow("Budynek: ", self.budynek)
        self.layout.addRow(QLabel('<font color="#707070">Wyznanie: </font>'), self.wyznanie)

    def confirm(self):
        imie = self.imie.text()
        nazwisko = self.nazwisko.text()
        data_ur = self.data_ur.text()
        grupa_krwi = self.grupa_krwi.currentText()
        wyznanie = self.wyznanie.text()
        ranga = self.ranga.currentText()
        budynek = self.budynek.currentText()
        if self.oldPesel is not None:
            if (Connector.update_row("oficerowie",
                                     ["imie", "nazwisko", "data_ur", "wyznanie", "budynek", "ranga", "grupa_krwi"],
                                     [imie, nazwisko, data_ur, wyznanie, budynek, ranga, grupa_krwi], self.oldPesel,
                                     "pesel", str)):
                self.commited.emit()
                self.close()
        else:
            pesel = self.pesel.text()
            if(Connector.insert_row("oficerowie", ["pesel", "imie", "nazwisko", "data_ur", "wyznanie", "id_jednostki",
                                                   "budynek", "ranga", "grupa_krwi"],
                                    [pesel, imie, nazwisko, data_ur, wyznanie, self.id_jednostki, budynek, ranga,
                                    grupa_krwi])):
                self.commited.emit()
                self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = OfficerForm("1")
    window.show()
    app.exec_()
