from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtCore import Qt
import addStud, style
import sqlite3

con = sqlite3.connect("students.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS students (id integer PRIMARY KEY AUTOINCREMENT,
 name text, address text, add_year integer, phone text,
  branch text, curr_year text, curr_sem text)''')
con.commit()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students Record Management")
        self.setGeometry(250, 130, 1200, 800)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tab()
        self.widgets()
        self.layout()
        self.displayStudents()
        self.branchWise()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ###################Tool Bar buttons#################
        ######################Add Student###################
        self.add = QAction(QIcon('images/add.jpg'), "Add Students", self)
        self.tb.addAction(self.add)
        self.add.triggered.connect(self.addStudent)
        self.tb.addSeparator()

    def addStudent(self):
        self.close()
        self.open = addStud.AddStudents()
        window = Main()
        window.show()

    def tab(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Records")
        self.tabs.addTab(self.tab2, "Branchwise")

    def widgets(self):
        #########################tab1 widgets##############
        #####################search widgets###################
        self.searchLabel = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search Here")
        self.searchBtn = QPushButton("Search")
        self.searchBtn.setStyleSheet(style.searchBtnStyle())
        self.searchBtn.clicked.connect(self.searchStudent)
        ###############################List Widgets###################
        self.first = QRadioButton("First Year")
        self.second = QRadioButton("Second Year")
        self.third = QRadioButton("Third Year")
        self.final = QRadioButton("Final Year")
        self.listBtn = QPushButton("List")
        self.listBtn.setStyleSheet(style.listBtnStyle())
        ##################table#########################
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Student Id"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Branch"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Year"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Semester"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Address"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("Phone"))
        self.table.doubleClicked.connect(self.selectedStudent)
        #######################tab2 widgets#######################
        #######################combo widgets#######################
        self.branchLbl = QLabel("Branch")
        self.branchCombo = QComboBox()
        self.branchCombo.addItems(["CSE","ECE","IT","MECH","CHEMICAL","INSTRUMENTAL"])
        self.branchCombo.setFixedSize(300,24)
        self.searchButton = QPushButton("Find")
        self.searchButton.clicked.connect(self.branchWise)
        #########################table widget###################
        self.branchTable = QTableWidget()
        self.branchTable.setColumnCount(6)
        self.branchTable.setHorizontalHeaderItem(0, QTableWidgetItem("Student Id"))
        self.branchTable.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.branchTable.setHorizontalHeaderItem(2, QTableWidgetItem("Year"))
        self.branchTable.setHorizontalHeaderItem(3, QTableWidgetItem("Semester"))
        self.branchTable.setHorizontalHeaderItem(4, QTableWidgetItem("Address"))
        self.branchTable.setHorizontalHeaderItem(5, QTableWidgetItem("Phone"))
        self.branchTable.doubleClicked.connect(self.reSelectedStudent)

    def layout(self):
        ##################tab1 layouts##################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.topRightLayout = QHBoxLayout()
        self.topLeftLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.topLeftGroupBox = QGroupBox("Search Box")
        self.topLeftGroupBox.setStyleSheet(style.searchBox())
        self.topRightGroupBox = QGroupBox("Listings")
        self.topRightGroupBox.setStyleSheet(style.listBox())
        ##################tab2 layouts###################
        self.mainLayoutTab2 = QVBoxLayout()
        self.topLayoutTab2 = QHBoxLayout()
        self.bottomLayoutTab2 = QHBoxLayout()
        #####################setting layouts################
        ##########################tab1###################
        self.topLeftLayout.addWidget(self.searchLabel)
        self.topLeftLayout.addWidget(self.searchEntry)
        self.topLeftLayout.addWidget(self.searchBtn)
        self.topRightLayout.addWidget(self.first)
        self.topRightLayout.addWidget(self.second)
        self.topRightLayout.addWidget(self.third)
        self.topRightLayout.addWidget(self.final)
        self.topRightLayout.addWidget(self.listBtn)
        self.bottomLayout.addWidget(self.table)

        self.listBtn.clicked.connect(self.listStudents)

        self.topLeftGroupBox.setLayout(self.topLeftLayout)
        self.topRightGroupBox.setLayout(self.topRightLayout)

        self.topLayout.addWidget(self.topLeftGroupBox,50)
        self.topLayout.addWidget(self.topRightGroupBox,50)
        self.mainLayout.addLayout(self.topLayout,13)
        self.mainLayout.addLayout(self.bottomLayout,87)
        self.tab1.setLayout(self.mainLayout)
        ##################tab2#########################3
        self.topLayoutTab2.addWidget(self.branchLbl)
        self.topLayoutTab2.addWidget(self.branchCombo)

        self.topLayoutTab2.addWidget(self.searchButton)
        self.topLayoutTab2.addStretch()
        self.bottomLayoutTab2.addWidget(self.branchTable)
        self.mainLayoutTab2.addLayout(self.topLayoutTab2)
        self.mainLayoutTab2.addLayout(self.bottomLayoutTab2)
        self.tab2.setLayout(self.mainLayoutTab2)

    def displayStudents(self):
        self.table.setFont(QFont("candara", 12))
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)

        query = cur.execute("SELECT * FROM students")
        for row_data in query:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def listStudents(self):
        if self.first.isChecked():
            query = "SELECT * FROM students WHERE curr_year = 'I'"
            one = cur.execute(query).fetchall()
            for i in reversed(range(self.table.rowCount())):
                self.table.removeRow(i)
            for row_data in one:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        elif self.second.isChecked():
            query = "SELECT * FROM students WHERE curr_year = 'II'"
            two = cur.execute(query).fetchall()
            for i in reversed(range(self.table.rowCount())):
                self.table.removeRow(i)
            for row_data in two:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        elif self.third.isChecked():
            query = "SELECT * FROM students WHERE curr_year = 'III'"
            three = cur.execute(query).fetchall()
            for i in reversed(range(self.table.rowCount())):
                self.table.removeRow(i)
            for row_data in three:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        else:
            query = "SELECT * FROM students WHERE curr_year = 'IV'"
            four = cur.execute(query).fetchall()
            for i in reversed(range(self.table.rowCount())):
                self.table.removeRow(i)

            for row_data in four:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def branchWise(self):
        branch = self.branchCombo.currentText()
        self.branchTable.setFont(QFont("candara", 12))
        for i in reversed(range(self.branchTable.rowCount())):
            self.branchTable.removeRow(i)

        query =("SELECT id, name, curr_year, curr_sem, address, phone"
                            " FROM students WHERE branch = ?")
        detail = cur.execute(query,(branch,)).fetchall()
        for row_data in detail:
            row_number = self.branchTable.rowCount()
            self.branchTable.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.branchTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.branchTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectedStudent(self):
        global student_id
        listStudent = []
        for i in range(0,6):
            listStudent.append(self.table.item(self.table.currentRow(),i).text())
        student_id = listStudent[0]
        self.close()
        self.stud = updateStud()
        self.stud.show()

    def reSelectedStudent(self):
        global student_id
        listStudent = []
        for i in range(0,6):
            listStudent.append(self.branchTable.item(self.branchTable.currentRow(),i).text())
        student_id = listStudent[0]
        self.close()
        self.stud = updateStud()
        self.stud.show()

    def searchStudent(self):
        value = self.searchEntry.text()
        if value == "":
            QMessageBox.information(self, "Info", "Please enter a name or id to search")
        else:
            self.searchEntry.setText("")

            query = ("SELECT * FROM students WHERE name LIKE ? OR id LIKE ?")
            results = cur.execute(query, ('%' + value + '%','%' + value + '%')).fetchall()

            if results == []:
                QMessageBox.information(self, "Info", "No Students found for this name or ID")

            else:
                for i in reversed(range(self.table.rowCount())):
                    self.table.removeRow(i)
                for row_data in results:
                    row_number = self.table.rowCount()
                    self.table.insertRow(row_number)

                    for column_number, data in enumerate(row_data):
                        self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

class updateStud(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update")
        self.setWindowIcon(QIcon('images/icon.ico'))
        self.setGeometry(450, 130, 450, 800)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.studentDetails()
        self.layouts()
        self.widgets()

    def layouts(self):
        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()

    def studentDetails(self):
        global student_id
        query = "SELECT * FROM students WHERE id =?"
        student = cur.execute(query, (student_id,)).fetchone()
        self.name = student[1]
        self.studBranch = student[2]
        self.curr_year = student[3]
        self.curr_sem = student[4]
        self.address = student[5]
        self.phone = student[6]
        self.add_year = student[7]

    def widgets(self):
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.updateStudent)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteStudent)
        self.updateStudentImg = QLabel()
        self.img = QPixmap('images/images.png')
        self.updateStudentImg.setPixmap(self.img)
        self.titleText = QLabel("Update Student")
        self.titleText.setStyleSheet(style.titleStyle())
        #################################################
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter the name of Student")
        self.nameEntry.setText(self.name)
        self.addressEntry = QLineEdit()
        self.addressEntry.setPlaceholderText("Enter the address of Student")
        self.addressEntry.setText(self.address)

        self.addmissionYear = QLineEdit()
        self.addmissionYear.setPlaceholderText("Enter the addmission year of Student")
        self.addmissionYear.setText(str(self.add_year))

        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter the Mobile No of Student")
        self.phoneEntry.setText(str(self.phone))

        self.year = QComboBox()
        self.year.addItems(["I", "II", "III", "IV"])
        self.year.setCurrentText(self.curr_year)

        self.semester = QComboBox()
        self.semester.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])
        self.semester.setCurrentText(str(self.curr_sem))

        self.branch = QComboBox()
        self.branch.addItems(["CSE", "ECE", "IT", "MECH", "CHEMICAL", "INSTRUMENTAL"])
        self.branch.setCurrentText(self.studBranch)
        ##################################################################################
        self.topLayout.addWidget(self.updateStudentImg)
        self.topLayout.addWidget(self.titleText)
        ##############################################################################
        self.bottomLayout.addRow(QLabel("Name :"), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Address :"), self.addressEntry)
        self.bottomLayout.addRow(QLabel("Addmission Year :"), self.addmissionYear)
        self.bottomLayout.addRow(QLabel("Phone :"), self.phoneEntry)
        self.bottomLayout.addRow(QLabel("Branch:"), self.branch)
        self.bottomLayout.addRow(QLabel("Current Year:"), self.year)
        self.bottomLayout.addRow(QLabel("Current Sem :"), self.semester)
        self.bottomLayout.addRow(" ", self.submitBtn)
        self.submitBtn.setStyleSheet(style.ButtonStyle())
        self.bottomLayout.addRow(" ", self.deleteBtn)
        self.deleteBtn.setStyleSheet(style.deleteButtonStyle())
        ###############################################################################
        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.bottomLayout)
        self.setLayout(self.layout)

    def deleteStudent(self):
        global student_id
        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete the Student",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM students WHERE id =?"
                cur.execute(query,(student_id,))
                con.commit()
                QMessageBox.information(self, "Information", "Student has been deleted")
                self.close()
                self.main = Main()
            except:
                QMessageBox.information(self, "Information", "Student can not be deleted")

    def updateStudent(self):
        global student_id
        name = self.nameEntry.text()
        add = self.addressEntry.text()
        addYear = self.addmissionYear.text()
        phone = self.phoneEntry.text()
        branch = self.branch.currentText()
        year = self.year.currentText()
        sem = self.semester.currentText()
        if (self.name != ""):
            try:
                query = "UPDATE students SET name =?, address =?, add_year =?, phone =?, branch =?," \
                        "curr_year =?,curr_sem =? WHERE id =?"
                cur.execute(query,(name, add, addYear,phone, branch, year, sem,student_id))
                con.commit()
                QMessageBox.information(self, "Information", "Student details updated")
                self.close()
                self.main = Main()
            except:
                QMessageBox.information(self, "Information", "Student details not updated")
        else:
            QMessageBox.information(self, "Information", "Please Enter Name")

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()


