# MIT License
#
# Copyright (c) 2021 Youjun Hu (https://github.com/Youjunhu/Youjunhu.github.io/blob/main/figures/wave_packet1.plt)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set term gif size 350,262 animate delay 15
set output "wave_packet.gif"
set samples 1000
set xrange [0:20]
set title  "wave packet with Vg>Vp"
unset key
set grid lc rgb "grey"

dx=sqrt(2.)
k0=5
omega0=pi/20. #omega0/k0 is the phase velocity
vg=pi/20. #group velocity
do for [i=0:100] {
t=i*1.0
plot  exp(-(x-4-vg*t)**2/(4.*dx**2))*cos(k0*x-omega0*t) lw 3 lc rgb "green" notitle,  exp(-(x-4-vg*t)**2/(4.*dx**2)) lw 3 lc rgb "blue" notitle,-exp(-(x-4-vg*t)**2/(4.*dx**2)) lw 3 lc rgb "blue" notitle

}

set output