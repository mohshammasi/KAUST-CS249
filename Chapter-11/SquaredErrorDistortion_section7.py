from math import sqrt

def read_input(filename):
    try:
        input_file = open(filename, "r")
        k, m = input_file.readline().split(" ")
        k = int(k)
        m = int(m)

        centers = []
        points = []
        reading_centers = True
        for line in input_file:
            if line == '--------\n':
                reading_centers = False
                continue

            point = tuple(map(float, line.split()))
            if reading_centers:
                centers.append(point)
            else:
                points.append(point)
    except:
        print("Exception caught, file probably doesnt exist")
    return k, m, centers, points

def farthest_first_traversal(k, m, points):
    centers = [points[0]]
    while len(centers) < k:

        # First, for each data point find its closest center
        points_and_d = []

        # Find the point with the max distance to its center
        farthest_p = None
        d_of_p = 0
        for p in points_and_d:
            if p[1] > d_of_p:
                d_of_p = p[1]
                farthest_p = p[0]
        centers.append(farthest_p)
    return centers

def squared_error_distortion(k, m, centers, points):
    sum = 0
    n = len(points)
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
        # Square the distance and add it to the sum so then we can find the mean
        sum += (distance_to_c**2)

    error = round(sum/n, 3)
    return error

def start():
    k, m, centers, points = read_input("dataset.txt")
    squared_error = squared_error_distortion(k, m, centers, points)
    print(squared_error)

if __name__ == '__main__':
    start()
