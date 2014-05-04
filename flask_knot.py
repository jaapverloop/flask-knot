# -*- coding: utf-8 -*-

"""
Flask-Knot
~~~~~~~~~~

A Flask extension for dependency management with Knot.

:copyright: (c) 2014 by Jaap Verloop.
:license: MIT, see LICENSE for more details.
"""

from weakref import ref
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


class ContainerResolver(object):
    def __init__(self):
        self._vals = {}
        self._refs = {}

    def __get__(self, instance, owner):
        obj_id = id(instance)

        if obj_id not in self._vals:
            self.__set__(instance, Container())

        real_obj = self._vals[obj_id]
        return real_obj if isinstance(real_obj, Container) else real_obj()

    def __set__(self, instance, real_obj):
        obj_id = id(instance)

        vals = self._vals
        refs = self._refs

        def clean(ref):
            del vals[obj_id]
            del refs[obj_id]

        vals[obj_id] = real_obj
        refs[obj_id] = ref(instance, clean)


class ContainerProxy(MutableMapping):
    _container = ContainerResolver()

    def __init__(self, container=None):
        if container is not None:
            self._container = container

    def __getitem__(self, key):
        return self._container[key]

    def __setitem__(self, key, value):
        self._container[key] = value

    def __delitem__(self, key):
        del self._container[key]

    def __iter__(self):
        return iter(self._container)

    def __len__(self):
        return len(self._container)

    def __call__(self, *args, **kwargs):
        return self._container(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._container, name)


class Knot(ContainerProxy):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
            self.update(app.config)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['knot'] = self


current_container = ContainerProxy(get_container)
