import simplejson
import matplotlib.pyplot as plt

if __name__ == "__main__":
	with open('result.txt', 'r') as f:
		array = simplejson.loads(f.read())
	lowest = 0
	for a in range(len(array)):
		if array[a] > lowest:
			lowest = array[a]
		array[a] = lowest
	z = open('result2.txt', 'w')
	simplejson.dump(array, z)
	z.close()
	x_axis = [0]*len(array)
	for i in range(len(array)):
		x_axis[i] = i/(60*24.0)
	plt.plot(x_axis,array)

	plt.ylabel('collected station data')
	plt.xlabel('days')
	axes = plt.gca()
	axes.set_ylim([0,1128])
	axes.set_yticks(list(plt.yticks()[0]) + [max(array)])

	axes.text(0, max(array), '< max', verticalalignment='center', horizontalalignment='left')

	plt.savefig('result.png', dpi = 300)
