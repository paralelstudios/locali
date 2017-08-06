# -*- coding: utf-8 -*-
"""
    locali.core
    ~~~~~~~~~~~~
    Flask extension imports
"""
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort
from sqlalchemy.orm import load_only
from boto3.session import Session
from .helpers import try_committing


class LocaliException(Exception):
    def __init__(self, msg):
        self.msg = msg


class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        try_committing(db.session)
        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.query.all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs)

    def get_query_with_cols(self, *cols):
        """Gets all the instances of the model with only certain cols selected"""
        return self.__model__.query.options(load_only(*cols))

    def first_or_404(self, **kwargs):
        """Tries to find an instance of the model filtered by the specified key word
        arguments, raising a 404 if that instance isn't found
        """
        instance = self.first(**kwargs)
        if not instance:
            abort(404,
                  description="Instance not found in {}".format(
                      self.__model__.__tablename__))
        return instance

    def first(self, with_for_update=False, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        q = self.find(**kwargs)
        if with_for_update:
            q = q.with_for_update()
        return q.first()

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def get_and_409(self, **kwargs):
        m = self.__model__.query.filter_by(**kwargs).first()
        if m:
            abort(409, description="{} already exists".format(m))

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()


class S3Client(object):
    def __init__(self):
        self._s3 = None

    def init_app(self, app):
        self._session = Session(
            aws_access_key_id=app.config.get('AWS_ACCESS_KEY', None),
            aws_secret_access_key=app.config.get('AWS_SECRET_KEY', None),
            region_name=app.config['AWS_REGION'])
        self._s3 = self._session.resource('s3')

    def __getattr__(self, name):
        return getattr(self._s3, name)


s3 = S3Client()
db = SQLAlchemy()
