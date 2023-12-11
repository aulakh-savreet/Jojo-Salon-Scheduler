# Import necessary modules
import csv
import os
from appointment import Appointment


def create_weekly_calendar():
    # Create a weekly calendar with appointments from Monday to Saturday, 9 AM to 4 PM
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ["{:02d}:00".format(hour) for hour in range(9, 17)]
    return [Appointment(day, hour) for day in days for hour in hours]


def load_scheduled_appointments(calendar):
    # Load scheduled appointments from a file
    while True:
        filename = input("Enter appointment filename: ")
        if os.path.isfile(filename):
            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                count = 0
                for row in reader:
                    client_name, client_phone, appt_type, day, start_time = row
                    # Correct format for start time
                    start_time = (
                        "{:02d}:00".format(int(start_time))
                        if len(start_time) <= 2
                        else start_time
                    )
                    appointment = find_appointment(calendar, day, start_time)
                    if appointment:
                        appointment.schedule(client_name, client_phone, int(appt_type))
                        count += 1
                print(f"{count} previously scheduled appointments have been loaded.")
                break
        else:
            print("File not found. Re-enter appointment filename: ")


def find_appointment(calendar, day, start_time):
    # Find an appointment in the calendar by day and start time
    for appointment in calendar:
        if (
            appointment.get_day_of_week() == day
            and appointment.get_start_time_hour() == start_time
        ):
            return appointment
    return None


def save_scheduled_appointments(calendar):
    # Save scheduled appointments to a file
    while True:
        filename = input("Enter appointment filename: ")
        if os.path.isfile(filename):
            overwrite = input(
                "File already exists. Do you want to overwrite it (Y/N)? "
            ).lower()
            if overwrite == "y":
                break
        else:
            break

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        count = 0
        for appointment in calendar:
            if appointment.get_appt_type() != 0:
                writer.writerow(
                    [
                        appointment.get_client_name(),
                        appointment.get_client_phone(),
                        appointment.get_appt_type(),
                        appointment.get_day_of_week(),
                        appointment.get_start_time_hour(),
                    ]
                )
                count += 1
        print(f"{count} scheduled appointments have been successfully saved")


def schedule_appointment(calendar):
    # Schedule a new appointment
    print("\n** Schedule an appointment **")
    day_input = input("What day: ").capitalize()
    start_time_input = input("Enter start hour (24-hour clock): ")
    # Correct format for start time
    start_time = (
        f"{int(start_time_input):02d}:00"
        if len(start_time_input) < 3
        else start_time_input
    )
    # Validate the entered day and time
    valid_day = day_input in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    valid_time = start_time in [
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
    ]
    if not valid_day or not valid_time:
        print("Sorry, that time slot is not in the weekly calendar!")
        return
    appointment = find_appointment(calendar, day_input, start_time)
    if appointment:
        if appointment.get_appt_type() == 0:
            # Process for scheduling an appointment
            client_name = input("Client Name: ")
            client_phone = input("Client Phone: ")
            print(
                "Appointment types: 1: Mens Cut $50, 2: Ladies Cut $80, 3: Mens Colouring $50, 4: Ladies Colouring $120"
            )
            appt_type = int(input("Type of Appointment: "))
            # Validate appointment type
            if appt_type in [1, 2, 3, 4]:
                appointment.schedule(client_name, client_phone, appt_type)
                print(
                    f"OK, {client_name}'s appointment for {day_input} at {start_time} is scheduled!"
                )
            else:
                print("Sorry, that is not a valid appointment type!")
        else:
            print("Sorry, that time slot is booked already!")
    else:
        print("Error: No appointment slot found for that time.")


