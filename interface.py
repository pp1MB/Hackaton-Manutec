import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from indentifica_audio import transcreva_audio
from lista_tarefas import generate_task_list
from lista_tarefas import generate_tool_list
from encontra_ferramentas import buscar_codigo_sap

class MaintenanceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente de Manutenção")
        self.root.geometry("360x640")

        # Inicializa a lista de resultados
        self.results = []

        # Caminho para o diretório atual do script
        self.base_dir = os.path.dirname(__file__)

        # Carregar a imagem de fundo
        background_path = os.path.join(self.base_dir, "background_image.png")
        self.background_image = Image.open(background_path).resize((360, 640), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Frame para imagem de fundo
        self.bg_frame = tk.Frame(root, width=360, height=640)
        self.bg_frame.pack(fill="both", expand=True)
        label_bg = tk.Label(self.bg_frame, image=self.bg_image)
        label_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame para o conteúdo principal
        self.content_frame = tk.Frame(self.bg_frame)
        self.content_frame.pack(fill="both", expand=True)

        # Carregar imagens para os botões
        self.load_images()

        # Inicializa as abas
        self.audio_tab = self.create_audio_tab()
        self.checklist_tab = self.create_checklist_tab()
        self.tools_tab = self.create_tools_tab()

        # Adiciona os frames de abas ao frame de conteúdo
        self.audio_tab.pack(fill="both", expand=True)
        self.checklist_tab.pack(fill="both", expand=True)
        self.tools_tab.pack(fill="both", expand=True)

        # Botões na parte inferior para alternar entre as seções
        button_frame = tk.Frame(self.bg_frame)
        button_frame.pack(side="bottom", fill="x")

        self.audio_button = tk.Button(button_frame, image=self.audio_image, command=lambda: self.show_tab(self.audio_tab, "audio"), borderwidth=0)
        self.audio_button.pack(side="left", expand=True)

        self.checklist_button = tk.Button(button_frame, image=self.checklist_image, command=lambda: self.show_tab(self.checklist_tab, "checklist"), borderwidth=0)
        self.checklist_button.pack(side="left", expand=True)

        self.tools_button = tk.Button(button_frame, image=self.tools_image, command=lambda: self.show_tab(self.tools_tab, "tools"), borderwidth=0)
        self.tools_button.pack(side="left", expand=True)

        # Exibe a aba de áudio por padrão
        self.show_tab(self.audio_tab, "audio")


    def load_images(self):
        # Função para carregar imagens
        self.audio_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "audio_icon.png")).resize((120, 32)))
        self.audio_selected_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "audio_icon_selected.png")).resize((120, 36)))

        self.checklist_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "checklist_icon.png")).resize((120, 32)))
        self.checklist_selected_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "checklist_icon_selected.png")).resize((120, 36)))

        self.tools_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "tools_icon.png")).resize((120, 32)))
        self.tools_selected_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "tools_icon_selected.png")).resize((120, 36)))

        self.load_text_image = ImageTk.PhotoImage(Image.open("load_text_icon.png").resize((120, 32)))  # Ícone para carregar texto
        self.load_audio_image = ImageTk.PhotoImage(Image.open("load_audio_icon.png").resize((120, 32)))  # Ícone para carregar áudio
        self.load_busca_image = ImageTk.PhotoImage(Image.open("busca_icon.png").resize((20,20)))

    def create_audio_tab(self):
        tab = tk.Frame(self.content_frame)

        # Adiciona o label de imagem de fundo
        background_label = tk.Label(tab, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche o frame inteiro

        # Adiciona o label de boas-vindas
        welcome_label = tk.Label(tab, text="Bem-vindo\n colaborador!", font=("League Spartan", 28, "bold"), bg="#F1F2FF")
        welcome_label.pack(pady=(10, 5))  # Espaçamento acima e abaixo do texto
        welcome2_label = tk.Label(tab, text="Quais tarefas você fará hoje?", font=("League Spartan", 15, "bold"), bg="#F1F2FF")
        welcome2_label.pack(pady=(10, 5))

        # Caixa de texto para o usuário escrever um texto
        self.user_input_text = tk.Text(tab, wrap="word", height=5, bg="#004AAD", fg="#F1F2FF", font=("League Spartan", 12))
        self.user_input_text.pack(fill="both", padx=10, pady=5)
        self.user_input_text.insert("end", "Escreva seu texto aqui...")

        # Frame para os botões
        button_frame = tk.Frame(tab, bg="#F1F2FF")
        button_frame.pack(padx=10, pady=5,)

        # Botões lado a lado
        tk.Button(button_frame, image=self.load_text_image, command=self.load_text, compound="left", bg="#F1F2FF", font=("League Spartan", 10)).pack(side="left", padx=5)  # Empilhado à esquerda
        tk.Button(button_frame, image=self.load_audio_image, command=self.load_audio, compound="left",  bg="#F1F2FF", font=("League Spartan", 10)).pack(side="left", padx=5)  # Empilhado à esquerda

        # Caixa de texto para transcrição de áudio
        self.transcription_text = tk.Text(tab, wrap="word", height=10, bg="#004AAD", fg="white", font=("League Spartan", 12))
        self.transcription_text.pack(fill="both", padx=10, pady=5)
        self.transcription_text.insert("end", "Instruções da tarefa aparecerão aqui...")

        return tab

    def create_checklist_tab(self):
        tab = tk.Frame(self.content_frame)

        # Adiciona o label de imagem de fundo
        background_label = tk.Label(tab, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche o frame inteiro

        # Adiciona o label de boas-vindas
        welcome_label = tk.Label(tab, text="Bem-vindo\n colaborador!", font=("League Spartan", 28, "bold"), bg="#F1F2FF")
        welcome_label.pack(pady=(10, 5))  # Espaçamento acima e abaixo do texto
        welcome2_label = tk.Label(tab, text="Veja a sua checklist de hoje:", font=("League Spartan", 15, "bold"), bg="#F1F2FF")
        welcome2_label.pack(pady=(10, 5))

        # Frame para conter os Checkbuttons com o mesmo fundo que o restante
        self.checklist_frame = tk.Frame(tab, bg="#F1F2FF", padx=10, pady=10)  # Frame com padding
        self.checklist_frame.pack(fill="both", expand=True)

        background_label = tk.Label(self.checklist_frame, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche o frame inteiro

        self.checklist_items = []  # Exemplo inicial
        self.checklist_vars = []

        for item in self.checklist_items:
            self.add_checkbox(item, self.checklist_frame)  # Usa o método add_checkbox para criar as tarefas iniciais

        return tab

    def add_checkbox(self, item_text, frame=None):
        if frame is None:
            frame = self.checklist_frame

        # Cria a variável de controle e o checkbox
        var = tk.BooleanVar()
        chk = tk.Checkbutton(
            frame,
            text=item_text,
            variable=var,
            font=("League Spartan", 18),
            bg="#F1F2FF",  # Fundo igual ao do frame
            wraplength=300  # Limite de largura para quebra de linha
        )
        chk.pack(anchor="w", padx=5, pady=5)  # Padding para espaçamento

        # Adiciona a variável à lista de controle de variáveis
        self.checklist_vars.append(var)


    def create_tools_tab(self):
        tab = tk.Frame(self.content_frame)

        # Adiciona o label de imagem de fundo
        background_label = tk.Label(tab, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche o frame inteiro

        # Adiciona o label de boas-vindas
        welcome_label = tk.Label(tab, text="Bem-vindo\n colaborador!", font=("League Spartan", 28, "bold"), bg="#F1F2FF")
        welcome_label.pack(pady=(10, 5))  # Espaçamento acima e abaixo do texto
        welcome2_label = tk.Label(tab, text="De quais ferramentas você precisa?", font=("League Spartan", 15, "bold"), bg="#F1F2FF")
        welcome2_label.pack(pady=(10, 5))

        # Frame para a barra de pesquisa e o botão
        search_frame = tk.Frame(tab, bg="#F1F2FF")
        search_frame.pack(padx=10, pady=5)

        # Barra de pesquisa
        self.search_entry = tk.Entry(search_frame, font=("League Spartan", 18), bg="#004AAD", fg="white")
        self.search_entry.pack(side="left", fill="x", expand=True)  # Preenchendo à esquerda

        # Botão de busca ao lado da barra de pesquisa
        search_button = tk.Button(search_frame, image=self.load_busca_image, command=self.search_new_tool, width=20, height=20)
        search_button.pack(side="right", padx=5)  # Posicionando à direita

        self.search_results = tk.Listbox(tab, font=("League Spartan", 18), bg="#004AAD", fg="white", width=350)
        self.search_results.pack(fill="both", expand=True, padx=10, pady=10)

        return tab

    def set_label(self, parent, text):
        return tk.Label(parent, text=text, font=("League Spartan", 12, "bold"))

    def show_tab(self, tab, button):
        # Oculta todas as abas e exibe a aba selecionada
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        tab.pack(fill="both", expand=True)
        
        # Atualiza as imagens dos botões
        self.update_button_state(button)

    def update_button_state(self, selected_button):
        if selected_button == "audio":
            self.audio_button.config(image=self.audio_selected_image)
            self.checklist_button.config(image=self.checklist_image)
            self.tools_button.config(image=self.tools_image)
        elif selected_button == "checklist":
            self.audio_button.config(image=self.audio_image)
            self.checklist_button.config(image=self.checklist_selected_image)
            self.tools_button.config(image=self.tools_image)
        elif selected_button == "tools":
            self.audio_button.config(image=self.audio_image)
            self.checklist_button.config(image=self.checklist_image)
            self.tools_button.config(image=self.tools_selected_image)

    def load_audio(self):
        audio_file = filedialog.askopenfilename(
            title="Selecione um arquivo de áudio",
            filetypes=[("Arquivo de áudio OGG", "*.ogg")]
        )
        
        if audio_file:
            wav_file = "converted.wav"
            transcribed_text = transcreva_audio(audio_file, wav_file)
            print("Texto Transcrito:", transcribed_text)
            #transcription = "Instruções para a tarefa transcritas a partir do áudio."
            self.transcription_text.delete("1.0", "end")
            self.transcription_text.insert("end", transcribed_text)
            messagebox.showinfo("Audio carregado", "Tasks Geradas. Observe a aba tasks")
            tasklist = generate_task_list(transcribed_text)
            for item in tasklist:
                print(item)
                app.add_checkbox(item)
            
            tool_list = generate_tool_list(tasklist)
            for tool in tool_list:
                codigo_sap = buscar_codigo_sap(tool)
                if codigo_sap != "Ferramenta não encontrada na planilha.":
                    app.add_to_results(codigo_sap)   

            self.search_tools()

                       
    def load_text(self):
        transcribed_text = self.user_input_text.get("1.0", "end").strip()
        
        messagebox.showinfo("Tasks Geradas", "Observe a aba tasks")
        tasklist = generate_task_list(transcribed_text)
        for item in tasklist:
            print(item)
            app.add_checkbox(item)
        
        tool_list = generate_tool_list(tasklist)
        for tool in tool_list:
            codigo_sap = buscar_codigo_sap(tool)
            if codigo_sap != "Ferramenta não encontrada na planilha.":
                app.add_to_results(codigo_sap)
        self.search_tools()

    def add_to_results(self, item_text):
        # Adiciona um novo item à lista de resultados
        self.results.append(item_text)

    def search_tools(self):
        query = self.search_entry.get()
        self.search_results.delete(0, "end")

        # Popula a listbox com os itens de results
        for item in self.results:
            self.search_results.insert("end", item)
        
        #messagebox.showinfo("Busca Concluída", f"Resultados para '{query}' exibidos.")
        
    def search_new_tool(self):
        query = self.search_entry.get()
        codigo_sap = buscar_codigo_sap(query)
        if(codigo_sap not in self.results):
            self.add_to_results(codigo_sap)
            self.search_tools()
        
        
        

# Inicialização da aplicação
root = tk.Tk()
app = MaintenanceAssistantApp(root)
root.mainloop()
