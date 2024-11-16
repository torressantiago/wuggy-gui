# Pseudoword Generator GUI

This project provides a graphical user interface (GUI) for generating pseudowords using the **Wuggy** language generator. The user can select between English and Spanish languages, input custom sequences, set the number of candidate pseudowords per sequence, and export the results to a CSV file. This tool uses the Wuggy library, which is an implementation for generating pseudowords based on lexical properties of a language.

## Features

- Select a language (English or Spanish).
- Input custom sequences for pseudoword generation.
- Specify the number of candidate pseudowords per sequence.
- Generate and display the pseudowords.
- Export the generated pseudowords to a CSV file.
- Built using **PyQt5** for the GUI and **Wuggy** for pseudoword generation.

## Installation

For now, binaries for Linux or Windows are provided under releases.

### Prerequisites

Make sure you have Python 3.x installed. You can download Python from [python.org](https://www.python.org/).

## For developers
### 1. Clone this repository:

```bash
git clone https://github.com/torressantiago/pseudoword-generator.git
cd pseudoword-generator
python -m venv venv
```
### 2. Set up a virtual environment (optional but recommended):
```bash
python -m venv venv
```
####Activate the virtual environment:
**On Windows:**

```bash

venv\Scripts\activate
```
**On macOS/Linux:**

```bash

source venv/bin/activate
```
### 3. Install required dependencies:
```bash

pip install pyqt5, wuggy
```
### 4. Run the application:
```bash
python app.py
```

## Usage
1. Select the desired language (English or Spanish).
2. Input a list of sequences (e.g., words).
3. Choose the number of candidate pseudowords you want to generate per sequence.
4. Press the "Generate" button to create the pseudowords.
5. Optionally, export the results to a CSV file using the "Export to CSV" button.

## Authors and Credits
This project uses the Wuggy pseudoword generator, created by Michael Piotrowski.

- **Wuggy**: [https://www.mpi.nl/people/michael-piotrowski](https://www.mpi.nl/people/michael-piotrowski)

Wuggy is a powerful tool used in psycholinguistic research, developed by Michael Piotrowski at the Max Planck Institute for Psycholinguistics. It generates pseudowords that closely resemble real words in a given language and have specific properties, such as segment structure, phonotactics, and syllable types.

For further details on Wuggy, please refer to the original Wuggy documentation.
