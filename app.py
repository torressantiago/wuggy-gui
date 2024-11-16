import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from wuggy import WuggyGenerator

# Assuming your WuggyGenerator and methods are available here
# from your_wuggy_module import WuggyGenerator

class WuggyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wuggy Pseudoword Generator")
        self.setGeometry(100, 100, 600, 500)

        self.language_label = QLabel("Select Language:")
        self.language_combobox = QComboBox()
        self.language_combobox.addItems(["English", "Spanish"])
        self.language_combobox.setCurrentIndex(0)

        self.sequence_label = QLabel("Input Sequences (comma-separated):")
        self.sequence_entry = QLineEdit()

        self.candidates_label = QLabel("Number of Candidates per Sequence:")
        self.candidates_entry = QLineEdit()

        self.generate_button = QPushButton("Generate Pseudowords")
        self.generate_button.clicked.connect(self.generate_pseudowords)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)

        self.output_label = QLabel("Generated Pseudowords:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # Layouts
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.language_label)
        input_layout.addWidget(self.language_combobox)
        input_layout.addWidget(self.sequence_label)
        input_layout.addWidget(self.sequence_entry)
        input_layout.addWidget(self.candidates_label)
        input_layout.addWidget(self.candidates_entry)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.export_button)

        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_text)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

    def generate_pseudowords(self):
        # Retrieve user inputs
        language = self.language_combobox.currentText().lower()
        language = "orthographic_"+language
        input_sequences = self.sequence_entry.text().replace(" ", "")
        input_sequences = input_sequences.split(",")

        try:
            ncandidates = int(self.candidates_entry.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Please enter a valid number for candidates.")
            return
        
        # Create the appropriate generator object
        try:
            generator = WuggyGenerator()  # Use the correct constructor
            generator.download_language_plugin(language, auto_download=True)
            generator.load(language)
            pseudoword_matches = generator.generate_classic(input_sequences, ncandidates_per_sequence=ncandidates)

            # Display the pseudowords in the text box
            self.output_text.clear()  # Clear existing content
            for match in pseudoword_matches:
                pseudoword = match["pseudoword"]
                self.output_text.append(pseudoword)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_help(self):
        help_message = """
        This application generates pseudowords based on input sequences.

        Steps:
        1. Select a language (English or Spanish).
        2. Enter comma-separated input sequences (e.g., "dog, cat").
        3. Set the number of words to be returned per sequence (e.g., 10).
        4. Click 'Generate Pseudowords' to see the generated words.

        You can export the results to a CSV file for further use.
        """
        QMessageBox.information(self, "Help", help_message)

    def export_to_csv(self):
        # Get the current pseudoword matches
        pseudoword_matches = self.output_text.toPlainText().split("\n")
        
        if not pseudoword_matches:
            QMessageBox.warning(self, "No Data", "No pseudowords to export.")
            return
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)", options=options)

        if file_path:
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Pseudoword"])  # CSV header
                    for match in pseudoword_matches:
                        writer.writerow([match])
                QMessageBox.information(self, "Success", "Pseudowords successfully exported to CSV.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WuggyApp()
    window.show()
    sys.exit(app.exec_())
