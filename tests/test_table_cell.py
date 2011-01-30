#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test table cells
# Created: 21.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import unittest

# trusted or separately tested modules
from ezodf.xmlns import CN, etree, wrap
from ezodf.text import Paragraph

# objects to test
from ezodf.cells import Cell, CoveredCell

COVERED_TABLE_CELL = """
<table:covered-table-cell xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

TABLE_CELL = """
<table:table-cell xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestCellAttributes(unittest.TestCase):
    def test_has_TAG(self):
        cell = Cell()
        self.assertEqual(cell.TAG, CN('table:table-cell'))

    def test_Cell_is_kind_of_Cell(self):
        cell = Cell()
        covered_cell = Cell()
        self.assertEqual(covered_cell.kind, cell.kind)

    def test_is_covered(self):
        cell = Cell()
        self.assertFalse(cell.covered)

    def test_uncover_cell(self):
        cell = Cell()
        cell.covered = False
        self.assertFalse(cell.covered)
        self.assertEqual(cell.TAG, Cell.TAG)

    def test_cover_cell(self):
        cell = Cell()
        cell.covered = True
        self.assertTrue(cell.covered)
        self.assertEqual(cell.TAG, CoveredCell.TAG)

    def test_has_xmlnode(self):
        cell = Cell()
        self.assertIsNotNone(cell.xmlnode)

    def test_if_covered_cell_class_is_registered(self):
        cell = wrap(etree.XML(COVERED_TABLE_CELL))
        self.assertEqual(cell.TAG, CN('table:covered-table-cell'), 'class is not registered')

    def test_if_cell_class_is_registered(self):
        cell = wrap(etree.XML(TABLE_CELL))
        self.assertEqual(cell.TAG, CN('table:table-cell'), 'class is not registered')

    def test_get_style_name(self):
        cell = Cell()
        self.assertIsNone(cell.style_name)

    def test_set_style_name(self):
        cell = Cell()
        cell.style_name = 'STYLE'
        self.assertEqual(cell.style_name, 'STYLE')
        self.assertEqual(cell.get_attr(CN('table:style-name')), 'STYLE', 'wrong tag name')

    def test_get_content_validation_name(self):
        cell = Cell()
        self.assertIsNone(cell.content_validation_name)

    def test_set_content_validation_name(self):
        cell = Cell()
        cell.content_validation_name = 'validation'
        self.assertEqual(cell.content_validation_name, 'validation')
        self.assertEqual(cell.get_attr(CN('table:content-validation-name')), 'validation',
                         'wrong tag name')

    def test_get_formula(self):
        cell = Cell()
        self.assertIsNone(cell.formula)

    def test_set_formula(self):
        cell = Cell()
        cell.formula = "=[.A1]"
        self.assertEqual(cell.formula, "=[.A1]")
        self.assertEqual(cell.get_attr(CN('table:formula')), "=[.A1]",
                         'wrong tag name')

    def test_set_display_form(self):
        cell = Cell()
        cell.set_value(100.)
        cell.display_form = "100,00"
        self.assertEqual(cell.plaintext(), "100,00")

    def test_replace_display_form(self):
        cell = Cell()
        cell.set_value(100.)
        cell.display_form = "100,00"
        self.assertEqual(cell.plaintext(), "100,00")
        cell.display_form = "200,00"
        self.assertEqual(cell.plaintext(), "200,00")

    def test_error_display_form_None(self):
        cell = Cell()
        with self.assertRaises(TypeError):
            cell.display_form = "raise Error"

    def test_error_display_form_for_string(self):
        cell = Cell('cell with string')
        with self.assertRaises(TypeError):
            cell.display_form = "raise Error"

    def test_get_protected(self):
        cell = Cell()
        self.assertFalse(cell.protected)

    def test_set_protected(self):
        cell = Cell()
        cell.protected = True
        self.assertTrue(cell.protected)

    def test_get_span(self):
        cell = Cell()
        self.assertEqual(cell.span, (1, 1))

    def test_set_span(self):
        cell = Cell()
        cell.span = (2, 3)
        self.assertEqual(cell.span, (2, 3))


