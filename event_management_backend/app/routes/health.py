from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Health", "health", url_prefix="/api/health", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    """Returns service health status."""
    def get(self):
        """Get health status.
        Returns:
            JSON payload with message 'Healthy'
        """
        return {"message": "Healthy"}
