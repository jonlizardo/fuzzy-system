import datetime as dt
import unittest
from unittest.mock import patch

from core import utils
from core.exceptions import PrinterDataTypeError
from core.utils import DateFilter


class TestUtilsFunctions(unittest.TestCase):
    def test_camel_to_snake(self):
        res = 'camel_to_snake'
        self.assertEqual(utils.camel_to_snake('CamelToSnake'), res)
        self.assertEqual(utils.camel_to_snake('camelToSnake'), res)

    @patch('core.utils.print')
    def test_printer(self, mock_print):
        with self.subTest('Dict'):
            data = {'a': 1}
            utils.printer(data)
            mock_print.assert_called_once_with(data)

        with self.subTest('List'):
            data = [1, 2, 3]
            utils.printer(data)
            # + 1 due to the prev subtest
            self.assertEqual(len(data) + 1, mock_print.call_count)

        with self.subTest('Other'):
            with self.assertRaises(PrinterDataTypeError):
                utils.printer('f')


class TestDateFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.start = dt.date(2022, 1, 1)
        self.end = dt.date(2022, 2, 1)
        self.filter_ = DateFilter(start=self.start, end=self.end)

    def test_reversed_date(self):
        other_filter = DateFilter(start=self.end, end=self.start)
        self.assertEqual(self.filter_, other_filter)

    def test_from_str(self):
        for format_ in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
            start = self.start.strftime(format_)
            end = self.end.strftime(format_)
            self.assertEqual(
                self.filter_, DateFilter.from_str(start, end, format_),
            )

    def test_repr(self):
        self.assertEqual(str(self.filter_), f'{self.start} - {self.end}')

    def test_check(self):
        sub_tests = [
            (self.start - dt.timedelta(days=1), 'before start', False),
            (self.start, 'start', True),
            (self.start + dt.timedelta(days=1), 'after start', True),
            (self.end - dt.timedelta(days=1), 'before end', True),
            (self.end, 'end', True),
            (self.end + dt.timedelta(days=1), 'after end', False),
        ]
        for date, label, expected in sub_tests:
            with self.subTest(label):
                self.assertEqual(self.filter_.check(date), expected)
