import datetime



class Reminder:
    def __init__(self, reminder_text : str):
        self.reminder_text = reminder_text

class BirthdayReminder(Reminder):
    def __init__(self, reminder_date : str, reminder_text : str):
        super().__init__(reminder_text)
        self.reminder_date = datetime.datetime.strptime(reminder_date, "%Y-%m-%d")

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
        self.reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")

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
                reminder_text = input("Enter text: ")
                return NoteReminder(reminder_time, reminder_text)
            case "birthday":
                reminder_date = input(f'{i}. Enter date of birth in "YYYY-MM-DD" format: ')
                reminder_text = input("Enter name: ")
                return BirthdayReminder(reminder_date, reminder_text)
            case _:
                raise ValueError(f"Unknown reminder type: {reminder_type}")

    def create_reminders_list(self, reminder_type: str) -> list:
        reminders_list = []
        cnt = 0
        match reminder_type.lower():
            case "note":
                cnt = int(input("How many notes would you like to add: "))
            case "birthday":
                cnt = int(input("How many dates of birth would you like to add: "))
            case _:
                raise ValueError(f"Unknown reminder type: {reminder_type}")

        for i in range(1, cnt + 1):
            reminder = self.create_reminder(reminder_type, i)
            if reminder is not None:
                reminders_list.append(reminder)
        return reminders_list