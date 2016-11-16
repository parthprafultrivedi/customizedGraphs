def getPrecisieValue(input,precision):
    value=round(float(input),precision)
    if value-int(value) == 0:
        return int(value)
    else:
        return value

import numpy as np
import matplotlib.pyplot as plt
from csv import reader as csvReader
import argparse
from matplotlib import rc
import re

rc('mathtext', default='regular')

#ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
#ax2.set_ylabel(r"Temperature ($^\circ$C)")

descriptionMsg="""
Get graph plot based on specified Data Format . . .
<T1(String)>,<T2(Number)>,<T3(Amount)>
Amount will be outputed as a shaded region in Gray Colour and
the number of transactions coreesponding to that amount will be
displayed as bar graph in gray colour.
"""

parser = argparse.ArgumentParser(description=descriptionMsg)

parser.add_argument('file',help='Input CSV file')
parser.add_argument('--precisionFlag','-p',type=int,help='Indicates floating precision')
parser.add_argument('--xAxisLabelRotationFlag','-r',type=int,help='Indicates the orientation of the labels on the horrizontal axis. Takes value from 0 to 180')
parser.add_argument('--barColor','-bc',type=str,help='Indicates HEX colour code of the bars representing the numbers')
parser.add_argument('--areaColor','-ac',type=str,help='Indicates HEX colour code of the area representing the amount')
parser.add_argument('--figSize','-s',type=list,help='[X,Y] Figure Size indicating width=X inches and height=Y inches')
parser.add_argument('--transparentFlag','-t',type=bool,help='True or False indicating transparency while saving')
parser.add_argument('title',type=str,help='Graph Title')
parser.add_argument('--format','-f',help='Output format [pdf|png|svg] of the resultant plot.')

progArgs=parser.parse_args()

fId=open(progArgs.file,'r+')
csvContents=list(csvReader(fId))

countList=[]
amountList=[]
labelList=[]

xAxisLabel=csvContents[0][0]
legendValNumber=csvContents[0][1]
legendValAmount=csvContents[0][2]

for i in range(1,len(csvContents)):
    labelList.append(csvContents[i][0])
    countList.append(csvContents[i][1])
    amountList.append(csvContents[i][2])
fId.close()

if progArgs.precisionFlag != None:
    if progArgs.precisionFlag==0:
        countList=[ int(float(i)) for i in countList ]
        amountList=[ int(float(i)) for i in amountList ]
    else:
        countList=[ getPrecisieValue(i,progArgs.precisionFlag) for i in countList ]
        amountList=[ getPrecisieValue(i,progArgs.precisionFlag) for i in amountList ]
else:
    countList=[ int(float(i)) for i in countList ]
    amountList=[ int(float(i)) for i in amountList ]

#Debug CSV FILE VALUES BASED ON PRECISION COUNT
#print labelList
#print countList
#print amountList
#print legendValNumber
#print legendValAmount

noOfRows=len(labelList)

y = np.row_stack((amountList))

x = np.arange(noOfRows)

##y1, y2, y3 = fnx(), fnx(), fnx()

if progArgs.figSize:
    val=''
    for item in progArgs.figSize:
        val=val+item
    matchedValues=re.findall(r'\[(.*),(.*)\]',val)
    figWidth=int(matchedValues[0][0])
    figHeight=int(matchedValues[0][1])
    fig=plt.figure(figsize=(figWidth, figHeight))
else:
    fig=plt.figure()

ax = fig.add_subplot(111)

ax.set_xticks([i for i in range(len(labelList))])

if progArgs.xAxisLabelRotationFlag:
    ax.set_xticklabels((i for i in labelList),rotation=progArgs.xAxisLabelRotationFlag)
else:
    ax.set_xticklabels((i for i in labelList),rotation=0)

ax.set(title=progArgs.title, ylabel='', xlabel=xAxisLabel)

if progArgs.barColor:
    ax.bar([i for i in range(len(labelList))], countList, align='center', width=0.5, color='#'+progArgs.barColor, edgecolor='#'+progArgs.barColor)#,tick_label=testNames)
else:
    ax.bar([i for i in range(len(labelList))], countList, align='center', width=0.5, color='#ae285d', edgecolor='#ae285d')#,tick_label=testNames)

if progArgs.areaColor:
    ax.stackplot(x, amountList, colors=('#'+progArgs.areaColor,), color='#'+progArgs.areaColor)#,'#ae285d'
else:
    ax.stackplot(x, amountList, colors=('grey',), color='grey')#,'#ae285d'

for i in range(len(labelList)):
    ax.text(i-0.5,amountList[i]+1,str(amountList[i]))

from datetime import datetime
if progArgs.format:
    opFileName='areaBarGraph_'+progArgs.file[:-4]+str(datetime.now().strftime("_%d_%m_%Y_%H_%M"))+'.'+progArgs.format
else:
    opFileName='areaBarGraph_'+progArgs.file[:-4]+str(datetime.now().strftime("_%d_%m_%Y_%H_%M"))+'.svg'
plt.savefig(opFileName,dpi=300,transparent=True)

plt.show()



#"""
#Thanks Josh Hemann for the example

#This examples comes from an application in which grade school gym
#teachers wanted to be able to show parents how their child did across
#a handful of fitness tests, and importantly, relative to how other
#children did. To extract the plotting code for demo purposes, we'll
#just make up some data for little Johnny Doe...

