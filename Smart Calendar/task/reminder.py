import datetime
import re
from abc import ABC, abstractmethod


class Reminder(ABC):
    def __init__(self, reminder_text : str):
        self.reminder_text = reminder_text

    @abstractmethod
    def get_date(self):
        pass
    @abstractmethod
    def is_date(self, d):
        pass

    def get_text(self):
        return self.reminder_text
        
    

class BirthdayReminder(Reminder):
    def __init__(self, reminder_date : str, reminder_text : str):
        super().__init__(reminder_text)
        try:
            self.reminder_date = datetime.datetime.strptime(reminder_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect format")

    def get_date(self):
        d = datetime.datetime.now()
        future_date = self.reminder_date.replace(year=d.year)
        if future_date < d: future_date = future_date.replace(year=d.year + 1)
        return future_date

    def is_date(self, d):
        return self.get_date().month == d.month and self.get_date().day == d.day

    def __str__(self):
        future_date = self.get_date()
        d = datetime.datetime.now()

        diff = future_date - d
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        if hours > 0: days += 1
        age = d.year - self.reminder_date.year
        if future_date.year != d.year: age += 1

        return f"Birthday: \"{self.reminder_text} (turns {age})\". Remains: {days} day(s)"


class NoteReminder(Reminder):
    def __init__(self, reminder_time : str, reminder_text : str):
        super().__init__(reminder_text)
        try:
            self.reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Incorrect format")

    def is_date(self, d):
        return self.get_date().year == d.year and self.get_date().month == d.month and self.get_date().day == d.day

    def get_date(self):
        d = datetime.datetime(self.reminder_time.year, self.reminder_time.month, self.reminder_time.day)
        return d

    def __str__(self):
        d = datetime.datetime.now()
        diff = self.reminder_time - d
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds= divmod(remainder, 60)
        if seconds > 0: minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 24:
            days += 1
            hours = 0

        return f"Note: \"{self.reminder_text}\". Remains: {days} day(s), {hours} hour(s), {minutes} minute(s)"


class ReminderList:
    def __init__(self):
        self.reminders_list = []

    def add_reminder(self, reminder : Reminder):
        self.reminders_list.append(reminder)

    def add_reminders_list(self, reminders_list : list):
        self.reminders_list.extend(reminders_list)

    def __str__(self):
        output = '\n'.join(str(obj) for obj in self.reminders_list)
        return output

    def print_list(self, lst):
        for reminder in lst:
            print(reminder)

    def view_reminders(self):
        while True:
            filter = input("Specify filter (all, date, text, birthdays, notes): ")
            try:
                match filter.lower():
                    case "all":
                        print(self)
                    case "date":
                        filter_date = input("Enter date in \"YYYY-MM-DD\" format: ")
                        try:
                            d = datetime.datetime.strptime(filter_date, "%Y-%m-%d")
                        except ValueError:
                            raise ValueError("Incorrect date or time values")
                        lst = [rem for rem in self.reminders_list if rem.is_date(d)]
                        self.print_list(lst)
                    case "text":
                        filter_text = input("Enter text: ")
                        lst = [rem for rem in self.reminders_list if filter_text.lower() in rem.get_text().lower()]
                        self.print_list(lst)
                    case "birthdays":
                        lst = [rem for rem in self.reminders_list if isinstance(rem, BirthdayReminder)]
                        self.print_list(lst)
                    case "notes":
                        lst = [rem for rem in self.reminders_list if isinstance(rem, NoteReminder)]
                        self.print_list(lst)
                    case _:
                        raise ValueError("Incorrect type")
                break
            except ValueError as e:
                print(e)

    def compare_date(self, param, d):
        # if param.year != d.year: return False
        if param.month != d.month: return False
        if param.day != d.day: return False
        return True


class ReminderFactory:
    def create_reminder(self, reminder_type: str, i: int) -> Reminder:
        match reminder_type.lower():
            case "note":
                reminder_time = input(f'{i}. Enter datetime in "YYYY-MM-DD HH:MM" format: ')
                self.check_date(reminder_time, reminder_type)
                reminder_text = input("Enter text: ")
                return NoteReminder(reminder_time, reminder_text)
            case "birthday":
                reminder_date = input(f'{i}. Enter date of birth in "YYYY-MM-DD" format: ')
                self.check_date(reminder_date, reminder_type)
                reminder_text = input("Enter name: ")
                return BirthdayReminder(reminder_date, reminder_text)
            case _:
                raise ValueError(f"Incorrect type")

    def create_reminders_list(self, reminder_type: str) -> list:
        reminders_list = []
        match reminder_type.lower():
            case "note":
                cntstr = input("How many notes would you like to add: ")
            case "birthday":
                cntstr = input("How many dates of birth would you like to add: ")
            case _:
                raise ValueError(f"Incorrect type")
        try:
            cnt = int(cntstr)
        except ValueError:
            raise ValueError("Incorrect number")
        except Exception:
            raise ValueError("Incorrect type")
        if cnt <= 0: raise ValueError("Incorrect number")

        for i in range(1, cnt + 1):
            reminder = self.create_reminder(reminder_type, i)
            if reminder is not None:
                reminders_list.append(reminder)
        return reminders_list

    def check_date_values(self, reminder_time, pattern):
        try:
            x = datetime.datetime.strptime(reminder_time, pattern)
        except ValueError:
            raise ValueError("Incorrect date or time values")

    def check_date_pattern(self, reminder_time, pattern):
        if not re.match(pattern, reminder_time):
            raise ValueError("Incorrect format")

    def check_date(self, date_input: str, reminder_type: str) -> bool:
        pattern = ""
        regexp = None

        match reminder_type.lower():
            case "note":
                pattern = "%Y-%m-%d %H:%M"
                regexp = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
            case "birthday":
                pattern = "%Y-%m-%d"
                regexp = r"^\d{4}-\d{2}-\d{2}$"
        self.check_date_values(date_input, pattern)
        self.check_date_pattern(date_input, regexp)

        d = datetime.datetime.strptime(date_input, pattern)
        n = datetime.datetime.now()
        if d < n and reminder_type.lower() == "note":
            raise ValueError("Incorrect format")
        if d > n and reminder_type.lower() == "birthday":
            raise ValueError("Incorrect format")
