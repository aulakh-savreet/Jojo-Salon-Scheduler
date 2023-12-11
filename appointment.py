class Appointment:
    def __init__(self, day_of_week, start_time_hour):
        self.__client_name = "Available"
        self.__client_phone = ""
        self.__appt_type = 0
        self.__day_of_week = day_of_week
        self.__start_time_hour = start_time_hour

    def get_client_name(self):
        return self.__client_name

    def get_client_phone(self):
        return self.__client_phone

    def get_appt_type(self):
        return self.__appt_type

    def get_day_of_week(self):
        return self.__day_of_week

    def get_start_time_hour(self):
        return self.__start_time_hour

    def get_end_time_hour(self):
        start_hour = int(self.__start_time_hour.split(":")[0])
        end_time = start_hour + 1
        return "{:02d}".format(end_time)

    def get_appt_type_desc(self):
        appt_types = {
            0: "Available",
            1: "Mens Cut",
            2: "Ladies Cut",
            3: "Mens Colouring",
            4: "Ladies Colouring",
        }
        return appt_types.get(self.__appt_type, "Unknown")

    def set_client_name(self, name):
        self.__client_name = name

    def set_client_phone(self, phone):
        self.__client_phone = phone

    def set_appt_type(self, appt_type):
        self.__appt_type = appt_type

    def schedule(self, client_name, client_phone, appt_type):
        self.set_client_name(client_name)
        self.set_client_phone(client_phone)
        self.set_appt_type(appt_type)

    def cancel(self):
        self.__client_name = "Available"
        self.__client_phone = ""
        self.__appt_type = 0

    def format_record(self):
        return f"{self.__client_name},{self.__client_phone},{self.__appt_type},{self.__day_of_week},{self.__start_time_hour}"

    def __str__(self):
        return (
            f"{self.__client_name:<20} {self.__client_phone:<15} "
            f"{self.__day_of_week:<10} {self.__start_time_hour}:00  -  "
            f"{self.get_end_time_hour()}:00   {self.get_appt_type_desc()}"
        )
