import graphene

from .entity import get_entity_query, register_entity
from .service import get_service_query


def _get_query(schema, query_cls=None, auto_camelcase=True):
    bases = [get_service_query(schema)]
    entity_cls = get_entity_query(auto_camelcase)
    if entity_cls:
        bases.append(entity_cls)
    if query_cls is not None:
        bases.append(query_cls)
    bases = tuple(bases)
    federated_query_cls = type('Query', bases, {})
    return federated_query_cls


def build_schema(query=None, mutation=None, **kwargs):
    auto_camelcase = kwargs.pop("auto_camelcase", True)
    schema = graphene.Schema(query=query, mutation=mutation, auto_camelcase=auto_camelcase, **kwargs)
    return graphene.Schema(query=_get_query(schema, query, auto_camelcase=auto_camelcase), mutation=mutation, **kwargs)
