#
# Directed graph - out-degree Distribution. G(23947347, 57708624). 31115 (0.0013) nodes with out-deg > avg deg (4.8), 0 (0.0000) with >2*avg.deg (Sun Aug  7 15:13:06 2016)
#

set title "Directed graph - out-degree Distribution. G(23947347, 57708624). 31115 (0.0013) nodes with out-deg > avg deg (4.8), 0 (0.0000) with >2*avg.deg"
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
set output 'outDeg.USROAD.png'
plot 	"outDeg.USROAD.tab" using 1:2 title "" with linespoints pt 6
