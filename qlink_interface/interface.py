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


# Supported request types (create and keep, measure directly, and remote state preparation)
class RequestType(Enum):
    K = 0
    M = auto()
    R = auto()
    RECV = auto()
    STOP_RECV = auto()


# Types of replies from the link layer protocol
class ReturnType(Enum):
    OK_K = 0
    OK_M = auto()
    OK_R = auto()
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
