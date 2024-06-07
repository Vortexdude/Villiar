def init_app(app):
    from importlib import import_module
    module_names = ['auth', 'monitor']
    if not module_names:
        from glob import glob
        import os
        module_names = [os.path.basename(file) for file in glob("./Viliar/src/modules/[!_]*")]

    for module_name in module_names:
        module = import_module(f"Viliar.src.modules.{module_name}", "app")
        module.init_app(app)
