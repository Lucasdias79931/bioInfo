from Bio import SeqIO
import os
import sys


def getSeq(inputfile: str = "", max_codon_in_sequence: int = None, max_gap_in_sequence:int = 4)->list:
    try:
        with open(inputfile, "r") as file:
            multipleGenome = []
            
            for sequence_id, sequence in SeqIO.FastaIO.SimpleFastaParser(file):
                
                if max_codon_in_sequence is not None and len(sequence) // 3 > max_codon_in_sequence:
                    continue

                
                
                codonsN = 0
                #quantidade de N
                manyCodonN = False 
                # se manyN == True, não adiciona sequence

                
                for nucleotide in range(0, len(sequence), 3):
                    if sequence[nucleotide] == "N" and sequence[nucleotide + 1] == "N" and sequence[nucleotide + 2] == "N":
                        codonsN += 1

                    if codonsN == max_gap_in_sequence:
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
                file.write(f"{genome[0]}\n{genome[1]}\n")
    except FileExistsError as e:
        print(f"Error:{e}")
        exit(1)
    except IOError as e:
        print(e)
        exit(1)    

def errorInputs():
    print("Argumentos ausentes ou passados errado!")
    print("1: diretório de entrada (obrigatório)")
    print("2: Diretório de saída (padrão: diretório atual/Sequences_filtered_by_gaps_and_length/)")
    print("3: Número máximo de códons (padrão: None)")
    print("4: Número máximo de GAPs (padrão: None)")
    sys.exit(1)  


here = os.path.abspath(os.path.dirname(__file__))

# Valores padrão
rootDirectory = None
outputFilePath = os.path.join(here, "Sequences_filtered_by_gaps_and_length")
max_codon_in_sequence = None
max_gap_in_sequence = None

# Processa os argumentos da linha de comando
if len(sys.argv) < 2:
    errorInputs()

rootDirectory = sys.argv[1]

if not os.path.isdir(rootDirectory):
    print("Diretório de entrada inexistente!")
    errorInputs()

if len(sys.argv) > 2:
    if os.path.exists(sys.argv[2]):
        outputFilePath = sys.argv[2]
    else:
        os.makedirs(outputFilePath, exist_ok= True)      
else:
    os.makedirs(outputFilePath, exist_ok= True)

if len(sys.argv) > 3:
    try:
        max_codon_in_sequence = int(sys.argv[3])
    except ValueError:
        print("Erro: O número máximo de códons deve ser um inteiro!")
        errorInputs()

if len(sys.argv) > 4:
    try:
        max_gap_in_sequence = int(sys.argv[4])
    except ValueError:
        print("Erro: O número máximo de GAPs deve ser um inteiro!")
        errorInputs()

# Mudar conforme nescessário
rootDirectory = os.path.join(here, "spike_ordenadoPorData")

print("Iniciando Processo!")
for file in range(34):
    #Mudar conforme nescessário!
    inputFile = os.path.join(rootDirectory, f"sequencias_spike{file}.fasta")
    multple_genomes = getSeq(inputFile, max_codon_in_sequence, max_gap_in_sequence)
    print(f"Sequências Colhidas no arquivo: {inputFile}")

    #Mudar conforme nescessário!
    outputFile = os.path.join(outputFilePath, f"sequencias_spike{file}.fasta")
    writeSeq(outputFile, multple_genomes)
    print(f"Sequências filtradas escritas no arquivo: {outputFile}")

print(f"Sequências salvos no diretório: {outputFilePath}")
print("Processo concluído com sucesso!")