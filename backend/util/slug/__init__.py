# FROM WEBSAUNA - https://github.com/websauna/websauna/

import base64
import uuid


def uuid_to_slug(uuid_: uuid.UUID) -> str:
    """Convert UUID object to a compact base64 string presentation.
    .. note ::
        Slugs are supposed to be human readable. We are stretching that definition here a bit.
    :param uuid_: UUID object
    :return: String like ''I0p4RyoIQe-EQ1GU_QicoQ'
    """

    # Catch some common typing errors
    assert isinstance(uuid_, uuid.UUID)

    encoded = base64.b64encode(uuid_.bytes)

    # https://docs.python.org/2/library/base64.html#base64.urlsafe_b64encode

    # URLs don't like +
    return encoded.decode("utf-8").rstrip('=\n').replace('/', '_').replace("+", "-")
