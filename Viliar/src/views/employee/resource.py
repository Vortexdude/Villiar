from .models import Designation, Address, Employee, db


class EmployeeResource:
    def __init__(self, args):
        self.args = args

    def oboard(self):
        designation = Designation.get_by_name(self.args['designation'])
        if not designation:
            return {"Error": "Please approach to administrator."}
        address = Address(street="MIG colony", city="Indore", state="M.P.", zip_code=471001)
        employee = Employee(
            name=self.args['name'],
            salary=self.args['salary'],
            total_experience=self.args['total_experience'],
            address=address,
            designation=designation
        )
        db.add_all([address, designation, employee])
        db.commit()
        return {"data": "inserted"}
