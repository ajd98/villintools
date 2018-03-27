#!/usr/bin/env python
import numpy
import matplotlib
import matplotlib.pyplot as pyplot

def plot_entropy(numpyfile, ax):
    entropy = numpy.load(numpyfile)
    T = 273.15
    R = .0083145
    # In kJ/mol
    state0entropy = entropy[0,:,-1]*-1*R*T 
    state1entropy = entropy[1,:,-1]*-1*R*T

    ys = state1entropy - state0entropy
    print(ys.max(), ys.min())

    xs = numpy.arange(0,35)
    ax.bar(xs, ys, 0.8, align='center', color=(0,0,0,1), label="N'")
    ax.plot((-0.6,34.6), (0,0), color='black', linewidth=0.5)
     
    for kw in ['top', 'right']:
        ax.spines[kw].set_visible(False)

    for kw in ['bottom', 'left']:
        ax.spines[kw].set_linewidth(0.5)

    ax.set_xlim(-0.6, 34.6)
    ax.set_xticks(xs)

    ax.set_ylim(-4,4)
    ax.set_yticks(numpy.arange(-4,5,1))
    ax.set_yticklabels(['-4', '', '-2', '', '0', '', '2', '', '4'])

    labels = [1,5,10,15,20,25,30,35]
    ax.set_xticklabels(["{:d}".format(i) if i in labels else '' for i in range(1,36) ])

    ax.tick_params(direction='out', width=0.5, labelsize=6)

def main():
    matplotlib.rcParams['font.size'] = 6
    fig, axes = pyplot.subplots(2)
    fig.set_size_inches(8.8/2.54,6/2.54)

    plot_entropy('ff14sb.entropy.npy', axes[0])
    plot_entropy('ff03w.entropy.npy', axes[1])

    axes[1].set_xlabel('Residue index')
    y = axes[0].transAxes.inverted().transform(axes[1].transAxes.transform((0,1)))[1]
    y = (y+0)/2
    axes[0].text(-0.08, y, u"T\u0394S$_{N'\u2192N}$ (kJ mol\u207B\u00B9)", transform=axes[0].transAxes, 
                 rotation=90, va='center', ha='center')

    axes[0].text(0.02, 0.9, 'ff14sb', transform=axes[0].transAxes)
    axes[1].text(0.02, 0.9, 'ff03w', transform=axes[1].transAxes)

    pyplot.subplots_adjust(top=0.98, left=0.1, right=0.98, bottom=.15)

    pyplot.savefig('entropy.pdf')

if __name__ == "__main__":
    main()
