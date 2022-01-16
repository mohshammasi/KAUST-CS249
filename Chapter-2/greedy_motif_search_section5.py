import numpy as np

def read_input(filename):
    input_file = open(filename, "r")
    k, t = input_file.readline().strip().split(" ")
    dnas = input_file.read().splitlines()
    input_file.close()
    return int(k), int(t), dnas

def profile_most_probable_kmer(genome, k, profile_matrix):
    n = len(genome)
    most_probable_pattern = genome[0:k]
    most_probable_probability = 0
    for i in range(0, n-k+1):
        pattern = genome[i:i+k]
        probability = 1
        for offset, n in enumerate(pattern):
            if n == 'A':
                probability *= profile_matrix[0][offset]
            elif n == 'C':
                probability *= profile_matrix[1][offset]
            elif n == 'G':
                probability *= profile_matrix[2][offset]
            elif n == 'T':
                probability *= profile_matrix[3][offset]
            else:
                print('Weird string, Exiting...')
                exit()

        if probability > most_probable_probability:
            most_probable_pattern = pattern
            most_probable_probability = probability
    return most_probable_pattern

# motifs is a n x k matrix, example chapter 2 section 3 step 3
# returns both the count matrix and the consensus string
def count_motifs(motifs, k):
    # construct a count matrix of 0's which is a 4 x k matrix
    count_matrix = [[0 for i in range(k)] for row in range(4)]

    # Transpose matrix to count from each column
    transposed_motifs = np.array(motifs).T.tolist()

    # Use count() to count occurances in each column
    consensus_string = ''
    for i in range(0, len(transposed_motifs)):
        count_matrix[0][i] = transposed_motifs[i].count('A')
        count_matrix[1][i] = transposed_motifs[i].count('C')
        count_matrix[2][i] = transposed_motifs[i].count('G')
        count_matrix[3][i] = transposed_motifs[i].count('T')

        # 'A' case, 'C' case, 'G' case and finally 'T' case
        max_count = 0
        popular_letter = ''
        if count_matrix[0][i] > max_count:
            max_count = count_matrix[0][i]
            popular_letter = 'A'
        if count_matrix[1][i] > max_count:
            max_count = count_matrix[1][i]
            popular_letter = 'C'
        if count_matrix[2][i] > max_count:
            max_count = count_matrix[2][i]
            popular_letter = 'G'
        if count_matrix[3][i] > max_count:
            max_count = count_matrix[3][i]
            popular_letter = 'T'

        # building the consensus string
        consensus_string += popular_letter

    return count_matrix, consensus_string


def profile_motifs(count_matrix, t):
    return (np.array(count_matrix)/t).tolist()

# Consensus is the consensus string broken down character wise in a list
def score_motifs(motifs, consensus, k):
    score = 0
    for i in range(0, len(motifs)):
        for j in range(0, k):
            if motifs[i][j] != consensus[j]:
                score += 1
    return score

def greedy_motif_search(k, t, dnas):
    best_motifs = []
    for i in range(0, len(dnas)):
        first_kmer = dnas[i][0:k]
        best_motifs.append(list(first_kmer))

    for i in range(0, len(dnas[0])-k+1):
        motifs = [list(dnas[0][i:i+k])]
        for j in range(1, t):
            # Create a Profile matrix from the current motifs collection
            count_matrix, consensus_string = count_motifs(motifs, k)
            profile_matrix = profile_motifs(count_matrix, len(motifs)) # number of rows of motifs to divide by

            # Get next DNA most probable string to be added to our collection
            next_motif = profile_most_probable_kmer(dnas[j], k, profile_matrix)
            motifs.append(list(next_motif))

        # Get the consensus string for the best motifs collection to compute score
        best_count_matrix, best_consensus = count_motifs(best_motifs, k)

        # Compute scores
        motifs_score = score_motifs(motifs, consensus_string, k)
        bestmotifs_score = score_motifs(best_motifs, best_consensus, k)

        if motifs_score < bestmotifs_score:
            best_motifs = motifs
    return best_motifs


def start():
    k, t, dnas = read_input("dataset.txt")
    result = greedy_motif_search(k, t, dnas)
    for pattern in result:
        print(''.join(pattern))


if __name__ == '__main__':
    start()
