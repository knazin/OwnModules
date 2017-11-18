from matplotlib import style
from matplotlib import mlab
from math import pi
import matplotlib.animation as animation
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import random

#style.use('ggplot') # fivethrityeight, ggplot

def simple_plots(
    xs=[[],[]],
    ys=[[],[]],
    typ='line',
    style=[],
    colors=[],
    xlabel=[''],
    ylabel=[''],
    title=None,
    labels=[],
    together=False):
    '''
    IN \n
    (list of lists) x = list of lists arguments \n
    (list of lists) y = list of lists arguments \n


    (str) typ = type of plot [To choose: "line", "bar", "hist", "scatter"] \n
    (list) style = style of line [To choose: "-", "--", "-.", ".", "o", "x"] \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (str) xlabel = name of axes x \n
    (str) ylabel = name of axes y \n
    (str) title = title of the plot \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n

    (bool) together = make lines in one plot or on separatlies plots\n

    OUT \n
    Image of plot or Save the plot
    '''

    slabels = labels

    plt.subplots_adjust(hspace=1.5)
    # Poniewaz .pop() pobiera ostatni a nie pierwszy element listy
    xlabel.reverse()
    ylabel.reverse()
    labels.reverse()
    colors.reverse()
    xs.reverse()
    ys.reverse()

    try:
        for i in range(0,len(xs)):
            l = labels.pop() if len(labels) >= 1 else ''
            c = colors.pop() if len(colors) >= 1 else 'b'
            s = style.pop() if len(style) >= 1 else '-'

            if not together:
                if typ == 'line':
                    plt.plot(xs.pop(), ys.pop(), s, color=c, label=l)
                elif typ == 'bar':
                    plt.bar(xs.pop(), ys.pop(), color=c, label=l)
                elif typ == 'hist':
                    plt.hist(ys.pop(),bins=xs.pop(),histtype='stepfilled',rwidth=1.0, facecolor=c, label=l)
                elif typ == 'scatter':
                    plt.scatter(xs.pop(),ys.pop(),label=l,color=c, marker='*', s=30)

                if title is not None: plt.title(title)
                if labels is not None: plt.legend()
                if len(xlabel) >= 1: plt.xlabel(xlabel[len(xlabel)-1])
                if len(ylabel) >= 1: plt.ylabel(ylabel[len(ylabel)-1])
                plt.grid(True)

            else:
                xl = xlabel.pop() if len(xlabel) >= 1 else ''
                yl = ylabel.pop() if len(ylabel) >= 1 else ''
                num = str(len(xs)+i) + '1' + str(i+1)
                plt.subplot(int(num))

                if typ == 'line':
                    plt.plot(xs.pop(), ys.pop(), s, color=c, label=l)
                elif typ == 'bar':
                    plt.bar(xs.pop(), ys.pop(), color=c, label=l)
                elif typ == 'hist':
                    plt.hist(ys.pop(),bins=xs.pop(),histtype='stepfilled',rwidth=1.0, facecolor=c, label=l)
                elif typ == 'scatter':
                    plt.scatter(xs.pop(),ys.pop(),label=l,color=c, marker='*', s=3)
                
                if title is not None: plt.title(title)
                if labels is not None: plt.legend()
                plt.xlabel(xl)
                plt.ylabel(yl)
                plt.grid(True)

    except Exception as e:
        print(str(e))
    
    plt.show()

### Tworzy losowe dane do wykresow
def create_plots(x=11,y=10):
        xs = []
        ys = []

        for i in range(x):
            x = i
            y = random.random()*10

            xs.append(x)
            ys.append(y)

        return xs, ys

### Pobiera dane z pliku
def get_data_from_file(filename, delimiter=',', unpack=False):
    '''
    IN \n

    (str) filename = name of file which will be download. If file is not in the same folder as program path+filename \n
    (str) delimiter = char which separated two colummns \n
    (bool) unpack = True means that function return list of columns. False means that function will return list of rows \n

    OUT \n
    list of columns or list of rows
    '''

    if not unpack: x = np.loadtxt(filename,delimiter=delimiter,unpack=unpack)
    else:
        x = [] 
        [x.append(i) for i in np.loadtxt(filename,delimiter=delimiter,unpack=unpack)]
    return x

### Przetwarza wykres na zywo
def live_graph():
    '''
    IN \n

    '''
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        
        gd = np.loadtxt('example.txt',delimiter=',')
        xs= []
        ys= []
        for line in gd:#lines:
            if len(line) > 1:
                x,y = line[0],line[1]#line.split(',')
                xs.append(x)
                ys.append(y)

        ax1.clear()
        ax1.plot(xs,ys)

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

