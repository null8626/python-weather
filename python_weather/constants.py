import re

METRIC = "C"
IMPERIAL = "F"

LOCAL_DATETIME_REGEX = re.compile(r"^\d{4}\-\d{2}\-\d{2} (\d{2})\:(\d{2}) (A|P)M$")
UTC_DATETIME_REGEX = re.compile(r"(\d{2})\:(\d{2}) (A|P)M$")
DATE_REGEX = re.compile(r"^(\d{4})\-(\d{2})\-(\d{2})$")
TIME_REGEX = re.compile(r"^(\d{2})\:(\d{2}) (A|P)M$")
LATLON_REGEX = re.compile(r"^Lat ([\d\-\.]+) and Lon ([\d\-\.]+)$")
VALID_FORMATS = ('F', 'C')

is_invalid_format = lambda fmt: not fmt or not isinstance(fmt, str) or fmt.upper() not in VALID_FORMATS