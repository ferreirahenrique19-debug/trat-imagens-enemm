"""
Propósito: remover as bordas laterais das paginas
Autor: Alexandre Nassar de Peder
Criacao: 02/10/2025
Atualizacao: 03/06/2026
"""

from PIL import Image
import os

pasta_imagens = "imagens-convertidas"
pasta_saida = "sem-bordas-externas"
CORTE_LATERAL = 360

os.makedirs(pasta_saida, exist_ok=True)

if not os.path.exists(pasta_imagens):
    print("ERRO: A pasta 'imagens-convertidas' nao existe!")
    print("Certifique-se de puxar a pasta 'imagens-convertidas' do passo 1 para esta pasta.")
    exit()

print("Processando imagens...")
print("Cortando 360px da ESQUERDA e 360px da DIREITA")
print("")

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(".png"):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        
        try:
            imagem = Image.open(caminho_entrada)
            largura, altura = imagem.size
            
            if largura <= (CORTE_LATERAL * 2):
                print("Imagem " + nome_arquivo + " ignorada - largura muito pequena")
                continue
            
            caixa_corte = (CORTE_LATERAL, 0, largura - CORTE_LATERAL, altura)
            imagem_cortada = imagem.crop(caixa_corte)
            
            caminho_saida = os.path.join(pasta_saida, nome_arquivo)
            imagem_cortada.save(caminho_saida)
            
            print(nome_arquivo + " processado")
            
        except Exception as e:
            print("ERRO ao processar " + nome_arquivo + ": " + str(e))

print("")
print("Recorte das laterais concluido!")