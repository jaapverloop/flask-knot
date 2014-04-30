# -*- coding: utf-8 -*-

"""
Flask-Knot
~~~~~~~~~~

A Flask extension for dependency management with Knot.

:copyright: (c) 2014 by Jaap Verloop.
:license: MIT, see LICENSE for more details.
"""

from collections import MutableMapping
from flask import current_app
from knot import Container


def get_container(app=None):
    if app is None:
        app = current_app

    if 'knot' not in app.extensions:
        raise RuntimeError('The Flask-Knot extension was not registered to the '
                           'current application.')

    container = app.extensions['knot']
    return container


class ContainerProxy(MutableMapping):
    def __init__(self, container=None):
        self._container = container or Container()

    def __getitem__(self, key):
        return self._real_object[key]

    def __setitem__(self, key, value):
        self._real_object[key] = value

    def __delitem__(self, key):
        del self._real_object[key]

    def __iter__(self):
        return iter(self._real_object)

    def __len__(self):
        return len(self._real_object)

    def __call__(self, *args, **kwargs):
        return self._real_object(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._real_object, name)

    @property
    def _real_object(self):
        if isinstance(self._container, Container):
            return self._container
        return self._container()


class Knot(ContainerProxy):
    def __init__(self, app=None):
        super(Knot, self).__init__()
        if app is not None:
            self.init_app(app)
            self.update(app.config)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['knot'] = self
