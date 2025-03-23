from werkzeug.exceptions import HTTPException

class CustomException(HTTPException):
    code = 400
    
class MLModelException(HTTPException):
    code = 500
    description = "There was a error in ML model"
