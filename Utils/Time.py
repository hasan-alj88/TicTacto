from datetime import timezone, timedelta
import re
from typing import Optional


def parse_timezone_string(tz_string: str) -> timezone:
    """
    Parse a timezone string and return a timezone object.

    Supported formats:
    - 'UTC' -> UTC timezone
    - 'UTC+3', 'UTC-5' -> UTC with offset
    - '+03:00', '-05:00' -> Direct offset format
    - '+0300', '-0500' -> Direct offset format without colon
    - '+3', '-5' -> Simple hour offset

    Args:
        tz_string (str): The timezone string to parse

    Returns:
        timezone: A timezone object

    Raises:
        ValueError: If the timezone string format is not supported

    Examples:
        >>> parse_timezone_string('UTC')
        datetime.timezone.utc
        >>> parse_timezone_string('UTC+3')
        datetime.timezone(datetime.timedelta(seconds=10800))
        >>> parse_timezone_string('+05:30')
        datetime.timezone(datetime.timedelta(seconds=19800))
    """
    if not isinstance(tz_string, str):
        raise ValueError("Timezone must be a string")

    tz_string = tz_string.strip().upper()

    # Handle UTC case
    if tz_string == 'UTC':
        return timezone.utc

    # Handle UTC+N or UTC-N format
    utc_offset_match = re.match(r'UTC([+-])(\d{1,2})(?::(\d{2}))?$', tz_string)
    if utc_offset_match:
        sign = 1 if utc_offset_match.group(1) == '+' else -1
        hours = int(utc_offset_match.group(2))
        minutes = int(utc_offset_match.group(3)) if utc_offset_match.group(3) else 0

        if hours > 14 or (hours == 14 and minutes > 0):
            raise ValueError(f"Invalid timezone offset: {tz_string}. Offset must be between -14:00 and +14:00")

        total_minutes = sign * (hours * 60 + minutes)
        return timezone(timedelta(minutes=total_minutes))

    # Handle direct offset formats: +HH:MM, -HH:MM, +HHMM, -HHMM, +H, -H
    direct_offset_match = re.match(r'([+-])(\d{1,2})(?::?(\d{2}))?$', tz_string)
    if direct_offset_match:
        sign = 1 if direct_offset_match.group(1) == '+' else -1
        hours = int(direct_offset_match.group(2))
        minutes = int(direct_offset_match.group(3)) if direct_offset_match.group(3) else 0

        if hours > 14 or (hours == 14 and minutes > 0):
            raise ValueError(f"Invalid timezone offset: {tz_string}. Offset must be between -14:00 and +14:00")

        total_minutes = sign * (hours * 60 + minutes)
        return timezone(timedelta(minutes=total_minutes))

    raise ValueError(f"Unsupported timezone format: {tz_string}")


def safe_parse_timezone_string(tz_string: str, default: Optional[timezone] = None) -> timezone:
    """
    Safely parse a timezone string with fallback to default.

    Args:
        tz_string (str): The timezone string to parse
        default (timezone, optional): Default timezone if parsing fails. Defaults to UTC.

    Returns:
        timezone: A timezone object
    """
    if default is None:
        default = timezone.utc

    try:
        return parse_timezone_string(tz_string)
    except (ValueError, TypeError):
        return default


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_cases = [
        'UTC',
        'UTC+3',
        'UTC-5',
        'UTC+10:30',
        '+03:00',
        '-05:00',
        '+0300',
        '-0500',
        '+3',
        '-5',
        '+14',
        '-12'
    ]

    print("Testing timezone parsing:")
    for tz_str in test_cases:
        try:
            tz = parse_timezone_string(tz_str)
            print(f"'{tz_str}' -> {tz}")
        except ValueError as e:
            print(f"'{tz_str}' -> Error: {e}")

    # Test invalid cases
    print("\nTesting invalid cases:")
    invalid_cases = ['UTC+25', 'invalid', '+15:00', 'GMT+3']
    for tz_str in invalid_cases:
        try:
            tz = parse_timezone_string(tz_str)
            print(f"'{tz_str}' -> {tz}")
        except ValueError as e:
            print(f"'{tz_str}' -> Error: {e}")

    # Test safe parsing
    print(f"\nSafe parsing 'invalid' -> {safe_parse_timezone_string('invalid')}")