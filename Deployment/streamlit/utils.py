import matplotlib.pyplot as plt

def get_delay_state(minutes):
    if (minutes < 0):
        return "early"
    elif (minutes > 0 ):
        return "late"
    else:
        return "on time"
    
def late_category(x):
    if (x > 60*24):
        return "> 1 day"
    elif (x > 60*2):
        return "> 2 hours"
    elif (x > 60):
        return "between 1h & 2h"
    elif (x > 30):
        return "between 30min & 1h"
    elif (x > 15):
        return "between 15min & 30min"
    elif (x > 0):
        return "< 15min"
    else:
        return "on time"

late_category_ordered = ["on time", "< 15min", "between 15min & 30min", "between 30min & 1h",
                               "between 1h & 2h", "> 2 hours", "> 1 day"]
    
def display_pie_chart(series):
    plt.style.use("default")
    plt.pie(series.value_counts(), labels=series.value_counts().index, autopct=lambda p:f'{p:.2f}%\n({p*sum(series.value_counts())/100 :.0f})')
    plt.figlegend(series.value_counts().index)
    plt.show()