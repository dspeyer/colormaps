#!/bin/sh

ffmpeg -framerate 10 -pattern_type glob -i 'slice*_1024_plurality.png'   -c:v libx264 -pix_fmt yuv420p slicevid.mp4
