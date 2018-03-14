#!/usr/bin/env python
import numpy
import matplotlib
import matplotlib.pyplot as pyplot

matplotlib.rcParams['font.size'] = 6

class RMSFPlot(object):
   def __init__(self, state0file, state1file, ax):
       rmsf0 = numpy.loadtxt(state0file, usecols=(1,), skiprows=1)[:35]
       rmsf1 = numpy.loadtxt(state1file, usecols=(1,), skiprows=1)[:35]


       state0xs = numpy.arange(0,35)
       state1xs = state0xs + 0.4
       ax.bar(state0xs, rmsf0, 0.4, align='center', color=(0,0,0,1), label="N'")
       ax.bar(state1xs, rmsf1, 0.4, align='center', color=(1,0,1,1), label="N")

       for kw in ['top', 'right']:
           ax.spines[kw].set_visible(False)

       for kw in ['bottom', 'left']:
           ax.spines[kw].set_linewidth(0.5)

       ax.set_xlim(-0.3, 34.7)
       ax.set_xticks(state0xs+0.2)

       ax.set_ylim(0,8)
       ax.set_yticks(numpy.arange(0,10,2))

       labels = [1,5,10,15,20,25,30,35]
       ax.set_xticklabels(["{:d}".format(i) if i in labels else '' for i in range(1,36) ])

       ax.tick_params(direction='out', width=0.5, labelsize=6)

if __name__ == "__main__":
    fig, axes = pyplot.subplots(2)
    fig.set_size_inches(8.8/2.54,6/2.54)
    RMSFPlot('ff14sb/rmsf.0.dat', 'ff14sb/rmsf.1.dat', axes[0])
    axes[0].legend(frameon=False)
    RMSFPlot('ff03w/rmsf.0.dat', 'ff03w/rmsf.1.dat', axes[1])

    axes[1].set_xlabel('Residue index')
    y = axes[0].transAxes.inverted().transform(axes[1].transAxes.transform((0,1)))[1]
    y = (y+0)/2
    axes[0].text(-0.08, y, u'RMS fluctuation (\u00c5)', transform=axes[0].transAxes, 
                 rotation=90, va='center', ha='center')

    axes[0].text(0.02, 0.9, 'ff14sb', transform=axes[0].transAxes)
    axes[1].text(0.02, 0.9, 'ff03w', transform=axes[1].transAxes)

    pyplot.subplots_adjust(top=0.98, left=0.1, right=0.98, bottom=.15)

    pyplot.savefig('rmsf.pdf')

