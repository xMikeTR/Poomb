import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import nest_asyncio
import asyncio
from pyppeteer import launch
nest_asyncio.apply()



async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    post_url = 'https://www.instagram.com/p/COmlv7iLHlG/'

    await page.goto(post_url,)
    await page.waitForSelector('img[alt]')

    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')
    img_tag = soup.find('img')
    post_text = img_tag['alt']



response = asyncio.get_event_loop().run_until_complete(main())
print(response)
