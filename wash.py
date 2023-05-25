from enum import Enum, IntEnum
from dataclasses import dataclass
from datetime import date
from csv import DictReader

TOTAL_VEHICLE_CAPACITY: int = 20
WASH_BAY_CAPACITY: int = 3
TIP_PERCENTAGE: float = 0.02
CARD_PERCENTAGE: float = 0.03
MAX_NAME_LENGTH: int = 50


class Status(Enum):
    NOT_FULL = 0
    FULL = 1


class Bay(IntEnum):
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


current_date = date.today()

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


def capacity_check(cust_num: int) -> Status:
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


def calculate_service_cost(choice: int) -> float:
    service_cost = SERVICE_COSTS[choice]

    return service_cost


def calculate_total_cost(total_service_cost: float, tip: float, card: float) -> float:
    return total_service_cost + tip + card


def print_receipt(
    customer: Customer,
    total_service_cost: float,
    tip: float,
    card: float,
    total: float,
    date: date = current_date,
) -> None:
    print("RECEIPT\n")
    print(f"Name: {customer.name}")
    print(f"Date visited: {date:%d-%B-%Y}")
    print(f"License plate #: {customer.plate_num}")
    print(f"Method of payment: {customer.pay_method.name}")
    print(f"Total service cost: ${total_service_cost:.2f}")
    print(f"Tip percentage: {TIP_PERCENTAGE:.0%}")
    print(f"Tip amount: ${tip:.2f}")
    print(f"Card fee: ${card:.2f}")
    print(f"Total: ${total:.2f}")


def bay_check(bay_num: int) -> Status:
    if bay_num >= WASH_BAY_CAPACITY:
        status = Status.FULL
    else:
        status = Status.NOT_FULL

    return status


def show_bay_status() -> None:
    for idx, bay in enumerate(bays, start=1):
        print(f"Bay {idx}\t{bay.name}")


def bay_choice_check() -> int:
    while True:
        try:
            bay_choice = int(input("Enter bay number: "))
            if not 1 <= bay_choice <= WASH_BAY_CAPACITY:
                raise ValueError
        except ValueError:
            print("Invalid entry.")
        else:
            return bay_choice


def add_car() -> int:
    while True:
        bay_choice = bay_choice_check()
        bay_choice -= 1

        if bays[bay_choice] == Bay.OCCUPIED:
            print("That bay is not vacant. Choose another bay.")
        else:
            bays[bay_choice] = Bay.OCCUPIED
            return bay_choice + 1


def remove_car() -> int:
    while True:
        bay_choice = bay_choice_check()
        bay_choice -= 1

        if bays[bay_choice] == Bay.VACANT:
            print("That bay is not occupied.")
        else:
            bays[bay_choice] = Bay.VACANT
            return bay_choice + 1


def find_repeat_customers() -> dict:
    customer_list = {}

    with open("data.txt", newline="") as f:
        fieldnames = ["name", "license_plate", "payment_method", "amount_spent"]
        reader = DictReader(f, fieldnames=fieldnames)

        for row in reader:
            name = row["name"]
            amount = float(row["amount_spent"])

            if name not in customer_list:
                customer_list[name] = [1, amount]
            else:
                customer_list[name][0] += 1
                customer_list[name][1] += amount

    print(f"{'NAME':<30} {'TIMES VISITED':<20} {'AMOUNT SPENT ($)':>20}")
    for name, stats in customer_list.items():
        if stats[0] > 1:
            print(f"{name:<30} {stats[0]:<20} {stats[1]:>20.2f}")

    return customer_list


def most_frequent(customer_list: dict) -> None:
    sorted_dict = sorted(customer_list.items(), key=lambda item: item[1][0])

    name, stats = sorted_dict[-1]

    print("\nMOST FREQUENT CUSTOMER")
    print(f"{name:<30} {stats[0]:<20}")


def update_customer_total(cust_total: int) -> int:
    cust_total += 1

    return cust_total


def display_sales(
    totals: list[float],
    cust_total: int,
    grand_total: float,
    tip_total: float,
    date: date = current_date,
) -> None:  # TODO: add function
    print(f"Sales Report for {date: %d-%B-%Y}")
    print(f"{'SERVICE':<35} {'TOTAL ($)':>20}")
    print(f"{'Wash and Vacuum':<35} {totals[0]:>20.2f}")
    print(f"{'Engine Wash':<35} {totals[1]:>20.2f}")
    print(f"{'Polishing':<35} {totals[2]:>20.2f}")
    print(f"{'Buffing':<35} {totals[3]:>20.2f}")
    print(f"{'Roof Cleaning':<35} {totals[4]:>20.2f}")
    print(f"{'Interior Shampooing':<35} {totals[5]:>20.2f}")

    print(f"\n{'Total # of customers':<35} {cust_total:>20}")
    print(f"{'Grand Total ($)':<35} {grand_total:>20.2f}")
    print(f"{'Tips Total ($)':<35} {tip_total:>20.2f}")
