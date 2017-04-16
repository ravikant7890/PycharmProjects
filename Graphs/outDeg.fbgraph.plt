#
# Directed graph - out-degree Distribution. G(4039, 88234). 591 (0.1463) nodes with out-deg > avg deg (43.7), 197 (0.0488) with >2*avg.deg (Sun Aug  7 14:19:57 2016)
#

set title "Directed graph - out-degree Distribution. G(4039, 88234). 591 (0.1463) nodes with out-deg > avg deg (43.7), 197 (0.0488) with >2*avg.deg"
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
set output 'outDeg.fbgraph.png'
plot 	"outDeg.fbgraph.tab" using 1:2 title "" with linespoints pt 6
