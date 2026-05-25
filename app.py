from flask import Flask, render_template, request,  session, redirect
import psycopg2

app = Flask(__name__)
app.secret_key = '123456'

conexao = psycopg2.connect(
    host="localhost",
    database="controle_maquinas",
    user="postgres",
    password="Matheus@2009"
)
@app.route('/', methods = ['GET', 'POST'])
def home():
    if 'usuario' not in session:
        return redirect('/login')
    
    conexao = conexao.cursor()
    
    if request.method == 'POST':

        nome = request.form['nome']

        cursor = conexao.cursor()

        cursor.execute(
            "insert into maquinas (nome, status) values (%s, %s)",
            (nome, "Disponível")
        )

        conexao.commit()
    cursor.execute(
        "SELECT * FROM maquinas"
    )

    maquinas = cursor.fetchall()

    total = len(maquinas)

    return render_template(
        'index.html',
        maquinas=maquinas,
        total=total
    )
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        cursor = conexao.cursor()
        cursor.execute(
            "select * from usuarios where  usuario = %s and senha = %s",
            (usuario, senha)
        )
        usuario_encontrado = cursor.fetchone()


        if usuario_encontrado:

            session['usuario'] = usuario

            return redirect('/')

        else:
            return "Usuário ou senha incorretos"
    return render_template('login.html')

@app.route('/api/maquinas')

def maquinas():

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM maquinas"
    )

    maquinas = cursor.fetchall()

    lista = []

    for maquina in maquinas:

        lista.append({
            "id": maquina[0],
            "nome": maquina[1],
            "status": maquina[2]
        })

    return lista
@app.route('/logout')
def logout():

    session.pop('usuario')

    return redirect('/login')
app.run(host='0.0.0.0')

