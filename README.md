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
````
```
cd GH-paint
```

I'd recommend using venv.
e.g.
```
python3 -m venv .venv
source .venv/bin/activate
```

## Usage

![pixel art to be converted](https://raw.githubusercontent.com/badZombi/GH-paint/main/images/doc/johnzblack.jpg)
```
python doit.py -y=2016 -m=1 -d=1 -i=images/johnzblack.png -r=git@github.com:badZombi/jan2016-example.git
```
![pixel art to be converted](https://raw.githubusercontent.com/badZombi/GH-paint/main/images/doc/jan2016-dk.jpg)

----

- Bullets
- Like this
- And so on

> Blockquotes

[Links](http://like.so/)
