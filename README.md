# Basic usage:

Create an pixel image (will give pallette details here in a bit)

    tool I used: https://www.pixilart.com/draw


Create an empty repo in github and copy the url e.g. `git@github.com:badZombi/2022-artwork.git`


select a date you want your artwork to begin, e.g. 01-02-2022

the tool will select the appropriate Sunday to start drawing on for that week.

Run the command and point to the image you created:

`python doit.py -y=2022 -m=1 -d=2 -i=images/gh2.png -r=git@github.com:badZombi/2022-artwork.git`


will add more detail later when I clean up the messy code.

Also added a "full" version that uses the github CLI to create and destroy repos as necessary. This version is intended to be an easy way to clear and update an art repo so it can always be on the "contributions in the last year" timeline where a visitor will land. You need to log into the CLI and gove it destroy scope perms. It auto-names the libraries based on input so it would be really difficult to have a collision and accidental deletion of an unrelated repo. 

Its all very messy still and has old code/comments scattered around. It's a work-in-progress to be continued when I am bored and have time.