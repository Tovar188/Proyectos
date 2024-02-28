from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)

# Cargar datos desde el archivo Excel
df = pd.read_excel('nombres.xlsx', header=0, names=['Nombres'])

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Validar la contraseña con la expresión regular
    password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
    if re.fullmatch(password_regex, password):
        return redirect(url_for('buscar'))
    else:
        return "Contraseña inválida", 400

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        # Obtener el nombre ingresado en el formulario
        nombre_ingresado = request.form['nombre']

        # Utilizar expresiones regulares para buscar coincidencias en los nombres
        pat = re.compile(f'.*{re.escape(nombre_ingresado)}.*', re.IGNORECASE)
        resultados = df[df['Nombres'].apply(lambda x: bool(pat.match(str(x))))]

        return render_template('resultados.html', resultados=resultados)
    else:
        return render_template('index.html', resultados=None)

if __name__ == '__main__':
    app.run(debug=True)
