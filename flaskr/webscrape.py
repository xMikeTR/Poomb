import asyncio
import os
from pyppeteer import launch
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import base64
from io import BytesIO
import nest_asyncio

nest_asyncio.apply()

async def extract_image_text(url):
    browser = await launch(headless=True, timeout=0)
    page = await browser.newPage()

    await page.goto(url)
    await page.waitForSelector('.wp-image-5559')

    image_data = await page.evaluate('() => {'
                                    '  const image = document.querySelector(".wp-image-5559");'
                                    '  const canvas = document.createElement("canvas");'
                                    '  const context = canvas.getContext("2d");'
                                    '  canvas.width = image.width;'
                                    '  canvas.height = image.height;'
                                    '  context.drawImage(image, 0, 0, image.width, image.height);'
                                    '  return canvas.toDataURL();'
                                    '}')

    await browser.close()

    tessdata_dir = r'C:/Program Files/Tesseract-OCR/tessdata'
    tessdata_dir_config = f'--tessdata-dir {tessdata_dir}'
    tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    os.environ['TESSDATA_PREFIX'] = tessdata_dir

    image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
    text = pytesseract.image_to_string(image, lang='por', config=tessdata_dir_config)

    return text

website_url = 'https://powerexpoportugal.com/'
image_text = asyncio.get_event_loop().run_until_complete(extract_image_text(website_url))

print('Image Text:', image_text)
