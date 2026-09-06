from pathlib import Path
import re


class RenomeadorQuestoes:

    def __init__(self, pasta, pasta_saida, primeira_questao, ultima_questao):
        self.pasta = Path(pasta)
        self.pasta_saida = Path(pasta_saida)
        self.primeira_questao = primeira_questao
        self.ultima_questao = ultima_questao

    def listar_imagens(self):
        if not self.pasta.exists():
            raise FileNotFoundError(
                f"A pasta '{self.pasta}' não foi encontrada."
            )

        # Ordena de forma NUMÉRICA, extraindo o número do nome do arquivo
        imagens = sorted(
            self.pasta.glob("*.png"),
            key=lambda arquivo: int(
                re.search(r'(\d+)', arquivo.stem).group(1)
            )
        )

        return imagens

    def validar_quantidade(self, quantidade):
        esperado = (
            self.ultima_questao
            - self.primeira_questao
            + 1
        )

        print(f"Imagens encontradas : {quantidade}")
        print(f"Imagens esperadas   : {esperado}")

        if quantidade != esperado:
            print("\nAviso:")
            print(
                "A quantidade de imagens não corresponde "
                "à quantidade de questões.\n"
            )

    def renomear(self):
        imagens = self.listar_imagens()

        self.validar_quantidade(len(imagens))

        # Criar pasta de saída
        self.pasta_saida.mkdir(parents=True, exist_ok=True)

        numero = self.primeira_questao

        for imagem in imagens:

            if numero > self.ultima_questao:
                break

            # Copiar (shutil.copy2) para la pasta de saída com o novo nome
            from shutil import copy2

            novo_nome = self.pasta_saida / f"questao-{numero}.png"

            # Se já existe na pasta de saída, apaga para não dar erro
            if novo_nome.exists():
                novo_nome.unlink()

            copy2(imagem, novo_nome)

            print(
                f"{imagem.name}  →  {novo_nome.name}"
            )

            numero += 1

        print("\nRenomeação concluída!")
        print(f"Imagens salvas na pasta: {self.pasta_saida}")

    def executar(self):
        self.renomear()


if __name__ == "__main__":

    renomeador = RenomeadorQuestoes(
        pasta="ImagensDasQuestoes",
        pasta_saida="renomeadas",
        primeira_questao=91,
        ultima_questao=180
    )

    renomeador.executar()