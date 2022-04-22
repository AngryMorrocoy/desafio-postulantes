from requests_html import HTMLSession, HTML, Element
from typing import List
from requests import Response

PAYROLL_URL = (
    "https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html"
)


def get_voluntary_registration_payroll():
    html_session = HTMLSession()

    request: Response = html_session.get(PAYROLL_URL, timeout=15_000)
    if request.status_code != 200:
        raise ValueError("?")

    # Runs the javascript so the target table gets rendered
    request.html.render()

    html_data: HTML = request.html

    data_table: Element = html_data.find("#tabledatasii", first=True)
    table_rows: List[Element] = data_table.find("tbody > tr")

    for row in table_rows:
        print(row.text.splitlines())

    # print(table_rows[0].raw_html)


if __name__ == "__main__":
    get_voluntary_registration_payroll()
