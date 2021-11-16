#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:05:48 2020

@author: abdelhamid abouhassane
"""

import requests
from lxml import html
from PIL import Image
from pytesseract import image_to_string
import sys
import os
import re
import subprocess
import tempfile
import gpyocr
from selenium import webdriver

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/abdelhamid/Documents/My First Project-340fe406b723.json"

def parse_captcha(filename):
    """Return the text for thie image using Tesseract
    """
    img = threshold(filename)
    return tesseract(img)


def threshold(filename, limit=100):
    """Make text more clear by thresholding all pixels above / below this limit to white / black
    """
    # read in colour channels
    img = Image.open(filename)
    # resize to make more clearer
    m = 2
    img = img.resize((int(img.size[0] * m), int(img.size[1] * m))).convert('RGB')
    pixdata = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0] < limit:
                # make dark color black
                pixdata[x, y] = (0, 0, 0, 255)
            else:
                # make light color white
                pixdata[x, y] = (255, 255, 255, 255)
    img.save('threshold_' + filename)
    return img.convert('L')  # convert image to single channel greyscale


def call_command(*args):
    """call given command arguments, raise exception if error, and return output
    """
    c = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = c.communicate()
    if c.returncode != 0:
        if error:
            print(error)
        print("Error running `%s'" % ' '.join(args))
    return output


def tesseract(image):
    """Decode image with Tesseract
    """
    # create temporary file for tiff image required as input to tesseract
    input_file = tempfile.NamedTemporaryFile(suffix='.tif')
    image.save(input_file.name)

    # perform OCR
    output_filename = input_file.name.replace('.tif', '.txt')
    call_command('tesseract', input_file.name, output_filename.replace('.txt', ''))

    # read in result from output file
    result = open(output_filename).read()
    os.remove(output_filename)
    return clean(result)


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        return text.description

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def clean(s):
    """Standardize the OCR output
    """
    # remove non-alpha numeric text
    return re.sub('[\W]', '', s)


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                             'Safari/537.36', }
    page = requests.get('https://www.amazon.com', headers=headers);
    page.raise_for_status()
    tree = html.fromstring(page.content)

    imageCaptchaUrl = tree.xpath('//form//img/@src')
    print(imageCaptchaUrl)

    if imageCaptchaUrl:
        imageCaptchaBytes = requests.get(imageCaptchaUrl[0])
        filename = "captcha.jpg"
        file = open(filename, "wb")
        file.write(imageCaptchaBytes.content)
        file.close()

        captchaImage = Image.open("captcha.jpg")

        img = threshold(filename)
        print(img)
        print('Tesseract:', tesseract(img))
        print('Gocr:', gpyocr.tesseract_ocr('threshold_' + filename, lang='eng', psm=7))
        print('google:', detect_text(filename))
    else:
        print('NO CAPTCHA IMAGE!!')
