import sys
import csv
import os
import multiprocessing as mp
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTextEdit, QMessageBox, QFileDialog)
from wuggy import WuggyGenerator
from spanenglish.orthographic_spanish import LanguagePlugin
from mod_spanish.orthographic_spanish import LanguagePlugin

def get_resource_path(relative_path):
    """Get the absolute path to a resource, works for both development and PyInstaller mode."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Example usage
spanish_file = get_resource_path("spanenglish/orthographic_spanish.txt")
mod_file = get_resource_path("mod_spanish/orthographic_spanish.txt")

class WuggyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wuggy Pseudoword Generator")
        self.setGeometry(100, 100, 600, 500)
        
        # UI Elements
        self.language_combobox = QComboBox()
        self.language_combobox.addItems(["English", "Spanish", "Spanenglish"])
        
        self.sequence_entry = QLineEdit()
        self.sequence_entry.setPlaceholderText("Enter sequences (comma-separated)")  # Aide utilisateur
        
        self.candidates_entry = QLineEdit()
        self.candidates_entry.setPlaceholderText("Enter number of candidates")

        self.import_button = QPushButton("Import from CSV", clicked=self.import_from_csv)
        self.generate_button = QPushButton("Generate Pseudowords", clicked=self.generate_pseudowords)
        self.export_button = QPushButton("Export to CSV", clicked=self.export_to_csv)
        self.help_button = QPushButton("Help", clicked=self.show_help)
        
        self.output_text = QTextEdit(readOnly=True)
        
        # Layouts
        input_layout = QVBoxLayout()
        for label, widget in [("Select Language:", self.language_combobox),
                              ("Input Sequences:", self.sequence_entry),
                              ("Number of Candidates:", self.candidates_entry)]:
            input_layout.addWidget(QLabel(label))
            input_layout.addWidget(widget)
        
        button_layout = QHBoxLayout()
        for btn in [self.import_button, self.generate_button, self.help_button, self.export_button]:
            button_layout.addWidget(btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("Generated Pseudowords:"))
        main_layout.addWidget(self.output_text)
        self.setLayout(main_layout)
    
    def import_from_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    sequences = [row[0] for row in reader if row]
                    self.sequence_entry.setText(", ".join(sequences))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read CSV: {e}")
    
    def generate_pseudowords(self):
        language = self.language_combobox.currentText().lower()
        if language == "english":
            language = "orthographic_english"
        elif language == "spanish":
            language = "mod_spanish"

        try:
            sequences = [seq.strip().lower() for seq in self.sequence_entry.text().split(",") if seq.strip()]
            ncandidates = int(self.candidates_entry.text())
            if not sequences or ncandidates <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter valid sequences and a positive integer for candidates.")
            return

        self.output_text.clear()

        if __name__ == '__main__':  # Protect multiprocessing on Windows
            with mp.Pool(processes=mp.cpu_count()) as pool:
                results = pool.starmap(self.generate_single_sequence, [(language, seq, ncandidates) for seq in sequences])

            for res in results:
                self.output_text.append("\n".join(res))
    
    @staticmethod
    def generate_single_sequence(language, sequence, ncandidates):
        try:
            generator = WuggyGenerator()
            if (language == "spanenglish") or (language == "mod_spanish"):
                print(f"Loading {language}...")
                generator.load(language, LanguagePlugin())
            else:
                generator.download_language_plugin(language, auto_download=True)
                generator.load(language)
            return [match["pseudoword"] for match in generator.generate_classic([sequence], ncandidates_per_sequence=ncandidates)]
        except Exception:
            return [f"Error generating for: {sequence}"]
    
    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Pseudoword"])
                    writer.writerows([[match] for match in self.output_text.toPlainText().split("\n") if match])
                QMessageBox.information(self, "Success", "Pseudowords exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV: {e}")
    
    def show_help(self):
        QMessageBox.information(self, "Help", """
        Steps to generate pseudowords:
        1. Select a language.
        2. Enter sequences separated by commas.
        3. Enter the number of candidates per sequence.
        4. Click 'Generate Pseudowords'.
        5. Export results as CSV if needed.
        """)

if __name__ == '__main__':
    mp.freeze_support()  # Required for Windows
    app = QApplication(sys.argv)
    window = WuggyApp()
    window.show()
    sys.exit(app.exec_())
