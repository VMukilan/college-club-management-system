"""
Entry point for College Club Management System (v0.1)
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Running in debug mode for development environment in v0.1
    app.run(host='127.0.0.1', port=5000, debug=True)
