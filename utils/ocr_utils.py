"""OCR utilities for term sheet validation"""

import logging
import pytesseract
from PIL import Image
import pdf2image
import os

logger = logging.getLogger(__name__)

def perform_ocr(file_path):
    """
    Perform OCR on an image or PDF file
    
    Args:
        file_path (str): Path to the image or PDF file
    
    Returns:
        str: Extracted text from the image
    """
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # For PDF files, convert to images first
        if file_extension == '.pdf':
            return ocr_pdf(file_path)
        
        # For image files, process directly
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            return ocr_image(file_path)
        
        else:
            logger.error(f"Unsupported file format for OCR: {file_extension}")
            return ""
    
    except Exception as e:
        logger.error(f"Error during OCR processing: {str(e)}")
        return ""

def ocr_image(image_path):
    """
    Perform OCR on a single image
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Extracted text from the image
    """
    try:
        logger.debug(f"Performing OCR on image: {image_path}")
        
        # Open the image
        image = Image.open(image_path)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image, lang='eng')
        
        return text
    
    except Exception as e:
        logger.error(f"Error performing OCR on image {image_path}: {str(e)}")
        return ""

def ocr_pdf(pdf_path):
    """
    Convert PDF to images and perform OCR
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        str: Extracted text from all pages of the PDF
    """
    try:
        logger.debug(f"Converting PDF to images and performing OCR: {pdf_path}")
        
        # Convert PDF to list of PIL Image objects
        images = pdf2image.convert_from_path(pdf_path)
        
        if not images:
            logger.error(f"Failed to convert PDF to images: {pdf_path}")
            return ""
        
        # Perform OCR on each image and combine the results
        text = ""
        for i, image in enumerate(images):
            logger.debug(f"Processing page {i+1} of {len(images)}")
            page_text = pytesseract.image_to_string(image, lang='eng')
            text += f"\n--- Page {i+1} ---\n{page_text}\n"
        
        return text
    
    except Exception as e:
        logger.error(f"Error performing OCR on PDF {pdf_path}: {str(e)}")
        return ""