#"""
#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib.ticker import MaxNLocator
#from collections import namedtuple

#Student = namedtuple('Student', ['name', 'grade', 'gender'])
#Score = namedtuple('Score', ['score', 'percentile'])

## GLOBAL CONSTANTS
#testNames = ['Pacer Test', 'Flexed Arm\n Hang', 'Mile Run', 'Agility',
#             'Push Ups']
#testMeta = dict(zip(testNames, ['laps', 'sec', 'min:sec', 'sec', '']))


#def attach_ordinal(num):
#    """helper function to add ordinal string to integers

#    1 -> 1st
#    56 -> 56th
#    """
#    suffixes = dict((str(i), v) for i, v in
#                    enumerate(['th', 'st', 'nd', 'rd', 'th',
#                               'th', 'th', 'th', 'th', 'th']))

#    v = str(num)
#    # special case early teens
#    if v in {'11', '12', '13'}:
#        return v + 'th'
#    return v + suffixes[v[-1]]


#def format_score(scr, test):
#    """
#    Build up the score labels for the right Y-axis by first
#    appending a carriage return to each string and then tacking on
#    the appropriate meta information (i.e., 'laps' vs 'seconds'). We
#    want the labels centered on the ticks, so if there is no meta
#    info (like for pushups) then don't add the carriage return to
#    the string
#    """
#    md = testMeta[test]
#    if md:
#        return '{0}\n{1}'.format(scr, md)
#    else:
#        return scr


#def format_ycursor(y):
#    y = int(y)
#    if y < 0 or y >= len(testNames):
#        return ''
#    else:
#        return testNames[y]


#def plot_student_results(student, scores, cohort_size):
#    #  create the figure
#    fig, ax1 = plt.subplots(figsize=(9, 7))
#    fig.subplots_adjust(left=0.115, right=0.88)
#    fig.canvas.set_window_title('Eldorado K-8 Fitness Chart')

#    pos = np.arange(len(testNames)) + 0.5  # Center bars on the Y-axis ticks

#    rects = ax1.barh(pos, [scores[k].percentile for k in testNames],
#                     align='center',
#                     height=0.5, color='m',
#                     tick_label=testNames)

#    ax1.set_title(student.name)

#    ax1.set_xlim([0, 100])
#    ax1.xaxis.set_major_locator(MaxNLocator(11))
#    ax1.xaxis.grid(True, linestyle='--', which='major',
#                   color='grey', alpha=.25)

#    # Plot a solid vertical gridline to highlight the median position
#    ax1.axvline(50, color='grey', alpha=0.25)
#    # set X-axis tick marks at the deciles
#    cohort_label = ax1.text(.5, -.07, 'Cohort Size: {0}'.format(cohort_size),
#                            horizontalalignment='center', size='small',
#                            transform=ax1.transAxes)

#    # Set the right-hand Y-axis ticks and labels
#    ax2 = ax1.twinx()

#    scoreLabels = [format_score(scores[k].score, k) for k in testNames]

#    # set the tick locations
#    ax2.set_yticks(pos)
#    # make sure that the limits are set equally on both yaxis so the
#    # ticks line up
#    ax2.set_ylim(ax1.get_ylim())

#    # set the tick labels
#    ax2.set_yticklabels(scoreLabels)

#    ax2.set_ylabel('Test Scores')

#    ax2.set_xlabel(('Percentile Ranking Across '
#                    '{grade} Grade {gender}s').format(
#                        grade=attach_ordinal(student.grade),
#                        gender=student.gender.title()))

#    rect_labels = []
#    # Lastly, write in the ranking inside each bar to aid in interpretation
#    for rect in rects:
#        # Rectangle widths are already integer-valued but are floating
#        # type, so it helps to remove the trailing decimal point and 0 by
#        # converting width to int type
#        width = int(rect.get_width())

#        rankStr = attach_ordinal(width)
#        # The bars aren't wide enough to print the ranking inside
#        if (width < 5):
#            # Shift the text to the right side of the right edge
#            xloc = width + 1
#            # Black against white background
#            clr = 'black'
#            align = 'left'
#        else:
#            # Shift the text to the left side of the right edge
#            xloc = 0.98*width
#            # White on magenta
#            clr = 'white'
#            align = 'right'

#        # Center the text vertically in the bar
#        yloc = rect.get_y() + rect.get_height()/2.0
#        label = ax1.text(xloc, yloc, rankStr, horizontalalignment=align,
#                         verticalalignment='center', color=clr, weight='bold',
#                         clip_on=True)
#        rect_labels.append(label)

#    # make the interactive mouse over give the bar title
#    ax2.fmt_ydata = format_ycursor
#    plt.show(fig)
#    # return all of the artists created
#    return {'fig': fig,
#            'ax': ax1,
#            'ax_right': ax2,
#            'bars': rects,
#            'perc_labels': rect_labels,
#            'cohort_label': cohort_label}

#student = Student('Johnny Doe', 2, 'boy')
#scores = dict(zip(testNames,
#                  (Score(v, p) for v, p in
#                   zip(['7', '48', '12:52', '17', '14'],
#                       np.round(np.random.uniform(0, 1,
#                                                  len(testNames))*100, 0)))))
#cohort_size = 62  # The number of other 2nd grade boys

#arts = plot_student_results(student, scores, cohort_size)
