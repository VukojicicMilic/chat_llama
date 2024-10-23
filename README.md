# chat_llama
Chat with the .pdf file in Llama models 

A Python script that converts PDF files to Markdown and allows users to chat with a language model using the extracted content. Supports OCR for image-based PDFs.

# Features
+ Convert PDFs to Markdown (.md) format.
+ Use OCR to extract text from scanned PDFs.
+ Chat with a language model and interactively ask questions.
+ Export responses in multiple formats: .txt, .md, .pptx, .docx, .xlsx.

# Prerequisites
+ Python 3.6 or higher
+ Pip (Python package manager)

# Required libraries:
+ fitz (PyMuPDF)
+ markdownify
+ pytesseract
+ Pillow
+ openpyxl
+ pandoc (for format conversion)

# Installing Required Libraries
You can install the required libraries using pip:

Copy code

pip install PyMuPDF markdownify pytesseract Pillow openpyxl

Make sure to install Pandoc separately. You can download it from Pandoc's official site.

# Tesseract OCR Installation

For OCR functionality, you need to install Tesseract. Follow the instructions for your operating system:

# Linux:

Copy code
sudo apt install tesseract-ocr

# Windows:

Download the Tesseract installer from UB Mannheim's Tesseract page.
Install it and add the installation path to your system's environment variables.


# Usage

Running the Script
You can run the script from the command line. Provide the paths to the PDF files you want to process and use the -ocr flag if you want to use OCR for text extraction.

# On Linux:

Copy code
python3 chatllama_linux.py [path_to_pdf1 path_to_pdf2 ...] -ocr

# On Windows:

Copy code
python chatllama_windows.py [path_to_pdf1 path_to_pdf2 ...] -ocr


# Interaction Flow

Input PDF: You will be prompted to enter the path of a PDF file.
Chat with the Model: The content of the PDF will be sent to the language model, and you can interactively chat with it.
Output Response: After each interaction, you can choose to save the model's output in various formats.
Available Output Formats
.txt
.md
.pptx
.docx
.xlsx
Example
Run the script with a PDF file:


python pdf_chatbot.py example.pdf -ocr
Follow the prompts to interact with the model.
