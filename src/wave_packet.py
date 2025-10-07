# MIT License
# Original gnuplot by Youjun Hu; Python port by Yunseo Kim (2025)
#
# Copyright (c) 2021 Youjun Hu (original work: https://github.com/Youjunhu/Youjunhu.github.io/blob/main/figures/wave_packet1.plt)
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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ----- Parameters -----
dx = np.sqrt(2.0)
k0 = 5.0
omega0 = np.pi / 20.0   # phase velocity = omega0/k0
vg = np.pi / 20.0       # group velocity

# ----- Grid -----
x = np.linspace(0.0, 20.0, 1000)

def envelope(x, t):
    return np.exp(-((x-4.0-vg*t)**2) / (4.0 * dx**2))

def carrier(x, t):
    return np.cos(k0 * x - omega0 * t)

def packet(x, t):
    return envelope(x, t) * carrier(x, t)

# ----- Figure -----
fig, ax = plt.subplots(figsize=(4, 3), dpi=200)
ax.set_xlim(0, 20)
ax.set_ylim(-1.0, 1.0)
ax.set_title("wave packet with Vg>Vp")
ax.grid(True, color="grey", alpha=0.5)

# Three curves: packet (green), +envelope (blue), -envelope (blue)
(line_packet,) = ax.plot([], [], color="#03ff03", linewidth=2)
(line_env_plus,) = ax.plot([], [], color="blue", linewidth=2)
(line_env_minus,) = ax.plot([], [], color="blue", linewidth=2)

def init():
    line_packet.set_data([], [])
    line_env_plus.set_data([], [])
    line_env_minus.set_data([], [])
    return line_packet, line_env_plus, line_env_minus

def update(i):
    t = float(i)
    env = envelope(x, t)
    line_packet.set_data(x, env * carrier(x, t))
    line_env_plus.set_data(x, env)
    line_env_minus.set_data(x, -env)
    return line_packet, line_env_plus, line_env_minus

anim = FuncAnimation(
    fig, update, init_func=init,
    frames=101, interval=150, blit=True
)

# Save GIF
writer = PillowWriter(fps=7)
anim.save("../figs/wave_packet.gif", writer=writer)
anim.save("../figs/wave_packet.webp", writer=writer)
