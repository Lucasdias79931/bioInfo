from Bio import SeqIO
import re
import os
import sys
import datetime

def getHeaders(inputfile: str) -> list:
    try:
        with open(inputfile, 'r') as handle:
            multiple_genomes = []
            current_position = 0  # Posição atual no arquivo (em bytes)

            for line in handle: # Itera linha por linha do arquivo
                line_bytes = line.encode() # Codifica a linha para bytes
                line_length = len(line_bytes) # Obtém o comprimento da linha em bytes

                if line.startswith(">"): # Verifica se a linha é um cabeçalho
                    date_str = line.split("|") # Separa a string de data

                    # Extrai ano, mês e dia da string de data
                    if len(date_str) == 3:
                        date_str = date_str[1].split("-")
                    else:
                        date_str = date_str[2].split("-")

                    year = 0
                    month = 0
                    day = 1

                    if len(date_str) == 3:
                        year, month, day = map(int, date_str)
                    else:
                        year, month = map(int, date_str)

                    date_obj = datetime.datetime(year, month, day) # Cria objeto datetime
                    timestamp = date_obj.timestamp() # Obtém o timestamp

                    multiple_genomes.append((current_position, timestamp)) # Usa current_position como offset

                current_position += line_length # Atualiza a posição atual

            return multiple_genomes
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        return None
    except IOError as e:
        print(f"Erro de leitura/escrita: {e}")
        return None





def ordenaAllSeq(sequence:list)->list:
    return sorted(sequence, key=lambda x: x[1])

rootDirectory = ""
destine = ""



if len(sys.argv) < 2:
    print("Informe o diretório em que se encontram as sequências")
    print('1 - diretório de entrada (obrigatório)\n2 - arquivo de saída (opcional)')
    raise ValueError("Erro: Parâmetros insuficientes")
    exit(1)
else:
    rootDirectory = sys.argv[1]


if len(sys.argv) < 3:
    here = os.path.abspath(os.path.dirname(__file__))
    destine = os.path.join( here, "spike_ordenadoPorData")
    os.makedirs(destine, exist_ok=True)
    destine = os.path.join(destine, "spike_ordenado.fasta") 
else:
    destine = sys.argv[2]




print("Iniciando Processo!")
headers = list()
print("Colhendo headers!")
for root, foulders, files in os.walk(rootDirectory):
   
    for file in files:
       
        genome_file_path = os.path.join(root, file)
        
        
        if genome_file_path.endswith(f'.fasta'):
           
            headers = getHeaders(genome_file_path)

print("Headers colhidos com sucesso!")
print("Ordenando headers!")
headers = ordenaAllSeq(headers)



print("Headers ordenados!")
print("Iniciando processo de salvar sequências na ordem correta!")
try:
    genome_file_path = os.path.join(rootDirectory, 'spikeFrom11_19ToNow.fasta')

    with open(destine,'a') as file:
        with open(genome_file_path, "r") as genome:
            for offset, date in headers: # Itera sobre os cabeçalhos e offsets
                genome.seek(offset) # Posiciona o ponteiro no offset correto
                sequence_id = genome.readline() # Lê o identificador da sequência
                sequence = genome.readline() # Lê a sequência

                file.write(f"{sequence_id}{sequence}")
except FileNotFoundError as e:
    print(e)
        
            

print("Processo Conclúido!")
print(f"Sequências ordenadas salvas em:{destine}")


