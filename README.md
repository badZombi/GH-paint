
# GH-Paint

  

This is a little _boredom project_ I made to entertain myself. Originally it started as an automated way to fill my Github timeline with random noise during periods with little activity. I realized that drawing actual pictures would be a lot more fun and possibly even ueful so I went that route.

The idea is to create a small pixe-art file and have it parsed into varying numbers of commits in an empty project. The final timeline color is determined by how many commits are made on a day. By adjusting the total number we can control each day as a pixel on a roughly 7x53 pixel grid.

This is not a well polished project that follows any coding standards or good code practices. It was just an idea I wanted to make when I was bored.

There are 2 versions.

The more advanced or "full" version will automate the creation (and destruction) of the repo. Be caerful with this one. it is intended to place an artwork on your profile landing timeline. It will always try to start on the first day of the "last year"

# Simple version:
The simple version will place the artwork anywhere you like on your timeline. It requires an existing empty project to work.

## Setup

You will need git installed and configured with your name and email etc.

```
git clone git@github.com:badZombi/GH-paint.git
```
```
cd GH-paint
```
I'd recommend using venv.
e.g.
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
  ... and you're ready to go.

## Usage
An input image like this:

![pixel art to be converted](https://raw.githubusercontent.com/badZombi/GH-paint/main/images/doc/johnzblack.jpg)

And the command:
```
python doit.py -y=2016 -m=1 -d=1 -i=images/johnzblack.png -r=git@github.com:badZombi/jan2016-example.git
```
Will generate and push commits resulting in a timeline like this:

![pixel art to be converted](https://raw.githubusercontent.com/badZombi/GH-paint/main/images/doc/jan2016-dk.jpg)

 - date arguments: `-y=2016 -m=1 -d=1`
Pretty self explanatory. It specifies the week that your artwork will begin on. It takes the input date and figures out the previous Sunday. This will be the top "pixel" of the drawing. 

- source image path and filename: `-i=images/johnzblack.png`
The example image above is blown up for visibility. The actual input images correspond to the output where 1 pixel = 1 day so the actual source image is, in this example, 7px by 53px:  ![foo](https://raw.githubusercontent.com/badZombi/GH-paint/main/images/johnzblack.png)
Your souce image should have a limited pallette and only use the expected colors:
 
  - #39d353
  - #26a641
  - #006d32
  - #0e4429
  - #161b22
technically you can use black too (#000000) but any other colors will result in an error.

  I've used photoshop and an [online tool](https://www.pixilart.com/draw?ref=home-page#) to make my source images and they have worked great. Just save as a .png and put it in the images directory.

- ssh address for the repo: `-r=git@github.com:badZombi/jan2016-example.git`
you need to create the repo on github first. Doesnt matter if it is public or private. It should simply exist on github and be empty. That means no commits, no readme, etc.  If you have the Github CLI set up you can use the create command: `gh repo create jan2016-example --public` to do it very easily.

Thats all the args from the example. Here are a few more you can try:

- `-mx <int> (--max)` : Adding this flag with a value will allow you to specify how many commits are used to achieve each color. The more commits on a given day the higher on the color scale it will be charted. This seems to be calculated on an average of the tisplayed timeline data so if you have other commits on the potrion of timeline you want to add your art, they may interfere depending on where they fall in the average calculation. Adding more using the --max flag may add enough weight that it doesnt disrupt your artwork so much. Default is 20.
- `-c <int> (--columns)`: 
- `-fx <str> (--file_extension)`: 


----

  

- Bullets
- Like this

- And so on

  

> Blockquotes

  

[Links](http://like.so/)