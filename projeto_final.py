
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Função para conectar ao banco
def conectar():
    return sqlite3.connect('banco2.db')

# Função para criar tabela
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            nome TEXT NOT NULL,
            cliente TEXT NOT NULL,
            tarefa TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fim TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para calcular tempo gasto em horas
def calcular_tempo(inicio, fim):
    try:
        formato = "%d/%m/%Y %H:%M"  # Formato esperado: dd/mm/yyyy HH:MM
        dt_inicio = datetime.strptime(inicio, formato)
        dt_fim = datetime.strptime(fim, formato)
        diferenca = dt_fim - dt_inicio
        horas = diferenca.total_seconds() / 3600  # Converter para horas
        return round(horas, 2)
    except ValueError:
        return None

# Inserir registro no banco
def inserir_registro():
    nome = nome_entry.get()
    cliente = cliente_entry.get()
    tarefa = tarefa_entry.get()
    inicio = inicio_entry.get()
    fim = fim_entry.get()

    horas = calcular_tempo(inicio, fim)

    if nome and cliente and tarefa and inicio and fim and horas is not None:
        conn = conectar()
        c = conn.cursor()
        c.execute("INSERT INTO registros VALUES(?,?,?,?,?)", (nome, cliente, tarefa, inicio, fim))
        conn.commit()
        conn.close()
        messagebox.showinfo('', f'DADOS INSERIDOS COM SUCESSO!\nTempo gasto: {horas} horas')
        mostrar_registro()
    else:
        messagebox.showwarning('', 'Preencha todos os campos corretamente (Formato: dd/mm/yyyy HH:MM)')

# Mostrar registros na Treeview
def mostrar_registro():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM registros')
    registro = c.fetchall()
    for us in registro:
        horas = calcular_tempo(us[3], us[4])
        horas_texto = f"{horas} h" if horas is not None else "Erro"
        tree.insert("", "end", values=(us[0], us[1], us[2], us[3], us[4], horas_texto))
    conn.close()

# Atualizar registro
def atualizar():
    selecao = tree.selection()
    if selecao:
        dado_edit = tree.item(selecao)['values'][0]
        novo_nome = nome_entry.get()
        novo_cliente = cliente_entry.get()
        novo_tarefa = tarefa_entry.get()
        novo_inicio = inicio_entry.get()
        novo_fim = fim_entry.get()

        if novo_nome and novo_cliente and novo_tarefa and novo_inicio and novo_fim:
            conn = conectar()
            c = conn.cursor()
            c.execute("UPDATE registros SET nome=?, cliente=?, tarefa=?, inicio=?, fim=? WHERE nome=?", 
                      (novo_nome, novo_cliente, novo_tarefa, novo_inicio, novo_fim, dado_edit))
            conn.commit()
            conn.close()
            messagebox.showinfo('', 'DADOS ATUALIZADOS COM SUCESSO!')
            mostrar_registro()
        else:
            messagebox.showwarning('', 'Todos os campos precisam ser preenchidos')
    else:
        messagebox.showerror('', 'Selecione um registro para atualizar')

# Deletar registro
def delete_registro():
    selecao = tree.selection()
    if selecao:
        reg_del = tree.item(selecao)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM registros WHERE nome=?", (reg_del,))
        conn.commit()
        conn.close()
        messagebox.showinfo('', 'DADO DELETADO COM SUCESSO')
        mostrar_registro()
    else:
        messagebox.showerror('', 'Selecione um registro para deletar')

# Interface gráfica
janela = tk.Tk()
janela.title('Controle de Processos - Escritório')
janela.geometry('900x650')

tk.Label(janela, text='REGISTROS DE PROCESSOS', font=('Arial', 16)).grid(row=0, column=0, pady=10, padx=10)

fr0 = tk.Frame(janela)
fr0.grid()

# Campos de entrada
tk.Label(fr0, text='NOME', font=('Arial', 14)).grid(row=1, column=0, pady=10, padx=10)
nome_entry = tk.Entry(fr0, font=('Arial', 14))
nome_entry.grid(row=1, column=1)

tk.Label(fr0, text='CLIENTE', font=('Arial', 14)).grid(row=2, column=0, pady=10, padx=10)
cliente_entry = tk.Entry(fr0, font=('Arial', 14))
cliente_entry.grid(row=2, column=1)

tk.Label(fr0, text='TAREFA', font=('Arial', 14)).grid(row=3, column=0, pady=10, padx=10)
tarefa_entry = tk.Entry(fr0, font=('Arial', 14))
tarefa_entry.grid(row=3, column=1)

tk.Label(fr0, text='INÍCIO (dd/mm/yyyy HH:MM)', font=('Arial', 14)).grid(row=4, column=0, pady=10, padx=10)
inicio_entry = tk.Entry(fr0, font=('Arial', 14))
inicio_entry.grid(row=4, column=1)

tk.Label(fr0, text='FIM (dd/mm/yyyy HH:MM)', font=('Arial', 14)).grid(row=5, column=0, pady=10, padx=10)
fim_entry = tk.Entry(fr0, font=('Arial', 14))
fim_entry.grid(row=5, column=1)

# Botões
fr = tk.Frame(janela)
fr.grid(pady=10)

tk.Button(fr, text='SALVAR', font=('Arial', 14), command=inserir_registro).grid(row=0, column=0, padx=10)
tk.Button(fr, text='ATUALIZAR', font=('Arial', 14), command=atualizar).grid(row=0, column=1, padx=10)
tk.Button(fr, text='DELETAR', font=('Arial', 14), command=delete_registro).grid(row=0, column=2, padx=10)

# Treeview para mostrar registros
fr2 = tk.Frame(janela)
fr2.grid()

colunas = ('NOME', 'CLIENTE', 'TAREFA', 'INÍCIO', 'FIM', 'TEMPO (h)')
tree = ttk.Treeview(fr2, columns=colunas, show='headings', height=20)
tree.grid(row=6, column=0, padx=10, sticky='nsew')

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=140)

# Inicializar banco e mostrar dados
criar_tabela()
mostrar_registro()

janela.mainloop()
