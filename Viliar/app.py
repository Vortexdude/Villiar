from factory import create_app, MODULES
from utils import BaseParser
app = create_app(MODULES)
base = BaseParser(check_env=False)
base.add(name="host", type='string', default="0.0.0.0")
base.add(name="port", type='int', default=5000)
base.add(name="debug", type='bool', default=False)


if __name__ == "__main__":
    args = base.arguments
    app.run(host=args['host'], port=args['port'], debug=args['debug'])
