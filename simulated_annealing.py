"""
Implementing Einstein's Fish riddle explained here:
    http://blog.pluszero.ca/blog/2016/07/17/
        using-simulated-annealing-to-solve-logic-puzzles/
"""

import numpy as np


# house          1            2          3          4            5
animals       = ['bird',      'dog',     'cat',     'horse',     'fish']
cigarettes    = ['pall mall', 'dunhill', 'blends',  'prince',    'blue master']
nationalities = ['british',   'danish',  'swedish', 'norwegian', 'german']
house_colours = ['yellow',    'red',     'white',   'green',     'blue']
drinks        = ['water',     'tea',     'milk',    'coffee',    'root beer']

CFG = np.array([animals, cigarettes, nationalities, house_colours, drinks])


def adjacents(arr):
    return (np.arange(len(filter(None, arr))) ==
            arr.nonzero()[0] - min(arr.nonzero()[0])
           ).all()


def cost(cfg):
    """ Score for a configuration of the houses' wrt constraints of the riddle.

    Lower result indicates a better configuration; closer to the desired constraints.

    The Brit lives in the house with red walls.
    The Swede has a dog.
    The Dane drinks tea.
    The house with green walls is directly to the left of the house with white
        walls.
    The owner of the house with green walls drinks coffee.
    The person who smokes Pall Mall cigars owns a bird.
    The owner of the house with yellow walls smokes Dunhill.
    The man living in the center house drinks milk.
    The Norwegian lives in the first house.
    The man who smokes blends lives next to the cat owner.
    The horse's owner lives next to the man who smokes Dunhill.
    The man who smokes Blue Master drinks root beer.
    The German smokes Prince.
    The Norwegian lives next to the house with blue walls.
    The man who smokes Blends lives next to the man who drinks water.
    """
    score = [
        2 in ((cfg == 'british') | (cfg == 'red')).sum(axis=0),
        2 in ((cfg == 'swedish') | (cfg == 'dog')).sum(axis=0),
        2 in ((cfg == 'danish') | (cfg == 'tea')).sum(axis=0),
        1 == list(cfg[3,:]).index('green') - list(cfg[3,:]).index('white'),
        2 in ((cfg == 'green') | (cfg == 'coffee')).sum(axis=0),
        2 in ((cfg == 'bird') | (cfg == 'pall mall')).sum(axis=0),
        2 in ((cfg == 'yellow') | (cfg == 'dunhill')).sum(axis=0),
        'milk' in cfg[:, 2],
        'norwegian' in cfg[:, 0],
        adjacents(((cfg == 'blends') | (cfg == 'cat')).sum(0)),
        adjacents(((cfg == 'horse') | (cfg == 'dunhill')).sum(0)),
        2 in ((cfg == 'blue master') | (cfg == 'root beer')).sum(axis=0),
        2 in ((cfg == 'german') | (cfg == 'prince')).sum(axis=0),
        adjacents(((cfg == 'norwegian') | (cfg == 'blue')).sum(0)),
        adjacents(((cfg == 'blends') | (cfg == 'water')).sum(0)),
    ]
    return -1 * sum(score)


def shuffle(arr):
    choice = np.random.randint(len(arr))
    np.random.shuffle(arr[choice])
    return arr


def main():
    cfg_cost = cost(CFG)
    cfg = CFG
    N = 10000
    for i in range(N):
        if i % (N / 20.0) == 0:
            print(cost(cfg))
        cfg_prime = shuffle(np.copy(cfg))
        cfg_prime_cost = cost(cfg_prime)
        if cfg_prime_cost < cfg_cost:
            cfg = cfg_prime
            cfg_cost = cfg_prime_cost

    print(cost(cfg))


if __name__ == '__main__':
    main()
