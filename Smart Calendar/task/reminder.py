import datetime


class Reminder:
    def __init__(self, reminder_time : str, reminder_text : str):
        self.reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        self.reminder_text = reminder_text

    def __str__(self):
        d = datetime.datetime.now()
        diff = self.reminder_time - d
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds= divmod(remainder, 60)
        if seconds > 0: minutes += 1

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
    def create_reminder(self, reminder_type: str) -> Reminder:

        match reminder_type.lower():
            case "note":
                reminder_time = input('Enter datetime in "YYYY-MM-DD HH:MM" format: ')
                reminder_text = input("Enter text: ")
                return Reminder(reminder_time, reminder_text)
            case _:
                raise ValueError(f"Unknown reminder type: {reminder_type}")

    def create_reminders_list(self, reminder_type: str) -> list:
        reminders_list = []
        reminder = self.create_reminder(reminder_type)
        if reminder is not None:
            reminders_list.append(reminder)
        return reminders_list