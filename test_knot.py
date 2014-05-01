# -*- coding: utf-8 -*-

import unittest
from flask import Flask
from flask.ext.knot import Knot


def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


class TestKnot(unittest.TestCase):
    def test_acts_like_container(self):
        app = create_app()
        dic = Knot(app)

        def foo(c):
            return 'bar'

        dic.add_factory(foo)

        self.assertEqual(dic.provide('foo'), 'bar')

    def test_does_use_app_config_on_initialization(self):
        app = create_app()
        app.config['foo'] = 'bar'
        dic = Knot(app)

        self.assertEqual(dic['foo'], 'bar')

    def test_does_not_use_app_config_after_initialization(self):
        app = create_app()
        app.config['foo'] = 'bar'
        dic = Knot()
        dic.init_app(app)

        self.assertRaises(KeyError, lambda: dic['foo'])


if __name__ == '__main__':
    unittest.main()
