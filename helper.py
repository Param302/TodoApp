import datetime

class TodayDateTime:
    TODAY_DATE = datetime.datetime.today()

    def get_short_date(self):
        return self.TODAY_DATE.strftime("%d-%b-%Y")

    def get_full_date(self):
        year = self.TODAY_DATE.year
        month, date, day = self.TODAY_DATE.strftime("%B %d %A").split()
        full_date = f"{day}, {date[1:] if date[0]=='0' else date}th {month}'{year%100}"
        return full_date

    def get_current_time(self):
        return datetime.datetime.now().strftime("%I : %M : %S")

if __name__ == "__main__":
    today_dt = TodayDateTime()
    print(today_dt.get_short_date())
    print(today_dt.get_full_date())
    print(today_dt.get_current_time())