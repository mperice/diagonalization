#!/usr/bin/env python

"""

You can enable picking by setting the "picker" property of an artist
(for example, a matplotlib Line2D, Text, Patch, Polygon, AxesImage,
etc...)

There are a variety of meanings of the picker property

    None -  picking is disabled for this artist (default)

    boolean - if True then picking will be enabled and the
      artist will fire a pick event if the mouse event is over
      the artist

    float - if picker is a number it is interpreted as an
      epsilon tolerance in points and the artist will fire
      off an event if it's data is within epsilon of the mouse
      event.  For some artists like lines and patch collections,
      the artist may provide additional data to the pick event
      that is generated, for example, the indices of the data within
      epsilon of the pick event

    function - if picker is callable, it is a user supplied
      function which determines whether the artist is hit by the
      mouse event.

         hit, props = picker(artist, mouseevent)

      to determine the hit test.  If the mouse event is over the
      artist, return hit=True and props is a dictionary of properties
      you want added to the PickEvent attributes


After you have enabled an artist for picking by setting the "picker"
property, you need to connect to the figure canvas pick_event to get
pick callbacks on mouse press events.  For example,

  def pick_handler(event):
      mouseevent = event.mouseevent
      artist = event.artist
      # now do something with this...


The pick event (matplotlib.backend_bases.PickEvent) which is passed to
your callback is always fired with two attributes:

  mouseevent - the mouse event that generate the pick event.  The
    mouse event in turn has attributes like x and y (the coordinates in
    display space, such as pixels from left, bottom) and xdata, ydata (the
    coords in data space).  Additionally, you can get information about
    which buttons were pressed, which keys were pressed, which Axes
    the mouse is over, etc.  See matplotlib.backend_bases.MouseEvent
    for details.

  artist - the matplotlib.artist that generated the pick event.

Additionally, certain artists like Line2D and PatchCollection may
attach additional meta data like the indices into the data that meet
the picker criteria (for example, all the points in the line that are within
the specified epsilon tolerance)

The examples below illustrate each of these methods.
"""

from matplotlib.pyplot import figure, show,text,draw,plot,cla,gca,get_current_fig_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage
import numpy as np
from numpy.random import rand
import string



prefix="D:/diagonalization/ideal_toy/"

selected_inds=set([])
#fig = figure()
#ax1 = fig.add_subplot(211)
#ax1.set_title('click on points, rectangles or text', picker=True)
#ax1.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))
#line, = ax1.plot(rand(438341), 'o', picker=5)  # 5 points tolerance

# pick the rectangle
#ax2 = fig.add_subplot(212)

#bars = ax2.bar(range(10), rand(10), picker=True)
#for label in ax2.get_xticklabels():  # make the xtick labels pickable
#    label.set_picker(True)


xs=[]
ys=[]
ex_classes=[]
words=[]
colors=[]
documents=[]
domains=[]
fig = figure(figsize=(6*3.13,4*3.13))
ax1 = fig.add_subplot(111)

ex_properties=""

def redraw(hide=False):
    global fig,ax1,xs,ys,colors,selected_inds,ex_properties
    cla()


    col = ax1.scatter([xs[i] for i in selected_inds]+[-30],[ys[i] for i in selected_inds]+[-30],s=70,c='r', picker=1)
    col2 = ax1.scatter(xs,ys,c=colors, picker=1)
    if not hide:
        print "Risem vse ..."

    #print ax1.points
    #fig.savefig('pscoll.eps')
    print "redrawing done."
    #draw()
    #fig.canvas.clear()
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    aa=ax1.text(-100, -100, ex_properties, size=12, bbox=bbox_props)
    aa.set_family("monospace")
    fig.canvas.draw()
    if not hide:
        fig.canvas.mpl_connect('button_press_event', onpick3)

    print ex_properties
# plot()
    #show()

print "new"
points=[]#np.array([])
#fig.canvas.mpl_connect('pick_event', onpick1)
mig_mag_file=open(prefix+"redpin/points.txt", 'r')
#hevristic_scores="all/HevristicsScores.txt"
#every=5

