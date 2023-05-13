import asyncio
import os
from pyppeteer import launch
from bs4 import BeautifulSoup
import nest_asyncio

nest_asyncio.apply()

async def get_page_text(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    await asyncio.sleep(3) # Wait for page to load completely
    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')
    page_text = soup.get_text()
    await browser.close()
    return page_text

url = 'https://powerexpoportugal.com/'
page_text = asyncio.get_event_loop().run_until_complete(get_page_text(url))
print(page_text)
