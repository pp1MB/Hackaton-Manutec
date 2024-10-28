import openai
import pandas as pd

with open('key.txt', 'r') as file:
    openai.api_key = file.read().strip()

# Carregar a planilha do Excel
df = pd.read_excel("CodigosSAP2.xlsx")  # Altere para o caminho da sua planilha

def identificar_categoria(descricao_ferramenta):
    # Perguntar ao GPT qual é a categoria da ferramenta com base na descrição
    prompt = f"Baseado na seguinte descrição, qual é a categoria da ferramenta? Dê como resposta apenas o nome da categoria, sem pontuação, escolhendo uma que esteja entre as opções dadas.\n\nDescrição: '{descricao_ferramenta}'\n\nAs opções de categorias são: 'Ferramentas de Corte', 'Ferramentas de Medição', 'Equipamentos de Solda', 'Lubrificação e Manutenção', 'Equipamentos de Segurança', 'Equipamentos de Elevação', 'Componentes Mecânicos', 'Equipamentos Hidráulicos', 'Equipamentos Elétricos', 'Ferramentas Manuais'."
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.3
    )
    categoria = resposta['choices'][0]['message']['content'].strip()
    #print(f"Categoria identificada: {categoria}")
    return categoria

def buscar_ferramenta_por_categoria_e_descricao(descricao_ferramenta, categoria):
    # Filtrar a planilha pela categoria identificada
    ferramentas_filtradas = df[df["Categoria"].str.contains(categoria, case=False, na=False)]

    # Listar as descrições filtradas para o GPT escolher a melhor opção
    lista_ferramentas = "\n".join(ferramentas_filtradas["Descrição do Material/Equipamento"].tolist())
    prompt = f"Abaixo estão as opções de ferramentas da categoria '{categoria}'. Com base na descrição '{descricao_ferramenta}', qual das opções é a mais apropriada? Escolha apenas uma e digite apenas o nome dala.\n\nOpções:\n{lista_ferramentas}"
    
    #print(lista_ferramentas)
    
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.3
    )
    
    nome_ferramenta = resposta['choices'][0]['message']['content'].strip()
    #print(f"Ferramenta selecionada: {nome_ferramenta}")
    
    # Obter o código SAP para a ferramenta selecionada
    ferramenta_encontrada = ferramentas_filtradas[ferramentas_filtradas["Descrição do Material/Equipamento"].str.contains(nome_ferramenta, case=False, na=False)]
    
    if not ferramenta_encontrada.empty:
        codigo_sap = ferramenta_encontrada.iloc[0]["Código SAP"]
        return (f"{nome_ferramenta}: {codigo_sap}")
    else:
        return "Ferramenta não encontrada na planilha."

# Função principal que integra os passos
def buscar_codigo_sap(descricao_ferramenta):
    # Identificar a categoria primeiro
    categoria = identificar_categoria(descricao_ferramenta)
    
    # Buscar a ferramenta exata com base na categoria e na descrição
    codigo_sap = buscar_ferramenta_por_categoria_e_descricao(descricao_ferramenta, categoria)
    return codigo_sap

# Exemplo de uso
if __name__ == "__main__":
    descricao = "Equipamento para cortar com precisão em trabalhos de marcenaria"
    codigo_sap = buscar_codigo_sap(descricao)
    print(f"Código SAP: {codigo_sap}")