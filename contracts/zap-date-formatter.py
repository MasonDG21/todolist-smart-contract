from datetime import datetime, timedelta, timezone
from dateutil import parser

# Input data (represents the Input_Data fields in a code by Zapier module)
input_data = {
    'time': '2024-07-26 9:30 PM',  # Example input
    'timezone_in': 'UTC',  # Example input
    'timezone_out': 'Australia/Sydney'  # Example input
}

time = input_data['time']
timezone_in = input_data['timezone_in']
timezone_out = input_data['timezone_out']

# Timezone offsets for common timezones
timezones = {
    'UTC': 0,
    'Australia/Sydney': 10,
    'America/New_York': -5,
    'America/Chicago': -6,
    'America/Denver': -7,
    'America/Los_Angeles': -8,
    'Europe/London': 0,
    'Europe/Berlin': 1,
    'Europe/Paris': 1,
    'Asia/Tokyo': 9,
    'Asia/Shanghai': 8,
    'Asia/Kolkata': 5.5,
    'Asia/Dubai': 4,
    'Africa/Johannesburg': 2,
    'Pacific/Auckland': 12,
    'Australia/Adelaide': 9.5,
    'America/Toronto': -5,
    'America/Sao_Paulo': -3,
    'Asia/Singapore': 8,
    'Asia/Hong_Kong': 8
}

# Function to check for DST in a given timezone
def is_dst(dt, timezone):
    if timezone in ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Toronto']:
        start = datetime(dt.year, 3, 8)
        end = datetime(dt.year, 11, 1)
        dst_start = start + timedelta(days=(6-start.weekday()))  # Second Sunday in March
        dst_end = end + timedelta(days=(6-end.weekday()))  # First Sunday in November
        return dst_start <= dt < dst_end
    elif timezone in ['Europe/London', 'Europe/Berlin', 'Europe/Paris']:
        start = datetime(dt.year, 3, 25)
        end = datetime(dt.year, 10, 25)
        dst_start = start + timedelta(days=(6-start.weekday()))  # Last Sunday in March
        dst_end = end + timedelta(days=(6-end.weekday()))  # Last Sunday in October
        return dst_start <= dt < dst_end
    elif timezone in ['Australia/Sydney', 'Australia/Adelaide']:
        start = datetime(dt.year, 10, 1)
        end = datetime(dt.year, 4, 1)
        dst_start = start + timedelta(days=(6-start.weekday()))  # First Sunday in October
        dst_end = end + timedelta(days=(6-end.weekday()))  # First Sunday in April
        return dst_start <= dt < dst_end
    elif timezone == 'Pacific/Auckland':
        start = datetime(dt.year, 9, 25)
        end = datetime(dt.year, 4, 1)
        dst_start = start + timedelta(days=(6-start.weekday()))  # Last Sunday in September
        dst_end = end + timedelta(days=(6-end.weekday()))  # First Sunday in April
        return dst_start <= dt < dst_end
    else:
        return False

# Function to parse date strings
def parse_date(date_str):
    try:
        return parser.parse(date_str)
    except parser.ParserError:
        date_formats = [
            "%Y/%m%d %I:%M%p",  # 2024/0726 9:30PM
            "%A, %B %d, %Y, %I:%M:%S %p"  # Tuesday, July 23, 2024, 10:30:00 PM
        ]
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        raise ValueError(f"Unknown date format: {date_str}")

# Function to make datetime offset-aware
def make_aware(dt, offset):
    return dt.replace(tzinfo=timezone(timedelta(hours=offset)))

# Convert the input date string to a datetime object
start_time = parse_date(time)

# Adjust for timezone offset
timezone_in_offset = timezones.get(timezone_in)
timezone_out_offset = timezones.get(timezone_out)

# Error handling for undefined timezones
if timezone_in_offset is None:
    raise ValueError(f"Timezone '{timezone_in}' is not defined.")
if timezone_out_offset is None:
    raise ValueError(f"Timezone '{timezone_out}' is not defined.")

# Ensure both datetimes are aware
start_time = make_aware(start_time, timezone_in_offset)
time_difference = timezone_out_offset - timezone_in_offset
start_time_out_tz = start_time + timedelta(hours=time_difference)
start_time_out_tz = make_aware(start_time_out_tz, timezone_out_offset)

# Format the date and time in the output timezone
formatted_date = start_time_out_tz.strftime("%A, %B %d")
day_suffix = 'th'
if 4 <= start_time_out_tz.day <= 20 or 24 <= start_time_out_tz.day <= 30:
    day_suffix = 'th'
else:
    day_suffix = ['st', 'nd', 'rd'][start_time_out_tz.day % 10 - 1]

formatted_time = start_time_out_tz.strftime("%I:%M%p").lower()

# Construct the pretty printed output in the output timezone
pretty_output = f"{formatted_date}{day_suffix} {start_time_out_tz.year} @ {formatted_time} ({timezone_out})"
pretty_output_short = f"{formatted_date}{day_suffix} @ {formatted_time} ({timezone_out})"

# Additional formats in the output timezone
format_iso = start_time_out_tz.isoformat()
format_slash = start_time_out_tz.strftime("%Y/%m/%d")
format_slash_time = start_time_out_tz.strftime("%Y/%m/%d %I:%M%p").lower()
format_dash = start_time_out_tz.strftime("%Y-%m-%d %H:%M:%S")
format_us = start_time_out_tz.strftime("%m/%d/%Y %I:%M %p").lower()
format_eu = start_time_out_tz.strftime("%d-%m-%Y %H:%M")

# Formats in the input timezone
formatted_date_in = start_time.strftime("%A, %B %d")
formatted_time_in = start_time.strftime("%I:%M%p").lower()

pretty_output_in = f"{formatted_date_in}{day_suffix} {start_time.year} @ {formatted_time_in} ({timezone_in})"
pretty_output_short_in = f"{formatted_date_in}{day_suffix} @ {formatted_time_in} ({timezone_in})"

# Output dictionary
output = {
    'pretty_long': pretty_output,
    'pretty_short': pretty_output_short,
    'iso_format': format_iso,
    'slash_format': format_slash,
    'slash_format_with_time': format_slash_time,
    'dash_format': format_dash,
    'us_format': format_us,
    'eu_format': format_eu,
    'formatted_appointment_in_timezone_in': pretty_output_in,
    'short_format_in_timezone_in': pretty_output_short_in
}

# Print the output for demonstration purposes
print("Formatted Appointment:", output['pretty_long'])
print("Short Format:", output['pretty_short'])
print("ISO Format:", output['iso_format'])
print("Slash Format:", output['slash_format'])
print("Slash Format with Time:", output['slash_format_with_time'])
print("Dash Format:", output['dash_format'])
print("US Format:", output['us_format'])
print("EU Format:", output['eu_format'])
print("Formatted Appointment in Input Timezone:", output['formatted_appointment_in_timezone_in'])
print("Short Format in Input Timezone:", output['short_format_in_timezone_in'])
