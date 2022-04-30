from calendar import HTMLCalendar 
from datetime import date, datetime

class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, highlight=[], booked=[], date=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._highlight = highlight
            self._booked = booked
            self._date = date
            
    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return super().formatday(0,0)
        elif day in self._highlight:
            return '<td class="%s" bgcolor="pink"><a href="" class="header__link"> %d</a></td>' % (self.cssclasses[weekday], day)
        elif day in self._booked:
            year = datetime.fromisoformat(str(self._date)).year
            month = datetime.fromisoformat(str(self._date)).month
            formatted_date=date(year,month,day).isoformat()
            return f'<td class="{self.cssclasses[weekday]}" bgcolor="red"><a href="?date={formatted_date}" class="header__link"> {day}</a></td>'
        else:
            year = datetime.fromisoformat(str(self._date)).year
            month = datetime.fromisoformat(str(self._date)).month
            formatted_date=date(year,month,day).isoformat()
            return f'<td class="{self.cssclasses[weekday]}"><a href="?date={formatted_date}" class="header__link"> {day}</a></td>'
        