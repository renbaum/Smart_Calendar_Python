import datetime
import re


class Reminder:
    def __init__(self, reminder_text : str):
        self.reminder_text = reminder_text

class BirthdayReminder(Reminder):
    def __init__(self, reminder_date : str, reminder_text : str):
        super().__init__(reminder_text)
        try:
            self.reminder_date = datetime.datetime.strptime(reminder_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect format")

    def __str__(self):
        d = datetime.datetime.now()
        future_date = self.reminder_date.replace(year=d.year)
        if future_date < d: future_date = future_date.replace(year=d.year + 1)

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
