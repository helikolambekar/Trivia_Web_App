from source import create_app

ENV = 'DEV' 

app = create_app(ENV)

if __name__ == '__main__':
    if ENV == "PROD":
        app.run(debug=False)
    else:
        app.run(debug=True)