import openai
from indentifica_audio import transcreva_audio

with open('key.txt', 'r') as file:
    openai.api_key = file.read().strip()


def generate_task_list(transcribed_text):
    # Define the prompt with the context you provided
    prompt = (
        f"{transcribed_text}\n\n"
        "Crie uma lista de Tarefas a serem feitas. Foque apenas em informações que sejam relevantes a um trabalhador de chão de fábrica. Escreva apenas as tarefas."
    )

    # Call the ChatGPT API to generate the task list
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente especializado em gerar listas de tarefas de manutenção."},
                  {"role": "user", "content": prompt}]
    )

    # Extract and return the generated task list
    task_list = response['choices'][0]['message']['content']
    task_list_splited = task_list.split("\n")
    return task_list_splited

def generate_tool_list(task_list):
    # Define the prompt to generate a list of tools based on the task list
    prompt = (
        f"{task_list}\n\n"
        "Com base nas tarefas listadas, crie apenas uma lista de todas as possíveis ferramentas que podem ser utilizadas (inclusive todos EPIs)\nA saída deve ser apenas a lista dos nomes idividuais e específicos das ferramentas, com um - antes de cada nome, e inserindo uma quebra de linha entre cada item. Não é necessário incluir nada relacionado à ficha técnica, apenas o nome individual do componente."
    )

    # Call the ChatGPT API to generate the tool lists
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente especializado em manutenção industrial."},
                  {"role": "user", "content": prompt}]
    )

    # Extract and return the generated tool list
    tool_list = response['choices'][0]['message']['content']
    tool_list_splited = tool_list.split("\n")
    return tool_list_splited

if __name__ == "__main__":
    transcribed_audio = "Bom dia é hoje Valdo tudo certo passando para tia Liana e as coisas que ficaram pendente aí para gente fazer no domingo o cara alguns serviços que acabaram que a gente não conseguiu tocar durante a semana mas deixa eu te explicar aqui pelo para vocês algumas coisas aqui na que a gente tem que resolver logo Tá bom então conhecendo pela pela linha três eu preciso que faça a lubrificação dos Rolamentos ali essa máquina ali ela já tá dando sinais de desgaste já tem um certo tempo o pessoal reportou já barulho estranho já nesse nesse equipamento Então tem que botar o lubrificante correto ele já tá no estoque aquele código lá o azul 6624 Então já toma cuidado com isso já faz a essa lubrificação com essa máquina aí e não pode esquecer de conferir a ficha técnica dele para colocar a quantidade certa tá da outra vez deu problema então depois disso eu preciso também que vocês dê uma uma verificada no nível de óleo lá da desencapadora lá da linha 12 é um equipamento que ele do nada dar uns picos de temperatura lá o pessoal já já reportou já mandou pra gerência foi uma merda isso então revisar mesmo as medições ver se tá tudo certo lá com o nível de óleo dela porque se sair do óleo recomendado começar a esquentar e corre risco de parar e vai dar vai dar b.o. e também queria só dar uma olhada lá no compressor cinco aquele lá bem da central né o filtro de ar já passou do ponto ele estava para ser trocado na última parada mas ele acabou ficando para agora então tá bem crítico então Ah tem que fazer a substituição agora agora no domingo já não dá para esperar o filtro de novo já fechei Mandei o menino trazer lá do do almoxarifado tá debaixo da bancada só vocês pegarem e trocar também tá E aproveita que você tá no compressor Aproveita e dá um pulinho lá naquela bomba da da bomba de circulação aquela lá do canto lá do canto direito ela também estava o pessoal falou que ela tá fazendo um barulho Aproveita e dá uma olhadinha lá para mim tá é basicamente isso qualquer coisa aí você não me avisa tá porque eu tô de folga segundo momento resolve valeu"
    
    # Generate task list
    task_list = generate_task_list(transcribed_audio)
    print(task_list)
    
    # Generate tool list based on the task list
    tool_list = generate_tool_list(task_list)
    print("\n")
    print(tool_list)
