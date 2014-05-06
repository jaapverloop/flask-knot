# -*- coding: utf-8 -*-

from __future__ import with_statement

import unittest
from flask import Flask
from flask.ext.knot import Knot, get_container, current_container


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

    def test_container_is_shared(self):
        app1 = create_app()
        app2 = create_app()

        dic = Knot()
        dic.init_app(app1)
        dic.init_app(app2)

        dic1 = get_container(app1)
        dic2 = get_container(app2)

        assert dic1 is dic2

    def test_registration_is_required(self):
        app = create_app()

        self.assertRaises(RuntimeError, lambda: get_container(app))

    def test_top_of_app_ctx_is_utilized_by_current_container(self):
        app1 = create_app()
        dic1 = Knot(app1)
        dic1['foo'] = 'bar'

        with app1.test_request_context():
            self.assertEqual(current_container['foo'], 'bar')

        app2 = create_app()
        dic2 = Knot(app2)
        dic2['foo'] = 'baz'

        with app2.test_request_context():
            self.assertEqual(current_container['foo'], 'baz')


if __name__ == '__main__':
    unittest.main()
