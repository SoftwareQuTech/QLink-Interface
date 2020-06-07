"""This defines the service interface of the link layer and provides a magic link layer protocol.
For details about this interface and specific header fields see the paper:

* A Link Layer Protocol for Quantum Networks
  https://arxiv.org/abs/1903.09778

and the QIRG draft:

* The Link Layer service in a Quantum Internet
  https://datatracker.ietf.org/doc/draft-dahlberg-ll-quantum

"""

from enum import Enum, auto
from collections import namedtuple


class EPRType(Enum):
    K = 0
    M = auto()
    R = auto()


# Supported request types (create and keep, measure directly, and remote state preparation)
class RequestType(Enum):
    K = EPRType.K.value
    M = EPRType.M.value
    R = EPRType.R.value
    RECV = auto()
    STOP_RECV = auto()


# Types of replies from the link layer protocol
class ReturnType(Enum):
    OK_K = EPRType.K.value
    OK_M = EPRType.M.value
    OK_R = EPRType.R.value
    ERR = auto()
    CREATE_ID = auto()


# Error messages
class ErrorCode(Enum):
    UNSUPP = 0
    NOTIME = auto()
    NORES = auto()
    TIMEOUT = auto()
    REJECTED = auto()
    OTHER = auto()
    EXPIRE = auto()
    CREATE = auto()


# Choice of random bases sets
class RandomBasis(Enum):
    NONE = 0
    XZ = auto()
    XYZ = auto()
    CHSH = auto()


# Bases return from link layer about which basis was randomly chosen
class Basis(Enum):
    Z = 0
    X = auto()
    Y = auto()
    ZPLUSX = auto()
    ZMINUSX = auto()


# What Bell state is generated
class BellState(Enum):
    PHI_PLUS = 0  # |00> + |11>
    PHI_MINUS = auto()  # |00> - |11>
    PSI_PLUS = auto()  # |01> + |10>
    PSI_MINUS = auto()  # |01> - |10>


# CREATE message to the link layer for entanglement generation
LinkLayerCreate = namedtuple("LinkLayerCreate", [
    "remote_node_id",
    "purpose_id",
    "type",
    "number",
    "random_basis_local",
    "random_basis_remote",
    "minimum_fidelity",
    "time_unit",
    "max_time",
    "priority",
    "atomic",
    "consecutive",
    "probability_dist_local1",
    "probability_dist_local2",
    "probability_dist_remote1",
    "probability_dist_remote2",
    "rotation_X_local1",
    "rotation_Y_local",
    "rotation_X_local2",
    "rotation_X_remote1",
    "rotation_Y_remote",
    "rotation_X_remote2",
])
LinkLayerCreate.__new__.__defaults__ = (
    (0, 0, RequestType.K, 1, RandomBasis.NONE, RandomBasis.NONE) +
    (0,) * (len(LinkLayerCreate._fields) - 6)
)

# RECV message to the link layer to allow for entanglement generation with a remote node
LinkLayerRecv = namedtuple("LinkLayerRecv", [
    "type",
    "remote_node_id",
    "purpose_id",
])
LinkLayerRecv.__new__.__defaults__ = (RequestType.RECV,) + (0,) * (len(LinkLayerRecv._fields) - 1)

# RECV message to the link layer to stop allowing for entanglement generation with a remote node
LinkLayerStopRecv = namedtuple("LinkLayerStopRecv", [
    "type",
    "remote_node_id",
    "purpose_id",
])
LinkLayerStopRecv.__new__.__defaults__ = (RequestType.STOP_RECV,) + (0,) * (len(LinkLayerStopRecv._fields) - 1)

# OK message from the link layer of successful generation of entanglement that is kept in memory
LinkLayerOKTypeK = namedtuple("LinkLayerOKTypeK", [
    "type",
    "create_id",
    "logical_qubit_id",
    "directionality_flag",
    "sequence_number",
    "purpose_id",
    "remote_node_id",
    "goodness",
    "goodness_time",
    "bell_state",
])
LinkLayerOKTypeK.__new__.__defaults__ = (ReturnType.OK_K,) + (0,) * (len(LinkLayerOKTypeK._fields) - 1)

# OK message from the link layer of successful generation of entanglement that is measured directly
LinkLayerOKTypeM = namedtuple("LinkLayerOKTypeM", [
    "type",
    "create_id",
    "measurement_outcome",
    "measurement_basis",
    "directionality_flag",
    "sequence_number",
    "purpose_id",
    "remote_node_id",
    "goodness",
    "bell_state",
])
LinkLayerOKTypeM.__new__.__defaults__ = (ReturnType.OK_M,) + (0,) * (len(LinkLayerOKTypeM._fields) - 1)

# OK message from the link layer of successful generation of entanglement that was used for remote state preparation
# (to creator node)
LinkLayerOKTypeR = namedtuple("LinkLayerOKTypeR", [
    "type",
    "create_id",
    "measurement_outcome",
    "directionality_flag",
    "sequence_number",
    "purpose_id",
    "remote_node_id",
    "goodness",
    "bell_state",
])
LinkLayerOKTypeR.__new__.__defaults__ = (ReturnType.OK_R,) + (0,) * (len(LinkLayerOKTypeR._fields) - 1)

# Error message from the link layer
LinkLayerErr = namedtuple("LinkLayerErr", [
    "type",
    "create_id",
    "error_code",
    "use_sequence_number_range",
    "sequence_number_low",
    "sequence_number_high",
    "origin_node_id",
])
LinkLayerErr.__new__.__defaults__ = (ReturnType.ERR,) + (0,) * (len(LinkLayerErr._fields) - 1)


def get_creator_node_id(local_node_id, create_request):
    """Returns the node ID of the node that submitted the given create request"""
    if create_request.directionality_flag == 1:
        return create_request.remote_node_id
    else:
        return local_node_id
