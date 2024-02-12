from fitz import fitz, Rect
import os

def add_label(pdf_path, x, y, width, height, position):
    img = open("CE_Label.png", "rb").read()
    pdf = fitz.open(pdf_path)
    if position == "right":
        page = pdf[0]  # Get the first page
        page_rect = page.rect
        rect = Rect(page_rect.width - width, y, page_rect.width, y + height)
    else:
        rect = Rect(0, 0, x, y)  # Default to original if position not 'right'

    if not pdf[0].is_wrapped:
        pdf[0].wrap_contents()
    pdf[0].insert_image(rect, stream=img)  # Insert image only on the first page
    
    # Compress the PDF here before saving
    compressed_pdf_bytes = compress_pdf(pdf, 3000)  # PDF size target in KB
    
    updated_folder_path = "./updated_pdfs"
    os.makedirs(updated_folder_path, exist_ok=True)
    
    new_pdf_name = os.path.basename(os.path.splitext(pdf_path)[0] + " with CE Label.pdf")
    new_pdf_path = os.path.join(updated_folder_path, new_pdf_name)
    
    # Save the compressed PDF
    with open(new_pdf_path, "wb") as f:
        f.write(compressed_pdf_bytes)
    
    pdf.close()

def compress_pdf(doc, target_size):
    # Assuming 'doc' is a fitz.Document object
    compressed_pdf_bytes = doc.tobytes(
        deflate=True,
        garbage=4,
    )
    print(len(compressed_pdf_bytes))  # Check output of compressed pdf
    return compressed_pdf_bytes

def process_folder(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            add_label(pdf_path, 0, 0, 120, 120, "right")

if __name__ == "__main__":
    folder_path = "./pdfs"
    process_folder(folder_path)
