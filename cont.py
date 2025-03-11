





file = "/mnt/c/Users/lucas/Downloads/workspace-20250309T192120Z-001/workspace/BIO/refSeq/refSpike.fasta"


with open(file, 'r') as file:
    sequence = ""

    for line in file:
        sequence += line.strip()
    print(len(sequence)//3)    