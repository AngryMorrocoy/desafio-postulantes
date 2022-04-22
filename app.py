from quart import Quart
import datetime
from utils.payroll_scrapper import get_voluntary_registration_payroll

app = Quart(__name__)


@app.route("/api/payroll/", methods=["GET"])
async def get_payroll():
    registration_payroll = await get_voluntary_registration_payroll()
    return {"results": [row.as_dict() for row in registration_payroll]}


def main():
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
