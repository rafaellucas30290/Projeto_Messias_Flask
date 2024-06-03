import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente para modo de desenvolvimento debug
os.environ['FLASK_DEBUG'] = 'True'
app.debug = os.environ.get('FLASK_DEBUG') == 'True'


@app.route('/')
def pagina_home():
    return render_template('index.html')


# Exemplo de rota para a página sobre
@app.route('/sobre')
def pagina_sobre():
    return render_template('sobre.html')


# Exemplo de rota para a página de glossário
@app.route('/cursos')
def cursos():

    lista_de_cursos = []

    with open(
            'bd_cursos.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            lista_de_cursos.append(l)

    return render_template('cursos.html',
                           cursos=lista_de_cursos)


@app.route('/novo_curso')
def novo_curso():
    return render_template('adicionar_curso.html')


@app.route('/adicionar_curso', methods=['POST', ])
def adicionar_curso():
    curso = request.form['curso']
    carga_h = request.form['carga_h']
    descricao = request.form['descricao']

    with open(
            'bd_cursos.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([curso, descricao, carga_h])

    return redirect(url_for('cursos'))


@app.route('/excluir_curso/<int:curso_id>', methods=['POST'])
def excluir_curso(curso_id):

    with open('bd_cursos.csv', 'r', newline='') as arquivo:
        leitor = csv.reader(arquivo)
        linhas = list(leitor)
    
    for i, linha in enumerate(linhas):
        if i == curso_id:
            del linhas[i]
            break

    
    with open('bd_cursos.csv', 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerows(linhas)

    return redirect(url_for('cursos'))



if __name__ == '__main__':
    app.run()