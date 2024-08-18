import sys
from enum import Enum


class EnumAutoName(Enum):
    """Apparently we need this if we want auto() to generate the name automatically as
    the value of the enum thing 🤦🏻‍♂️"""

    if sys.version_info >= (3, 12):

        @staticmethod
        def _generate_next_value_(name, start, count, last_values):
            return name

    else:

        @classmethod
        def _generate_next_value_(cls, name, start, count, last_values):
            return name
