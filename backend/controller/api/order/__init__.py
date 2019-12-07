from .delete import deleteNS
from .select_by_slug import selectBySlugNS
from .select_from_user import selectFromUserNS

NSOrder = [
    deleteNS,
    selectBySlugNS,
    selectFromUserNS
]