def find_appointment_by_name(calendar, client_name):
    # Find appointments by client name
    matching_appointments = [
        appointment
        for appointment in calendar
        if client_name.lower() in appointment.get_client_name().lower()
    ]
    print(
        "{:<20} {:<15} {:<10} {:<10} {:<10} {:<15}".format(
            "Client Name", "Phone", "Day", "Start", "End", "Type"
        )
    )
    print("-" * 80)
    for appointment in matching_appointments:
        if appointment.get_appt_type() != 0:
            # Display client name and appointment details
            client_name_display = (
                appointment.get_client_name()[:17] + "..."
                if len(appointment.get_client_name()) > 20
                else appointment.get_client_name()
            )
            client_phone_display = (
                appointment.get_client_phone()[:12] + "..."
                if len(appointment.get_client_phone()) > 15
                else appointment.get_client_phone()
            )
            appt_type_display = appointment.get_appt_type_desc()
            print(
                "{:<20} {:<15} {:<10} {:<10} {:<10} {:<15}".format(
                    client_name_display,
                    client_phone_display,
                    appointment.get_day_of_week(),
                    appointment.get_start_time_hour() + ":00",
                    appointment.get_end_time_hour() + ":00",
                    appt_type_display,
                )
            )
    if not matching_appointments:
        print("No appointments found for the client: ", client_name)


def print_calendar_for_day(calendar):
    # Print the calendar for a specific day
    print("\n** Print calendar for a specific day **")
    day_input = input("Enter day of week: ")
    day_formatted = day_input.capitalize()
    print(f"Appointments for {day_formatted}\n")
    print(
        "{:<20} {:<15} {:<10} {:<10} {:<10} {:<15}".format(
            "Client Name", "Phone", "Day", "Start", "End", "Type"
        )
    )
    print("-" * 80)
    for appointment in calendar:
        if appointment.get_day_of_week().lower() == day_input.lower():
            # Display appointment details for the specified day
            client_name_display = (
                appointment.get_client_name()
                if appointment.get_appt_type() != 0
                else ""
            )
            client_phone_display = (
                appointment.get_client_phone()
                if appointment.get_appt_type() != 0
                else ""
            )
            appt_type_display = (
                appointment.get_appt_type_desc()
                if appointment.get_appt_type() != 0
                else "Available"
            )
            print(
                "{:<20} {:<15} {:<10} {:<10} {:<10} {:<15}".format(
                    client_name_display,
                    client_phone_display,
                    appointment.get_day_of_week(),
                    appointment.get_start_time_hour() + ":00",
                    appointment.get_end_time_hour() + ":00",
                    appt_type_display,
                )
            )


def cancel_appointment(calendar):
    # Cancel an existing appointment
    day = input("What day: ").capitalize()
    start_time_input = input("Enter start hour (24-hour clock): ")
    # Correct format for start time
    start_time = (
        f"{int(start_time_input):02d}:00"
        if len(start_time_input) < 3
        else start_time_input
    )
    # Process to cancel the appointment
    appointment = find_appointment(calendar, day, start_time)
    if appointment:
        if appointment.get_appt_type() != 0:
            appointment_name = appointment.get_client_name()
            appointment.cancel()
            print(
                f"Appointment: {day} {start_time} - {appointment.get_end_time_hour()}:00 for {appointment_name} has been cancelled!"
            )
        else:
            print("That time slot isn't booked and doesn't need to be canceled.")
    else:
        print("No such appointment found.")


def print_menu():
    # Display the main menu
    print(
        """
Jojo's Hair Salon Appointment Manager
=====================================
1) Schedule an appointment
2) Find appointment by name
3) Print calendar for a specific day
4) Cancel an appointment
9) Exit the system
"""
    )


def main():
    # Main function to run the appointment manager system
    calendar = create_weekly_calendar()
    print("Starting the Appointment Manager System")
    print("Weekly calendar created")
    if (
        input(
            "Would you like to load previously scheduled appointments from a file (Y/N)? "
        ).lower()
        == "y"
    ):
        load_scheduled_appointments(calendar)
    while True:
        print_menu()
        selection = input("Enter your selection: ")
        if selection == "1":
            schedule_appointment(calendar)
        elif selection == "2":
            client_name = input("Enter Client Name: ")
            find_appointment_by_name(calendar, client_name)
        elif selection == "3":
            print_calendar_for_day(calendar)
        elif selection == "4":
            cancel_appointment(calendar)
        elif selection == "9":
            if (
                input(
                    "Would you like to save all scheduled appointments to a file (Y/N)? "
                ).lower()
                == "y"
            ):
                save_scheduled_appointments(calendar)
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
