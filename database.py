"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""
from filters import valid_attribute
import operator

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        self.neo_trie = {}
        self.cad_trie = {}
        self.named_neo_list = []

        # Create a trie of CADs using it's designation.
        for cad in self._approaches:
            node = self.cad_trie
            for ch in cad._designation:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            if '$' in node:
                node['$'].append(cad)
            else:
                node['$'] = [cad]

        
        for neo in self._neos:
            # Create a list of NEOs with a name. This list will make searching for NEOs by name much faster
            if neo.name != '': self.named_neo_list.append(neo)
            
            # Add associated approaches for the NEO to its 'approaches' instance list by searching the trie of approaches for the NEO's designation
            cad_node = self.cad_trie

            # Create a trie of NEOs using it's designation.
            for ch in neo.designation:
                if ch in cad_node:
                    cad_node = cad_node[ch]
            if '$' in cad_node: 
                neo.approaches.extend(cad_node['$']) 
                for cad in cad_node['$']:
                    cad.neo = neo

            node = self.neo_trie
            for ch in neo.designation:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node[f'$'] = neo

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """

        #Use the trie of NEOs that are structured based on their designation for faster searching.
        hit = True
        node = self.neo_trie
        for ch in designation:
            if ch in node:
                node = node[ch]
        

        return node['$'] if '$' in node else None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return_neo = None

        for neo in self.named_neo_list:
            if neo.name == name:
                return_neo = neo
        return return_neo

    def query(self, filters={}):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        for approach in self._approaches:
            fits_criteria = True
            if filters['date'] is not None and not valid_attribute(approach, operator.eq, filters['date'], 'time'):
                    fits_criteria = False
            if filters['start_date'] is not None and not valid_attribute(approach, operator.ge, filters['start_date'], 'time'):
                    fits_criteria = False      
            if filters['end_date'] is not None and not valid_attribute(approach, operator.le, filters['end_date'], 'time'):
                    fits_criteria = False 
            if filters['distance_min'] is not None and not valid_attribute(approach, operator.ge, filters['distance_min'], 'distance'):
                    fits_criteria = False      
            if filters['distance_max'] is not None and not valid_attribute(approach, operator.le, filters['distance_max'], 'distance'):
                    fits_criteria = False
            if filters['velocity_min'] is not None and not valid_attribute(approach, operator.ge, filters['velocity_min'], 'velocity'):
                    fits_criteria = False      
            if filters['velocity_max'] is not None and not valid_attribute(approach, operator.le, filters['velocity_max'], 'velocity'):
                    fits_criteria = False
            if filters['diameter_min'] is not None and not valid_attribute(approach, operator.ge, filters['diameter_min'], 'diameter'):
                    fits_criteria = False      
            if filters['diameter_max'] is not None and not valid_attribute(approach, operator.le, filters['diameter_max'], 'diameter'):
                    fits_criteria = False
            if filters['hazardous'] is not None and not valid_attribute(approach, operator.eq, filters['hazardous'], 'hazardous'):
                    fits_criteria = False
            
            if fits_criteria:
                yield approach  