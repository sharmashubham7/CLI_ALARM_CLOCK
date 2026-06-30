# CLI_ALARM_CLOCK
CLI based alarm clock
# Alarm Clock (CLI)

A small command-line alarm clock written in Python, standard library only — no
dependencies, no web UI, no database. You set alarms by 24-hour time, list them
with a live countdown, and the program rings when each is due. Alarms are
daily-recurring: once one fires, it re-arms for the same time the next day.

## Features

- Set alarms by absolute 24-hour time (`HH:MM`), with an optional label
- List active alarms, sorted by next fire time, each with a derived countdown
- Rings due alarms with the terminal bell and a printed message
- Daily-recurring alarms (a fired alarm re-arms for the same time tomorrow)
- Input validation that rejects malformed times without crashing

## Requirements

- Python 3.10+ (uses standard-library modules only)

## Usage

Run the program:

```bash
python alarm.py
```

You'll get an interactive prompt. Commands:

| Command | Description |
|---|---|
| `set HH:MM [label]` | Add an alarm at the given 24-hour time, with an optional label |
| `list` | Show active alarms with their countdowns |
| `quit` | Exit |

Example session:

```
alarm clock — commands: set HH:MM [label] | list | quit
> set 07:30 wake up
set 'wake up' for 07:30 (rings in 9h 12m)
> set 06:00 gym
> list
  06:00  gym  (rings in 7h 42m)
  07:30  wake up  (rings in 9h 12m)
> quit
```

If you set a time that has already passed today, it automatically rolls to the
next day, so an alarm always points at its next future occurrence.


## Design notes

A few decisions worth calling out:

- **The clock is injected.** Core functions (`due_alarms`, `parse_alarm_time`)
  take the current time as an argument instead of reading the system clock. This
  keeps the logic pure and deterministic, so it can be tested instantly without
  waiting on real time.
- **Daily-recurring by design, so there's no "has fired" flag.** When an alarm
  rings, its fire time is bumped forward a day, which naturally silences it until
  the next occurrence. The forward bump does the work a status flag otherwise
  would, so that state simply doesn't exist.
- **Source of truth, derived views.** Each alarm stores only its fire time; the
  countdown shown in `list` is computed on demand against the current time. A
  stored countdown would go stale the moment the clock ticked.
- **Parse at the boundary.** The user types a simple `HH:MM` string, which is
  normalized into a `datetime` immediately. Simple input at the edge, a rich type
  in the core.

## Known limitations

- **Alarms are checked on each input.** The loop uses blocking input, so a due
  alarm rings when you next press Enter rather than in continuous real time.
  Real-time firing would need a background ticker or non-blocking input
  (e.g. `select`).
- **Local time only.** Times are naive and assume the system's local time zone;
  there's no time-zone or DST handling.
- **Session-scoped.** Alarms live only while the program is running; they are not
  persisted across runs.

## Possible improvements

In rough priority order:

1. Real-time firing (background ticker / non-blocking input)
2. Persistence across runs (e.g. a JSON file)
3. Removing and editing alarms
4. Snooze
5. Time-zone awareness
