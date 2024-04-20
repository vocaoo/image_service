from abc import ABC

from didiator import Query as DQuery, QueryHandler as DQueryHandler


class Query[QRes](DQuery[QRes], ABC):
    pass


class QueryHandler[Q: Query, QRes](DQueryHandler[Q, QRes], ABC):
    pass
