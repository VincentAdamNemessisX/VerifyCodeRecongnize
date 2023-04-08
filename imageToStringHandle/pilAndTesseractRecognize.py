"""
# File       : pilAndTesseractRecognize.py
# Time       : 11:40 AM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import pytesseract
from PIL import Image
image = Image.open('../img/test.png')
# image = image.convert('L')
# image.show()
# image = image.convert('1')

# handle strange lines and recognize code
image = image.convert('L')
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
image.show()
print("Text:" + pytesseract.image_to_string(image, lang='eng'))
image.close()
