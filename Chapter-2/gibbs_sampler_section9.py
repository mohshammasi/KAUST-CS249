import numpy as np
from random import randint, choices

def read_input(filename):
    input_file = open(filename, "r")
    k, t, N = input_file.readline().strip().split(" ")
    dnas = input_file.read().splitlines()
    input_file.close()
    return int(k), int(t), int(N), dnas

def profile_randomly_generated_kmer(genome, k, profile_matrix):
    probabilities = []
    n = len(genome)
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

        probabilities.append(probability)

    # Calculate C, the sum of the probabilities
    C = sum(probabilities)

    # Our 'die'
    die = (np.array(probabilities)/C).tolist()

    return probabilities, C, die


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
        count_matrix[0][i] = transposed_motifs[i].count('A') + 1
        count_matrix[1][i] = transposed_motifs[i].count('C') + 1
        count_matrix[2][i] = transposed_motifs[i].count('G') + 1
        count_matrix[3][i] = transposed_motifs[i].count('T') + 1

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

def gibbs_sampler(k, t, N, dnas):
    # Randomly select kmers from each DNA string
    n = len(dnas[0]) # all strings have the same length
    motifs = []
    for i in range(0, len(dnas)):
        random_num = randint(0, n-k)
        random_kmer = dnas[i][random_num:random_num+k]
        motifs.append(list(random_kmer))


    best_motifs = motifs
    bestmotifs_score = 0
    best_consensus = ''
    for j in range(1, N):
        i = randint(0, t-1)

        # Delete the i-th motif
        motif_i = motifs.pop(i)

        count_matrix, consensus = count_motifs(motifs, k)
        profile_matrix = profile_motifs(count_matrix, t+(len(motifs)-1))

        # Get Profile randomly generated kmer
        probabilities_of_i, C, die_i = profile_randomly_generated_kmer(dnas[i], k, profile_matrix)

        # Roll the 'die' to pick the i-th kmer in the removed DNA
        indices = [idx for idx in range(0, len(die_i))]
        # corresponds each element in indices to a weight from the die, then randomly select a num
        kmer_pos = choices(indices, die_i)

        # For some reason kmer_pos is returned as a list
        # Slice the ith kmer from the removed DNA and add this new random kmer to the motifs collection
        ith_kmer = dnas[i][kmer_pos[0]:kmer_pos[0]+k]
        motifs.insert(i, list(ith_kmer))

        # Get the consensus string for the best motifs collection to compute score
        best_count_matrix, best_consensus = count_motifs(best_motifs, k)

        # Calculate scores
        motifs_score = score_motifs(motifs, consensus, k)
        bestmotifs_score = score_motifs(best_motifs, best_consensus, k)

        if motifs_score < bestmotifs_score:
            best_motifs = motifs

    return best_motifs, bestmotifs_score, best_consensus


def start():
    k, t, N, dnas = read_input("subtle_motif_dataset.txt")
    best_score = float('inf')
    best_motifs = []
    best_consensus = ''
    for i in range(0, 50):
        motifs, score, consensus = gibbs_sampler(k, t, N, dnas)
        if score < best_score:
            best_score = score
            best_motifs = motifs
            best_consensus = consensus

    for motif in best_motifs:
        print(''.join(motif))
    print(best_score)
    print(best_consensus)


if __name__ == '__main__':
    start()
