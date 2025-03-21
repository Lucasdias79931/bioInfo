import os
import sys
import hashlib
import time

def transforInHash(sequence: str) -> str:
    
    return hashlib.sha512(sequence.encode()).hexdigest()

here = os.path.abspath(os.path.dirname(__file__))

inputFile = None
outputFile = None


if len(sys.argv) < 2:
    print("Argumentos ausentes!")
    print("1: arquivo de entrada (obrigatório)")
    print("2 - arquivo de saída (padrão: sequencias_sem_duplicatas/sequencias.fasta)")

elif len(sys.argv) < 3:
    inputFile = sys.argv[1]

    outputFilePath = os.path.join(here, "sequencias_sem_duplicatas")
    os.makedirs(outputFilePath, exist_ok = True)
    outputFile = os.path.join(outputFilePath, "sequencias.fasta")

elif len(sys.argv) < 4:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
else:
    print("Argumentos incorrentos!")
    print("1: arquivo de entrada (obrigatório)")
    print("2 - arquivo de saída (padrão: sequencias_sem_duplicatas/sequencias.fasta)")

    print("Argumentos passados")
    for i in range(1, len(sys.argv)):
        print(sys.argv[i])
    
    exit(1)

startTime = time.time()

print("Iniciando processo...")

total_sequenciasProcessadas = 0
total_sequenciasFinal = 0
total_duplicata = 0
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
                else:
                    total_duplicata += 1
                sequence = []
        
        print(
            f"Sequências processadas e duplicatas eliminadas!\nTotal de sequências processadas:{total_sequenciasProcessadas}\nNúmero de duplicatas:{total_duplicata}\nNúmero de Sequências Final:{total_sequenciasFinal}")
        print(f"Resultado guardado em:{outputFile}")
        endTime = time.time() - startTime
        print(f"tempo de execução:{endTime:.4}s")
except FileNotFoundError:
    print(f"Erro: O arquivo '{inputFile}' não foi encontrado.")
    sys.exit(1)
except Exception as e:
    print(f"Erro inesperado: {e}")
    sys.exit(1)
