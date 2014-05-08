# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""

from nose.tools import eq_
from cryptos.tests import load_app

__all__ = ['ModelTest']


def setup():
    """Setup test fixture for all model tests."""
    load_app()


def teardown():
    """Tear down test fixture for all model tests."""
    pass


class ModelTest(object):
    """Base unit test case for the models."""

    klass = None
    attrs = {}

    def setUp(self):
        """Setup test fixture for each model test method."""
        try:
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass(**new_attrs)
            return self.obj
        except:
            raise

    def tearDown(self):
        """Tear down test fixture for each model test method."""

    def do_get_dependencies(self):
        """Get model test dependencies.

        Use this method to pull in other objects that need to be created
        for this object to be build properly.

        """
        return {}

    def test_create_obj(self):
        """Model objects can be created"""
        pass

    def test_query_obj(self):
        """Model objects can be queried"""
        for key, value in self.attrs.items():
            eq_(getattr(obj, key), value)
