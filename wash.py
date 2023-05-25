from enum import Enum, IntEnum
from dataclasses import dataclass

TOTAL_VEHICLE_CAPACITY: int = 20
WASH_BAY_CAPACITY: int = 3
TIP_PERCENTAGE: float = 0.02
CARD_PERCENTAGE: float = 0.03
MAX_NAME_LENGTH: int = 50


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


def record_information() -> Customer:
    while True:
        customer_name = input("Enter name of customer: ")

        if len(customer_name) > MAX_NAME_LENGTH:
            print("Name length exceeded.")
        else:
            break

    while True:
        customer_plate_num = input("Enter customer's license plate number: ")

        check = license_check(customer_plate_num)

        if check is False:
            print(
                "Invalid license plate number. Try again.\n"
                "License plate number should have\n"
                "4 digits and by 2 capital letters."
            )
        else:
            break

    while True:
        print(
            f"{PaymentMethod.CASH}.\t{PaymentMethod.CASH.name}\n"
            f"{PaymentMethod.CARD}.\t{PaymentMethod.CARD.name}"
        )

        try:
            customer_pay_method = int(input("Select customer's payment method: "))
            if not PaymentMethod.CASH <= customer_pay_method <= PaymentMethod.CARD:
                raise ValueError
        except ValueError:
            print("Invalid entry.")
        else:
            break

    customer = Customer(
        name=customer_name,
        plate_num=customer_plate_num,
        pay_method=PaymentMethod(customer_pay_method),
    )

    return customer


def license_check(license: str) -> bool:
    valid_license = True

    if len(license) != 6:
        valid_license = False
        return valid_license

    if not license[:4].isdigit():
        valid_license = False
        return valid_license

    if not license[4:].isupper():
        valid_license = False
        return valid_license

    return valid_license
