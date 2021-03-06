#!/usr/bin/env python
#
#    reference_node_loader.py: unit tests for vytree.referencetree.ReferenceTreeLoader
#    Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA

import os
import vytree
import vytree.referencetree
import unittest

import pkg_resources

class MockType(object):
    @staticmethod
    def get_format_string(constraint):
        return "fgsfds"

class TestVytreeReferenceLoader(unittest.TestCase):
    def setUp(self):
        data_dir = os.environ["VYCONF_DATA_DIR"]
        test_data_dir = os.environ["VYCONF_TEST_DATA_DIR"]
        self.reference_tree = vytree.referencetree.ReferenceNode('root')
        xml_file = os.path.join(test_data_dir, "interface_definition_valid.xml")
        schema_file = os.path.join(data_dir, "schemata", "interface_definition.rng")

        loader = vytree.referencetree.ReferenceTreeLoader(xml_file, {"mock": MockType}, schema=schema_file)
        loader.load(self.reference_tree)

    def test_get_child(self):
        child = self.reference_tree.get_child(['foo', 'bar'])
        self.assertIsInstance(child, vytree.referencetree.ReferenceNode)

    def test_invalid_interface_definition(self):
        data_dir = os.environ["VYCONF_DATA_DIR"]
        test_data_dir = os.environ["VYCONF_TEST_DATA_DIR"]
        xml_file = os.path.join(test_data_dir, "interface_definition_invalid.xml")
        schema_file = os.path.join(data_dir, "schemata", "interface_definition.rng")
        self.assertRaises(vytree.referencetree.ReferenceTreeLoaderError,
                          vytree.referencetree.ReferenceTreeLoader,
                          xml_file, {"mock": MockType}, schema=schema_file)
