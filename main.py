import sys
import re
import sqlite3
from about_system import AboutSystemPage
from datetime import date

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
    QStackedWidget, QLineEdit, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QDateEdit,
    QStatusBar
)

from PyQt6.QtCore import QDate
import database


class AttendanceSystem(QMainWindow):

    def __init__(self):
        super().__init__()

        database.create_tables()

        self.setWindowTitle(
            "Student Attendance Management System - Passang Gyem (08230162)"
        )

        self.setMinimumSize(1050, 650)
        self.resize(1200, 720)

        self.editing_student_id = None
        self.editing_attendance_id = None

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #E6E6FA;
                font-family: Arial;
                font-size: 13px;
            }
            QLabel#Heading {
                color: #C8A2E8;
                font-weight: bold;
            }
            QFrame#Sidebar {
                background-color: #142B4A;
                border: none;
            }

            QLabel#Logo {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
            }

            QPushButton#NavButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 13px;
                border: none;
                border-radius: 6px;
            }

            QPushButton#NavButton:hover {
                background-color: #1E5AA8;
            }

            QPushButton {
                background-color: #1E5AA8;
                color: white;
                padding: 9px 14px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #16477F;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #C9D3DF;
                border-radius: 5px;
                padding: 8px;
                min-height: 20px;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #D5DDE7;
                gridline-color: #E3E8EF;
                selection-background-color: #DCEBFA;
                selection-color: #142B4A;
            }

            QHeaderView::section {
                background-color: #EAF1F8;
                color: #142B4A;
                padding: 9px;
                border: none;
                font-weight: bold;
            }

            QLabel#Heading {
                color:#C8A2E8;
                font-size: 23px;
                font-weight: bold;
            }

            QLabel#CardTitle {
                color: #536579;
                font-size: 13px;
            }

            QLabel#CardNumber {
                color: #C8A2E8;
                font-size: 27px;
                font-weight: bold;
            }
        """)

        self.create_menu()
        self.create_interface()
        self.load_students()
        self.load_attendance()
        self.update_dashboard()

    # MENU BAR

    def create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        refresh_action = file_menu.addAction("Refresh")
        refresh_action.triggered.connect(self.refresh_all)

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        help_menu = menu.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    # MAIN INTERFACE

    def create_interface(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        side_layout = QVBoxLayout(sidebar)

        logo = QLabel("ATTENDANCE\nMANAGEMENT")
        logo.setObjectName("Logo")
        side_layout.addWidget(logo)

        self.stack = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.students_page = self.create_students_page()
        self.attendance_page = self.create_attendance_page()
        self.about_page = AboutSystemPage()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.students_page)
        self.stack.addWidget(self.attendance_page)
        self.stack.addWidget(self.about_page)

        nav_buttons = [
            ("Dashboard", 0),
            ("Students", 1),
            ("Attendance", 2),
            ("About System", 3)
        ]

        for text, index in nav_buttons:

            button = QPushButton(text)
            button.setObjectName("NavButton")

            button.clicked.connect(
                lambda checked=False, i=index:
                self.stack.setCurrentIndex(i)
            )

            side_layout.addWidget(button)

        side_layout.addStretch()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(
            "Student Attendance Management System"
        )

    # DASHBOARD PAGE

    def create_dashboard_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(25, 25, 25, 25)

        heading = QLabel("Dashboard")
        heading.setObjectName("Heading")

        welcome = QLabel(
            "Welcome to the Student Attendance Management System."
        )

        layout.addWidget(heading)
        layout.addWidget(welcome)

        grid = QGridLayout()

        self.total_label = self.create_card("Total Students")
        self.present_label = self.create_card("Present Today")
        self.absent_label = self.create_card("Absent Today")
        self.late_label = self.create_card("Late Today")

        grid.addWidget(self.total_label[0], 0, 0)
        grid.addWidget(self.present_label[0], 0, 1)
        grid.addWidget(self.absent_label[0], 1, 0)
        grid.addWidget(self.late_label[0], 1, 1)

        layout.addLayout(grid)
        layout.addStretch()

        refresh = QPushButton("Refresh Dashboard")
        refresh.clicked.connect(self.update_dashboard)

        layout.addWidget(refresh)

        return page

    def create_card(self, title):

        card = QFrame()

        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 9px;
                border: 1px solid #E0E6ED;
            }
        """)

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        number_label = QLabel("0")
        number_label.setObjectName("CardNumber")

        layout.addWidget(title_label)
        layout.addWidget(number_label)

        return card, number_label

    def update_dashboard(self):

        today = date.today().isoformat()

        total, present, absent, late = database.get_dashboard_counts(today)

        self.total_label[1].setText(str(total))
        self.present_label[1].setText(str(present))
        self.absent_label[1].setText(str(absent))
        self.late_label[1].setText(str(late))

    # STUDENT PAGE

    def create_students_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(25, 25, 25, 25)

        heading = QLabel("Student Management")
        heading.setObjectName("Heading")

        layout.addWidget(heading)

        form = QGridLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter student name")
        self.name_input.setMaxLength(50)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter student ID")
        self.id_input.setMaxLength(15)

        self.year_input = QComboBox()
        self.year_input.addItems([
            "1st Year", "2nd Year", "3rd Year", "4th Year"
        ])

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female"])

        form.addWidget(QLabel("Student Name"), 0, 0)
        form.addWidget(self.name_input, 0, 1)

        form.addWidget(QLabel("Student ID"), 0, 2)
        form.addWidget(self.id_input, 0, 3)

        form.addWidget(QLabel("Academic Year"), 1, 0)
        form.addWidget(self.year_input, 1, 1)

        form.addWidget(QLabel("Gender"), 1, 2)
        form.addWidget(self.gender_input, 1, 3)

        layout.addLayout(form)

        button_row = QHBoxLayout()

        self.save_student_button = QPushButton("Add Student")
        self.save_student_button.clicked.connect(self.save_student)

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_student)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_student)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_student_form)

        button_row.addWidget(self.save_student_button)
        button_row.addWidget(edit_button)
        button_row.addWidget(delete_button)
        button_row.addWidget(clear_button)

        layout.addLayout(button_row)

        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText(
            "Search by student name or ID..."
        )

        self.student_search.textChanged.connect(self.search_student)

        layout.addWidget(self.student_search)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(4)

        self.student_table.setHorizontalHeaderLabels([
            "Student ID", "Student Name", "Academic Year", "Gender"
        ])

        self.prepare_table(self.student_table)

        layout.addWidget(self.student_table)

        return page

    def prepare_table(self, table):

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        table.setAlternatingRowColors(True)

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def load_students(self, rows=None):

        if rows is None:
            rows = database.get_students()

        self.student_table.setRowCount(0)

        for row_data in rows:

            row = self.student_table.rowCount()
            self.student_table.insertRow(row)

            for column, value in enumerate(row_data):

                self.student_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

    def save_student(self):

        name = self.name_input.text().strip()
        student_id = self.id_input.text().strip().upper()

        year = self.year_input.currentText()
        gender = self.gender_input.currentText()

        if not re.fullmatch(r"[A-Za-z][A-Za-z '-]{1,49}", name):

            QMessageBox.warning(
                self,
                "Invalid Name",
                "Enter a name with at least 2 letters. "
                "Numbers and special symbols are not allowed."
            )

            return

        if not re.fullmatch(r"[A-Za-z0-9-]{3,15}", student_id):

            QMessageBox.warning(
                self,
                "Invalid Student ID",
                "Student ID must contain 3 to 15 letters, numbers or hyphens."
            )

            return

        try:

            if self.editing_student_id:

                database.update_student(
                    self.editing_student_id, name, year, gender
                )

                QMessageBox.information(
                    self,
                    "Updated",
                    "Student details updated successfully."
                )

            else:

                database.add_student(student_id, name, year, gender)

                QMessageBox.information(
                    self,
                    "Saved",
                    "Student added successfully."
                )

            self.clear_student_form()
            self.load_students()
            self.update_dashboard()
            self.load_attendance()

        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                "Duplicate ID",
                "This student ID already exists."
            )

    def edit_student(self):

        row = self.student_table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Student",
                "Please select a student to edit."
            )

            return

        self.editing_student_id = self.student_table.item(row, 0).text()

        self.id_input.setText(self.editing_student_id)
        self.id_input.setEnabled(False)

        self.name_input.setText(
            self.student_table.item(row, 1).text()
        )

        self.year_input.setCurrentText(
            self.student_table.item(row, 2).text()
        )

        self.gender_input.setCurrentText(
            self.student_table.item(row, 3).text()
        )

        self.save_student_button.setText("Update Student")

    def delete_student(self):

        row = self.student_table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Student",
                "Please select a student to delete."
            )

            return

        student_id = self.student_table.item(row, 0).text()

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete this student and their attendance records?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            database.delete_student(student_id)

            self.load_students()
            self.load_attendance()
            self.update_dashboard()

            QMessageBox.information(
                self,
                "Deleted",
                "Student deleted successfully."
            )

    def clear_student_form(self):

        self.name_input.clear()
        self.id_input.clear()

        self.id_input.setEnabled(True)

        self.year_input.setCurrentIndex(0)
        self.gender_input.setCurrentIndex(0)

        self.editing_student_id = None

        self.save_student_button.setText("Add Student")

    def search_student(self, keyword):

        self.load_students(database.search_students(keyword))

    # ATTENDANCE PAGE

    def create_attendance_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(25, 25, 25, 25)

        heading = QLabel("Attendance Recording")
        heading.setObjectName("Heading")

        layout.addWidget(heading)

        form = QGridLayout()

        self.attendance_student = QComboBox()

        self.attendance_date = QDateEdit()
        self.attendance_date.setCalendarPopup(True)
        self.attendance_date.setDate(QDate.currentDate())
        self.attendance_date.setDisplayFormat("yyyy-MM-dd")

        self.attendance_status = QComboBox()
        self.attendance_status.addItems([
            "Present", "Absent", "Late"
        ])

        form.addWidget(QLabel("Select Student"), 0, 0)
        form.addWidget(self.attendance_student, 0, 1)

        form.addWidget(QLabel("Date"), 0, 2)
        form.addWidget(self.attendance_date, 0, 3)

        form.addWidget(QLabel("Status"), 1, 0)
        form.addWidget(self.attendance_status, 1, 1)

        layout.addLayout(form)

        button_row = QHBoxLayout()

        mark_button = QPushButton("Mark Attendance")
        mark_button.clicked.connect(self.mark_attendance)

        edit_button = QPushButton("Update Selected")
        edit_button.clicked.connect(self.edit_attendance)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_attendance)

        button_row.addWidget(mark_button)
        button_row.addWidget(edit_button)
        button_row.addWidget(delete_button)

        layout.addLayout(button_row)

        filter_row = QHBoxLayout()

        self.attendance_search = QLineEdit()
        self.attendance_search.setPlaceholderText(
            "Search by student name or ID..."
        )

        self.attendance_search.textChanged.connect(
            self.filter_attendance
        )

        self.filter_date = QDateEdit()
        self.filter_date.setCalendarPopup(True)
        self.filter_date.setDisplayFormat("yyyy-MM-dd")
        self.filter_date.setDate(QDate.currentDate())

        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "All", "Present", "Absent", "Late"
        ])

        filter_button = QPushButton("Apply Filter")
        filter_button.clicked.connect(self.filter_attendance)

        clear_filter = QPushButton("Show All")
        clear_filter.clicked.connect(self.clear_attendance_filter)

        filter_row.addWidget(self.attendance_search)
        filter_row.addWidget(self.filter_date)
        filter_row.addWidget(self.status_filter)
        filter_row.addWidget(filter_button)
        filter_row.addWidget(clear_filter)

        layout.addLayout(filter_row)

        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(6)

        self.attendance_table.setHorizontalHeaderLabels([
            "Record ID", "Student ID", "Student Name",
            "Academic Year", "Date", "Status"
        ])

        self.prepare_table(self.attendance_table)

        layout.addWidget(self.attendance_table)

        return page

    def refresh_student_selector(self):

        self.attendance_student.clear()

        self.attendance_student.addItem("Select a student", None)

        for student_id, name, year, gender in database.get_students():

            self.attendance_student.addItem(
                f"{name} ({student_id})", student_id
            )

    def mark_attendance(self):

        student_id = self.attendance_student.currentData()

        if not student_id:

            QMessageBox.warning(
                self,
                "Missing Student",
                "Please select a student."
            )

            return

        selected_date = self.attendance_date.date().toString("yyyy-MM-dd")
        status = self.attendance_status.currentText()

        try:

            database.mark_attendance(student_id, selected_date, status)

            QMessageBox.information(
                self,
                "Saved",
                "Attendance recorded successfully."
            )

            self.load_attendance()
            self.update_dashboard()

        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                "Duplicate Record",
                "Attendance has already been recorded for this student "
                "on this date. Select the record and use Update Selected."
            )

    def load_attendance(self, rows=None):

        if rows is None:
            rows = database.get_attendance()

        self.attendance_table.setRowCount(0)

        for record in rows:

            row = self.attendance_table.rowCount()
            self.attendance_table.insertRow(row)

            for column, value in enumerate(record):

                self.attendance_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

        self.refresh_student_selector()

    def edit_attendance(self):

        row = self.attendance_table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Record",
                "Please select an attendance record to update."
            )

            return

        self.editing_attendance_id = int(
            self.attendance_table.item(row, 0).text()
        )

        current_status = self.attendance_table.item(row, 5).text()

        self.attendance_status.setCurrentText(current_status)

        answer = QMessageBox.question(
            self,
            "Update Attendance",
            "Update this record's attendance status?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            try:

                database.update_attendance(
                    self.editing_attendance_id,
                    self.attendance_status.currentText()
                )

                self.load_attendance()
                self.update_dashboard()

                QMessageBox.information(
                    self,
                    "Updated",
                    "Attendance updated successfully."
                )

            except sqlite3.Error as error:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(error)
                )

        self.editing_attendance_id = None

    def delete_attendance(self):

        row = self.attendance_table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Record",
                "Please select an attendance record to delete."
            )

            return

        record_id = int(self.attendance_table.item(row, 0).text())

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this attendance record?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            database.delete_attendance(record_id)

            self.load_attendance()
            self.update_dashboard()

    def filter_attendance(self):

        keyword = self.attendance_search.text().strip()

        selected_date = self.filter_date.date().toString("yyyy-MM-dd")

        status = self.status_filter.currentText()

        rows = database.search_attendance(
            keyword, selected_date, status
        )

        self.load_attendance(rows)

    def clear_attendance_filter(self):

        self.attendance_search.clear()

        self.filter_date.setDate(QDate.currentDate())

        self.status_filter.setCurrentIndex(0)

        self.load_attendance()

    # OTHER FUNCTIONS

    def refresh_all(self):

        self.load_students()
        self.load_attendance()
        self.update_dashboard()

        self.statusBar().showMessage("Data refreshed", 3000)

    def show_about(self):

        QMessageBox.about(
            self,
            "About",
            "Student Attendance Management System\n\n"
            "Developed by: Passang Gyem\n"
            "Student ID: 08230162\n"
            "Framework: PyQt6\n"
            "Database: SQLite"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = AttendanceSystem()
    window.show()

    sys.exit(app.exec())