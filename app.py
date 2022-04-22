from flask import Flask
from flask_restful import Api

from resources.payroll import PayrollResource

app = Flask(__name__)
api = Api(app)

api.add_resource(PayrollResource, "/api/payroll")


def main():
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
