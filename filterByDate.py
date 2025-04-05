from Bio import SeqIO
import re
import os
import sys
import datetime
import calendar

import re
import datetime
from Bio import SeqIO

def getSeq(inputfile: str, data: float, totalS: int) -> list:
    try:
        with open(inputfile, 'r') as handle:
            multiple_genomes = []

            for sequence_id, sequence in SeqIO.FastaIO.SimpleFastaParser(handle):
                
             
                
                try:
                    date_str = sequence_id.split("|")

                    if len(date_str) == 3:
                        date_str = date_str[1].split("-")
                    else:
                        date_str = date_str[2].split("-")

                    if len(date_str) < 2:
                        continue
                    

                
                    year = 0
                    month = 0
                    day = 1
                    
                    if len(date_str) == 3:
                        year, month, day = map(int, date_str)
                    else:
                        year, month = map(int, date_str)
                     
                    
                    date_obj = datetime.datetime(year, month, day)
                    timestamp = date_obj.timestamp()
                    
                    
                    # Se o timestamp for maior ou igual ao limite, adiciona a sequência
                    if timestamp >= data:
                        totalS += 1
                        
                        multiple_genomes.append((sequence_id, sequence))
                
                   
                except ValueError as e:
                    print(f"Erro ao processar a data para o identificador {sequence_id}: {e}")
                    logfile = destine.replace(".fasta","ERROS.txt")
                    
                    with open(logfile, "a") as log:
                        log.write(f"{sequence_id}\n{e}\n")
                        
                
        return multiple_genomes, totalS

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        return None
    except IOError as e:
        print(f"Erro de leitura/escrita: {e}")
        return None

    
def writeSeq(outputFile:str, sequences:list):
    try:
        
        with open(outputFile, "a")as file:
            fileHeaders = outputFile.replace(".fasta","Headers.fasta")

            with open(fileHeaders, 'a') as headers:
                for sequence in sequences:
                    
                    file.write(f">{sequence[0]}\n{sequence[1]}\n")
                    headers.write(f">{sequence[0]}\n")
    except IOError as e:
        print(f"error:{e}")
        return None


data = ""
rootDirectory = ""
destine = ""



if len(sys.argv) < 2:
    print("Informe o diretório em que se encontram as sequências")
    print('1 - diretório de entrada (obrigatório)\n2 - arquivo de saída (opcional)\n3 - data de filtragem (padrão:2019-11)')
    raise ValueError("Erro: Parâmetros insuficientes")
    exit(1)
else:
    rootDirectory = sys.argv[1]


if len(sys.argv) < 3:
    here = os.path.abspath(os.path.dirname(__file__))
    destine = os.path.join( here, "spike_filtrado_data")
    os.makedirs(destine, exist_ok=True)
    destine = os.path.join(destine, "spikeFrom11_19ToNow.fasta") 
else:
    destine = sys.argv[2]

if len(sys.argv) < 4:
    data = '2019-11'
else:
    data = sys.argv[3]
    padrao = re.compile(r'\d{4}-\d{2}')  
    
    
    if not data:  # Verifica se a string corresponde exatamente ao padrão
        raise ValueError(f"Data inserida no formato incorreto\nData digitada: {data}\nFormato sugerido: YYYY-MM")
    


padrao = re.compile(r'\d{4}-\d{2}') 
data = padrao.search(data)
data = data.group(0)  # Extrai a string da data

# Converte para datetime
year, month = map(int, data.split('-'))
day = 1
date_obj = datetime.datetime(year, month, day)


timestamp = date_obj.timestamp()



print("Iniciando Processo!")
totalSequenciasFiltradas = 0



for root, foulders, files in os.walk(rootDirectory):
   
    for file in files:
       
        genome_file_path = os.path.join(root, file)
        # imprime apenas os headers
        fileHeaders = os.path.join(root, ("headers.fasta"))
        if genome_file_path.endswith(f'.fasta'):

            
            
            sequencias, totalS = getSeq(genome_file_path, timestamp, totalSequenciasFiltradas)

            totalSequenciasFiltradas = totalS
           
            print(f"Sequências filtradas até aqui:{totalSequenciasFiltradas}")
            print(f"Gravando em {destine}")
            writeSeq(destine, sequencias)
            

print("Processo Conclúido!")
print(f"Número de Sequências filtradas:{totalSequenciasFiltradas}")
print(f"Sequências filtradas salvas em:{destine}")


