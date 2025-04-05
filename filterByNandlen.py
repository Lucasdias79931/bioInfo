from Bio import SeqIO

import os
import sys



def getSeq(inputfile: str = "", maxCodon: int = None, maxN:int = None)->list:
    try:
        with open(inputfile, "r") as file:
            multipleGenome = []
            
            for sequence_id, sequence in SeqIO.FastaIO.SimpleFastaParser(file):
                
                if maxCodon is not None and maxCodon < len(sequence) //3:
                    continue

                
                
                nCodonsN = 0
                #quantidade de N
                manyCodonN = False 
                # se manyN == True, não adiciona sequence

                if maxN:
                    for nucleotide in range(0, len(sequence), 3):
                        if sequence[nucleotide] == "N" and sequence[nucleotide + 1] == "N" and sequence[nucleotide + 2] == "N":
                            nCodonsN += 1

                        if nCodonsN == maxN:
                            manyCodonN = True
                            break    
                    if manyCodonN:
                        continue
                
                multipleGenome.append([sequence_id, sequence])
                
            return multipleGenome

    except FileNotFoundError as e:
        print(f"Erro ao tentar encontrar arquivo: {inputfile}")
        print(f"Error:{e}")
        exit(1)
    except IOError as e:
        print(e)
        exit(1)


def writeSeq(outputFile: str, multiple_genomes: list)->None:
    try:
        with open(outputFile, "w") as file:
            for genome in multiple_genomes:
                file.write(f">{genome[0]}\n{genome[1]}\n")
    except FileExistsError as e:
        print(f"Error:{e}")
        exit(1)
    except IOError as e:
        print(e)
        exit(1)    



here = os.path.abspath(os.path.dirname(__name__))
destine = os.path.join(here, "sequences_filtrado_por_comprimento_maxN")
os.makedirs(destine, exist_ok = True)

inputFilePath  = None
outputFilePath = os.path.join(destine, "sequences.fasta")
maxCodon = None
maxGap = None


if len(sys.argv) == 5:
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    maxCondon = int(sys.argv[3])
    maxGap = int(sys.argv[4])
elif len(sys.argv) == 4:
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    maxCondon = int(sys.argv[3])

elif len(sys.argv) == 3:
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
elif len(sys.argv) == 2:
    inputFilePath = sys.argv[1]
else:
    print("Parametros incorrentos!")
    print("1: Arquivo de entrada [obrigatório]!")
    print("2: Arquivo de saída [padrão: /sequences_filtrado_por_comprimento_maxN/output.fasta]!")
    print("3: Número máximo de códon [padão: None]")
    print("4: Número de gap [padrão: None]")
    exit(1)




print("Iniciando processo!")
for file in range(34):
    inputfile = os.path.join(here, f"spike_ordenadoPorData/sequencias_spike{file}.fasta")

    print(f"Colhendo sequências no diretório: {inputfile}")
    multiple_genomes = getSeq(inputfile, maxCodon, maxGap)

    outputFile = os.path.join(destine, f"sequencias_spike{file}.fasta")


    print(f"Escrevendo no diretório: {outputFile}")
    writeSeq(outputFile, multiple_genomes)
    
print(f"Genomes filtrados por comprimento e quantidade de N!\nsequências guardadas no diretório {destine}!")


