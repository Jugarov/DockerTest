from flask import Flask, jsonify, request, render_template_string
import os
import psycopg2
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "¡Hola desde Flask con Docker!"

@app.route("/grafica", methods=["GET"])
def grafica():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT x, y FROM coordenadas;")
    data = cur.fetchall()
    cur.close()
    conn.close()

    if data:
        x_vals, y_vals = zip(*data)
    else:
        x_vals, y_vals = [], []

    plt.figure()
    plt.scatter(x_vals, y_vals, marker="o", color="blue")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Coordenadas almacenadas")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    html_template = f"""
    <html>
        <body>
            <h1>Gráfica de Coordenadas</h1>
            <img src="data:image/png;base64,{plot_url}" /><br><br>
            <form action="/agregar_punto" method="post">
                <label for="x">Coordenada X:</label>
                <input type="text" id="x" name="x" required>
                <label for="y">Coordenada Y:</label>
                <input type="text" id="y" name="y" required>
                <button type="submit">Agregar Punto</button>
            </form>
        </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/agregar_punto", methods=["POST"])
def agregar_punto():
    x = request.form.get("x")
    y = request.form.get("y")

    if not x or not y:
        return "Faltan valores", 400

    try:
        x, y = float(x), float(y)
    except ValueError:
        return "Valores inválidos", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO coordenadas (x, y) VALUES (%s, %s);", (x, y))
    conn.commit()
    cur.close()
    conn.close()

    return '<script>alert("Punto agregado correctamente"); window.location.href="/grafica";</script>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
