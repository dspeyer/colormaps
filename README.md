# Colormaps
Visualizing the [XKCD color survey data](https://blog.xkcd.com/2010/05/03/color-survey-results/)

## Plurality Color Names

For each shade, the most common name for it.

<a href=results/fullsat_plurality.png><img src=results/fullsat_plurality.png width=256 height=256 /></a>
<a href=results/pastel_plurality.png><img src=results/pastel_plurality.png width=256 height=256 /></a>
<a href=results/slice256_2048_plurality.png><img src=results/slice256_2048_plurality.png width=256 height=256 /></a>
<a href=results/slice384_2048_plurality.png><img src=results/slice384_2048_plurality.png width=256 height=256 /></a>
<a href=results/slice512_2048_plurality.png><img src=results/slice512_2048_plurality.png width=256 height=256 /></a>

[All the fixed-luminosity slices as a youtube video](https://www.youtube.com/watch?v=FuBFTUmHS5c)

### More like this, but wih weirder slices through the color-cube

<a href=results/ParPlane0_128_plurality.png><img src=results/ParPlane0_128_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane0_192_plurality.png><img src=results/ParPlane0_192_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane0_64_plurality.png><img src=results/ParPlane0_64_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane1_128_plurality.png><img src=results/ParPlane1_128_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane1_192_plurality.png><img src=results/ParPlane1_192_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane1_64_plurality.png><img src=results/ParPlane1_64_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane2_128_plurality.png><img src=results/ParPlane2_128_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane2_192_plurality.png><img src=results/ParPlane2_192_plurality.png width=128 height=256 /></a>
<a href=results/ParPlane2_64_plurality.png><img src=results/ParPlane2_64_plurality.png width=128 height=256 /></a>
<a href=results/primary0_plurality.png><img src=results/primary0_plurality.png width=128 height=256 /></a>
<a href=results/primary1_plurality.png><img src=results/primary1_plurality.png width=128 height=256 /></a>
<a href=results/primary2_plurality.png><img src=results/primary2_plurality.png width=128 height=256 /></a>

This one omits votes for "orange", "brown", "blue", "purple" and "pink" so the rare color names can be more visible:

<a href=results/orange_plurality.png><img src=results/orange_plurality.png width=128 height=128 /></a>


## Localmax Color Names

For each shade, the name that most describes it more than it describes surrounding shades

<a href=results/fullsat_localmax.png><img src=results/fullsat_localmax.png width=256 height=256 /></a>
<a href=results/pastel_localmax.png><img src=results/pastel_localmax.png width=256 height=256 /></a>
<a href=results/slice256_2048_localmax.png><img src=results/slice256_2048_localmax.png width=256 height=256 /></a>
<a href=results/slice384_2048_localmax.png><img src=results/slice384_2048_localmax.png width=256 height=256 /></a>
<a href=results/slice512_2048_localmax.png><img src=results/slice512_2048_localmax.png width=256 height=256 /></a>

## Majority Color Names

The name, if any, that a majority of respondants called the shade.  Note that most shades are unlabeled.

<a href=results/fullsat_majority.png><img src=results/fullsat_majority.png width=256 height=256 /></a>
<a href=results/pastel_majority.png><img src=results/pastel_majority.png width=256 height=256 /></a>
<a href=results/slice256_2048_majority.png><img src=results/slice256_2048_majority.png width=256 height=256 /></a>
<a href=results/slice384_2048_majority.png><img src=results/slice384_2048_majority.png width=256 height=256 /></a>
<a href=results/slice512_2048_majority.png><img src=results/slice512_2048_majority.png width=256 height=256 /></a>

## Topographic Color Names

For some interesting names, show what fraction of respondants called that shade that color

<a href=results/fullsat_topo__cyanyellowpinkblack.png><img src=results/fullsat_topo__cyanyellowpinkblack.png width=256 height=256 /></a>
<a href=results/fullsat_topo__orangebrowntealpurple.png><img src=results/fullsat_topo__orangebrowntealpurple.png width=256 height=256 /></a>
<a href=results/fullsat_topo__redgreenblue.png><img src=results/fullsat_topo__redgreenblue.png width=256 height=256 /></a>
<a href=results/slice384_1024_topo__bluegreenorangepink.png><img src=results/slice384_1024_topo__bluegreenorangepink.png width=256 height=256 /></a>
<a href=results/slice384_1024_topo__browngrey.png><img src=results/slice384_1024_topo__browngrey.png width=256 height=256 /></a>
<a href=results/slice384_1024_topo__redmustardlimetealpurple.png><img src=results/slice384_1024_topo__redmustardlimetealpurple.png width=256 height=256 /></a>

## Graphs

For some interesting lines through the cube (shown above) graph how common different names were

<a href=results/edge02_plurality_withgraph.png><img src=results/edge02_plurality_withgraph.png width=256 height=256 /></a>
<a href=results/edge10_plurality_withgraph.png><img src=results/edge10_plurality_withgraph.png width=256 height=256 /></a>
<a href=results/edge12_plurality_withgraph.png><img src=results/edge12_plurality_withgraph.png width=256 height=256 /></a>

# The Code

In `src` you will find `mappers` which has ways of mapping colorspace the a 2d image, `visualizers` which has the code to draw all this stuff, and `colormaps` which pulls it all together.  You'll also find `getdata.sh` which downloads the data and converts it to an sqllite file, and `mkvid.sh` which puts together slices into a video.