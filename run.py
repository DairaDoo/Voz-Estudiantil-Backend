# run.py
from app.app import create_app

app = create_app(testing=False)

if __name__ == '__main__':
    app.run(debug=True)
