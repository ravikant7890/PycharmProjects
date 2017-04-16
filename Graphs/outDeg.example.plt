#
# Directed graph - out-degree Distribution. G(100, 1000). 0 (0.0000) nodes with out-deg > avg deg (20.0), 0 (0.0000) with >2*avg.deg (Sun Aug  7 14:14:50 2016)
#

set title "Directed graph - out-degree Distribution. G(100, 1000). 0 (0.0000) nodes with out-deg > avg deg (20.0), 0 (0.0000) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Out-degree"
set ylabel "Count"
set tics scale 2
set terminal png size 1000,800
set output 'outDeg.example.png'
plot 	"outDeg.example.tab" using 1:2 title "" with linespoints pt 6
