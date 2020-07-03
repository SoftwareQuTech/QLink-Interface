"""This defines the service interface of the link layer and provides a magic link layer protocol.
For details about this interface and specific header fields see the paper:

* A Link Layer Protocol for Quantum Networks
  https://arxiv.org/abs/1903.09778

and the QIRG draft:

* The Link Layer service in a Quantum Internet
  https://datatracker.ietf.org/doc/draft-dahlberg-ll-quantum

"""

from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class ReqCreateBase:
    """Base for "create" requests. Not a supported request type itself.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    remote_node_id: int = 0  # ID of the node to create entanglement with
    minimum_fidelity: float = 0  # the desired minimum fidelity, between 0 and 1
    time_unit: int = 0  # 0 for microseconds, 1 for milliseconds, 2 for seconds
    max_time: int = 0  # the maximum number of "time_unit"s the higher layer is willing to wait for the request
    purpose_id: int = 0  # allows higher layer to tag request for a specific purpose
    number: int = 1  # number of entangled pairs to generate
    priority: int = 0  # large value indicates this request is of high priority and should be fulfilled early
    atomic: bool = False  # should entangled qubits be available in memory at the same time?
    consecutive: bool = False  # should entangled pairs be created close in time?


@dataclass
class ReqCreateAndMeasureBase(ReqCreateBase):
    """Base for "create and measure" requests. Not a supported request type itself.

    Measurement bases can be manipulated by performing a general rotation on a qubit before measurement.
    Any rotation can be decomposes into first an X rotation, then an Y rotation, and then another X rotation.
    By specifying the three corresponding angles (these are Euler angles), the pre-measurement rotation is specified.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    x_rotation_angle_local_1: float = 0  # local qubit initial X rotation
    y_rotation_angle_local: float = 0  # local qubit Y rotation
    x_rotation_angle_local_2: float = 0  # local qubit final X rotation
    x_rotation_angle_remote_1: float = 0  # remote qubit initial X rotation
    y_rotation_angle_remote: float = 0  # remote qubit Y rotation
    x_rotation_angle_remote_2: float = 0  # remote qubit final X rotation


@dataclass
class ReqCreateAndMeasureTwoBasesBase(ReqCreateAndMeasureBase):
    """Base for "create and measure" requests with two random base choices. Not a supported request type itself.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    probability_distribution_parameter_local_1: float = .5  # probability of measuring local qubit in first basis
    probability_distribution_parameter_remote_1: float = .5  # probability of measuring remote qubit in first basis


@dataclass
class ReqCreateAndMeasureThreeBasesBase(ReqCreateAndMeasureBase):
    """Base for "create and measure" requests with three random base choices. Not a supported request type itself.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    probability_distribution_parameter_local_1: float = 1 / 3  # probability of measuring local qubit in first basis
    probability_distribution_parameter_remote_1: float = 1 / 3  # probability of measuring remote qubit in first basis
    probability_distribution_parameter_local_2: float = 1 / 3  # probability of measuring local qubit in second basis
    probability_distribution_parameter_remote_2: float = 1 / 3  # probability of measuring remote qubit in 2nd basis


class ReqCreateAndKeep(ReqCreateBase):
    """Request to generate entanglement and store it in memory.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    pass


@dataclass
class ReqCreateAndMeasureFixed(ReqCreateAndMeasureBase):
    """Request to generate entanglement and measure it immediately in a specified basis.

    Measurement in an arbitrary basis is performed by first rotating the qubit and then performing a Z measurement.
    Any rotation can be decomposes into first an X rotation, then an Y rotation, and then another X rotation.
    By specifying the three corresponding angles (these are Euler angles), measurement in an arbitrary fixed basis
    can be performed.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    pass


@dataclass
class ReqCreateAndMeasureXZ(ReqCreateAndMeasureTwoBasesBase):
    """Request to generate entanglement and measure it immediately, randomly in either X or Z (BB84).

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    pass


@dataclass
class ReqCreateAndMeasureXYZ(ReqCreateAndMeasureThreeBasesBase):
    """Request to generate entanglement and measure it immediately, randomly in either X, Y or Z.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    pass