##############################################################################################################

### wykres liniowy
def line_plot(xs=[],ys=[],style='--',colors='b',xlabel=None,ylabel=None,title=None,labels=None,save=False):
    '''
    IN \n
    (list) x = list of arguments \n
    (list) y = list of arguments \n

    (list) style = style of line [To choose: "-", "--", "-.", ".", "o", "x"] \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (str) xlabel = name of axes x \n
    (str) ylabel = name of axes y \n
    (str) title = title of the plot \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n

    OUT \n
    (Save False)Image of plot or (Save True)Save the plot
    '''

    plt.plot(xs, ys, style, color=colors, label=labels)

    if title is not None: plt.title(title)
    if xlabel is not None: plt.xlabel(xlabel)
    if ylabel is not None: plt.ylabel(ylabel)
    if labels is not None: plt.legend()
    plt.grid(True)

    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres slupkowy
def bar_plot(xs=[],ys=[],colors='b',xlabel=None,ylabel=None,title=None,labels=None,save=False):
    '''
    IN \n
    (list) x = list of arguments \n
    (list) y = list of arguments \n

    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (str) xlabel = name of axes x \n
    (str) ylabel = name of axes y \n
    (str) title = title of the plot \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n

    OUT \n
    Image of plot or Save the plot
    '''

    plt.bar(xs, ys, color=colors, label=labels)

    if title is not None: plt.title(title)
    if xlabel is not None: plt.xlabel(xlabel)
    if ylabel is not None: plt.ylabel(ylabel)
    if labels is not None: plt.legend()
    plt.grid(True)

    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres histogram
def hist_plot(x=[],bins=[],color='b',xlabel='',ylabel='',title='',label='',histtype='bar',save=False):
    '''
    IN \n
    (list) x = list arguments \n
    (list) bins = list arguments \n

    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (str) xlabel = name of axes x \n
    (str) ylabel = name of axes y \n
    (str) title = title of the plot \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n
    (str) histtype = type of histogram [To choose: "bar","step","stepfilled"] \n

    OUT \n
    Image of plot or Save the plot
    '''

    plt.hist(x,bins=bins,histtype='bar',rwidth=0.8,label=label,color=color)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres kropkowy
def scatter_plot(x=[],y=[],marker='*',size=3,color='b',xlabel='x',ylabel='y',title='plot',label='krzywa',save=False):
    '''
    IN \n
    (list) x = list of arguments \n
    (list) y = list of arguments \n


    (str) marker = type of dot in plot [To choose: "*","o","."] \n
    (int) size = size of dot in plot \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (str) xlabel = name of axes x \n
    (str) ylabel = name of axes y \n
    (str) title = title of the plot \n
    (str) labels = name of lines [if labels is not None, legend will be show] \n

    OUT \n
    Image of plot or Save the plot
    '''

    plt.scatter(x,y,label=label,color=color,marker=marker,s=size)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres kolowy
def pie_plot(slices=[],colors=[],title='plot',labels=[],startangle=90,save=False):
    '''
    IN \n
    (list) slices = list of arguments \n

    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (str) title = title of the plot \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n
    (int) startangle = give angle which plot will be defined \n

    OUT \n
    Image of plot or Save the plot
    '''

    if len(slices) != len(colors): colors = None

    plt.pie(slices,labels=labels,colors=colors,startangle=startangle)
    plt.title(title)
    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres pudelkowy
def box_plot(x=[],title='plot',save=False):
    '''
    IN \n
    (list) x = list of arguments \n

    (str) title = title of the plot \n

    OUT \n
    Image of plot or Save the plot
    '''

    plt.boxplot(x)
    plt.title(title)
    plt.grid(True)
    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres pudelkowy gladki
def violin_plot(x=[],title='plot',save=False):
    '''
    IN \n
    (list) x = list of arguments \n

    (str) title = title of the plot \n

    OUT \n
    Image of plot or Save the plot
    '''

    plt.violinplot(x,showmeans=False,showmedians=True)
    plt.title(title)
    plt.grid(True)
    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

