
class Months(object):

    """Implementation of the 'Months' enum.

    An integer enum representing Month names

    Attributes:
        JANUARY: TODO: type description here.
        FEBRUARY: TODO: type description here.
        MARCH: TODO: type description here.
        APRIL: TODO: type description here.
        MAY: TODO: type description here.
        JUNE: TODO: type description here.
        JULY: TODO: type description here.
        SEPTEMBER: TODO: type description here.
        OCTOBER: TODO: type description here.
        NOVEMBER: TODO: type description here.
        DECEMBER: TODO: type description here.

    """
    _all_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    JANUARY = 1

    FEBRUARY = 2

    MARCH = 3

    APRIL = 4

    MAY = 5

    JUNE = 6

    JULY = 7

    AUGUST = 8

    SEPTEMBER = 9

    OCTOBER = 10

    NOVEMBER = 11

    DECEMBER = 12

    @classmethod
    def validate(cls, value):
        """Validates value against enum.

        Args:
            value: the value to be validated against.

        Returns:
            boolean : if value is valid for this model.

        """
        if value is None:
            return None

        return value in cls._all_values