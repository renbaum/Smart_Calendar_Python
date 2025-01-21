import datetime
import reminder

if __name__ == "__main__":
    factory = reminder.ReminderFactory()
    storage = reminder.ReminderList()

    print("Current date and time:")
    d = datetime.datetime.now()
    d = d.strftime("%Y-%m-%d %H:%M")
    print(d)
    while True:
        try:
            command = input("Enter the command (add, view, delete, exit): ")
            match command.lower():
                case "add":
                    reminder_type = input("Specify type (note, birthday): ")
                    lst = factory.create_reminders_list(reminder_type)
                    storage.add_reminders_list(lst)
                    for rem in lst:
                        print(rem)
                    print()
                case "exit":
                    print("Goodbye!")
                    break
                case "view":
                    storage.view_reminders()
                case "delete":
                    print("Not implemented yet")
                case _:
                    raise ValueError("Incorrect command")
        except ValueError as e:
            print(e)

