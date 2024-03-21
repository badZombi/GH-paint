import argparse
import os
from PIL import Image
import matplotlib as mpl
from datetime import datetime, timedelta
from subprocess import Popen

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
        return datetime(year, month, day).replace(hour=16, minute=20)
    else:
        sub = day - this_day
        newday = datetime(year, month, day) - timedelta(days=this_day)
        print("The previous Sunday was {}.".format(newday.strftime('%Y-%m-%d')))
        return newday.replace(hour=16, minute=20)

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
    pixels = []
    pixel = 1
    while x < h:
        y = 0
        print("week of {}".format(active_day.strftime('%m-%d-%Y')))
        while y < v:
            r, g, b, a = image_data[x,y]
            hex = f"{r:02x}{g:02x}{b:02x}"
            commits = hex_to_daily_commit_count[hex]
            print("We need {} commits on {}".format(commits, active_day.strftime('%m-%d-%Y')))
            
            pixels.append({
                "date": active_day,
                "commits": commits
            })

            y = y + 1
            active_day = active_day + timedelta(days=1)
        x = x + 1
    return pixels

def main():
    args = arguments()
    curr_date = datetime.now()

    # print(curr_date.replace(hour=20, minute=0))
    col=None
    if args.columns:
        col = args.columns

    # map_image(args.image, start_date, col)

    curr_date = datetime.now()
    # directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repo = args.repo
    if repo is not None:
        start = repo.rfind('/') + 1
        end = repo.rfind('.')
        directory = repo[start:end]
        print("Creating new repo in {} dir".format(directory))

    os.mkdir(directory)
    os.system('cp {} {}/{}'.format(args.image, directory, "src_image"))
    os.chdir(directory)
    run(['git', 'init'])
    start_date = find_sunday_before_date(args.year, args.month, args.day)

    pixels = map_image("src_image", start_date, col)
    # print(pixels)
    for p in pixels:
        # print(p)
        this_commit = 0
        while this_commit < p['commits']:
            date = p['date'].replace(hour=16, minute=20)
            commit(date + timedelta(minutes=this_commit))
            this_commit = this_commit + 1
    run(['git', 'remote', 'add', 'origin', repo])
    run(['git', 'push', '-u', 'origin', 'main'])

def commit(date):
    filename = "{}.py".format(date.strftime('%m%d%Y'))
    with open(os.path.join(os.getcwd(), filename), 'a') as file:
        file.write(code(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % code(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])

def code(date):
    return "print('yep' if this_is_art else 'meh') # {}".format(date.strftime('%H:%M:%S'))

def comment(date):
    return "pixel data for {}".format(date.strftime('%H:%M:%S'))

def run(commands):
    Popen(commands).wait()

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image',
                        required=False, type=str, default="gh1.png",
                        help="""the image to be drawn""")
    parser.add_argument('-m', '--month',
                        required=True, type=int,
                        help="""month of start date""")
    parser.add_argument('-d', '--day',
                        required=True, type=int,
                        help="""day of start date""")
    parser.add_argument('-y', '--year',
                        required=True, type=int,
                        help="""year of start date""")
    parser.add_argument('-c', '--columns',
                        required=False, type=int,
                        help="""max number of columns to process""")
    parser.add_argument('-r', '--repo',
                        required=True, type=str,
                        help="""the github repository to push to""")
    return parser.parse_args()
                        



if __name__ == "__main__":
    main()