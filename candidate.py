# Kelas untuk merepresentasikan data seorang kandidat proyek.
class Candidate:
    def __init__(self, id_kandidat: str, nama: str, cost: float):
        self.id = id_kandidat     
        self.nama = nama         
        self.cost = cost

    def __repr__(self):
        return f"Candidate(ID: {self.id}, Nama: {self.nama}, Cost: {self.cost})"