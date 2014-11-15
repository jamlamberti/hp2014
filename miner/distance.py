def compute_distance(x, y):
    def f(x, y):
        return (1.0*x+y)**2
    return (sum(map(f, x, y)))**0.5
def nearest_neighbor(k, v):
    ids = []
    dists = []
    for iid, val in v:
        dists.append(compute_distance(k, val))
        ids.append(iid)
    return ids[dists.index(min(dists))]
print compute_distance((0, 0), (1, 0))
print compute_distance((0, 0), (0, 1))
print compute_distance((0, 0), (1, 1))

print nearest_neighbor((0, 0), [[1, (1, 0)], [2, (0, 1)], [3, (1, 1)], [4, (0.5, 0.5)]])
