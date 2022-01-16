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

def farthest_first_traversal(k, m, points):
    centers = [points[0]]
    while len(centers) < k:

        # First, for each data point find its closest center
        points_and_d = []
        for p in points:
            distance_to_c = 9999999
            for c in centers:
                # Calculate the distance
                distance = 0
                for d in range(0, m):
                    distance += (p[d] - c[d])**2
                distance = sqrt(distance)

                if distance < distance_to_c:
                    distance_to_c = distance
            # add the point and its distance to its center to the list
            points_and_d.append((p, distance_to_c))

        # Find the point with the max distance to its center
        farthest_p = None
        d_of_p = 0
        for p in points_and_d:
            if p[1] > d_of_p:
                d_of_p = p[1]
                farthest_p = p[0]
        centers.append(farthest_p)
    return centers

def start():
    k, m, points = read_input("dataset.txt")
    centers = farthest_first_traversal(k, m, points)
    for c in centers:
        for d in range(0, m):
            print(c[d], end=" ")
        print()

if __name__ == '__main__':
    start()
