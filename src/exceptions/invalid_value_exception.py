class InvalidValueException(Exception):
    def __init__(self, value, message, line_number):
        self._value = value
        self._message = message
        self._line_number = line_number

    def __str__(self):
        return repr(f"""{self._message} - Value: {self._value} - Line Number: {self._line_number}""")
