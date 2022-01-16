import numpy as np

def read_input(filename):
    try:
        input_file = open(filename, "r")
        text = input_file.readline().rstrip('\n')
        input_file.close()
    except IOError as e:
        print(e)
    return text

def burrow_wheeler_transform(text):
    n = len(text)
    cyclic_rotations = []
    for i in range(0, n):
        rotation = text[n-i:n] + text[0:n-i]
        cyclic_rotations.append(rotation)
    cyclic_rotations.sort() # order them lexicographically

    bwm = np.zeros((n, n), dtype='object')
    for i, string in enumerate(cyclic_rotations):
        bwm[i] = list(string)

    transposed_bwm = np.array(bwm).T.tolist()
    bwt = ''.join(transposed_bwm[n-1])
    return bwm, bwt

def start():
    text = read_input("dataset.txt")
    bwm, bwt = burrow_wheeler_transform(text)
    print(bwt)



if __name__ == '__main__':
    start()
