import asyncio
from flask import Flask, render_template, jsonify
from flask_restx import Resource, Api
from pyppeteer import launch
from bs4 import BeautifulSoup
from flask import Blueprint
import nest_asyncio

nest_asyncio.apply()


bp = Blueprint('wbscrape', __name__)
scrape = Api(bp)


@bp.route('/wbscrape')
class ScrapeResource(Resource):
    def get(self):
        url = 'https://powerexpoportugal.com/'
        page_text = asyncio.get_event_loop().run_until_complete(get_page_text(url))
        truncated_text = page_text[:500] + '...' if len(page_text) > 500 else page_text
        return jsonify({'truncated_text': truncated_text})
    
    
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
    
