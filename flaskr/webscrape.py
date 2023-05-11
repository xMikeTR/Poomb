import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import nest_asyncio
import asyncio
from pyppeteer import launch
from PIL import Image
import pytesseract
nest_asyncio.apply()



async def extract_image_text(url):
    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.goto(url)
    await page.waitForSelector('.wp-image-5559')

    image_data = await page.evaluate('(async () => {'
                                    '  const image = document.querySelector(".wp-image-5559");'
                                    '  const canvas = document.createElement("canvas");'
                                    '  const context = canvas.getContext("2d");'
                                    '  canvas.width = image.width;'
                                    '  canvas.height = image.height;'
                                    '  context.drawImage(image, 0, 0, image.width, image.height);'
                                    '  return canvas.toDataURL();'
                                    '})()')

    await browser.close()

    image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
    text = pytesseract.image_to_string(image)

    return text

website_url = 'https://powerexpoportugal.com/'
image_text = asyncio.get_event_loop().run_until_complete(extract_image_text(website_url))

print('Image Text:', image_text)