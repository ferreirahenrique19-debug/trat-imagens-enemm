

from PIL import Image
import os


pasta_imagens = "sem-bordas-externas"        
nome_arquivo_cima = "pagina_enem_76.png" 
nome_arquivo_baixo = "pagina_enem_77.png"   
pasta_saida = "paginas-montadas2"             
nome_arquivo_final = "pagina_enem_76.png"          


os.makedirs(pasta_saida, exist_ok=True)

if not os.path.exists(pasta_imagens):
    print(f"ERRO: A pasta '{pasta_imagens}' não existe!")
    exit()

caminho_cima = os.path.join(pasta_imagens, nome_arquivo_cima)
caminho_baixo = os.path.join(pasta_imagens, nome_arquivo_baixo)

if not os.path.exists(caminho_cima):
    print(f"ERRO: O arquivo '{nome_arquivo_cima}' não foi encontrado!")
    exit()

if not os.path.exists(caminho_baixo):
    print(f"ERRO: O arquivo '{nome_arquivo_baixo}' não foi encontrado!")
    exit()

try:
    img_cima = Image.open(caminho_cima)
    img_baixo = Image.open(caminho_baixo)
    
    # Verificar se as larguras são iguais. Se não forem, redimensionar para a menor.
    largura_min = min(img_cima.width, img_baixo.width)
    
    if img_cima.width != largura_min:
        proporcao = largura_min / img_cima.width
        nova_altura = int(img_cima.height * proporcao)
        img_cima = img_cima.resize((largura_min, nova_altura), Image.Resampling.LANCZOS)
        
    if img_baixo.width != largura_min:
        proporcao = largura_min / img_baixo.width
        nova_altura = int(img_baixo.height * proporcao)
        img_baixo = img_baixo.resize((largura_min, nova_altura), Image.Resampling.LANCZOS)
    
    # Criar la nova imagem (branca de fundo)
    altura_total = img_cima.height + img_baixo.height
    imagem_final = Image.new('RGB', (largura_min, altura_total), (255, 255, 255))
    
    # Colar em cima e embaixo
    imagem_final.paste(img_cima, (0, 0))
    imagem_final.paste(img_baixo, (0, img_cima.height))
    
    caminho_final = os.path.join(pasta_saida, nome_arquivo_final)
    imagem_final.save(caminho_final)
    
    print(f"SUCESSO! Imagem salva em: {caminho_final}")
    
except Exception as e:
    print(f"ERRO ao processar as imagens: {str(e)}")