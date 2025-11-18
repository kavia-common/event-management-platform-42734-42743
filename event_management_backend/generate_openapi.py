import json
import os
from app import create_app

app = create_app()

with app.app_context():
    # flask-smorest stores the spec on the Api instance accessible via current_app.extensions
    api = app.extensions["smorest"]
    openapi_spec = api.spec.to_dict()

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
