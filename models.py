"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name=None, diameter='', hazardous=False,
                 approaches=[]):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation of the NEO. This is a
        unique identifier in the database, and its "name" to computer systems.
        :param name: The International Astronomical Union (IAU) name of
        the NEO. This is its "name" to humans.
        :param diameter: The NEO's diameter (from an equivalent sphere)
        in kilometers.
        :param hazardous: Whether NASA has marked the NEO as a
        "Potentially Hazardous Asteroid," roughly meaning that it's large
        and can come quite close to Earth.
        :param approaches: A list of Close Earth Approaches for this NEO.
        """
        self.designation = designation
        self.name = name if name != '' else None
        self.diameter = float(diameter) if diameter != '' else float('nan')
        self.hazardous = True if hazardous == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation + ' ' + self.name

    def __str__(self):
        """Return string representation of NEO."""
        return (f"Near Earth Object {self.fullname} has a diameter of "
                f"{self.diameter:.3f} km. It is "
                f"{'' if self.hazardous else 'not'} classified"
                f" as potentially hazardous and has "
                f"{str(len(self.approaches))} "
                f"near earth approach"
                f"{'es' if len(self.approaches) != 1 else ''}."
                ).replace("  ", " ")

    def __repr__(self):
        """Return computer readable string representation of NEO."""
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, diameter={self.diameter:.3f}, "
                f"hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative approach
    velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, _designation, time, distance, velocity, neo=None):
        """Create a new `CloseApproach`.

        :param _designation: The primary designation of the NEO associated
        with this close-approach.
        :param time: Time of close-approach
        :param distance: Nominal approach distance
        :param velocity: Velocity relative to the approach body at
        close approach (km/s)
        :param neo: The NEO object associated with this close-approach
        """
        self._designation = _designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of the approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return '' if self.neo is None else self.neo.designation + ' ' \
            + '' if self.neo is None else self.neo.name

    def __str__(self):
        """Return a string representation of this object."""
        return (f"At {self.time_str}, {self.fullname} approaches Earth at a "
                f"distance of {self.distance:.2f} au and a velocity of "
                f"{self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
