import wash


def main() -> None:
    customer_num = 0
    bay_num = 0
    total_customers = 0

    grand_total: float = 0
    tip_total: float = 0

    service_totals: list[float] = [0, 0, 0, 0, 0, 0]
    car_wash_status = wash.Status.NOT_FULL
    bay_status = wash.Status.NOT_FULL

    while True:
        print(
            "a)\tAccept Customer's Information and Payment\n"
            "b)\tWash Car\n"
            "c)\tDisplay Returning Customers\n"
            "d)\tDisplay Sales Report\n"
            "e)\tExit Program"
        )

        while True:
            selection = input("Select any option: ")
            selection = selection.lower()

            if not "a" <= selection <= "e":
                print("Invalid entry.")
            else:
                break

        if selection == "a":
            choices = [0, 1, 2, 3, 4, 5, 6]

            car_wash_status = wash.capacity_check(customer_num)

            print(f"Number of spaces occupied: {customer_num}")

            if car_wash_status == wash.Status.NOT_FULL:
                customer_num += 1
                total_service_cost: float = 0
                tip_amount: float = 0
                card_amount: float = 0

                customer = wash.record_information()

                print(
                    f"1. {'Wash and Vacuum':<35} {wash.SERVICE_COSTS[1]:.2f}\n"
                    f"2. {'Engine Wash':<35} {wash.SERVICE_COSTS[2]:.2f}\n"
                    f"3. {'Polishing':<35} {wash.SERVICE_COSTS[3]:.2f}\n"
                    f"4. {'Buffing':<35} {wash.SERVICE_COSTS[4]:.2f}\n"
                    f"5. {'Roof Cleaning':<35} {wash.SERVICE_COSTS[5]:.2f}\n"
                    f"6. {'Interior Shampooing':<35} {wash.SERVICE_COSTS[6]:.2f}"
                )

                while True:
                    try:
                        choice = int(input("Select any choices (-1 when done): "))
                        if not 1 <= choice <= 6:
                            if choice == -1:
                                break
                            else:
                                raise ValueError
                    except ValueError:
                        print("Invalid entry.")
                    else:
                        if choices[choice] == 0:
                            print("Already selected.")
                        else:
                            choices[choice] = 0

                            service_cost = wash.calculate_service_cost(choice)
                            total_service_cost += service_cost

                            choice -= 1
                            service_totals[choice] += service_cost

                grand_total += total_service_cost

                while True:
                    tip_choice = input("Do you want to tip (Y/N): ")
                    tip_choice = tip_choice.upper()

                    if tip_choice not in {"Y", "N"}:
                        print("Invalid entry.")
                    else:
                        break

                if tip_choice == "Y":
                    tip_amount = total_service_cost * wash.TIP_PERCENTAGE
                    tip_total += tip_amount

                if customer.pay_method == wash.PaymentMethod.CARD:
                    card_amount = total_service_cost * wash.CARD_PERCENTAGE
                    grand_total += card_amount

                total = wash.calculate_total_cost(
                    total_service_cost, tip_amount, card_amount
                )

                wash.print_receipt(
                    customer, total_service_cost, tip_amount, card_amount, total
                )

                with open("data.txt", "a") as f:
                    f.write(
                        f"{customer.name}, {customer.plate_num}, {customer.pay_method.name}, {total:.2f}\n"
                    )

                total_customers = wash.update_customer_total(total_customers)
            else:
                print("Maximum capacity reached.")
        elif selection == "b":
            bay_status = wash.bay_check(bay_num)

            wash.show_bay_status()
            print(f"Number of customers: {customer_num}")
            print(f"Number of car(s) in wash bay: {bay_num}")

            while True:
                print(
                    "1.\tAdd car to wash bay\n"
                    "2.\tRemove car from wash bay\n"
                    "3.\tGo back to main menu"
                )

                while True:
                    try:
                        choice = int(input("Enter choice: "))
                        if not 1 <= choice <= 3:
                            raise ValueError
                    except ValueError:
                        print("Invalid entry.")
                    else:
                        break
                break

            if choice == 1:
                if bay_status == wash.Status.NOT_FULL and customer_num >= 1:
                    print("Adding car to wash bay...")

                    bay_choice = wash.add_car()

                    print(f"Added car to bay #{bay_choice}")

                    bay_num += 1
                    customer_num -= 1
                else:
                    print("Cannot be selected.")
            elif choice == 2:
                if bay_num >= 1:
                    print("Removing car from bay...")

                    bay_choice = wash.remove_car()

                    print(f"Removed car from bay #{bay_choice}")

                    bay_num -= 1
                else:
                    print("Cannot be selected.")
            else:
                print("Returning to main menu...")
        elif selection == "c":
            if customer_num < 1:
                print("This cannot be selected.")
            else:
                wash.show_repeat_customers()
        elif selection == "d":
            if customer_num < 1 and bay_num < 1:
                print("Cannot be selected.")
            else:
                wash.display_sales(
                    service_totals, total_customers, grand_total, tip_total
                )
        else:
            print("Exiting program...")
            break

    input("Press ENTER to close program...")


if __name__ == "__main__":
    main()
