import tempfile
from typing import Union
import numpy as np
import pyboof as pb
from PIL import Image, ImageOps
import os
from starlette.datastructures import UploadFile

def extract_micro_qr_codes(image_path: str) -> list:
    """
    Detects micro QR codes in the given image and returns a list of dictionaries containing
    the decoded messages and bounds of each detected QR code.

    Parameters:
    - image_path (str): Path to the image file.

    Returns:
    - list: List of dictionaries with 'decoded' (decoded message) and 'bounds' (code bounds) keys.
    """
    detector = pb.FactoryFiducial(np.uint8).microqr()
    image = pb.load_single_band(image_path, np.uint8)
    detector.detect(image)
    qr_data_list = []
    for qr in detector.detections:
        qr_data = {
            "decoded": qr.message,
            "bounds": str(qr.bounds)
        }
        qr_data_list.append(qr_data)
    return qr_data_list

def extract_micro_qrs_from_images(image_paths: list) -> list:
    """
    Processes a list of image paths and returns a combined list of micro QR code information
    obtained from each image using extract_micro_qr_codes function.

    Parameters:
    - image_paths (list): List of paths to image files.

    Returns:
    - list: Combined list of dictionaries containing QR code information from all images.
    """
    all_results = []
    for image_path in image_paths:
        results = extract_micro_qr_codes(image_path)
        all_results.extend(results)
    return all_results

async def process_micro_qr_file(file_or_path: Union[bytes, str, UploadFile]) -> dict:
    """
    Processes either file content (bytes), file path (str), or an UploadFile object containing
    image data. Extracts micro QR code information and returns a dictionary with filename,
    processing status, and QR code results.

    Parameters:
    - file_or_path (Union[bytes, str, UploadFile]): Input file content, file path, or UploadFile object.

    Returns:
    - dict: Result dictionary containing 'filename', 'status', and 'results' keys.
    """
    if isinstance(file_or_path, UploadFile):
        contents = await file_or_path.read()
    elif isinstance(file_or_path, bytes):
        contents = file_or_path
    elif isinstance(file_or_path, str):
        with open(file_or_path, 'rb') as file:
            contents = file.read()
    else:
        raise ValueError("Invalid argument type. Use either bytes, str, or UploadFile.")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(contents)
        img_path = temp_file.name

    img = Image.open(img_path)
    inverted_img = ImageOps.invert(img.convert('RGB'))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        inverted_img.save(temp_file.name, format='PNG')
        inverted_img_path = temp_file.name

    micro_qr_results = extract_micro_qrs_from_images([img_path, inverted_img_path])

    result = {
        "filename": os.path.basename(file_or_path.filename if isinstance(file_or_path, UploadFile) else file_or_path),
        "status": "ok", "results": micro_qr_results
    }

    os.remove(img_path)
    os.remove(inverted_img_path)

    return result
