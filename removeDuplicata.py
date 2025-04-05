import os
import sys
import hashlib

def transforInHash(sequence: str) -> str:
    
    return hashlib.sha512(sequence.encode()).hexdigest()

here = os.path.abspath(os.path.dirname(__file__))

inputFile = "/home/asmita/workspace/bio/SPIKE/spike/sequencias_spike.fasta"
outputFile = os.path.join(here, "spikeParticionado/sequencias_spike.fasta")


total_sequenciasProcessadas = 0
total_sequenciasFinal = 0

try:
    with open(inputFile, "r") as file, open(outputFile, "w") as outFile:
        sequences = dict()  
        sequence = []

        for line in file:

            line = line.strip()

            if line.startswith(">"):
                sequence.append(line) 
            else:
                sequence.append(line)
                total_sequenciasProcessadas += 1

            if len(sequence) == 2:
                hash_sequence = transforInHash(sequence[1])

                if hash_sequence not in sequences:
                    total_sequenciasFinal += 1
                    sequences[hash_sequence] = 1
                    outFile.write(f"{sequence[0]}\n{sequence[1]}\n")
                sequence = []
        
        print(
            f"Sequências processadas e duplicatas eliminadas!\nTotal de sequências processadas:{total_sequenciasProcessadas}\nNúmero de Sequências Final:{total_sequenciasFinal}")
        print(f"Resultado guardado em:{outputFile}")

except FileNotFoundError:
    print(f"Erro: O arquivo '{inputFile}' não foi encontrado.")
    sys.exit(1)
except Exception as e:
    print(f"Erro inesperado: {e}")
    sys.exit(1)
