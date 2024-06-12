from factory import create_app, MODULES

app = create_app(MODULES)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