line = mig_mag_file.readline()    # Invokes readline() method on file
while line:
    if line!="\n":
        spl=line.split("\n")[0].split("\t")

        #print spl

        if spl[0]=="P":
            #print "aaa"
            _,x,y,word,greens_per_word,blues_per_word,domain,document,ex_class=spl
            xs.append(float(x))
            ys.append(float(y))
            words.append(word)
            ex_classes.append(ex_class)
            documents.append(document)
            colors.append('b' if ex_class=="1" else 'g')
            domains.append(domain+" |%2s %2s|" % (greens_per_word,blues_per_word))
        elif spl[0]=="CS":
            _,j,color=spl
        else: #BTERM
            _,j,b_term=spl


        #print i,spl[0]
     #   count+=1
    #i+=1
    line = mig_mag_file.readline()
    #print "row_perm:",row_perm_rev
mig_mag_file.close()
max_y=max(ys)
ys=[max_y-y for y in ys]
#points=np.array(points)
#x, y = rand(2, 300)
def onpick3(event):
    global ex_properties

    print event.xdata,event.ydata
    inds = [i for i,x in enumerate(xs) if event.xdata+3>x > event.xdata-3 and event.ydata + 3 > ys[i] > event.ydata-3]#set(event.ind)
    print inds
    for ind in inds:
        if ind in selected_inds:
            selected_inds.remove(ind)
            print "removed:",ind
        else:
            selected_inds.add(ind)

            print "added:",ind

    ex_properties=string.join([string.join([domains[i],words[i]]," ") for i in selected_inds],"\n")

    #selected_inds.extend(inds)
    #for ind in selected_inds:
    #    print ind, words[ind], documents[ind], domains[ind]


    #cla()

    #global fig
    #fig.canvas.draw()

    redraw()
    return True
#
#fig = figure()
#ax1 = fig.add_subplot(111)

redraw()

show()
#
#if 1: # picking with a custom hit test function
#    # you can define custom pickers by setting picker to a callable
#    # function.  The function has the signature
#    #
#    #  hit, props = func(artist, mouseevent)
#    #
#    # to determine the hit test.  if the mouse event is over the artist,
#    # return hit=True and props is a dictionary of
#    # properties you want added to the PickEvent attributes
#
#    def line_picker(line, mouseevent):
#        """
#        find the points within a certain distance from the mouseclick in
#        data coords and attach some extra attributes, pickx and picky
#        which are the data points that were picked
#        """
#        if mouseevent.xdata is None: return False, dict()
#        xdata = line.get_xdata()
#        ydata = line.get_ydata()
#        maxd = 0.05
#        d = np.sqrt((xdata-mouseevent.xdata)**2. + (ydata-mouseevent.ydata)**2.)
#
#        ind = np.nonzero(np.less_equal(d, maxd))
#        if len(ind):
#            pickx = np.take(xdata, ind)
#            picky = np.take(ydata, ind)
#            props = dict(ind=ind, pickx=pickx, picky=picky)
#            return True, props
#        else:
#            return False, dict()
#
#    def onpick2(event):
#        print('onpick2 line:', event.pickx, event.picky)
#
#    fig = figure()
#    ax1 = fig.add_subplot(111)
#    ax1.set_title('custom picker for line data')
#    line, = ax1.plot(rand(100), rand(100), 'o', picker=line_picker)
#    fig.canvas.mpl_connect('pick_event', onpick2)
#
#
#if 1: # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)
#
#    x, y, c, s = rand(4, 100)
#    def onpick3(event):
#        ind = event.ind
#        print('onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind))
#
#    fig = figure()
#    ax1 = fig.add_subplot(111)
#    col = ax1.scatter(x, y, 100*s, c, picker=True)
#    #fig.savefig('pscoll.eps')
#    fig.canvas.mpl_connect('pick_event', onpick3)
#
#if 1: # picking images (matplotlib.image.AxesImage)
#    fig = figure()
#    ax1 = fig.add_subplot(111)
#    im1 = ax1.imshow(rand(10,5), extent=(1,2,1,2), picker=True)
#    im2 = ax1.imshow(rand(5,10), extent=(3,4,1,2), picker=True)
#    im3 = ax1.imshow(rand(20,25), extent=(1,2,3,4), picker=True)
#    im4 = ax1.imshow(rand(30,12), extent=(3,4,3,4), picker=True)
#    ax1.axis([0,5,0,5])
#
#    def onpick4(event):
#        artist = event.artist
#        if isinstance(artist, AxesImage):
#            im = artist
#            A = im.get_array()
#            print('onpick4 image', A.shape)
#
#    fig.canvas.mpl_connect('pick_event', onpick4)
#
#
#show()