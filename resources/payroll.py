from flask_restful import Resource


class PayrollResource(Resource):
    def get(self):
        return {"It": "Works"}, 200
