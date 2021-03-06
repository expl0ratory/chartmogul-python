from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject, _add_method
from collections import namedtuple


class Summary(DataObject):
    """
    Optional information about a series of metrics.
    """
    class _Schema(Schema):
        current = fields.Number()
        previous = fields.Number()
        percentage_change = fields.Number(load_from='percentage-change')

        @post_load
        def make(self, data):
            return Summary(**data)

    _schema = _Schema(strict=True)


class Metrics(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#introduction-metrics-api
    """
    _path = "/metrics/all"
    _root_key = 'entries'
    _many_cls = namedtuple('Metrics', [_root_key, 'summary'])
    _many_cls.__new__.__defaults__ = (None,) * len(_many_cls._fields)

    class _Schema(Schema):
        """
        Fields are optional, so a subset present is good enough
        """
        date = fields.Date()
        customer_churn_rate = fields.Number(load_from='customer-churn-rate')
        mrr_churn_rate = fields.Number(load_from='mrr-churn-rate')
        ltv = fields.Number()
        customers = fields.Number()
        asp = fields.Number()
        arpa = fields.Number()
        arr = fields.Number()
        mrr = fields.Number()
        # MRR only
        mrr_new_business = fields.Number(load_from='mrr-new-business')
        mrr_expansion = fields.Number(load_from='mrr-expansion')
        mrr_contraction = fields.Number(load_from='mrr-contraction')
        mrr_churn = fields.Number(load_from='mrr-churn')
        mrr_reactivation = fields.Number(load_from='mrr-reactivation')

        @post_load
        def make(self, data):
            return Metrics(**data)

    _schema = _Schema(strict=True)

    @classmethod
    def _many(cls, entries, **kwargs):
        if 'summary' in kwargs:
            kwargs['summary'] = Summary._schema.load(kwargs['summary']).data
        return cls._many_cls(entries, **kwargs)


_add_method(Metrics, "mrr", "get", path='/metrics/mrr')
_add_method(Metrics, "arr", "get", path='/metrics/arr')
_add_method(Metrics, "arpa", "get", path='/metrics/arpa')
_add_method(Metrics, "asp", "get", path='/metrics/asp')
_add_method(Metrics, "customer_count", "get", path='/metrics/customer-count')
_add_method(Metrics, "customer_churn_rate", "get", path='/metrics/customer-churn-rate')
_add_method(Metrics, "mrr_churn_rate", "get", path='/metrics/mrr-churn-rate')
_add_method(Metrics, "ltv", "get", path='/metrics/ltv')
