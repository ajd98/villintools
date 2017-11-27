#!/usr/bin/env python
import numpy
import matplotlib.pyplot as pyplot
import matplotlib

matplotlib.rcParams['font.size'] = 7

class MultipleAxes(object):
    def __init__(self, gridspec, nrows, ncols):
        self.axes = []
        self.shape = (nrows, ncols)
        for irow in range(nrows):
            self.axes.append([pyplot.subplot(gridspec[irow,icol]) \
                              for icol in range(ncols)])
    def __getitem__(self, key):
        try:
            if len(key) == 2:
                return self.axes[key[0]][key[1]]
            else:
                raise IndexError("MultipleAxes object supports only 1- and "
                                 "2-dimensional indexing.")
        except TypeError:
            if type(key) is int:
                if key >= 0:
                    return self.axes[key//self.shape[1]][key%self.shape[1]]
                elif key == -1:
                    return self.axes[self.shape[0]-1][self.shape[1]-1]
                else:
                    raise IndexError
            else:
                raise IndexError

    def set_xlim(self, *lims):
        for ax in self:
            ax.set_xlim(*lims)

    def set_ylim(self, *lims):
        for ax in self:
            ax.set_ylim(*lims)

    def _inches_to_display(self, (xinches, yinches)):
        fig = pyplot.gcf()
        w = fig.get_figwidth()
        h = fig.get_figheight()
        return fig.transFigure.transform((xinches/w, yinches/h))

    def set_xlabel(self, xlabel, labelpad=21, **kwargs):
        '''
        Set the ``master`` xlabel.
        '''
        lastrow = self.shape[0] - 1

        # If there are an even number of columns, space the x label evenly
        # between the two middle columns.
        ncols = self.shape[1]
        if ncols % 2 == 0:
            # x1, x2 are in axes units (for the axis to the left of the middle)
            x1 = 1

            # Get the position of the left side of the axis the the right of the 
            # middle, in the units of the axis to the right of the middle
            invtrans = self[lastrow, ncols//2-1].transAxes.inverted()
            x2, _ = invtrans.transform(self[lastrow, ncols//2].transAxes.transform((0,0)))
            
            x = (x1+x2)/2

            axis = self[lastrow, ncols//2-1]
        else:
            x = 0.5
            axis = self[lastrow, ncols//2]

        # Now, get the y position for the xlabel. Do this in a hacky way...
        # In data units
        #_, labelbuffer = self._inches_to_display((7./72,7./72))
        #                                                     
        #print(axis.xaxis.get_ticklabels()[0].get_position()[1])
        #print(labelbuffer)
        #y = axis.xaxis.get_ticklabels()[0].get_position()[1] - labelbuffer \
        #    - self._inches_to_display((0,labelpad/72.))[1]
        #_, y = axis.transAxes.inverted().transform((0,y))

        #y = self[lastrow, ncols//2].xaxis.label.get_position()[1]
        #_, y = self[lastrow, ncols//2].transAxes.inverted().transform((0,y))

        y = axis.transAxes.transform((0,0))[1] - \
                self._inches_to_display((0,labelpad/72.))[1]
        _, y = axis.transAxes.inverted().transform((0,y))

        axis.text(x, y, xlabel, ha='center', va='top', clip_on=False, 
                  transform=axis.transAxes,
                  **kwargs)

    def set_ylabel(self, ylabel, labelpad=21, **kwargs):
        '''
        Set the ``master`` ylabel.
        '''
        firstcol = 0

        # If there are an even number of rows, space the y label evenly
        # between the two middle rows.
        nrows = self.shape[0]
        if nrows % 2 == 0:
            # y1, y2 are in axes units (for the axis just above the middle)
            x1 = 0

            # Get the position of the top of the axis just below the middle
            # in the units of the axis just above the middle
            invtrans = self[nrows//2-1, firstcol].transAxes.inverted()
            _, y2 = invtrans.transform(self[nrows//2, firstcol].transAxes.transform((0,1)))
            
            y = (y1+y2)/2

            axis = self[nrows//2-1, firstcol]
        else:
            y = 0.5
            axis = self[nrows//2, firstcol]

        # Now, get the x position for the ylabel. Do this in a hacky way...
        # In data units
        #x = self[nrows//2, firstcol].yaxis.label.get_position()[0]
        #x, _ = self[nrows//2, firstcol].transAxes.inverted().transform((x,0))
        x = axis.transAxes.transform((0,0))[0] - \
                self._inches_to_display((labelpad/72.,0))[0]
        x, _ = axis.transAxes.inverted().transform((x,0))

        axis.text(x, y, ylabel, ha='right', clip_on=False, rotation=90, va='center',
                  transform=axis.transAxes,
                  **kwargs)

    def _remove_xticklabels(self, axis):
        '''
        Remove the xtick labels from axis.
        '''
        axis.set_xticklabels(['' for tick in axis.xaxis.get_ticklabels()])

    def _remove_yticklabels(self, axis):
        '''
        Remove the ytick labels from axis.
        '''
        axis.set_yticklabels(['' for tick in axis.yaxis.get_ticklabels()])

    def clean(self):
        for irow in range(self.shape[0]):
            for icol in range(self.shape[1]):
                if irow != self.shape[0]-1:
                    self._remove_xticklabels(self[irow,icol])
                if icol != 0:
                    self._remove_yticklabels(self[irow,icol])


def format_axis(axis, linewidth=0.8):
    '''
    Remove top and right spines, and set line widths for remaining spines and
    ticks.
    '''
    for kw in ['top', 'right']:
        axis.spines[kw].set_visible(False)
    for kw in ['left', 'bottom']:
        axis.spines[kw].set_linewidth(linewidth)
    axis.tick_params(direction='out', width=linewidth)
    return

def plot_step(axis, edges, vals, **kwargs):
    '''
    On ``axis``, plot the histogram with bin edges ``edges`` and bin values
    ``vals``. Keyword arguments are passed to axis.plot.
    '''
    xs = numpy.concatenate((numpy.array((edges[0],)),
                            numpy.repeat(edges[1:-1], 2),
                            numpy.array((edges[-1],))))
    ys = numpy.repeat(vals, 2)
    return axis.plot(xs, ys, **kwargs)
