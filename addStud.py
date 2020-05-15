from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import recordManager
import style

con = sqlite3.connect("students.db")
cur = con.cursor()

class AddStudents(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setWindowIcon(QIcon('images/icon.ico'))
        self.setGeometry(450, 130, 450, 800)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.layout()
        self.widgets()

    def layout(self):
        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()

    def widgets(self):
        self.submitBtn = QPushButton("Submit")
        self.addStudentImg = QLabel()
        self.img = QPixmap('images/user.png')
        self.addStudentImg.setPixmap(self.img)
        self.titleText = QLabel("Add Student")
        self.titleText.setStyleSheet(style.titleStyle())
        #################################################
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter the name of Student")
        self.addressEntry = QLineEdit()
        self.addressEntry.setPlaceholderText("Enter the address of Student")

        self.addmissionYear = QLineEdit()
        self.addmissionYear.setPlaceholderText("Enter the addmission year of Student")

        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter the Mobile No of Student")

        self.year = QComboBox()
        self.year.addItems(["I","II","III","IV"])

        self.semester = QComboBox()
        self.semester.addItems(["1","2","3","4","5","6","7","8"])

        self.branch = QComboBox()
        self.branch.addItems(["CSE","ECE","IT","MECH","CHEMICAL","INSTRUMENTAL"])
        ##################################################################################
        self.topLayout.addWidget(self.addStudentImg)
        self.topLayout.addWidget(self.titleText)
        ##############################################################################
        self.bottomLayout.addRow(QLabel("Name :"),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Address :"),self.addressEntry)
        self.bottomLayout.addRow(QLabel("Addmission Year :"),self.addmissionYear)
        self.bottomLayout.addRow(QLabel("Phone :"),self.phoneEntry)
        self.bottomLayout.addRow(QLabel("Branch:"),self.branch)
        self.bottomLayout.addRow(QLabel("Current Year:"),self.year)
        self.bottomLayout.addRow(QLabel("Current Sem :"),self.semester)
        self.bottomLayout.addRow(" ",self.submitBtn)
        self.submitBtn.setStyleSheet(style.ButtonStyle())
        self.submitBtn.clicked.connect(self.dbHandle)
        ###############################################################################
        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.bottomLayout)
        self.setLayout(self.layout)

    def dbHandle(self):
        name = self.nameEntry.text()
        add = self.addressEntry.text()
        addYear = self.addmissionYear.text()
        phone = self.phoneEntry.text()
        branch = self.branch.currentText()
        year = self.year.currentText()
        sem = self.semester.currentText()

        if (name != ""):
            try:
                query = "INSERT INTO 'students' (name,address,add_year,phone,branch,curr_year,curr_sem)" \
                        " VALUES(?,?,?,?,?,?,?)"
                cur.execute(query, (name, add, addYear, phone, branch, year, sem))
                con.commit()
                QMessageBox.information(self, "Information", "Student has been added")
                self.close()
                self.main = recordManager.Main()
                self.main.show()
            except:
                QMessageBox.information(self, "Information", "Student has not been added")

        else:
            QMessageBox.information(self, "Information", "Please enter name")