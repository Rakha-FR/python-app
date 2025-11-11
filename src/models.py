def hitung_rata_rata(nilai1, nilai2, nilai3):
    rata_rata = (nilai1 + nilai2 + nilai3) / 3
    return rata_rata

def hitung_grade(rata_rata):
    if rata_rata >= 90:
        return "A"
    elif rata_rata >= 80:
        return "B"
    elif rata_rata >= 70:
        return "C"
    elif rata_rata >= 60:
        return "D"
    else:
        return "E"

def format_murid_data(murid):
    return {
        "id": murid['id'],
        "nama": murid['nama'],
        "nilai": {
            "nilai1": round(murid['nilai1'], 2),
            "nilai2": round(murid['nilai2'], 2),
            "nilai3": round(murid['nilai3'], 2)
        },
        "rata_rata": round(murid['rata_rata'], 2),
        "grade": murid['grade'],
        "created_at": murid['created_at'].strftime("%Y-%m-%d %H:%M:%S") if murid.get('created_at') else None
    }

def validasi_nilai(nilai1, nilai2, nilai3):
    nilai_list = [nilai1, nilai2, nilai3]
    for i, nilai in enumerate(nilai_list, 1):
        if nilai < 0 or nilai > 100:
            return False, f"Nilai {i} harus antara 0-100"
    return True, None