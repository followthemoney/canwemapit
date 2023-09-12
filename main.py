#!/bin/python

from followthemoney import model
from functools import reduce
import logging

schemata = filter(lambda s: not s.abstract, model.schemata.values())


def merge_properties(a, schema):
    for p in schema.properties.values():
        if p.name in a:
            try:
                assert (
                    a[p.name].type == p.type
                ), f"{a[p.name].qname} has type '{a[p.name].type}' while {p.qname} has type {p.type}"

                if p.type.name == "entity":
                    assert (
                        a[p.name].range == p.range
                    ), f"{a[p.name].qname} has range '{a[p.name].range}' while {p.qname} has range {p.range}"
            except AssertionError as e:
                logging.error(e)
        else:
            a[p.name] = p

    return a


mapping = reduce(merge_properties, schemata, {})

print(f"{len(mapping.keys())} fields in mapping")
