import random, math, pylab

def dist(x, y):
    return math.sqrt((x[0] -y[0]) ** 2 + (x[1] - y[1]) ** 2)

def tour_length(cities, N):
    return sum (dist(cities[k + 1], cities[k]) for k in range(N - 1)) + dist(cities[0], cities[N - 1])

N = 20
seed = 12345   #'hello'       # 'parrot',  'brian',  'hello',  12345
random.seed(seed)
cities = [(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)) for i in range(N)]
random.seed()
energy_min = float('inf')
for iter in xrange(10000000):
    random.shuffle(cities)
    energy =  tour_length(cities, N)
    if energy < energy_min:
        print energy
        energy_min = energy
        new_cities = cities[:]
cities = new_cities[:]
for i in range(1,N):
    pylab.plot([cities[i][0], cities[i - 1][0]], [cities[i][1], cities[i - 1][1]], 'bo-')
pylab.plot([cities[0][0], cities[N - 1][0]], [cities[0][1], cities[N - 1][1]], 'bo-')
pylab.title(str(energy_min) + ', seed = ' + str(seed) + ', N = ' + str(N))
pylab.axis('scaled')
pylab.axis([0.0, 1.0, 0.0, 1.0])
pylab.savefig('TSP_configuration_%s_n_%i.png' % (str(seed), N))
pylab.show()
