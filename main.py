"""
Add an alarm for a 24-hour HH:MM, with optional label.
List all alarms with id, time, label, and armed/triggered state.
Remove an alarm by id.
Run a foreground watcher that fires due alarms (prints a clear message) and disarms them.
Persist alarms across runs in JSON; survive process restarts.
Reject invalid input (bad time format, unknown id) with a readable error, not a traceback.


execution path
Skeleton — argparse with the 4 subcommands; load()/save() helpers; storage path. (~15 min)
add / list / remove — id assignment, HH:MM parse + next-occurrence calc, validation. (~20 min)
run — poll loop, fire due alarms, print, disarm, save; Ctrl-C handling. (~15 min)
Polish — messages, --help text, edge cases, quick manual test. (~10 min)


loop in main.py -> set_alarm list_alarm quit_alarm
memory list(alarms)

"""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Alarm:
    label: str
    fire_at: datetime


def due_alarms(alarms, now):
    return [a for a in alarms if a.fire_at <= now]


def format_countdown(remaining):
    total_minutes = int(remaining.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes}m"


def parse_alarm_time(text, now):

    text = text.strip()
    hour, minute = map(int, text.split(":"))

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"time out of range: {text!r}")

    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate



def ring(alarm):
    print(f"\a*** ALARM: {alarm.label} ({alarm.fire_at:%H:%M}) ***")
    alarm.fire_at += timedelta(days=1)


def cmd_set(alarms, arg, now):
    parts = arg.split(maxsplit=1)
    if not parts or not parts[0]:
        print("usage: set HH:MM [label]")
        return
    time_str = parts[0]
    label = parts[1] if len(parts) > 1 else "alarm"
    fire_at = parse_alarm_time(time_str, now)  # may raise ValueError
    alarms.append(Alarm(label=label, fire_at=fire_at))
    print(f"set '{label}' for {fire_at:%H:%M} "
          f"(rings in {format_countdown(fire_at - now)})")


def cmd_list(alarms, now):
    if not alarms:
        print("no alarms set")
        return
    for a in sorted(alarms, key=lambda x: x.fire_at):
        print(f"  {a.fire_at:%H:%M}  {a.label}  "
              f"(rings in {format_countdown(a.fire_at - now)})")


def main():
    alarms = []
    print("alarm clock — commands: set HH:MM [label] | list | quit")
    while True:
        now = datetime.now()

        for alarm in due_alarms(alarms, now):
            ring(alarm)

        try:
            raw = input("> ").strip()
        except EOFError:
            break
        if not raw:
            continue

        command, _, arg = raw.partition(" ")
        if command == "quit":
            break
        elif command == "set":
            try:
                cmd_set(alarms, arg, now)
            except ValueError as e:
                print(f"bad time: {e}")
        elif command == "list":
            cmd_list(alarms, now)
        else:
            print(f"unknown command: {command!r}")



if __name__ == "__main__":

    main()
