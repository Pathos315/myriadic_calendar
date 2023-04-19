import datetime
from typing import SupportsIndex

DAYS_IN_MONTH = [
    -1,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    28,
    1,
]
DAYNAMES = [
    None,
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
MONTHNAMES = [
    None,
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "Sol",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "Intercalary",
]
DAYS_BEFORE_MONTH = [-1]
days_before_month = 0
for days_in_month in DAYS_IN_MONTH[1:]:
    DAYS_BEFORE_MONTH.append(days_in_month)
    days_before_month += days_in_month
del days_before_month, days_in_month


def myriadic_is_leap(year):
    """Determine whether the given year is a leap year in the Myriadic calendar"""
    return year % 4 == 0 and year % 128 != 0


def myriadic_days_in_months(year, month):
    """Determine the number of days in the given month in the given year in the Myriadic calendar"""
    assert 1 <= month <= 14, f"Month must be in 1..14, not {month}"
    if month == 14:
        return 2 if myriadic_is_leap(year) else 1
    else:
        return DAYS_IN_MONTH[month]


def myriadic_days_before_year(year):
    """Determine the number of days before January 1st of the given year in the Myriadic calendar"""
    return (year - 1) * 365 + ((year - 1) // 4 - (year - 1) // 128)


def myriadic_days_before_month(year, month):
    """Determine the number of days in the year preceding the first day of the given month in the Myriadic calendar"""
    assert 1 <= month <= 14, f"Month must be in 1..14, not {month}"
    return DAYS_BEFORE_MONTH[month] + (month > 14 and myriadic_is_leap(year))


def myriadic_ymd2ord(year, month, day):
    """Convert a date in the Myriadic calendar to an ordinal, considering January 1st, 1 as day 1"""
    return (
        myriadic_days_before_year(year) + myriadic_days_before_month(year, month) + day
    )


DI128Y = myriadic_days_before_year(129)  # number of days in 128 years
DI4Y = 4 * 365 + 1  # number of days in 4 years

assert DI4Y == 1461, f"`DI4Y` must be in 1461, not {DI4Y}"
assert DI128Y == 46751, f"`DI128Y` must be in 46751, not {DI128Y}"


def myriadic_ord2ymd(cumulative_number_of_days: int):
    "ordinal -> (year, month, day), considering 01-Jan-0001 as day 1."

    # subtract 1 from cumulative_number_of_days to make it 0-based
    cumulative_number_of_days -= 1

    # calculate number of 128-year cycles preceding cumulative_number_of_days
    number_of_preceding_128_year_cycles, cumulative_number_of_days = divmod(
        cumulative_number_of_days, DI128Y
    )
    year = number_of_preceding_128_year_cycles * 128

    # calculate number of 4-year cycles preceding cumulative_number_of_days
    number_of_preceding_4_year_cycles, cumulative_number_of_days = divmod(
        cumulative_number_of_days, DI4Y
    )

    # calculate number of years (1-year cycles) preceding cumulative_number_of_days
    number_of_preceding_1_year_cycles, cumulative_number_of_days = divmod(
        cumulative_number_of_days, 365
    )

    # add up the number of years
    year += number_of_preceding_4_year_cycles * 4 + number_of_preceding_1_year_cycles

    # add the myriadic value
    year += 10000

    # determine if this is a leap year
    leapyear = myriadic_is_leap(year)
    if number_of_preceding_1_year_cycles == 4 or (
        number_of_preceding_128_year_cycles == 4
        and number_of_preceding_4_year_cycles == 31
    ):
        assert cumulative_number_of_days == 0
        return year - 1, 14, 2

    # if this is a leap year and we're in the last month, return it
    elif (
        leapyear
        and number_of_preceding_1_year_cycles >= 3
        and (
            number_of_preceding_4_year_cycles != 31
            or number_of_preceding_128_year_cycles == 3
        )
    ):
        month = 14
        day = number_of_preceding_1_year_cycles - 1
        return year, month, day
    month = 1
    day = cumulative_number_of_days
    while day >= myriadic_days_in_months(year, month):
        day -= myriadic_days_in_months(year, month)
        month += 1
    return year, month, day + 1


def myriadic_ctime(year, month, day):
    "Return ctime() style string."
    weekday = myriadic_ymd2ord(year, month, day) % 7 or 7
    base_year = year - 9999
    myriad = 1 if year >= 10000 else 0
    return f"{DAYNAMES[weekday]}, {myriad}-{base_year} {MONTHNAMES[month]} {day}"


def myriadic_conversion(
    year: SupportsIndex,
    month: SupportsIndex,
    day: SupportsIndex,
):
    ordinalized_date: int = datetime.date(year, month, day).toordinal()
    date: tuple[int, int, int] = myriadic_ord2ymd(ordinalized_date)
    date_named: str = myriadic_ctime(*date)
    print(
        f"The date {year}, {month}, {day} would be {date_named} in the Myriadic Calendar."
    )


if __name__ == "__main__":
    myriadic_conversion(2023, 4, 19)
