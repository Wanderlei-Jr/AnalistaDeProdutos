from flask import render_template, request, redirect, url_for, flash
import pandas as pd
import os
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisar', methods=['GET', 'POST'])
def analisar():
    if request.method == 'POST':
        marca = request.form.get('marca')
        codigo = request.form.get('codigo')
        dias = request.form.get('dias')

        if not marca and not codigo:
            flash("Você deve preencher pelo menos um dos campos: Marca ou Código.")
            return redirect(url_for('analisar'))

        try:
            dias = int(dias)
            if dias <= 0 or dias > 180:
                raise ValueError
        except ValueError:
            flash("Dias para Abastecimento do Estoque deve ser um número entre 1 e 180.")
            return redirect(url_for('analisar'))

        try:
            diretorio = 'caminho/para/seu/diretorio'  # Defina o caminho para o diretório das planilhas
            arquivo_vendas_90_dias = os.path.join(diretorio, 'Vendas_90_dias_atualizado.xlsx')
            vendas_90_dias = pd.read_excel(arquivo_vendas_90_dias)

            if marca:
                vendas_90_dias = vendas_90_dias[vendas_90_dias['Marca'] == marca]
            if codigo:
                vendas_90_dias = vendas_90_dias[vendas_90_dias['Produto'] == int(codigo)]

            if vendas_90_dias.empty:
                flash("Nenhum produto encontrado com os critérios fornecidos.")
                return redirect(url_for('analisar'))

            vendas_90_dias['Qtd. Necessária'] = vendas_90_dias['demanda_diaria_90_dias'] * dias - vendas_90_dias['Estoque']

            resultados = vendas_90_dias[['Produto', 'Descrição', 'Marca', 'Qtd. Necessária']].to_dict(orient='records')
            return render_template('resultado.html', resultados=resultados)

        except Exception as e:
            flash(f"Erro ao processar a análise de compras: {e}")
            return redirect(url_for('analisar'))

    return render_template('analisar.html')
