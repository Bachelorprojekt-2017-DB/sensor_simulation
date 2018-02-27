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
	x_axis = [0]*(len(array))
	for i in range(len(array)):
		x_axis[i] = i/len(array)*100
	plt.plot(x_axis,array)
	plt.axis([0,100,0,764])
	plt.ylabel('collected station data')
	plt.xlabel('time in % of month')
	plt.savefig('result.png')