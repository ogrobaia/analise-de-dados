import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import io
import base64

# Baixar dados da planilha
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTm3z0B1Aytqb0Ynn3N2PJiq8Qw6YBgqargtVeYUg7oVd8XINau3maEz4Ed3HjTK26hW7aWn-82niBx/pub?output=csv'
df = pd.read_csv(url)

# Flask para a página web
app = Flask(__name__)

# Função para gerar gráficos e converter para base64
def create_plot():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Exemplo de gráfico de ocorrências por tipo de ocorrência
    df['Tipo de Ocorrência'].value_counts().plot(kind='bar', ax=ax)
    plt.title('Ocorrências por Tipo de Ocorrência')
    plt.xlabel('Tipo de Ocorrência')
    plt.ylabel('Frequência')
    
    # Salvar o gráfico como imagem
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

# Rota principal do Flask
@app.route('/')
def index():
    # Gera o gráfico e envia para a página
    graph = create_plot()
    return render_template('index.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
