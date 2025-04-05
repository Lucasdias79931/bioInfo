
"""
Usei para verificar se o produto final de uma filtragem estava com sequências faltando


"""



from Bio import SeqIO

import os
import sys
import hashlib




def transforInHash(sequence: str) -> str:
    
    return hashlib.sha512(sequence.encode()).hexdigest()

def get_all_genome(sequence_path:str)->dict:
    try:
        all_genome = dict()

        with open(sequence_path, 'r') as handle:
            for sequence_id, sequence in SeqIO.FastaIO.SimpleFastaParser(handle):
                all_genome[sequence_id] = transforInHash(sequence)

            return all_genome    
    except IOError as e:
        print(e)
    except FileNotFoundError as error:
        print(error)
    except Exception as error:
        print(error)
def args_from_user_invalided():
    print("Argumentos faltando!")
    print("1 - arquivo de referência! [obrigatório]")
    print("2 - arquivo de comparação! [obrigatório]")
    print("3 - arquivo para relatório [padrão: diretório atual/relatório.txt]")
    exit(1)

def verify_file(filePath:str)->None:
    
    if not os.path.exists(filePath):
        print(f"Arquivo [{filePath}] não encontrado!")
        exit(1)

if len(sys.argv) < 3:
    args_from_user_invalided()
    


output_File_path = None
file_ref_path = sys.argv[1]
file_to_compare_path = sys.argv[2]
output_file = None
file_ref = None
file_to_compare = None
wrong_sequences_in_the_finalProduct = list()

if len(sys.argv) > 3:
    if not os.path.exists(sys.argv[4]):
        exit(1)
        output_File_path = os.path.abspath(os.path.dirname(__name__))
        os.makedirs(output_File_path, exist_ok=True)
        output_file = os.path.join(output_File_path, "relatorio.txt")
else:
    output_File_path = os.path.join(os.path.abspath(os.path.dirname(__name__)), "outputFile")

    os.makedirs(output_File_path, exist_ok=True)
    output_file = os.path.join(output_File_path, "relatorio.txt")

verify_file(file_ref_path)
verify_file(file_to_compare_path)

print("Inicinando processo...")
print("Colhendo sequências de referências!")

file_ref = get_all_genome(file_ref_path)

print("Colhendo sequências parar comparação!")

file_to_compare = get_all_genome(file_to_compare_path)

print("Iniciando Processo de Comparação")

for sequence_id in file_to_compare.keys():

    if not file_ref.get(sequence_id, False):
        header = sequence_id
        print(f"Sequência [{header}] não encontrada no arquivo [{file_ref_path}]")
        header = None
        wrong_sequences_in_the_finalProduct.append(sequence_id)

try:
    with open(output_file, "w") as file:
        file.write(f"Relatório de comparação entre o arquivo de referência [{file_ref_path}] e o arquivo de comparação [{file_to_compare_path}]\n\n")
        
        print("\n")
        if wrong_sequences_in_the_finalProduct:
            file.write(f"As sequências abaixo não foram encontradas no arquivo de referência:\n")
            for sequence_id in wrong_sequences_in_the_finalProduct:
                file.write(">" + sequence_id + "\n")
        else:
            file.write(f"Todas as sequências no arquivo de comparação [{file_to_compare_path}] estão contidas no arquivo de referência [{file_ref_path}]")
            print(f"Todas as sequências no arquivo de comparação [{file_to_compare_path}] estão contidas no arquivo de referência [{file_ref_path}]")

except IOError as error:
    print(error)

    print("Processo finalizado, mas não foi possivél gravar os resultados!")
    print(f"Número de sequências computadadas erradas no arquivo final {len(file_to_compare)}")