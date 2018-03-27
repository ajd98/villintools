#!/usr/bin/env python
import numpy
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib import cm


def plot_entropy(numpyfile, ax):
    labels = {0: '10 bins',
              1: '15 bins',
              2: '20 bins',
              3: '24 bins',
              4: '36 bins'}
    entropy = numpy.load(numpyfile)
    T = 273.15
    R = .0083145

    nbinschemes = entropy.shape[2]
    for i in range(nbinschemes):
        # In kJ/mol
        state0entropy = entropy[0,:,i]*-1*R*T 
        state1entropy = entropy[1,:,i]*-1*R*T

        ys = state1entropy - state0entropy

        xs = numpy.arange(0,35)
        color = cm.get_cmap('magma')(float(i)/nbinschemes)
        ax.bar(xs+0.8/nbinschemes*i, ys, 0.8/nbinschemes, align='center', color=color, label=labels[i])
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

    axes[0].legend(frameon=False)

    pyplot.subplots_adjust(top=0.98, left=0.1, right=0.98, bottom=.15)

    pyplot.savefig('binning.pdf')

if __name__ == "__main__":
    main()
