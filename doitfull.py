import argparse
import os, sys
from PIL import Image
import matplotlib as mpl
from datetime import datetime, timedelta
from subprocess import Popen, PIPE

hex_to_daily_commit_count = {
    "39d353": 20,
    "26a641": 15,
    "006d32": 10,
    "0e4429": 5,
    "161b22": 0,
    "000000": 0
}


def find_sunday_before_date(date):
    this_day = check_day(date)
    if (this_day == 0):
        print("We can start on this day.")
        return date.replace(hour=16, minute=20)
    else:
        newday = date - timedelta(days=this_day)
        print("The previous Sunday was {}.".format(newday.strftime('%Y-%m-%d')))
        return newday.replace(hour=16, minute=20)

def check_day(given_date):
    try:
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

    col=None
    if args.columns:
        col = args.columns

    pf = 25
    if args.pushfrequency:
        pf = args.pushfrequency

    curr_date = datetime.now()
    this_sun = find_sunday_before_date(curr_date)
    first_sun = this_sun - timedelta(weeks=52)
    
    artname = args.artname
    # if repo is not None:
    #     start = repo.rfind('/') + 1
    #     end = repo.rfind('.')
    #     directory = repo[start:end]
    #     print("Creating new repo in {} dir".format(directory))
    directory = "GH-Artwork-{}".format(artname)
    if os.path.isdir(directory):
        print("{} exists".format(directory))
    else:
        print("creating repo directory")
        os.mkdir(directory)
    
    os.system('cp {} {}/{}'.format(args.image, directory, "src_image"))
    os.chdir(directory)

    if os.path.isdir('.git'):
        print("git repository is initialized. archiving...")
        os.system('mv .git .git_bk_{}'.format(curr_date.strftime('"%Y-%m-%d_%H:%M:%S"')))

    print("initializing git repository")
    run(['git', 'init'])

    repo_url = "git@github.com:{}/{}.git".format(args.username, directory)
    os.system('gh repo delete {} --yes'.format(directory)) 

    os.system('gh repo create {} --private'.format(directory)) 

    start_date = first_sun

    pixels = map_image("src_image", start_date, col)
    # print(pixels)
    run(['git', 'remote', 'add', 'origin', repo_url])
    count = 0
    for p in pixels:
        op = ""
        # print(p)
        this_commit = 0
        while this_commit < p['commits']:
            count = count + 1
            date = p['date'].replace(hour=16, minute=20)
            commit(date + timedelta(minutes=this_commit))
            this_commit = this_commit + 1
            op = op + "."
            print(op)
            if count % pf == 0:
                print("push...")
                run(['git', 'push', '-u', 'origin', 'main'], True)

    run(['git', 'push', '-u', 'origin', 'main'])

def commit(date):
    filename = "{}.py".format(date.strftime('%m%d%Y'))
    with open(os.path.join(os.getcwd(), filename), 'a') as file:
        file.write(code(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % comment(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')], True)

def code(date):
    return "print('yep' if this_is_art else 'meh') # {}".format(date.strftime('%H:%M:%S'))

def comment(date):
    return "pixel data for {}".format(date.strftime('%H:%M:%S'))

def run(commands, suppress=False):
    if suppress == True:
        process = Popen(commands, stdout=PIPE, stderr=PIPE).wait()
        # stdout, stderr = process.communicate()
        # print(stdout)
        sys.stdout.write(".")
    else:
        Popen(commands).wait()

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image',
                        required=False, type=str, default="gh1.png",
                        help="""the image to be drawn""")
    parser.add_argument('-c', '--columns',
                        required=False, type=int,
                        help="""max number of columns to process""")
    parser.add_argument('-a', '--artname',
                        required=True, type=str,
                        help="""thename of this artwork""")
    parser.add_argument('-u', '--username',
                        required=True, type=str,
                        help="""github username""")
    parser.add_argument('-pf', '--pushfrequency',
                        required=False, type=int,
                        help="""push after how many commits""")
    return parser.parse_args()
                        



if __name__ == "__main__":
    main()