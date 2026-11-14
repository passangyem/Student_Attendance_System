
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QScrollArea
)
from PyQt6.QtCore import Qt


class AboutSystemPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F5F8;
                font-family: Arial;
                font-size: 13px;
            }

            QLabel#heading {
                color: #6A1B9A;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#subheading {
                color: #6A1B9A;
                font-size: 17px;
                font-weight: bold;
            }

            QFrame#information {
                background-color: white;
                border: 1px solid #DDDDDD;
                border-radius: 8px;
            }

            QLabel#content {
                color: #444444;
                font-size: 13px;
                padding: 5px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(15)

        # Page Heading
        heading = QLabel("About System")
        heading.setObjectName("heading")
        main_layout.addWidget(heading)

        subheading = QLabel("About the Application")
        subheading.setObjectName("subheading")
        main_layout.addWidget(subheading)

        # Information Container
        information = QFrame()
        information.setObjectName("information")

        info_layout = QVBoxLayout(information)
        info_layout.setContentsMargins(25, 20, 25, 20)

        content = QLabel("""
        <b>PROJECT INFORMATION</b>
        <br><br>

        STUDENT ATTENDANCE MANAGEMENT SYSTEM

        <br><br>
        Developer: Passang Gyem<br>
        Framework: Python PyQt6<br>
        Database: SQLite<br>
        Programming Language: Python<br>
        Application Version: 1.0

        <br><br><br>

        <b>PROJECT DESCRIPTION</b>
        <br>
        This desktop application is developed to manage
        student information and record daily attendance.
        It helps users register students, mark attendance,
        search records and manage attendance information.

        <br><br>

        <b>MAIN FEATURES</b>
        <br>
        • Student registration<br>
        • View student records<br>
        • Search student information<br>
        • Update and delete student records<br>
        • Mark students Present or Absent<br>
        • View attendance records<br>
        • Attendance summaries<br>
        • SQLite database storage
        """)

        content.setObjectName("content")
        content.setTextFormat(Qt.TextFormat.RichText)
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignmentFlag.AlignLeft |
                             Qt.AlignmentFlag.AlignTop)

        info_layout.addWidget(content)

        main_layout.addWidget(information)
        main_layout.addStretch()
