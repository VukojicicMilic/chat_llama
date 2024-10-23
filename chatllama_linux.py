import fitz  # PyMuPDF
import markdownify
import os
import argparse
import pytesseract
from PIL import Image
import io
import subprocess
import threading
from openpyxl import Workbook
import shlex

def extract_text_with_ocr(pdf_path):
    ocr_text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        ocr_text += pytesseract.image_to_string(img) + "\n\n"

    doc.close()
    return ocr_text

def pdf_to_markdown(pdf_path, use_ocr):
    if not os.path.exists(pdf_path):
        print(f"The specified PDF file does not exist: {pdf_path}")
        return None

    md_content = ""
    try:
        if use_ocr:
            md_content = extract_text_with_ocr(pdf_path)
        else:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text = page.get_text()
                    md_content += text + "\n\n"

        md_content = markdownify.markdownify(md_content, heading_style="ATX")
        md_file_path = os.path.splitext(pdf_path)[0] + '.md'
        with open(md_file_path, 'w') as md_file:
            md_file.write(md_content)

        print(f"Markdown file created: {md_file_path}")
        return md_file_path
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def run_ollama_model(prompt):
    command = f"echo {shlex.quote(prompt)} | ollama run llama3.2"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()

    if process.returncode == 0:
        return output.decode()
    else:
        print("Error running the model:")
        print(error.decode())
        return None

def convert_to_format(output, base_name, fmt):
    output_file = f"{base_name}.{fmt}"
    try:
        # Save the output in Markdown format first
        with open(f"{base_name}.md", 'w') as md_file:
            md_file.write(output)

        if fmt in ['txt', 'md', 'pptx', 'docx']:
            # Convert to the desired format using Pandoc
            subprocess.run(['pandoc', f"{base_name}.md", '-o', output_file])
            print(f"Converted to {output_file}")
        elif fmt == 'xlsx':
            # Create an Excel file
            wb = Workbook()
            ws = wb.active
            ws.title = "Output"
            ws.append(["Response"])  # Header
            ws.append([output])  # Content
            wb.save(output_file)
            print(f"Converted to {output_file}")
    except Exception as e:
        print(f"Error converting to {fmt}: {e}")

def chat_with_model(initial_prompt):
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Exiting the chat.")
            break

        # Prepare the prompt for the model
        prompt = f"{initial_prompt}\nUser: {user_input}\nModel:"
        response = run_ollama_model(prompt)

        if response:
            print("Model Output:\n" + response)

            # Ask if the user wants to convert the last output
            convert_choice = input("Do you want to save and convert the last output? (yes/no): ").strip().lower()
            if convert_choice == 'yes':
                base_name = input("Enter the base name for the output files: ")
                output_format = input("Choose the output format (txt/md/pptx/docx/xlsx): ").strip().lower()
                if output_format in ['txt', 'md', 'pptx', 'docx', 'xlsx']:
                    convert_to_format(response, base_name, output_format)
                else:
                    print("Invalid format selected.")

        print("\n" + "-" * 70 + "\n")

def main_loop(use_ocr):
    while True:
        pdf_path = input("Enter the path of the PDF file to load (or type 'exit' to quit): ")
        if pdf_path.lower() == 'exit':
            print("Exiting the program.")
            break

        md_file_path = pdf_to_markdown(pdf_path, use_ocr)
        if md_file_path:
            with open(md_file_path, 'r') as md_file:
                initial_prompt = md_file.read()
                print("\nInitial prompt sent to model.\n")
                response = run_ollama_model(initial_prompt)
                print("Model Output:\n" + response)

                print("\n----------------------")
                chat_with_model(initial_prompt)
                print("\n----------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF(s) to Markdown and chat with the Ollama model")
    parser.add_argument("pdf_paths", nargs='*', help="Path(s) to the initial PDF file(s)")
    parser.add_argument("-ocr", action="store_true", help="Use OCR for text extraction")

    args = parser.parse_args()

    # Process initial PDFs
    for pdf_path in args.pdf_paths:
        md_file_path = pdf_to_markdown(pdf_path, args.ocr)
        if md_file_path:
            with open(md_file_path, 'r') as md_file:
                initial_prompt = md_file.read()
                print("\nInitial prompt sent to model.\n")
                response = run_ollama_model(initial_prompt)
                print("Model Output:\n" + response)

                print("\n----------------------")
                chat_with_model(initial_prompt)
                print("\n----------------------")

    # Start the main loop for loading new PDFs
    main_loop(args.ocr)

