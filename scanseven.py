import sys
import os
import fitz  # PyMuPDF
from pyzbar.pyzbar import decode
from PIL import Image
import io


def extract_qr_codes_from_pdf(pdf_path, output_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Create or overwrite the output text file
    with open(output_file, 'w') as f_out:
        # Iterate through each page of the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # Extract images from the current page
            images = page.get_images(full=True)

            # Iterate through each image on the page
            for img_index, img_info in enumerate(images):
                xref = img_info[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]

                # Decode QR code from the image
                qr_decoded = decode(Image.open(io.BytesIO(image_bytes)))

                # Write the decoded text to the output file
                if qr_decoded:
                    f_out.write(f"Page {page_num + 1}, Image {img_index + 1}:\n")
                    for qr_result in qr_decoded:
                        f_out.write(f"QR Code Data: {qr_result.data.decode('utf-8')}\n")
                    f_out.write("\n")

    # Close the PDF document
    pdf_document.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_pdf> <output_file>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(pdf_file_path):
        print(f"Error: File '{pdf_file_path}' not found.")
        sys.exit(1)

    extract_qr_codes_from_pdf(pdf_file_path, output_file)
    print(f"QR codes extracted successfully. Output saved to {output_file}.")
