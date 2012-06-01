months = ["January", 
          "February",
          "March", 
          "April",
          "May",
          "June", 
          "July", 
          "August", 
          "September", 
          "October", 
          "November", 
          "December"]

month_dict = {m[0:3].lower() : m for m in months}


def valid_month(month):
  if month and len(month) > 2:
     month = month[0:3].lower()
     if month in month_dict:
       return month_dict[month]

def valid_day(day):
  if day and day.isdigit():
     num = int(day)
     if num > 0 and num < 32:
       return num

def valid_year(year):
  if year and year.isdigit():
     num = int(year)
     if num > 1899 and num < 2021:
       return num

