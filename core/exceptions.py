from typing import Any


class PrinterDataTypeError(Exception):
    def __init__(self, data: Any):
        self.message = f'Cant use printer to print {data} due to its type: ' \
                       f'{type(data)}'
        super().__init__(self.message)
