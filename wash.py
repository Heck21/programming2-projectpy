from enum import Enum, IntEnum
from dataclasses import dataclass

TOTAL_VEHICLE_CAPACITY: int = 20
WASH_BAY_CAPACITY: int = 3
TIP_PERCENTAGE: float = 0.02
CARD_PERCENTAGE: float = 0.03


class Status(Enum):
    NOT_FULL = 0
    FULL = 1


class Bay(Enum):
    VACANT = 0
    OCCUPIED = 1


class PaymentMethod(IntEnum):
    CASH = 1
    CARD = 2


@dataclass(kw_only=True)
class Customer:
    name: str
    plate_num: str
    pay_method: PaymentMethod


SERVICE_COSTS = (
    0.0,
    2500.0,
    2000.0,
    3500.0,
    5500.0,
    3200.0,
    7500.0,
)

bays = [Bay.VACANT for _ in range(WASH_BAY_CAPACITY)]


def capacity_check(status: Status, cust_num: int) -> Status:
    if cust_num >= TOTAL_VEHICLE_CAPACITY:
        status = Status.FULL
    else:
        status = Status.NOT_FULL

    return status
