from flask import Flask, jsonify
from config import Config
from database import init_db
from routes.murid_routes import murid_bp

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    app.register_blueprint(murid_bp)
    
    # Home endpoint
    @app.route('/', methods=['GET'])
    def home():
        """Endpoint home untuk informasi API"""
        return jsonify({
            "message": "Student REST API",
            "version": "1.0",
            "endpoints": {
                "POST /api/murid": "Tambah data murid baru",
                "GET /api/murid": "Ambil semua data murid",
                "GET /api/murid/<id>": "Ambil data murid berdasarkan ID",
                "PUT /api/murid/<id>": "Update data murid",
                "DELETE /api/murid/<id>": "Hapus data murid",
                "GET /api/murid/statistik": "Statistik nilai murid"
            }
        }), 200
    
    return app

if __name__ == '__main__':
    # Inisialisasi database
    print("=" * 60)
    print("Initializing database...")
    init_db()
    
    # Create app
    app = create_app()
    
    # Run application
    print("=" * 60)
    print("Student REST API is running!")
    print(f"Server: http://{Config.HOST}:{Config.PORT}")
    print("=" * 60)
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )