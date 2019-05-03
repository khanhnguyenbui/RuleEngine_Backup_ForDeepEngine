# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 01:32:11 2019

@author: tuannm, thuanngo
"""

from querybuilder.constants import Operator
from querybuilder.constants import Condition
from querybuilder.constants import Type
from elasticsearch_dsl import query
from elasticsearch_dsl.query import Q

class OperatorOpt:
    NESTED = 'nested'
    
class ElasticConstants:
    LESS = 'lt'
    LESS_OR_EQUAL = 'lte'
    GREATER = 'gt'
    GREATER_OR_EQUAL = 'gte'
    FIELD = 'field'
    KEYWORD_SUFFIX = '.keyword'
    PATH = 'path'
    NESTED ='nested'
    QUERY = 'query'
    AND = 'and'
    OPERATOR = 'operator'
    
    class Bool:
        MUST = 'must'
        SHOULD = 'should'
        MUST_NOT = 'must_not'
        
    
OPERATOR_DICT = {
    Operator.EQUAL: lambda field, val: query.Term(**{field: val}),
    Operator.NOT_EQUAL: lambda field, val: query.Bool(
        **{ElasticConstants.Bool.MUST_NOT: query.Term(**{field: val})}
    ),
    Operator.LESS: lambda field, val: query.Range(**{field: {ElasticConstants.LESS: val}}),
    Operator.LESS_OR_EQUAL: lambda field, val: query.Range(
        **{field: {ElasticConstants.LESS_OR_EQUAL: val}}
    ),
    Operator.GREATER: lambda field, val: query.Range(
        **{field: {ElasticConstants.GREATER: val}}
    ),
    Operator.GREATER_OR_EQUAL: lambda field, val: query.Range(
        **{field: {ElasticConstants.GREATER_OR_EQUAL: val}}
    ),
    Operator.BETWEEN: lambda field, val: query.Range(**{field: {
        ElasticConstants.GREATER_OR_EQUAL: val[0],
        ElasticConstants.LESS_OR_EQUAL: val[1]
    }}),
    Operator.NOT_BETWEEN: lambda field, val: query.Range(**{field: {
        ElasticConstants.LESS: val[0],
        ElasticConstants.GREATER: val[1]}}),
    Operator.IN: lambda field, val: query.Terms(**{field: val}),
    Operator.NOT_IN: lambda field, val: query.Bool(
        **{ElasticConstants.Bool.MUST_NOT: query.Term(**{field: val})}
    ),
    Operator.IS_NULL: lambda field, val: query.Bool(
        **{ElasticConstants.Bool.MUST_NOT: query.Exists(**{ElasticConstants.FIELD: field})}
    ),
    Operator.IS_NOT_NULL: lambda field, val: query.Exists(
        **{ElasticConstants.FIELD: field}),

    # String operations
    Operator.BEGINS_WITH: lambda field, val: query.Prefix(
        **{field: val}
    ),
    Operator.NOT_BEGINS_WITH: lambda field, val: query.Bool(
        **{ElasticConstants.Bool.MUST_NOT: query.Prefix(**{field: val})}
    ),
    Operator.CONTAINS: lambda field, val: query.Match(**{field:{ElasticConstants.QUERY:val, ElasticConstants.OPERATOR : ElasticConstants.AND}}),
    Operator.NOT_CONTAINS: lambda field, val: query.Bool(
        **{ElasticConstants.Bool.MUST_NOT: query.Match(**{field:{ElasticConstants.QUERY:val, ElasticConstants.OPERATOR : ElasticConstants.AND}})}
    )
    ,
    OperatorOpt.NESTED: lambda p, q:  Q(ElasticConstants.NESTED,**{ElasticConstants.PATH : p,ElasticConstants.QUERY : q})
    
}


def get_sub_query(rule):
    opt = rule.operator
    field = rule.field
    if rule.type == Type.STRING and opt not in [Operator.CONTAINS, Operator.NOT_CONTAINS]:
        field = field + ElasticConstants.KEYWORD_SUFFIX
    val = rule.value
    return OPERATOR_DICT[opt](field, val)



def to_esl_query_obsolate(r):
    if r == {} or r.is_empty:
        converted = Q()
    elif r.is_group:
        # converted['condition'] = rule.condition.value
        if r.condition.value == Condition.AND:
            bool_type = ElasticConstants.Bool.MUST
        elif r.condition.value == Condition.OR:
            bool_type = ElasticConstants.Bool.SHOULD
        else:
            raise ValueError('Operation is not supported')
        converted = query.Bool(**{bool_type: [to_esl_query_obsolate(r) for r in r.rules]})
    else:
        converted = get_sub_query(r)
    return converted


def to_esl_query(r):
    if r == {} or r.is_empty:
        converted = Q()
    elif r.is_group:
        # converted['condition'] = rule.condition.value
        if r.condition.value == Condition.AND:
            bool_type = ElasticConstants.Bool.MUST
        elif r.condition.value == Condition.OR:
            bool_type = ElasticConstants.Bool.SHOULD
        else:
            raise ValueError('Operation is not supported')
        converted = query.Bool(**{bool_type: [to_esl_query(r) for r in r.rules]})
    else:
        field = r.field
        print(field)
        paths = field.split('.');
        print(paths)
        if len(paths) > 1:
            path = '.'.join(paths[0:len(paths)-1])
            converted = OPERATOR_DICT[OperatorOpt.NESTED](path,get_sub_query(r))
        else:
            converted = get_sub_query(r)
    return converted
