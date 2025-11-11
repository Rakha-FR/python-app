from flask import Blueprint, request, jsonify
from psycopg2.extras import RealDictCursor
from database import get_db_connection
from models import (
    hitung_rata_rata, 
    hitung_grade, 
    format_murid_data, 
    validasi_nilai
)

# Membuat blueprint untuk routes murid
murid_bp = Blueprint('murid', __name__, url_prefix='/api/murid')

# ===== 4. INPUT & 5. OUTPUT =====
@murid_bp.route('', methods=['POST'])
def create_murid():
    try:
        data = request.get_json()
        required_fields = ['nama', 'nilai1', 'nilai2', 'nilai3']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{field}' wajib diisi"
                }), 400
        
        nama = data['nama']
        nilai1 = float(data['nilai1'])
        nilai2 = float(data['nilai2'])
        nilai3 = float(data['nilai3'])
        
        is_valid, error_msg = validasi_nilai(nilai1, nilai2, nilai3)
        
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": error_msg
            }), 400
        
        rata_rata = hitung_rata_rata(nilai1, nilai2, nilai3)
        grade = hitung_grade(rata_rata)
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            INSERT INTO murid (nama, nilai1, nilai2, nilai3, rata_rata, grade)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (nama, nilai1, nilai2, nilai3, rata_rata, grade))
        
        new_murid = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Data murid berhasil ditambahkan",
            "data": format_murid_data(new_murid)
        }), 201
        
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": "Nilai harus berupa angka"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@murid_bp.route('', methods=['GET'])
def get_all_murid():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM murid ORDER BY id ASC")
        murid_list = cur.fetchall()
        
        cur.close()
        conn.close()
        
        formatted_list = []
        for murid in murid_list:
            formatted_list.append(format_murid_data(murid))
        
        return jsonify({
            "status": "success",
            "total_data": len(formatted_list),
            "data": formatted_list
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@murid_bp.route('/<int:id>', methods=['GET'])
def get_murid_by_id(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM murid WHERE id = %s", (id,))
        murid = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if murid is None:
            return jsonify({
                "status": "error",
                "message": f"Murid dengan ID {id} tidak ditemukan"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": format_murid_data(murid)
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@murid_bp.route('/<int:id>', methods=['PUT'])
def update_murid(id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM murid WHERE id = %s", (id,))
        existing_murid = cur.fetchone()
        
        if existing_murid is None:
            cur.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": f"Murid dengan ID {id} tidak ditemukan"
            }), 404
        
        nama = data.get('nama', existing_murid['nama'])
        nilai1 = float(data.get('nilai1', existing_murid['nilai1']))
        nilai2 = float(data.get('nilai2', existing_murid['nilai2']))
        nilai3 = float(data.get('nilai3', existing_murid['nilai3']))
        
        is_valid, error_msg = validasi_nilai(nilai1, nilai2, nilai3)
        
        if not is_valid:
            cur.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": error_msg
            }), 400
        
        rata_rata = hitung_rata_rata(nilai1, nilai2, nilai3)
        grade = hitung_grade(rata_rata)
        
        cur.execute("""
            UPDATE murid 
            SET nama = %s, nilai1 = %s, nilai2 = %s, nilai3 = %s, 
                rata_rata = %s, grade = %s
            WHERE id = %s
            RETURNING *
        """, (nama, nilai1, nilai2, nilai3, rata_rata, grade, id))
        
        updated_murid = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Data murid berhasil diupdate",
            "data": format_murid_data(updated_murid)
        }), 200
        
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Nilai harus berupa angka"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@murid_bp.route('/<int:id>', methods=['DELETE'])
def delete_murid(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Cek apakah murid ada
        cur.execute("SELECT id FROM murid WHERE id = %s", (id,))
        murid = cur.fetchone()
        
        if murid is None:
            cur.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": f"Murid dengan ID {id} tidak ditemukan"
            }), 404
        
        cur.execute("DELETE FROM murid WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": f"Data murid dengan ID {id} berhasil dihapus"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@murid_bp.route('/statistik', methods=['GET'])
def get_statistik():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM murid")
        murid_list = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if len(murid_list) == 0:
            return jsonify({
                "status": "success",
                "message": "Belum ada data murid",
                "data": None
            }), 200
        
        total_murid = len(murid_list)
        total_rata_rata = 0
        grade_count = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        
        for murid in murid_list:
            total_rata_rata += murid['rata_rata']
            grade_count[murid['grade']] += 1
        
        rata_rata_kelas = total_rata_rata / total_murid
        
        murid_terbaik = murid_list[0]
        
        for murid in murid_list:
            if murid['rata_rata'] > murid_terbaik['rata_rata']:
                murid_terbaik = murid
        
        # ===== 5. OUTPUT =====
        # ===== 6. FORMAT TAMPILAN =====
        return jsonify({
            "status": "success",
            "data": {
                "total_murid": total_murid,
                "rata_rata_kelas": round(rata_rata_kelas, 2),
                "distribusi_grade": grade_count,
                "murid_terbaik": {
                    "nama": murid_terbaik['nama'],
                    "rata_rata": round(murid_terbaik['rata_rata'], 2),
                    "grade": murid_terbaik['grade']
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==================== FILE: app.py ====================
"""
Main application file
Entry point untuk menjalankan aplikasi
"""
from flask import Flask, jsonify
from config import Config
from database import init_db
from routes.murid_routes import murid_bp

def create_app():
    """
    Factory function untuk membuat Flask application
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints
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