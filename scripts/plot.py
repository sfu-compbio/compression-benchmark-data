# 786 

import os
import numpy as np
import pandas as pd

def generate_plot(data, tools, samples, file_type):
	from scipy.spatial import ConvexHull
	from matplotlib.lines import Line2D
	import matplotlib.pyplot as plt
	from matplotlib import rc
	rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
	rc('text', usetex=True)

	def tickfmt(x):
		if x < 0:
			x = - x + 1
		else:
			x = x + 1
		return '%g' % x

	def centeroidnp(arr):
	    length = arr.shape[0]
	    sum_x = np.sum(arr[:, 0])
	    sum_y = np.sum(arr[:, 1])
	    return sum_x/length, sum_y/length

	colors = [ # Taken from http://www.two4u.com/color/small-txt.html
		('Red                 ',     '#FF0000'),
		('Green               ',     '#00FF00'),
		('Blue                ',     '#0000FF'),
		('Magenta             ',     '#FF00FF'),
		('Cyan                ',     '#00FFFF'),
		('Orange              ',     '#FF7F00'),
		('Black               ',     '#000000'),
		('Aquamarine          ',     '#70DB93'),
		('Rich Blue           ',     '#5959AB'),
		('Very Dark Brown     ',     '#5C4033'),
		('Cadet Blue          ',     '#5F9F9F'),
		('Old Gold            ',     '#CFB53B'),
		('Dark Wood           ',     '#855E42'),
		('Spring Green        ',     '#00FF7F'),
		('Dim Grey            ',     '#545454'),
		('Firebrick           ',     '#8E2323'),
		('Flesh               ',     '#F5CCB0'),
		('Forest Green        ',     '#238E23'),
		('Gold                ',     '#CD7F32'),
		('Goldenrod           ',     '#DBDB70'),
		('Grey                ',     '#C0C0C0'),
		('Violet Red          ',     '#CC3299'),
		('Yellow              ',     '#FFFF00'),
		('Green Copper        ',     '#527F76'),
		('Khaki               ',     '#9F9F5F'),
		('Maroon              ',     '#8E236B'),
		('Midnight Blue       ',     '#2F2F4F'),
		('New Tan             ',     '#EBC79E'),
		('Orchid              ',     '#DB70DB'),
		('Quartz              ',     '#D9D9F3'),
		('Scarlet             ',     '#8C1717'),
		('Sea Green           ',     '#238E68'),
		('Semi-Sweet Chocolate',     '#6B4226'),
		('Sienna              ',     '#8E6B23'),
		('Slate Blue          ',     '#007FFF'),
		('Steel Blue          ',     '#236B8E'),
		('Summer Sky          ',     '#38B0DE'),
		('Tan                 ',     '#DB9370'),
		('Turquoise           ',     '#ADEAEA'),
		('Violet              ',     '#4F2F4F'),
	]
	markers = ['v','^','8','s','p','*','H','o','x','|','_','v','.','s']

	tools = zip(zip(markers, [t for t in tools]), [c[1] for c in colors])
	print tools

	fig = plt.figure()
	axes = []
	for index, threads in enumerate([1, 4]):
		ax1 = fig.add_subplot(120 + index + 1)
		axes.append(ax1)
		ax1.grid(True, linestyle='-', color='0.75')

		for _, color in tools:
			marker, tool = _

			x, y = [], []
			for sample in samples:
				dy = data[(data.tool == tool) & (data.threads == threads) & (data['sample'] == sample)]
				if threads == 1 and len(dy[dy.status == 1]) == 0:
					dy = data[(data.tool == tool) & (data.threads == 4) & (data['sample'] == sample)]

				reftool = 'samtools' if file_type == 'sam' else 'pigz'
				dr = data[(data.tool == reftool) & (data.threads == 1) & (data['sample'] == sample)] 
				
				if len(dy['status']) > 0 and dy['status'].iloc[0] == 1:
					xx = dy['size'].iloc[0]
					xx /= dr['size'].iloc[0] 
					if xx < 1: 
						xx = -1 / xx
					assert(not(-1 < xx < 1))
					if xx <= -1: 
						xx += 1
					else:	
						xx -= 1
					x.append(xx)

					yy = dy['walltime_ratio'].iloc[0]
					if yy < 1: yy = -1 / yy
					assert(not(-1 < yy < 1))
					if yy <= -1:
						yy += 1
					else:
						yy -= 1
					y.append(yy)

			if len(x) < 3:	continue
			
			l = ax1.scatter(x, y, color=color, marker=marker, s=50, label=tool)
			points = np.array([[x[j], y[j]] for j in xrange(len(x))])
			try:
				hull = ConvexHull(points).vertices
			except:
				hull = range(len(x))
			centroid = centeroidnp(points[hull])
			ax1.scatter(centroid[0], centroid[1], color=color, marker=marker, s=200, edgecolor='black', linewidth='1')
			ax1.fill(points[hull,0], points[hull,1], 'k', alpha=0.4, color=color)
			
			print tool, color, marker
		if file_type == 'sam':
			ax1.set_xlim([-1.4, 0.55])
			ax1.set_ylim([-12, 3.5])
		else:
			ax1.set_xlim([-1.2, 0.1])
			ax1.set_ylim([-5.5, 8.7])
		ax1.set_xticklabels(map(tickfmt, ax1.get_xticks()))
		ax1.set_yticklabels(map(tickfmt, ax1.get_yticks()))
		ax1.set_ylabel('Compression time ratio')
		ax1.set_xlabel('Compression  ratio')

		ax1.add_line(Line2D([-20, 20], [0, 0], linewidth=1, color='black'))
		ax1.add_line(Line2D([0, 0],[-20, 20], linewidth=1, color='black'))
	axes[0].legend(bbox_to_anchor=(1, 1.2), loc='upper center', borderaxespad=0., ncol=5, fancybox=True)

	fig.set_size_inches(20,8)
	fig.savefig('fig.png', bbox_inches='tight')
	# preview
	os.system('qlmanage -p fig.png')
