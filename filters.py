"""Gathers conditions for approaches and finds those that meet them.

Provide filters for querying close approaches and limit the generated
results. The 'valid_attribute' function takes an approach, an attribute,
a value, and a comparison check to see if the approach's attribute meets the
condition of the comparison check compared to the value provided
Used by the query method in the database module to check whether an NEO/CEA
meets the conditions defined in the execution of the create_filters function.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest
from the supplied `CloseApproach`.

The `limit` function limits the maximum number of values produced by an
iterator.
"""
import operator
import datetime
import itertools as it


def valid_attribute(approach, op, value, attribute):
    """Check whether an approach meets conditions in filters.

    The 'valid_attribute' function takes an approach, an attribute, a value,
    and a comparison check to see if the approach's attribute meets the
    condition of the comparison check compared to the value provided.
    Used by the query method in the database module to check whether an
    NEO/CEA meets the conditions defined in the execution of the
    create_filters function.

    :param approach: A `CloseApproach` on which to evaluate this filter.
    :param op: The operator this function will use to test validity.
    :param value: The value of the attribute we are testing against. This
    comes from the value of the associated argument in the filters.
    :param attribute: The NEO/CAE attribute we are testing against.
    :return: True if the CAE meets the condition for the attribute and
    value expected. False if not.
    """
    neo_attributes = ['diameter', 'hazardous']

    if attribute in neo_attributes:
        approach_or_its_neo = approach.neo
    else:
        approach_or_its_neo = approach

    if attribute == 'time':
        validation_check = op(getattr(approach_or_its_neo, attribute).date(),
                              value)
    elif attribute == 'hazardous':
        validation_check = op(getattr(approach_or_its_neo, attribute), value)
    else:
        validation_check = op(getattr(approach_or_its_neo, attribute), value)

    return validation_check


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from
    the user's options at the command line. Each one corresponds to a different
    type of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that
    occured on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    A dictionary is returned with the argument names as keys and the argument
    values as values.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching
    `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching
    `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching
    `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching
    `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching
    `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching
    `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching
    `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching
    `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is
    potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filter_dict = {'date': date,
                   'start_date': start_date,
                   'end_date': end_date,
                   'distance_min': distance_min,
                   'distance_max': distance_max,
                   'velocity_min': velocity_min,
                   'velocity_max': velocity_max,
                   'diameter_min': diameter_min,
                   'diameter_max': diameter_max,
                   'hazardous': hazardous
                   }

    return filter_dict


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    n = 10 if (n == 0 or n is None) else n

    return it.islice(iterator, n)
