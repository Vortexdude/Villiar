from sys import exception

from .models import Designation, Address, Employee, db
from Viliar.src.exceptions import UserAlreadyExistException, FormatterError, AttributeNotFound


class ResourceMixing(object):
    @staticmethod
    def _emp_validator(name):
        emp = Employee.get_by_name(name)
        if emp:
            raise UserAlreadyExistException()

    @staticmethod
    def _address_extractor(address: str):
        if len(address.split(",")) < 4:
            raise FormatterError()
        else:
            street, city, state, zipcode = address.split(",")
            if not zipcode.strip().isdigit():
                raise FormatterError()
            _addr = {
                "street": street.strip(),
                "city": city.strip(),
                "state": state.strip(),
                "zip_code": int(zipcode)
            }
            return Address(**_addr)

    @staticmethod
    def _designation_extractor(designation):
        _design = Designation.get_by_name(designation)
        if not _design:
            raise AttributeNotFound("Designation")
        return _design

    @staticmethod
    def _map_exception_with_status_code(_exception):
        exception_code_map = {
            UserAlreadyExistException: 409,
            FormatterError: 400,
            AttributeNotFound: 408
        }
        return exception_code_map.get(type(_exception), 500)


class EmployeeResource(ResourceMixing):
    def __init__(self, args):
        self.args = args

    def oboard(self):
        try:
            self._validate_employee()
            address = self._extract_address()
            designation = self._extract_designation()

        except (UserAlreadyExistException, FormatterError, AttributeNotFound) as e:
            return {"status": str(e)}, self._map_exception_with_status_code(e)

        employee = Employee(
            name=self.args['name'],
            salary=self.args['salary'],
            total_experience=self.args['total_experience'],
            address=address,
            designation=designation
        )
        db.add_all([address, designation, employee])
        try:
            db.commit()
            return {"data": "Data Inserted successfully."}, 201

        except Exception as e:
            return {"Status": f"Error with {e}"}

    def _validate_employee(self):
        self._emp_validator(self.args['name'])

    def _extract_address(self):
        return self._address_extractor(self.args['address'])

    def _extract_designation(self):
        return self._designation_extractor(self.args['designation'])

    @staticmethod
    def get_all():
        employees = Employee.get_all()
        if not employees:
            return {"Status": "No employee onboarded"}, 404
        return {"emp": [employee.to_dict() for employee in employees]}, 200
