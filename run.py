#/run.py
from app.app import app  # Asegúrate de importar la aplicación correctamente

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