### wykres radarowy
def radar_plot(cat=['Speed', 'Reliability', 'Comfort', 'Safety', 'Effieciency','Test'],
               values=[90, 60, 65, 70, 40, 50],save=False):
    # Set data
    yscale, str_yscale = [], []
    maxi, start = max(values), int(max(values)/len(values))
    for i in range(start,max(values)+1,start): yscale.append(i)
    for i in yscale: str_yscale.append(str(i))

    # Rest of program
    N = len(cat)
    x_as = [n / float(N) * 2 * pi for n in range(N)]

    # Because our chart will be circular we need to append a copy of the first 
    # value of each list at the end of each list with data
    values += values[:1]
    x_as += x_as[:1]

    # Set color of axes
    plt.rc('axes', linewidth=0.5, edgecolor="#888888")

    # Create polar plot
    ax = plt.subplot(111, polar=True)

    # Set clockwise rotation. That is:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Set position of y-labels
    ax.set_rlabel_position(0)

    # Set color and linestyle of grid
    ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
    ax.yaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)

    # Set number of radial axes and remove labels
    plt.xticks(x_as[:-1], [])

    # Set yticks
    plt.yticks(yscale, str_yscale)

    # Plot data
    ax.plot(x_as, values, linewidth=0, linestyle='solid', zorder=3)
    # Fill area
    ax.fill(x_as, values, 'b', alpha=0.3) # 
    # Set axes limits
    plt.ylim(0, maxi) # bylo 100

    # Draw ytick labels to make sure they fit properly
    for i in range(N):
        angle_rad = i / float(N) * 2 * pi

        if angle_rad == 0:
            ha, distance_ax = "center", 10
        elif 0 < angle_rad < pi:
            ha, distance_ax = "left", 1
        elif angle_rad == pi:
            ha, distance_ax = "center", 1
        else:
            ha, distance_ax = "right", 1

        ax.text(angle_rad, maxi + distance_ax, cat[i], size=10, horizontalalignment=ha, verticalalignment="center")

    # Show polar plot
    plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),title), dpi=600)

##############################################################################################################

### pare wykresow liniowych
def multi_line_plot(
    x=[[],[]], 
    y=[[],[]], 
    styles = [],
    titles = [],
    colors = [],
    labels = [],
    xlabels = [],
    ylabels = [],
    rows=1, 
    cols=1,
    save=False
    ):

    '''
    IN \n
    (list of lists) x = list of list arguments \n
    (list of lists) y = list of list arguments \n

    (list) style = style of line [To choose: "-", "--", "-.", ".", "o", "x"] \n
    (list) title = list of title of the plot \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (list) xlabel = list of names of axes x \n
    (list) ylabel = list of names of axes y \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n

    OUT \n
    Image of plot or Save the plot
    '''

    # zabezpieczenie przed zlym wpisaniem danych dodatkowych
    rc = rows*cols
    if rc > len(styles): [styles.append('-') for i in range(rc-len(styles))]
    if rc > len(titles): [titles.append('Nie oznaczony wykres {}'.format(str(i))) for i in range(rc-len(titles))]
    if rc > len(colors): [colors.append('b') for i in range(rc-len(colors))]
    if rc > len(xlabels): [xlabels.append('x{}'.format(str(i))) for i in range(rc-len(xlabels))]
    if rc > len(ylabels): [ylabels.append('y{}'.format(str(i))) for i in range(rc-len(ylabels))]
    if rc > len(labels): [labels.append('linia{}'.format(str(i))) for i in range(rc-len(labels))]

    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    # kod decyduje co robic jesli jednak decydujemy sie na jeden wykres
    axes = [axes] if rows < 2 and cols < 2 else axes.flatten()

    try:
        for i, ax in enumerate(axes):
            ax.plot(x[i], y[i], styles[i], color=colors[i], label=labels[i])
            ax.grid(True)
            ax.set_title(titles[i])
            ax.set_xlabel(xlabels[i])
            ax.set_ylabel(ylabels[i])
            ax.legend()

        fig.tight_layout()

        # Show or Save plot
        plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),','.join(t for t in titles)), dpi=600)

    except Exception as e:
        print(str(e))
    
