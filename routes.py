import uuid
from flask import render_template, request, Blueprint, current_app
from my_utils import CustomHTMLCalendar
from datetime import date
from dateutil import relativedelta

pages = Blueprint("plans", __name__, template_folder="templates", static_folder="static")

@pages.route("/", methods=["GET", "POST"])
def index():
    date_str= request.args.get("date")
    plan_get_id = request.args.get("id")
    plan_delete = request.args.get("delete")
    plan_completed =request.args.get("completed") 
    highlight = []
    
    if not date_str:
        today = date.today()
        highlight = range(today.day, today.day+1)
        date_str = date.today().isoformat()    
    
    if request.method == "POST":
        new_plan = request.form.get("plan")
        current_app.db.plans.insert_one({"_id": uuid.uuid4().hex, "date": date_str, "name" : new_plan, "completed": False})
      
    if plan_delete:
        current_app.db.plans.delete_one({"_id":plan_get_id})
        
    if plan_completed:
        current_app.db.plans.update_one({"_id":plan_get_id}, {"$set":{"completed": plan_completed}})
        
    year = date.fromisoformat(date_str).year
    month = date.fromisoformat(date_str).month
        
    current_year_month = date.fromisoformat(date_str).strftime("%Y-%m")
    next_month = date.fromisoformat(date_str) + relativedelta.relativedelta(months=1)
    prev_month = date.fromisoformat(date_str) + relativedelta.relativedelta(months=-1)

    booked=current_app.db.plans.find({"date": {"$gte": current_year_month, "$lte": next_month.strftime("%Y-%m")}}).sort("date", 1)
    
    new_booked = []
    for book in booked:
        bookdate = book["date"]
        day = date.fromisoformat(bookdate).day
        new_booked.append(day)

    c = CustomHTMLCalendar(highlight=highlight,booked=new_booked,firstweekday=0, date=date_str)
    my_calendar = c.formatmonth(year, month)
    
    plans = current_app.db.plans.find({"date": date_str})
    
    return render_template("index.html", 
                           plans=plans,
                           my_calendar=my_calendar,
                           next_month=next_month,
                           prev_month=prev_month,
                           title="Calendar"
                           )





