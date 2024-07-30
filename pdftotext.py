# import fitz
from PyPDF2 import PdfReader, PdfWriter
import os
from PassCrack import isEncrypted

#CHANGE NAMES OF FUNCTIONS TO APPLY TO ALL FILE TYPES


def check_file_extension(filename):
    # Get the file extension
    _, file_extension = os.path.splitext(filename)

    # Convert the file extension to lowercase for case-insensitivity
    file_extension = file_extension.lower()
    
    if file_extension == ".txt":
        return "Text"
    elif file_extension == ".docx":
        return "Word"
    elif file_extension == ".pdf":
        return "PDF"
    else:
        return "Unknown"

# def is_password_protected_pdf(pdf_file_path):
#     doc = fitz.Document(pdf_file_path)
#     if doc.needs_pass:
#         return True
#     return False
def is_password_protected(file_path):
    filetype = file_path[file_path.rfind('.')+1:]
    return isEncrypted(file_path,filetype)
#     try:
#         with open(file_path, "rb") as file:
#             data = file.read()
#         # Check if the file is password-protected
#         doc = fitz.Document(stream=data)
#         if doc.needs_pass:
#             return True
#         return False
#     except Exception as e:
#         print("Error:", e)
#         return False

# pdf_file_path = "pdf_file.pdf" #Specify your PDF path here
# print(is_password_protected(pdf_file_path))

# def decrypt_pdf1(pdf_file_path, password):
#     doc = fitz.Document(pdf_file_path)
#     if doc.authenticate(password):
#         file_name = pdf_file_path + "_decrypted.pdf"
#         doc.save(file_name)
#         print("\Successfully decrypted PDF")
#     else:
#         print("\t Password incorrect!! Cannot decrypt PDF!!!")
#     return file_name

# def decrypt_pdf2(pdf_file_path, password, fileName):
#     doc = fitz.Document(pdf_file_path)
#     if doc.authenticate(password):
#         output_folder = "documents"  # Specify the output folder
#         os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
#         #file_name = os.path.join(output_folder, os.path.basename(pdf_file_path) + "_decrypted.pdf")
#         base_name, extension = os.path.splitext(fileName)
#         #file_name = os.path.join(output_folder, base_name + '_decrypted'+ extension)
#         file_name = output_folder + "_decrypted" + extension
#         doc.save(file_name)
#         print("Successfully decrypted PDF")
#     else:
#         print("Password incorrect! Cannot decrypt PDF")
#     return file_name

def decrypt_pdf(input_path, password):
    try:
        _, extension = os.path.splitext(input_path)
        extension = extension.lower()
        
        if extension == '.pdf':
            pdf_reader = PdfReader(input_path)
            pdf_reader.decrypt(password)  # Apply the password for PDF decryption

            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            base_name, _ = os.path.splitext(input_path)
            new_document_path = base_name + "_decrypted.pdf"

            with open(new_document_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

            print("Successfully decrypted PDF:", new_document_path)
            return new_document_path
        else:
            print("Unsupported file type:", extension.upper())
            return None
    except Exception as e:
        print("Error:", e)
        return None

def read_pdf(file_path):
    reader = PdfReader(file_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text

#options to read other file formats in similar functions

# print(decrypt_pdf(pdf_file_path, "123456"))

# reader = PdfReader('pdf_decrypted.pdf')
# # printing number of pages in pdf file
# print(len(reader.pages))
  
# # getting a specific page from the pdf file
# page = reader.pages[0]
  
# # extracting text from page
# text = page.extract_text()
# print(text)

#input_path = "/home/jfrans/Hackathon/Forensics/pdf_file.pdf"  # Replace with your document path
#password = "123456"

#new_document_path = decrypt_pdf(input_path, password)
#if new_document_path:
 #   print("Decrypted document saved as:", new_document_path)