### pare wykresow slubkowych
def multi_bar_plot(
    x=[[],[]], 
    y=[[],[]], 
    titles = [],
    colors = [],
    labels = [],
    xlabels = [],
    ylabels = [],
    rows=1, 
    cols=1,
    save=False):
    '''
    IN \n
    (list of lists) x = list of list arguments \n
    (list of lists) y = list of list arguments \n

    (list) title = list of title of the plot \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (list) xlabel = list of names of axes x \n
    (list) ylabel = list of names of axes y \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n

    OUT \n
    Image of plot or Save the plot
    '''

    # zabezpieczenie przed zlym wpisaniem danych dodatkowych
    rc = rows*cols
    if rc > len(titles): [titles.append('Nie oznaczony wykres {}'.format(str(i))) for i in range(rc-len(titles))]
    if rc > len(colors): [colors.append('b') for i in range(rc-len(colors))]
    if rc > len(xlabels): [xlabels.append('x{}'.format(str(i))) for i in range(rc-len(xlabels))]
    if rc > len(ylabels): [ylabels.append('y{}'.format(str(i))) for i in range(rc-len(ylabels))]
    if rc > len(labels): [labels.append('linia{}'.format(str(i))) for i in range(rc-len(labels))]

    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    # kod decyduje co robic jesli jednak decydujemy sie na jeden wykres
    axes = [axes] if rows < 2 and cols < 2 else axes.flatten()

    try:
        for i, ax in enumerate(axes):
            ax.bar(x[i], y[i], color=colors[i], label=labels[i])
            ax.grid(True)
            ax.set_title(titles[i])
            ax.set_xlabel(xlabels[i])
            ax.set_ylabel(ylabels[i])
            ax.legend()

        fig.tight_layout()
        # Show or Save plot
        plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),','.join(t for t in titles)), dpi=600)
    except Exception as e:
        print(str(e))

### pare histogramow
def multi_hist_plot(
    x=[[],[]], 
    bins=[[],[]], 
    titles = [],
    colors = [],
    labels = [],
    xlabels = [],
    ylabels = [],
    histtypes = [],
    rows=1, 
    cols=1,
    save=False):
    '''
    IN \n
    (list of lists) x = list of list arguments \n
    (list of lists) bins = list of listed bins. Bins is for ex: [0,10,20,30] or [1,3,5,7]. List of ranges\n

    (list) title = list of title of the plot \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (list) xlabel = list of names of axes x \n
    (list) ylabel = list of names of axes y \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n
    (list) histtype = type of histogram [To choose: "bar","step","stepfilled"] \n

    OUT \n
    Image of plot or Save the plot
    '''

    # zabezpieczenie przed zlym wpisaniem danych dodatkowych
    rc = rows*cols
    if rc > len(titles): [titles.append('Nie oznaczony wykres {}'.format(str(i))) for i in range(rc-len(titles))]
    if rc > len(colors): [colors.append('b') for i in range(rc-len(colors))]
    if rc > len(xlabels): [xlabels.append('x{}'.format(str(i))) for i in range(rc-len(xlabels))]
    if rc > len(ylabels): [ylabels.append('y{}'.format(str(i))) for i in range(rc-len(ylabels))]
    if rc > len(labels): [labels.append('linia{}'.format(str(i))) for i in range(rc-len(labels))]
    if rc > len(histtypes): [histtypes.append('bar') for i in range(rc-len(histtypes))]

    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    # kod decyduje co robic jesli jednak decydujemy sie na jeden wykres
    axes = [axes] if rows < 2 and cols < 2 else axes.flatten()

    try:
        for i, ax in enumerate(axes):
            ax.hist(x[i], bins=bins[i], rwidth=0.8, color=colors[i], label=labels[i])
            ax.grid(True)
            ax.set_title(titles[i])
            ax.set_xlabel(xlabels[i])
            ax.set_ylabel(ylabels[i])
            ax.legend()

        fig.tight_layout()
        # Show or Save plot
        plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),','.join(t for t in titles)), dpi=600)
    except Exception as e:
        print(str(e))

