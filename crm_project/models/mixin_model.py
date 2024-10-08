from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect


class BaseModelMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
