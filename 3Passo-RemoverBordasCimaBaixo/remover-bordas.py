
from PIL import Image
import numpy as np
import os

pasta_imagens = "sem-bordas-externas01"
pasta_saida = "sem-bordas-externas"

os.makedirs(pasta_saida, exist_ok=True)

if not os.path.exists(pasta_imagens):
    print("ERRO: A pasta 'sem-bordas-externas01' nao existe!")
    exit()

print("Processando imagens de: " + pasta_imagens)
print("Salvando em: " + pasta_saida)
print("Cortando excesso de branco no topo e na base (laterais intactas)")
print("")

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(".png"):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        
        try:
            imagem = Image.open(caminho_entrada)
            largura_total, altura_total = imagem.size
            
            
            imagem_cinza = np.array(imagem.convert("L"))
            linhas_com_conteudo = np.where(imagem_cinza.min(axis=1) < 250)[0]
            
            if len(linhas_com_conteudo) == 0:
                print("Imagem " + nome_arquivo + " ignorada - nenhum conteúdo encontrado")
                continue
            
            inicio_conteudo = linhas_com_conteudo.min()
            margem_superior = 10
            inicio_conteudo = max(0, inicio_conteudo - margem_superior)
            
            
            limite_maximo_permitido = int(altura_total * 0.98)
            
            
            linhas_validas = linhas_com_conteudo[linhas_com_conteudo <= limite_maximo_permitido]
            
            if len(linhas_validas) == 0:
                print("Imagem " + nome_arquivo + " ignorada - conteúdo só no rodapé")
                continue
            
            
            linhas_ordenadas = np.sort(linhas_validas)
            ultima_linha_real = linhas_ordenadas[-1]
            
            
            if len(linhas_ordenadas) > 1:
                diferenca_ultima = linhas_ordenadas[-1] - linhas_ordenadas[-2]
                if diferenca_ultima > 70:
                    
                    ultima_linha_real = linhas_ordenadas[-2]
                else:
                    
                    pass
            
            
            margem_inferior = 2
            limite_inferior = min(altura_total, ultima_linha_real + margem_inferior)
            
            
            caixa_corte = (0, inicio_conteudo, largura_total, limite_inferior)
            imagem_cortada = imagem.crop(caixa_corte)
            
            caminho_saida = os.path.join(pasta_saida, nome_arquivo)
            imagem_cortada.save(caminho_saida)
            
            print(nome_arquivo + " processado")
            
        except Exception as e:
            print("ERRO ao processar " + nome_arquivo + ": " + str(e))

print("")
print("Recorte do topo e da base concluido!")