from abc import ABC

from dependency_injector.resources import Resource


class ServiceProvider(Resource, ABC):
    pass