### pare wykresow kropkowych
def multi_scatter_plot(
    x=[[],[]], 
    y=[[],[]], 
    titles = [],
    colors = [],
    labels = [],
    xlabels = [],
    ylabels = [],
    markers = [],
    sizes = [],
    rows=1, 
    cols=1,
    save=False):
    '''
    IN \n
    (list of lists) x = list of list arguments \n
    (list of lists) y = list of list arguments \n

    (list) title = list of title of the plot \n
    (list) colors = list of colors line [To choose: "b","g","r","c","m","y","k"] \n
    (list) xlabel = list of names of axes x \n
    (list) ylabel = list of names of axes y \n
    (list) labels = name of lines [if labels is not None, legend will be show] \n
    (list) markers = list of type of dot in plot [To choose: "*","o","."] \n
    (list of ints) sizes = list of sizes of dot in plot \n

    OUT \n
    Image of plot or Save the plot
    '''

    # zabezpieczenie przed zlym wpisaniem danych dodatkowych
    rc = rows*cols
    if rc > len(titles): [titles.append('Nie oznaczony wykres {}'.format(str(i))) for i in range(rc-len(titles))]
    if rc > len(colors): [colors.append('b') for i in range(rc-len(colors))]
    if rc > len(xlabels): [xlabels.append('x{}'.format(str(i))) for i in range(rc-len(xlabels))]
    if rc > len(ylabels): [ylabels.append('y{}'.format(str(i))) for i in range(rc-len(ylabels))]
    if rc > len(labels): [labels.append('linia{}'.format(str(i))) for i in range(rc-len(labels))]
    if rc > len(markers): [markers.append('o') for i in range(rc-len(markers))]
    if rc > len(sizes): [sizes.append(5) for i in range(rc-len(sizes))]

    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    # kod decyduje co robic jesli jednak decydujemy sie na jeden wykres
    axes = [axes] if rows < 2 and cols < 2 else axes.flatten()

    try:
        for i, ax in enumerate(axes):
            ax.scatter(x[i], y[i], marker=markers[i], s=sizes[i], color=colors[i], label=labels[i])
            ax.grid(True)
            ax.set_title(titles[i])
            ax.set_xlabel(xlabels[i])
            ax.set_ylabel(ylabels[i])
            ax.legend()

        fig.tight_layout()
        # Show or Save plot
        plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),','.join(t for t in titles)), dpi=600)
    except Exception as e:
        print(str(e))

### pare wykresow pudelkowych
def multi_box_plot(
    x = [[],[]],
    titles = [],
    rows = 1,
    cols = 1,
    save=False
    ): 
    '''
    IN \n
    (list) x = list of arguments \n

    (list) title = title of the plot \n

    OUT \n
    Image of plot or Save the plot
    '''
    # zabezpieczenie przed zlym wpisaniem danych dodatkowych
    rc = rows*cols
    if rc > len(titles): [titles.append('Nie oznaczony wykres {}'.format(str(i))) for i in range(rc-len(titles))]

    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    # kod decyduje co robic jesli jednak decydujemy sie na jeden wykres
    axes = [axes] if rows < 2 and cols < 2 else axes.flatten()

    try:
        for i, ax in enumerate(axes):
            ax.boxplot(x[i])
            ax.grid(True)
            ax.set_title(titles[i])
            ax.legend()

        fig.tight_layout()
        # Show or Save plot
        plt.show() if not save else plt.savefig('{} {}.png'.format(str(dt.datetime.today()),','.join(t for t in titles)), dpi=600)
    except Exception as e:
        print(str(e))

##############################################################################################################

### PRZYKLAD 1
def example1():
    np.random.seed(19680801)

    mu = 200
    sigma = 25
    n_bins = 50
    x = np.random.normal(mu, sigma, size=100)

    fig, ax = plt.subplots(figsize=(8, 4))

    # plot the cumulative histogram
    n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                            cumulative=True, label='Empirical')

    # Add a line showing the expected distribution.
    y = mlab.normpdf(bins, mu, sigma).cumsum()
    y /= y[-1]

    ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

    # Overlay a reversed cumulative histogram.
    ax.hist(x, bins=bins, normed=1, histtype='step', cumulative=-1,
            label='Reversed emp.')

    # tidy up the figure
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Cumulative step histograms')
    ax.set_xlabel('Annual rainfall (mm)')
    ax.set_ylabel('Likelihood of occurrence')

    plt.show()

### PRZYKLAD 2
def example2():
    # fake data
    np.random.seed(19680801)
    data = np.random.lognormal(size=(37, 4), mean=1.5, sigma=1.75)
    labels = list('ABCD')

    # compute the boxplot stats
    stats = cbook.boxplot_stats(data, labels=labels, bootstrap=10000)

    for n in range(len(stats)):
        stats[n]['med'] = np.median(data)
        stats[n]['mean'] *= 2

    print(list(stats[0]))

    fs = 10  # fontsize

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6, 6), sharey=True)
    axes[0, 0].bxp(stats)
    axes[0, 0].set_title('Default', fontsize=fs)

    axes[0, 1].bxp(stats, showmeans=True)
    axes[0, 1].set_title('showmeans=True', fontsize=fs)

    axes[0, 2].bxp(stats, showmeans=True, meanline=True)
    axes[0, 2].set_title('showmeans=True,\nmeanline=True', fontsize=fs)

    axes[1, 0].bxp(stats, showbox=False, showcaps=False)
    tufte_title = 'Tufte Style\n(showbox=False,\nshowcaps=False)'
    axes[1, 0].set_title(tufte_title, fontsize=fs)

    axes[1, 1].bxp(stats, shownotches=True)
    axes[1, 1].set_title('notch=True', fontsize=fs)

    axes[1, 2].bxp(stats, showfliers=False)
    axes[1, 2].set_title('showfliers=False', fontsize=fs)

    for ax in axes.flatten():
        ax.set_yscale('log')
        ax.set_yticklabels([])

    fig.subplots_adjust(hspace=0.4)
    plt.show()

