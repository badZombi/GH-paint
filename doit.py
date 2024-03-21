import argparse
from PIL import Image
import matplotlib as mpl
from datetime import datetime, timedelta

hex_to_daily_commit_count = {
    "39d353": 20,
    "26a641": 15,
    "006d32": 10,
    "0e4429": 5,
    "161b22": 0,
    "000000": 0
}

def find_sunday_before_date(year, month, day):
    this_day = check_day(year, month, day)
    if (this_day == 0):
        print("We can start on this day.")
        return datetime(year, month, day)
    else:
        sub = day - this_day
        newday = datetime(year, month, day) - timedelta(days=this_day)
        print("The previous Sunday was {}.".format(newday.strftime('%Y-%m-%d')))
        return newday

def check_day(year, month, day):
    try:
        # Create a datetime object for the given date
        given_date = datetime(year, month, day)
        days = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }
        # Use isoweekday() to get the weekday (Monday is 1 and Sunday is 7)
        numeric_day_of_week = given_date.isoweekday() % 7  # Convert Sunday from 7 to 0
        day_of_the_week = days[numeric_day_of_week]
        
         
        # Print the result
        print(f"The day of the week for {given_date.strftime('%Y-%m-%d')} is {day_of_the_week}")
         
    except ValueError as e:
        print(f"Error: {e}")
    return numeric_day_of_week
 

def rgb2hex(rgb):
    return mpl.colors.rgb2hex(rgb, keep_alpha=True)

def map_image(image, start_date, col):

    im = Image.open(image)
    image_data = im.load()
    h, v =  im.size 
    y = 0
    x = 0
    if col:
        h = col
    active_day = start_date

    while x < h:
        y = 0
        print("week of {}".format(active_day.strftime('%m-%d-%Y')))
        while y < v:
            r, g, b, a = image_data[x,y]
            hex = f"{r:02x}{g:02x}{b:02x}"
            print("We need {} commits on {}".format(hex_to_daily_commit_count[hex], active_day.strftime('%m-%d-%Y')))
            y = y + 1
            active_day = active_day + timedelta(days=1)
        x = x + 1


def main():
    args = arguments()
    curr_date = datetime.now()

    # print(curr_date.replace(hour=20, minute=0))
    start_date = find_sunday_before_date(args.year, args.month, args.day)
    col=None
    if args.columns:
        col = args.columns

    map_image(args.image, start_date, col)

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image',
                        required=False, type=str, default="gh1.png",
                        help="""the image to be drawn""")
    parser.add_argument('-m', '--month',
                        required=True, type=int,
                        help="""theimage to be drawn""")
    parser.add_argument('-d', '--day',
                        required=True, type=int,
                        help="""theimage to be drawn""")
    parser.add_argument('-y', '--year',
                        required=True, type=int,
                        help="""theimage to be drawn""")
    parser.add_argument('-c', '--columns',
                        required=False, type=int,
                        help="""max number of rows to process""")
    return parser.parse_args()
                        



if __name__ == "__main__":
    main()