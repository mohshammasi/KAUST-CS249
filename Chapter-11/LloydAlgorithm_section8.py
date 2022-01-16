from math import sqrt

def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, m = input_file.readline().split(" ")
        k = int(k)
        m = int(m)
        points = []
        for line in input_file:
            point = tuple(map(float, line.split()))
            points.append(point)
    except:
        print("Exception caught, file probably doesnt exist")
    return k, m, points

def lloyd_algorithm(k, m, points):
    centers = [points[p] for p in range(k)]
    i = 0
    while i < 1000:
        # Calculate the clusters
        clusters = dict()
        for p in points:
            distance_to_c = 9999999
            the_c = None
            for c in centers:
                # Calculate the distance
                distance = 0
                for d in range(0, m):
                    distance += (p[d] - c[d])**2
                distance = sqrt(distance)

                if distance < distance_to_c:
                    distance_to_c = distance
                    the_c = c

            # Add the point to the cluster of the center 'c'
            clusters.setdefault(the_c, []).append(p)

        # For each cluster, calculate its center of gravity and make it the new
        # center of that cluster
        centers.clear()
        for center in clusters:
            cluster = clusters[center] # contains all the points of the cluster

            # Calculate the center of gravity
            n = len(cluster)
            cog = []
            for d in range(0, m):
                dth_coord_avg = 0
                for p in cluster:
                    dth_coord_avg += p[d]
                dth_coord_avg = round(dth_coord_avg/n, 3)
                cog.append(dth_coord_avg)
            cog = tuple(cog)
            centers.append(cog)

        i += 1
    return centers

def start():
    k, m, points = read_input("dataset.txt")
    centers = lloyd_algorithm(k, m, points)
    for c in centers:
        for d in range(0, m):
            print(c[d], end=" ")
        print()

if __name__ == '__main__':
    start()
