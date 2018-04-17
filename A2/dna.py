base_pairs = ['AT', 'TA', 'CG', 'GC']

def is_base_pair(base1, base2):
    """(str, str) -> bool
    Precondition: len(base1) == 1 and len(base2) == 1, and both base1 and base2
    are uppercase.
    
    Return True iff base1 and base2 form a base pair.
    >>>is_base_pair('A', 'T')
    True
    >>>is_base_pair('C', 'G')
    True
    >>>is_base_pair('C', 'T')
    False
    """
    
    return base1 + base2 in base_pairs
        
def is_dna(strand1, strand2):
    """(str, str) -> bool
    precondition: len(strand1) == len(strand2), both strand1 and strand2
    is only consisting of 'A', 'T', 'C' or 'G'. 
    
    Return True iff strand1 and strand2 form a properly base-paired DNA 
    molecule.
    >>>is_dna('GGATC', 'CCTAG')
    True
    >>>is_dna('GGCC', 'CCGG')
    True
    >>>is_dna('GGATC', 'GGATC')
    False
    """
    for i in range(len(strand1)):
        if not is_base_pair(strand1[i], strand2[i]):
            return False
    return True

def is_dna_palindrome(strand1, strand2):
    """(str, str) -> bool
    Precondiction: strand1 and strand2 represent DNA strands; strand1 and 
    strand2 must be the inputs that can pass is_dna function.
    
    Return True iff strand1 and strand2 can form a DNA palindrome.
    >>>is_dna_palindrome('GGATCC', 'CCTAGG')
    True
    >>>is_dna_palindrome('GGATC', 'CCTAG')
    False
    """
    DNA_molecule = strand1 + strand2
    return DNA_molecule == DNA_molecule[::-1]

def restriction_sites(DNA_strand, sequence):
    """(str, str) -> list of int
    Precondiction: DNA_strand has to be a strand of DNA, and sequence has to be 
    a valid recognition sequence; len(DNA_strand) >= sequence.
    
    Return a list of integers which represent the indicies where the 
    sequence appears in the DNA_strand. 
    
    >>>restriction_sites('CATCGTCGATGGGCCTCGATAC', 'TCGA')
    [5, 15]
    >>>restriction_sites('CAGCAGGGGCAG', 'CAG')
    [0, 3, 9]
    """
    result = []
    i = 0
    while DNA_strand.find(sequence, i) != -1:
        result.append(DNA_strand.find(sequence, i))
        i = DNA_strand.find(sequence, i) + len(sequence)
        
    return result

def match_enzymes(DNA_strand, enzyme_names, recognition_sequences):
    """(str, list of str, list of str) -> 
    list of two-item [str, list of int] lists
    
    Precondiction: DNA_strand has to be a strand of DNA, len(enzyme_names) ==
    len(recognition_sequences); enzyme_names is a list of restriction enzyme
    names, and recognition_sequences is the corresponding list of recognition
    sequences. 
    
    Return a list of two-item lists where the first item of each two-item
    list is the name of a restriction enzyme and the second item is the list of 
    indices in DNA_strand of the restriction sites that the enzyme cuts.
    
    >>>match_enzymes('TCGATCGAGATCGATC', ['TaqI', 'Sau3A'], ['TCGA', 'GATC'])
    [['TaqI', [0, 4, 10]], ['Sau3A', [2, 8, 12]]]
    >>>match_enzymes('GGCCGATCGGCC', ['EcoRV', 'HaeIII'], ['GATATC', 'GGCC'])
    [['EcoRV', []], ['HaeIII', [0, 8]]]
    """
    result = []
    for i in range(len(recognition_sequences)):
        enzyme = [enzyme_names[i]]
        match = restriction_sites(DNA_strand, recognition_sequences[i])
        enzyme.append(match)
        result.append(enzyme)
    return result

def one_cutters(DNA_strand, enzyme_names, recognition_sequences):
    """(str, list of str, list of str) -> list of two-item [str, int] lists
    
    Precondiction: DNA_strand has to be a strand of DNA, len(enzyme_names) ==
    len(recognition_sequences); enzyme_names is a list of restriction enzyme
    names, and recognition_sequences is the corresponding list of recognition
    sequences. 
    
    Return a list of two-item lists where the first item of each two-item list
    is the name of a restriction enzyme and the second item is the index in 
    DNA_strand of the one restriction site that the enzyme cuts (meaning the 
    coressponding recognition_sequencese only appears once); return empty
    list if none of such one-cutter recognition_sequenceswas found in 
    DNA_strand.
    
    >>>one_cutters('GATCGAGGTGACGCCT',['TaqI', 'HgaI'], ['TCGA', 'GACGC'])
    [['TaqI', 2], ['HgaI', 9]]
    >>>one_cutters('GATATCGAATTCAGCT', ['AluI', 'NotI'], ['AGCT', 'GCGGCCGC'])
    [['AluI', 12]]
    >>>one_cutters('AGCTGGCCAGCTGGCC', ['AluI', 'HaeIII'], ['AGCT', 'GGCC'])
    []
    """
    result = []
    for i in range(len(recognition_sequences)):
        if DNA_strand.find(recognition_sequences[i]) != -1:
            ocur = restriction_sites(DNA_strand, recognition_sequences[i])
            if len(ocur) == 1:
                x = [enzyme_names[i], DNA_strand.find(recognition_sequences[i])]
                result.append(x)       
    return result

def correct_mutations(mutated_strands, clean_strand, enzyme_names, 
                      recognition_sequences):
    """(list of str, str, list of str, list of str) -> NoneType
    Precondiction: len(enzyme_names) == len(recognition_names)
    len(one_cutters(clean_strand, enzyme_names, recognition_sequences)) == 1
    
    This function does not return anything, but modifies the mutated strands in 
    the list mutated_strands which share a 1-cutter based on provided 
    enzyme_names and recognition_sequenceswith the clean_strand by 
    replacing all bases starting at the 1-cutter in the mutated strand with all
    bases starting at the 1-cutter in the clean strand, up tp and including the 
    end of the strand. The mutated strands will not be modified if the item does
    not share exactly 1-cutter with clean_strand. 
    
    >>> mutated_strands = ['ACGTGGCCTAGCT', 'CAGCTGATCG']
    >>> clean_strand = 'ACGGCCTT'
    >>> enzyme_names = ['HaeIII', 'HgaI', 'AluI']
    >>> recognition_sequences = ['GGCC', 'GACGC', 'AGCT']
    >>> correct_mutations(mutated_strands, clean_strand, enzyme_names, 
        recognition_sequences)
    >>> mutated_strands
    ['ACGTGGCCTT', 'CAGCTGATCG']
    
    >>> mutated_strands = ['ACGTGGCCTAGCTGGCC', 'CAGACGCAGCT']
    >>> clean_strand = 'ACGGCCTT'
    >>> enzyme_names = ['HaeIII', 'HgaI']
    >>> recognition_sequences = ['GGCC', 'GACGC']
    >>> correct_mutations(mutated_strands, clean_strand, enzyme_names, 
        recognition_sequences)
    >>> mutated_strands
    ['ACGTGGCCTAGCTGGCC', 'CAGACGCAGCT']
    """
    name = one_cutters(clean_strand, enzyme_names, recognition_sequences)[0][0]
    index = enzyme_names.index(name)
    sequence = recognition_sequences[index]
    for i in range(len(mutated_strands)):
        if len(restriction_sites(mutated_strands[i], sequence)) == 1:
            mutated_strands[i] = \
                mutated_strands[i][:mutated_strands[i].find(sequence)] + \
                clean_strand[clean_strand.find(sequence):]