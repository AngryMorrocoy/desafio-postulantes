from pyppeteer.element_handle import ElementHandle
from pyppeteer.page import Page
from pyppeteer import launch
from typing import List, Optional
from .types import VoluntaryRegistrationPayroll, TaxData
import datetime
import re
import asyncio
from config import CHROMIUM_BINARY_PATH

PAYROLL_URL = (
    "https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html"
)


def parse_tax_data_from_str(data: str) -> Optional[TaxData]:
    dr, res_number, date = re.split("\s?[/]\s?", data)
    if not all([dr, res_number, date]):
        return None

    day, month, year = map(int, date.split("-"))

    date = datetime.date(year, month, day)
    return TaxData(dr, res_number, date)


def parse_expire_date_from_str(date_string: str) -> datetime.date:
    # Here I decided to map to short month names in spanish
    # since the page is in spanish and couldn't found other months
    # than june :c
    MONTHS = {
        "ene": 1,
        "feb": 2,
        "mar": 3,
        "abr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "ago": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dic": 12,
    }

    # Since the date is in the format "month-XX"
    # I'll assume the XX digits represent the year (20XX), since it's always less
    # than the year of last update, unless it's excluded or pendant.
    month, year = date_string.split("-")
    return datetime.date(int(year) + 2000, MONTHS[month], 1)


def parse_row_text_into_voluntary_registration_payroll(
    row_text: str,
) -> VoluntaryRegistrationPayroll:

    columns = row_text.splitlines()

    if len(columns) != 7:
        raise ValueError(f"'{'|'.join(columns)}' Isn't a valid row!")

    REGISTRATION_DATA_COLUMN = columns[3]
    EXPIRES_AT_COLUMN = columns[4]
    LAST_UPDATE_DATA_COLUMN = columns[5]

    registration_data = parse_tax_data_from_str(REGISTRATION_DATA_COLUMN)
    last_update_data = parse_tax_data_from_str(LAST_UPDATE_DATA_COLUMN)
    expires_at = parse_expire_date_from_str(EXPIRES_AT_COLUMN)

    return VoluntaryRegistrationPayroll(
        int(columns[0]),  # The column of register
        columns[1],  # The column of social reason
        columns[2],  # The column of the country
        expires_at,
        columns[6],  # The column of the state
        registration_data,
        last_update_data,
    )


async def separate_columns_text_with_newline(page: Page, row: ElementHandle) -> str:
    row_columns = await row.querySelectorAll("td")
    columns_text = await asyncio.gather(
        *[
            page.evaluate("(element) => element.textContent", column)
            for column in row_columns
        ]
    )
    return "\n".join(columns_text)


async def get_voluntary_registration_payroll() -> List[VoluntaryRegistrationPayroll]:

    browser = await launch(executablePath=CHROMIUM_BINARY_PATH, args=["--no-sandbox"])
    page = await browser.newPage()

    await page.goto(PAYROLL_URL)

    data_table = await page.querySelector("#tabledatasii")
    table_rows = await data_table.querySelectorAll("tbody > tr")

    rows_as_text = await asyncio.gather(
        *[separate_columns_text_with_newline(page, row) for row in table_rows]
    )

    await browser.close()

    return [
        parse_row_text_into_voluntary_registration_payroll(row_text)
        for row_text in rows_as_text
        if row_text
    ]


if __name__ == "__main__":
    get_voluntary_registration_payroll()
