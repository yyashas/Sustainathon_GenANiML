from pdf2image import convert_from_path
import pytesseract
from googletrans import Translator
from deep_translator import GoogleTranslator
import cv2
import numpy as np
import os
from PIL import Image

class PDFTranslator:
    def __init__(self, tessdata_prefix='/opt/homebrew/share/tessdata/'):
        self.tessdata_prefix = tessdata_prefix
        self.translator = Translator()
        os.environ['TESSDATA_PREFIX'] = self.tessdata_prefix

    def convert_pdf_to_images(self, pdf_path):
        """Converts PDF pages to images."""
        return convert_from_path(pdf_path)

    def remove_table_lines(self, image):
        """Removes table lines using morphological operations."""
        # Convert PIL image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive threshold to make the image binary
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)

        # Define kernels for horizontal and vertical line detection
        kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))  # Detect horizontal lines
        kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))  # Detect vertical lines

        # Detect horizontal and vertical lines
        horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_horizontal, iterations=2)
        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_vertical, iterations=2)

        # Combine the detected lines into a mask
        table_mask = cv2.add(horizontal_lines, vertical_lines)

        # Invert mask to white (background) and apply bitwise operation
        no_table_image = cv2.bitwise_not(gray, mask=table_mask)

        # Convert back to PIL image
        processed_pil = Image.fromarray(cv2.cvtColor(no_table_image, cv2.COLOR_GRAY2RGB))
        return processed_pil

    def extract_text_from_image(self, image, lang):
        """Extracts text from an image using Tesseract OCR."""
        return pytesseract.image_to_string(image, lang=lang)

    def translate_text(self, text, src, dest):
        """Translates text using Deep Translator (Google)."""
        try:
            return GoogleTranslator(source=src, target=dest).translate(text)
        except Exception as e:
            print(f"Translation Error: {e}")
            return text  # Return original text if translation fails

    # def translate_text(self, text, src, dest):
    #     """Translates text from source language to destination language."""
    #     return self.translator.translate(text, src=src, dest=dest).text
        
    def chunk_text(self, text):
        """Splits text into meaningful chunks based on paragraphs."""
        paragraphs = text.strip().split("\n\n")
        chunks = [para.strip() for para in paragraphs if para.strip()]
        return chunks

    def process_pdf(self, pdf_path, lang, translate=False, src_lang='auto', dest_lang='en', output_folder="output_images"):
        """Processes a PDF file, saves images, extracts text, and translates if required."""
        os.makedirs(output_folder, exist_ok=True)
        images = self.convert_pdf_to_images(pdf_path)
        all_data = []

        for i, image in enumerate(images):
            # Save original image
            original_image_path = os.path.join(output_folder, f"page_{i+1}_original.jpg")
            image.save(original_image_path)
            # print(f"Saved original image: {original_image_path}")

            # Remove table lines
            processed_image = self.remove_table_lines(image)
            combined_image = Image.blend(image, processed_image, alpha=0.5)
            processed_image = combined_image
            processed_image_path = os.path.join(output_folder, f"page_{i+1}_processed.jpg")
            processed_image.save(processed_image_path)
            # print(f"Saved processed image: {processed_image_path}")

            # Extract text
            extracted_text = self.extract_text_from_image(processed_image, lang)
            # print(f"Extracted text from page {i+1}:\n", extracted_text)

            # Translate text if needed
            if translate:
                data = self.translate_text(extracted_text, src=src_lang, dest=dest_lang)
                # chunks = self.chunk_text(translated_text)
            else:
                data = self.chunk_text(extracted_text)

            all_data.append((i+1, data))

        return all_data

# Usage
if __name__ == "__main__":
    translator = PDFTranslator()
    
    pdf_path = "karnataka.pdf"  # Change to your PDF file path
    lang = "kan"  # Kannada (Tesseract Language Code)
    src_lang = "kn"  # Google Translate Source Language
    dest_lang = "en"  # Translate to English
    
    chunked_pages = translator.process_pdf(pdf_path, lang, translate=True, src_lang=src_lang, dest_lang=dest_lang)

    # Print extracted text chunks
    # for page_num, chunks in chunked_pages:
        # print(f"\nPage {page_num} Chunks:")
        # for j, chunk in enumerate(chunks, 1):
            # print(f"Chunk {j}: {chunk}\n")