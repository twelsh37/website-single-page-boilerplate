from flask import Flask, render_template, request
from config import DevelopmentConfig, ProductionConfig
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Load the appropriate configuration
if app.debug:
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

# Set up logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/skillsmatrix.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('SkillsMatrix startup')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index page: {str(e)}")
        return render_template('error.html'), 500

@app.route('/privacy')
def privacy():
    try:
        return render_template('privacy.html')
    except Exception as e:
        app.logger.error(f"Error rendering privacy page: {str(e)}")
        return render_template('error.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()