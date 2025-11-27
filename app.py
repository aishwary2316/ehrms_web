from flask import Flask, render_template, jsonify
from extensions import mongo, login_manager
from config import Config
import os

def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    mongo.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Import models after extensions are initialized
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user for Flask-Login."""
        return User.get_by_id(user_id)
    
    # Create upload folder if it doesn't exist
    upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_folder, exist_ok=True)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.users import users_bp
    from routes.profile import profile_bp
    from routes.notifications import notifications_bp
    from routes.stations import stations_bp
    from routes.leave import leave_bp
    from routes.transfer import transfer_bp
    from routes.duty import duty_bp
    from routes.attendance import attendance_bp
    from routes.grievance import grievance_bp
    from routes.reports import reports_bp
    from routes.assets import assets_bp
    from routes.payslip import payslip_bp
    from routes.kanglasha import kanglasha_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(stations_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(transfer_bp)
    app.register_blueprint(duty_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(grievance_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(payslip_bp)
    app.register_blueprint(kanglasha_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Health check endpoint for monitoring and keep-alive
    @app.route('/health')
    def health_check():
        """Health check endpoint for Render and monitoring services."""
        try:
            # Check database connection
            mongo.db.command('ping')
            db_status = 'healthy'
        except Exception as e:
            db_status = f'unhealthy: {str(e)}'
        
        return jsonify({
            'status': 'healthy' if db_status == 'healthy' else 'degraded',
            'database': db_status,
            'app': 'E-HRMS',
            'version': '1.0.0'
        }), 200 if db_status == 'healthy' else 503
    
    # Ping endpoint (lightweight for keep-alive)
    @app.route('/ping')
    def ping():
        """Lightweight ping endpoint for keep-alive services."""
        return jsonify({'status': 'ok', 'message': 'pong'}), 200
    
    return app

# Create app instance for Gunicorn (production) and direct imports
app = create_app()

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
