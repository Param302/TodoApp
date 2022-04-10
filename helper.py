import datetime


class TodayDateTime:
    TODAY_DATE = datetime.datetime.today()

    def get_short_date(self) -> str:
        return self.TODAY_DATE.strftime("%d-%b-%y")

    def get_full_date(self) -> str:
        year = self.TODAY_DATE.year
        month, date, day = self.TODAY_DATE.strftime("%B %d %A").split()
        full_date = f"{day}, {date[1:] if date[0]=='0' else date} {month}' {year%100}"
        return full_date

    def get_current_time(self) -> str:
        return datetime.datetime.now().strftime("%I : %M %p")


if __name__ == "__main__":
    today_dt = TodayDateTime()
    print(today_dt.get_short_date())
    print(today_dt.get_full_date())
    print(today_dt.get_current_time())
