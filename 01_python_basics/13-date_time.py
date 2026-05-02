import datetime as dt

date1 = dt.date(2021, 1, 5)
print(date1)
date_now = dt.date.today()
print(date_now)

print(f"Year: {date1.year} Month: {date1.month} Day: {date1.day}")
# ------------------------
print('\n---')
time1 = dt.time(10, 45, 30, 45667)
print(time1)
print(f"Hour: {time1.hour} Minute: {time1.minute} Second: {time1.second} Microseconds: {time1.microsecond}")
# ------------------------
print('\n---')

datetime_obj = dt.datetime(2021, 11,28, 23, 55, 59)
print(datetime_obj)
print(datetime_obj.date())
print(datetime_obj.time())

datetime_current = dt.datetime.now()

# ------------------------
print('\n---')

current_time = dt.datetime.now()
next_year = dt.datetime(2027, 2, 11)
time_remaining = next_year - current_time
print(time_remaining)

# ------------------------
print('\n---')
string_date = current_time.strftime("%A, %B %d, %Y")
print(string_date) # -> Saturday, May 02, 2026

print('\n---')
string_date = current_time.strftime("%b %-d, %I%p")
print(string_date) # -> May 2, 11AM

# ------------------------
print('\n---')
string_date = "21 June, 2021"
date_object = dt.datetime.strptime(string_date, "%d %B, %Y")
print(date_object)