# TODO: make more explicit what CHSH bases are
@dataclass
class ReqCreateAndMeasureCHSH(ReqCreateAndMeasureThreeBasesBase):
    """Request to generate entanglement and measure it immediately, randomly in CHSH rotated bases.

    Note
    ----
    Based on figure 1 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).
    This document says about the CHSH rotated bases: Z basis rotated by angles +/- pi/4 around Y axis.

    """

    pass


@dataclass
class ReqReceive:
    """Request to be ready for entanglement generation."""
    remote_node_id: int = 0
    purpose_id: int = 0


@dataclass
class ReqStopReceive:
    """Request to stop being ready for entanglement generation."""
    remote_node_id: int = 0
    purpose_id: int = 0


@dataclass
class ResCreate:
    """Base for different "create" responses. Not a response that is used itself.

    Note
    ----
    Based on Figures 3, 4 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol)

    """

    create_id: int = 0  # the same as the Create ID returned to the requester
    directionality_flag: bool = 0  # Specifies if the request came from this node (D=0) or the remote node (D=1)
    sequence_number: int = 0  # a sequence number for identifiying the entangled pair
    purpose_id: int = 0  # purpose ID of the request
    remote_node_id: int = 0  # used if connected to multiple nodes
    goodness: float = 0  # an estimate of the fidelity of the generated pair
    bell_state: int = 0  # index of the created Bell state # TODO add mapping


@dataclass
class ResCreateAndKeep(ResCreate):
    """Response corresponding to create and keep request.

    Note
    ----
    Based on Figure 3 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    logical_qubit_id: int = 0  # logical qubit id where the entanglement is stored
    time_of_goodness: int = 0  # time of the goodness estimate
    # TODO: what are the time units for time of goodness? As specified in request?


class MeasurementBasis(Enum):
    Z = 0
    X = auto()
    Y = auto()
    ZPLUSX = auto()
    ZMINUSX = auto()


@dataclass
class ResCreateAndMeasure(ResCreate):
    """Response corresponding to create and measure request.

    Note
    ----
    Based on Figure 4 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    measurement_outcome: bool = 0  # outcome of the measurement performed on the entangled pair
    measurement_basis: MeasurementBasis = MeasurementBasis.Z  # which basis the entangled pair was measured in
    # NOTE: this does not take rotations on the qubit before measurement into account.


@dataclass
class ResRemoteStatePrep(ResCreate):
    """Response corresponding to create and measure request.

    Note
    ----
    Based on Figure 4 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    measurement_outcome: bool = 0  # outcome of the measurement performed on the entangled pair
    measurement_basis: MeasurementBasis = MeasurementBasis.Z  # which basis the entangled pair was measured in
    # NOTE: this does not take rotations on the qubit before measurement into account.
    # NOTE: measurement outcome field is only valid on creator side


class ErrorCode(Enum):
    UNSUPP = 0
    NOTIME = auto()
    NORES = auto()
    TIMEOUT = auto()
    REJECTED = auto()
    OTHER = auto()
    EXPIRE = auto()
    CREATE = auto()


@dataclass
class ResError:
    """Response when an error occurs.

    Note
    ----
    Based on Figure 5 of https://tools.ietf.org/pdf/draft-dahlberg-ll-quantum-03.pdf (updated link-layer protocol).

    """

    create_id: int = 0  # the same as the Create ID returned to the requester
    error_code: ErrorCode = ErrorCode.UNSUPP  # the error that occured in the EGP
    use_sequence_number_range: bool = 0  # specifies whether a range of sequence numbers should be expired
    sequence_number_low: int = 0  # lower bound of range of sequence numbers to expire
    sequence_number_high: int = 0  # upper bound of range of sequence numbers to expire
    origin_node_id: int = 1  # used if the node is directly connected to multiple nodes


def get_creator_node_id(local_node_id, response):
    """Returns the node ID of the node that submitted the given create request"""
    if response.directionality_flag == 1:
        return response.remote_node_id
    else:
        return local_node_id
