from flask_smorest import Api as BaseApi


class Api(BaseApi):
    def register_blueprint(self, blp, *, base_prefix=None, parameters=None, **options):
        url_prefix = options.get("url_prefix", blp.url_prefix)
        if base_prefix is not None:
            options['url_prefix'] = url_prefix
        self._app.register_blueprint(blp, **options)
        blp.register_views_in_doc(
            api=self,
            app=self._app,
            spec=self.spec,
            name=blp.name,
            parameters=parameters
        )
        self.spec.tag({"name": blp.name, "description": blp.description})


spec_kwargs = {
    "components": {
        "securitySchemes": {
            "api_key": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "refresh_key": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
        }
    }
}

api = Api(spec_kwargs=spec_kwargs)
