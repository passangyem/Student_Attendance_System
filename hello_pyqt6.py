import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle("Hello World - PyQt6")
window.setGeometry(100, 100, 400, 250)

# Create a label
label = QLabel("Hello World!")

# Set font size
label.setStyleSheet("font-size: 20px;")

# Set layout
layout = QVBoxLayout()
layout.addWidget(label)
window.setLayout(layout)

# Display the window
window.show()

# Run the application
sys.exit(app.exec())