import asyncio
from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
from pyppeteer import launch
from bs4 import BeautifulSoup
from flask import Blueprint
import nest_asyncio
import json
from flask import Blueprint

nest_asyncio.apply()


bp = Blueprint('webscrape', __name__)
api = Api(bp)

@api.route('/webscrape')
class WbsScrape(Resource):
    def get(self):
        async def main():
            browserObj = await launch({"headless": True}, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, ignoreHTTPSErrors=True)
            page = await browserObj.newPage()
            await page.goto('https://www.openpowerlifting.org/mlist/all-portugal/2023')

            data = []
            rows = await page.querySelectorAll("tbody tr")

            for row in rows:
                columns = await row.querySelectorAll("td")
                row_data = {}

                for index, column in enumerate(columns):
                    column_header = await page.querySelector(f"thead th:nth-child({index + 1})")
                    header_value = await column_header.getProperty("textContent")
                    header_value = await header_value.jsonValue()

                    column_value = await column.getProperty("textContent")
                    column_value = await column_value.jsonValue()

                    row_data[header_value] = column_value

                data.append(row_data)

            await browserObj.close()
            return data
            
            
            

        async def run():
            extracted_data = await main()
            return(extracted_data)
        

        
        extracted_data = asyncio.run(run())
        return jsonify({'data': extracted_data})