### PRZYKLAD 3 - Histogramy
def example3():
    np.random.seed(19680801)

    n_bins = 10
    x = np.random.randn(1000, 3)

    fig, axes = plt.subplots(nrows=2, ncols=2)
    ax0, ax1, ax2, ax3 = axes.flatten()

    colors = ['red', 'tan', 'lime']
    ax0.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=colors)
    ax0.legend(prop={'size': 10})
    ax0.set_title('bars with legend')

    ax1.hist(x, n_bins, normed=1, histtype='bar', stacked=True)
    ax1.set_title('stacked bar')

    ax2.hist(x, n_bins, histtype='step', stacked=True, fill=False)
    ax2.set_title('stack step (unfilled)')

    # Make a multiple-histogram of data-sets with different length.
    x_multi = [np.random.randn(n) for n in [10000, 5000, 2000]]
    ax3.hist(x_multi, n_bins, histtype='bar')
    ax3.set_title('different sample sizes')

    fig.tight_layout()
    plt.show()

### PRZYKLAD 4 - FILL
def example4():
    x = np.linspace(0, 1, 500)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)

    fig, ax = plt.subplots()

    ax.fill(x, y, zorder=10)
    ax.grid(True, zorder=5)

    x = np.linspace(0, 2 * np.pi, 500)
    y1 = np.sin(x)
    y2 = np.sin(3 * x)

    fig, ax = plt.subplots()
    ax.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)

    plt.show()

### PRZYKLAD 5 - XCorr
def example5():
    # Fixing random state for reproducibility
    np.random.seed(19680801)


    x, y = np.random.randn(2, 100)
    fig, [ax1, ax2] = plt.subplots(2, 1, sharex=True)
    ax1.xcorr(x, y, usevlines=True, maxlags=50, normed=True, lw=2)
    ax1.grid(True)
    ax1.axhline(0, color='black', lw=2)

    ax2.acorr(x, usevlines=True, normed=True, maxlags=50, lw=2)
    ax2.grid(True)
    ax2.axhline(0, color='black', lw=2)

    plt.show()

##############################################################################################################

if __name__ == '__main__':
    print('Testowanie')

    # xs = []
    # ys = []

    # for i in range(0,2):
    #     x1, y1 = create_plots()
    #     xs.append(x1)
    #     ys.append(y1)

    # simple_plots(xs,ys,
    #     typ='scatter',
    #     colors=['b','r'],#'g'], 
    #     xlabel=['Siema x'],#,'Cos x'],
    #     ylabel=['Siema y'],
    #     title='Okidoki', 
    #     labels=['Siema','Cos'],#'Cos2'],
    #     together=False)

    x1, y1 = create_plots(x=20,y=11)

    #x = get_data_from_file('example.txt',delimiter=',',unpack=True)

    #example1()
    #example2()
    #example3()
    #example4()
    #example5()

    #line_plot(x1,y1,style='--',xlabel='x',ylabel='y',labels='krzywa1',title='Wykres')
    #bar_plot(x1,y1,xlabel='x',ylabel='y',labels='krzywa1',title='Wykres')
    #hist_plot(y1,x1,xlabel='x',ylabel='y',title='wykres',label='krzywa')
    #scatter_plot(x1,y1,marker='*',size=3,color='b',xlabel='x',ylabel='y')
    #pie_plot([y1[0],y1[1],y1[2],y1[3]],colors='b',title='plot',labels=['a','b','c','d'],startangle=90)
    #box_plot(y1,title='plot')
    #violin_plot(y1,title='plot')
    #radar_plot()

    multi_line_plot(
        x=[x1,x1,x1,x1], 
        y=[y1,y1,y1,y1], 
        #styles = ['-','-','.'], 
        titles = ['Jeden','Dwa','Trzy','Cztery'], 
        # colors = ['b','g','g','g'], 
        # labels = ['krzywa1','krzywa2','krzywa3','krzywa4'], 
        # xlabels = ['x','x','x','x'], 
        # ylabels = ['y','y','y','y'], 
        rows=2, 
        cols=2,
        save=False)

    print('Koniec testow')