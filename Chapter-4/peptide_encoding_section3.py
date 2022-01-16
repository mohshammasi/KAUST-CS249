from genetic_code import genetic_code

def read_input(filename):
    try:
        input_file = open(filename, "r")
        dna = input_file.readline().rstrip('\n')
        peptide = input_file.readline().rstrip('\n')
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return dna, peptide

def reverse_complement(string):
    reverse_string = ''
    for i in range(len(string)-1, -1, -1): # 2nd arg not inclusive hence -1
        if string[i] == 'A':
            reverse_string += 'T'
        elif string[i] == 'T':
            reverse_string += 'A'
        elif string[i] == 'C':
            reverse_string += 'G'
        elif string[i] == 'G':
            reverse_string += 'C'
        else:
            print('This string contains a weird thing')
    return reverse_string

def transcribe(dna):
    dna = list(dna)
    for i in range(0, len(dna)):
        if dna[i] == 'T':
            dna[i] = 'U'
    return ''.join(dna)

def flip_string(string):
    flipped_string = ''
    n = len(string)
    for i in range(0, n):
        flipped_string += string[n-1-i]
    return flipped_string

def peptide_encoding(dna, peptide):
    # Get the compliment
    reverse_c = reverse_complement(dna)

    # Transcribe botht the DNA string and its reverse complement
    transcribed_dna = transcribe(dna)
    transcribed_r = transcribe(reverse_c)

    n = len(dna)
    p_length = len(peptide)
    substring_size = p_length * 3

    patterns_encoding_peptide = []
    for i in range(0, n-substring_size+1):
        dna_substring_protein = ''
        r_substring_protein = ''
        for j in range(0, substring_size, 3):
            # Check substrings of both the dna and its reverse
            dna_substring_protein += genetic_code[transcribed_dna[(i+j):(i+j)+3]]
            r_substring_protein += genetic_code[transcribed_r[(n-i+j)-substring_size:(n-i+j)-substring_size+3]]

        if dna_substring_protein == peptide:
            patterns_encoding_peptide.append(dna[i:i+substring_size])
        elif r_substring_protein == peptide:
            patterns_encoding_peptide.append(dna[i:i+substring_size])

    return patterns_encoding_peptide

def start():
    dna, peptide = read_input("dataset.txt")
    result = peptide_encoding(dna, peptide)

    try:
        output_file = open("output.txt", "w")
        for string in result:
            output_file.write(string + '\n')
        output_file.close()
        print("Output written successfully to the textfile.")
    except:
        print('File I/O Error...')



if __name__ == '__main__':
    start()