class TestCellContent(unittest.TestCase):
    def test_get_default_value_type(self):
        cell = Cell()
        self.assertIsNone(cell.value_type)

    def test_check_valid_value_types(self):
        cell = Cell()
        for t in ('float', 'percentage', 'currency', 'date', 'time', 'boolean', 'string'):
            cell.set_value(1., t)
            self.assertEqual(cell.value_type, t)

    def test_set_value_type(self):
        cell = Cell()
        cell.set_value('a string')
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.get_attr(CN('office:value-type')), 'string',
                         'wrong tag name')

    def test_check_invalid_value_type(self):
        cell = Cell()
        with self.assertRaises(TypeError):
            cell.set_value('', value_type='invalid')

    def test_set_new_string(self):
        cell = Cell(value_type='string')
        cell.append_text('test')
        self.assertEqual(cell.plaintext(), 'test')
        self.assertEqual(cell.value, 'test')

    def test_append_text_accept_style_name(self):
        cell = Cell('Text')
        cell.append_text('Text', style_name='test')
        self.assertEqual(cell.value, 'TextText')

    def test_append_two_strings(self):
        cell = Cell('test1')
        cell.append_text('test2')
        self.assertEqual(cell.plaintext(), 'test1test2')
        self.assertEqual(cell.value, 'test1test2')

    def test_append_two_paragraphs(self):
        cell = Cell('test1')
        cell.append(Paragraph('test2'))
        self.assertEqual(cell.plaintext(), 'test1\ntest2')
        self.assertEqual(cell.value, 'test1\ntest2')

    def test_append_text_error(self):
        cell = Cell(1.)
        with self.assertRaises(TypeError):
            cell.append_text('test')

    def test_set_float_with_type(self):
        cell = Cell()
        cell.set_value('100', 'float')
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.value, 100.)

    def test_set_float_without_type(self):
        cell = Cell()
        # set type explicit else type is string
        cell.set_value(100.)
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.value, 100.0)

    def test_set_int_without_type(self):
        cell = Cell()
        cell.set_value(100)
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.value, 100.)

    def test_set_true_boolean_with_type(self):
        cell = Cell()
        cell.set_value(True, 'boolean')
        self.assertEqual(cell.value_type, 'boolean')
        self.assertEqual(cell.value, True)

    def test_set_true_boolean_without_type(self):
        cell = Cell()
        cell.set_value(True)
        self.assertEqual(cell.value_type, 'boolean')
        self.assertEqual(cell.value, True)

    def test_set_false_boolean_with_type(self):
        cell = Cell()
        cell.set_value(False, 'boolean')
        self.assertEqual(cell.value_type, 'boolean')
        self.assertEqual(cell.value, False)

    def test_set_false_boolean_without_type(self):
        cell = Cell()
        cell.set_value(False)
        self.assertEqual(cell.value_type, 'boolean')
        self.assertEqual(cell.value, False)

    def test_get_currency(self):
        cell = Cell()
        self.assertIsNone(cell.currency)

    def test_set_currency(self):
        cell = Cell()
        cell.set_value(100., currency='EUR')
        self.assertEqual(cell.currency, 'EUR')
        self.assertEqual(cell.value_type, 'currency')
        self.assertEqual(cell.value, 100.)

    def test_error_set_None_value(self):
        cell = Cell()
        with self.assertRaises(ValueError):
            cell.set_value(None)

    def test_set_time_value(self):
        cell = Cell()
        cell.set_value('PT0H05M00,0000S', 'time')
        self.assertEqual(cell.value_type, 'time')
        self.assertEqual(cell.value, 'PT0H05M00,0000S')

    def test_set_date_value(self):
        cell = Cell()
        cell.set_value('2011-01-29T12:00:00', 'date')
        self.assertEqual(cell.value_type, 'date')
        self.assertEqual(cell.value, '2011-01-29T12:00:00')

class TestCellCreation(unittest.TestCase):
    def test_init_no_args(self):
        cell = Cell()
        self.assertEqual(cell.value_type, None)
        self.assertEqual(cell.value, None)
        self.assertEqual(cell.plaintext(), "")

    def test_init_value_without_type(self):
        cell = Cell(value=100)
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.value, 100.)

    def test_init_type_without_value(self):
        cell = Cell(value_type='float')
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.value, None)
        self.assertEqual(cell.plaintext(), "")

    def test_string(self):
        cell = Cell('text')
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.value, 'text')

    def test_float_no_type(self):
        cell = Cell(1.0)
        self.assertEqual(cell.value_type, 'float')
        self.assertEqual(cell.value, 1.0)

    def test_float_with_type(self):
        cell = Cell(1.0, 'currency')
        self.assertEqual(cell.value_type, 'currency')
        self.assertEqual(cell.value, 1.0)

    def test_float_as_string(self):
        cell = Cell(1.0, 'string')
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.value, '1.0')

    def test_boolean_true(self):
        cell = Cell(True)
        self.assertEqual(cell.value_type, 'boolean')
        self.assertEqual(cell.value, True)

    def test_boolean_false(self):
        cell = Cell(False)
        self.assertEqual(cell.value_type, 'boolean')
        self.assertEqual(cell.value, False)

    def test_time_value(self):
        cell = Cell('PT0H05M00,0000S', 'time')
        self.assertEqual(cell.value_type, 'time')
        self.assertEqual(cell.value, 'PT0H05M00,0000S')

    def test_date_value(self):
        cell = Cell('2011-01-29T12:00:01', 'date')
        self.assertEqual(cell.value_type, 'date')
        self.assertEqual(cell.value, '2011-01-29T12:00:01')

    def test_wrapped_object(self):
        cell = Cell(Paragraph('text'))
        self.assertEqual(cell.value_type, 'string')
        self.assertEqual(cell.value, 'text')
        self.assertEqual(cell[0].kind, 'Paragraph')


if __name__=='__main__':
    unittest.main()