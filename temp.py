from datetime import date, timedelta

week_ago = date.today() - timedelta(days=7)
print(week_ago.strftime("%m/%d/%Y"))
