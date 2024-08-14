import csv
from datetime import datetime, timedelta
from dateutil import parser

# Function to determine if a date is in DST for a given timezone
def is_dst(dt, timezone):
    if timezone in ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Toronto']:
        start = datetime(dt.year, 3, 8)
        end = datetime(dt.year, 11, 1)
        dst_start = start + timedelta(days=(6-start.weekday()))
        dst_end = end + timedelta(days=(6-end.weekday()))
        return dst_start <= dt < dst_end
    elif timezone in ['Europe/London', 'Europe/Berlin', 'Europe/Paris']:
        start = datetime(dt.year, 3, 25)
        end = datetime(dt.year, 10, 25)
        dst_start = start + timedelta(days=(6-start.weekday()))
        dst_end = end + timedelta(days=(6-end.weekday()))
        return dst_start <= dt < dst_end
    elif timezone in ['Australia/Sydney', 'Australia/Adelaide']:
        start = datetime(dt.year, 10, 1)
        end = datetime(dt.year, 4, 1)
        dst_start = start + timedelta(days=(6-start.weekday()))
        dst_end = end + timedelta(days=(6-end.weekday()))
        return dst_start <= dt < dst_end
    elif timezone == 'Pacific/Auckland':
        start = datetime(dt.year, 9, 25)
        end = datetime(dt.year, 4, 1)
        dst_start = start + timedelta(days=(6-start.weekday()))
        dst_end = end + timedelta(days=(6-end.weekday()))
        return dst_start <= dt < dst_end
    else:
        return False

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

def parse_date(date_str):
    try:
        return parser.parse(date_str)
    except parser.ParserError:
        # Custom parsing logic for various date formats
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

def make_aware(dt, offset):
    return dt.replace(tzinfo=offset)

def run_test_cases(test_cases):
    results = []
    for i, test_case in enumerate(test_cases):
        try:
            time = test_case['time']
            timezone_in = test_case['timezone_in']
            timezone_out = test_case['timezone_out']

            # Convert the input date string to a datetime object using the custom parse_date function
            start_time = parse_date(time)

            # Adjust for timezone offset
            timezone_in_offset = timezones.get(timezone_in)
            timezone_out_offset = timezones.get(timezone_out)

            # Error handling for undefined timezones
            if timezone_in_offset is None:
                print(f"Warning: Timezone '{timezone_in}' is not defined. Proceeding without timezone adjustment.")
                timezone_in_offset = 0
            if timezone_out_offset is None:
                print(f"Warning: Timezone '{timezone_out}' is not defined. Proceeding without timezone adjustment.")
                timezone_out_offset = 0

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

            results.append({
                'test_status': 'PASSED',
                'test_data1': output['pretty_long'],
                'test_data2': output['pretty_short'],
                'test_data3': output['iso_format'],
                'test_data4': output['slash_format'],
                'test_data5': output['slash_format_with_time'],
                'test_data6': output['dash_format'],
                'test_data7': output['us_format'],
                'test_data8': output['eu_format'],
                'test_data9': output['formatted_appointment_in_timezone_in'],
                'test_data10': output['short_format_in_timezone_in']
            })

        except Exception as e:
            # Provide a basic formatted date in case of failure
            try:
                start_time = parse_date(time)
                results.append({
                    'test_status': f'FAILED with error: {e}',
                    'test_data1': start_time.strftime("%Y-%m-%d"),
                    'test_data2': start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'test_data3': start_time.strftime("%A, %B %d, %Y"),
                    'test_data4': start_time.strftime("%I:%M %p"),
                    'test_data5': start_time.strftime("%d-%m-%Y"),
                    'test_data6': '',
                    'test_data7': '',
                    'test_data8': '',
                    'test_data9': '',
                    'test_data10': ''
                })
            except Exception as parse_error:
                results.append({
                    'test_status': f'FAILED with error: {e}; Additional parsing error: {parse_error}',
                    'test_data1': '',
                    'test_data2': '',
                    'test_data3': '',
                    'test_data4': '',
                    'test_data5': '',
                    'test_data6': '',
                    'test_data7': '',
                    'test_data8': '',
                    'test_data9': '',
                    'test_data10': ''
                })

    return results

def read_test_cases_from_csv(filename):
    test_cases = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append(row)
    return test_cases

def write_test_results_to_csv(filename, test_cases, results):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    header = rows[0]
    for i, result in enumerate(results):
        row = i + 1  # assuming headers are in the first row
        rows[row][3] = result['test_status']
        rows[row][4] = result['test_data1']
        rows[row][5] = result['test_data2']
        rows[row][6] = result['test_data3']
        rows[row][7] = result['test_data4']
        rows[row][8] = result['test_data5']
        rows[row][9] = result['test_data6']
        rows[row][10] = result['test_data7']
        rows[row][11] = result['test_data8']
        rows[row][12] = result['test_data9']
        rows[row][13] = result['test_data10']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Main script
input_filename = 'timezone_testdata.csv'
test_cases = read_test_cases_from_csv(input_filename)
results = run_test_cases(test_cases)
write_test_results_to_csv(input_filename, test_cases, results)

print("Test cases executed and results written to the CSV file.")
