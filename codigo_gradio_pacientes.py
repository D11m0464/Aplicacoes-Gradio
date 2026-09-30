import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"

COLUNAS = [
    "timestamp",
    "nome",
    "idade",
    "convenio",
    "prioridade",
    "motivo"
]


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):

    # Validações
    if not nome or not nome.strip():
        return "Informe o nome do paciente.", pd.DataFrame(columns=COLUNAS)

    if idade is None:
        return "Informe a idade do paciente.", pd.DataFrame(columns=COLUNAS)

    if not convenio:
        return "Selecione o convênio.", pd.DataFrame(columns=COLUNAS)

    # Cria a nova linha
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo.strip() if motivo else ""
    }

    novo = pd.DataFrame([linha])

    # Grava no CSV
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(
            ARQUIVO_CSV,
            mode="a",
            header=False,
            index=False
        )
    else:
        novo.to_csv(
            ARQUIVO_CSV,
            mode="w",
            header=True,
            index=False
        )

    # Lê os últimos 5 pacientes
    dados = pd.read_csv(ARQUIVO_CSV)
    ultimos = dados.tail(5)

    return "Paciente cadastrado com sucesso!", ultimos


with gr.Blocks() as demo:

    gr.Markdown("# Cadastro de Pacientes")
    gr.Markdown("Preencha os dados do paciente abaixo.")

    nome = gr.Textbox(
        label="Nome do paciente",
        placeholder="Digite o nome completo"
    )

    idade = gr.Number(
        label="Idade",
        minimum=0,
        maximum=120,
        precision=0
    )

    convenio = gr.Dropdown(
        choices=[
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ],
        label="Convênio",
        value="Particular"
    )

    prioridade = gr.Slider(
        minimum=1,
        maximum=5,
        value=1,
        step=1,
        label="Prioridade do atendimento",
        info="1 = normal | 5 = urgente"
    )

    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        placeholder="Digite o motivo da consulta ou outras observações",
        lines=4
    )

    botao = gr.Button("Cadastrar")

    saida_msg = gr.Textbox(
        label="Status",
        interactive=False
    )

    tabela = gr.Dataframe(
        headers=COLUNAS,
        label="Últimos pacientes cadastrados",
        interactive=False
    )

    botao.click(
        fn=cadastrar_paciente,
        inputs=[
            nome,
            idade,
            convenio,
            prioridade,
            motivo
        ],
        outputs=[
            saida_msg,
            tabela
        ]
    )


demo.launch()
