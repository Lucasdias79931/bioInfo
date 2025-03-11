#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main(int argc, char *argv[]) {
    if(argc < 2){
        printf("Arquivo não especificado\n");
        return 1;
    }
    

    FILE *file = fopen(argv[1], "r");
    if(file == NULL){
        perror("ERROR");
        return 1;
    }

    
    int indexFile = 0;
    const int maxLen =  1024 * 1024;
    const int tamanhoFinal = 512;
    char *buffer = malloc(maxLen * sizeof(char));

    if(buffer == NULL){
        perror("ERROR");
        printf("\nErro ao tentar alocar buffer!");
        return 1;
    }

    
    printf("\nIniciando Processamento!");
    printf("\nTamanho final aproximado do cada arquivo no Fim do processo:%i MB\n",tamanhoFinal);
    int cont = 0;
    while(true){
        bool end = false;
       
        
        char pathDestine[200];
        sprintf(pathDestine, "/home/asmita/workspace/bio/SPIKE/spike_ordenadoPorData/sequencias_spike%d.fasta", indexFile);// mude de para onde quer guardar
        
        FILE *fileDestine = fopen(pathDestine, "a");
        if(fileDestine == NULL){
            perror("ERROR");
            printf("Destino não encontrado!");
            return 1;
        }

        for(int i = tamanhoFinal; i > 0; i--){
            
            
            int len = fread(buffer, 1, maxLen, file);
            if (len == 0) {
                end = true; 
                break; 
            }

            if(buffer[0] != '>'){
                fprintf(fileDestine, "%s", ">");
                fprintf(fileDestine, "%s", buffer);
            }else{
                fprintf(fileDestine, "%s", buffer);
            }
            
        

            
            char c;
            while((c = fgetc(file)) != '>' && c != EOF){
                fprintf(fileDestine, "%c", c);
                
            }
            memset(buffer, 0, maxLen);
            
            
            
            if(c == EOF ){
                end = true;
                break;
            }
            
        }

        indexFile++;

        fclose(fileDestine);
        
        cont++;
        if(end)break;

    }

    fclose(file);
    printf("\nQuantidade de arquivos:%i",cont);
    printf("\nFim do Processamento!\n");

    return 0;
}
