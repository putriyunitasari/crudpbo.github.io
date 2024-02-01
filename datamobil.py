from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class Data_Mobil(Tk):
    def __init__(self):
        super().__init__()
        self.title("Registrasi Data Mobil")
        self.geometry("850x600")
        # Koneksi ke database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="registrasi"
        )
        # Membuat kursor
        self.cursor = self.db.cursor()
        
        # Membuat dan menampilkan GUI
        self.tampilan_gui()
        
    def tampilan_gui(self):
        
        Label(self, text="Nopol Mobil").grid(row=0, column=0, padx=10, pady=10)
        self.nopol_entry = Entry(self, width=50)
        self.nopol_entry.grid(row=0, column=1, padx=10, pady=10)
        
        Label(self, text="Merk Mobil").grid(row=1, column=0, padx=10, pady=10)
        self.merk_entry = Entry(self, width=50)
        self.merk_entry.grid(row=1, column=1, padx=10, pady=10)
        
        Label(self, text="Warna Mobil").grid(row=2, column=0, padx=10, pady=10)
        self.warna_entry = Entry(self, width=50)
        self.warna_entry.grid(row=2, column=1, padx=10, pady=10)
        
        Label(self, text="Bahan Bakar ").grid(row=3, column=0, padx=10, pady=10)
        self.BahanBakar_entry = Text(self, width=37, height=5)
        self.BahanBakar_entry.grid(row=3, column=1, padx=10, pady=10)
        
        Button(self, text="Simpan Data",
            command=self.simpan_data).grid(row=4, column=0,
                                            columnspan=2, pady=10)
        
         # Menambahkan tombol update data
        Button(self, text="Update Data", command=self.update_data).grid(row=6, column=2, columnspan=2, pady=10, padx=10)
       
        # Menambahkan tombol delete data
        Button(self, text="Delete Data", command=self.hapus_data).grid(row=6, column=1, columnspan=2, pady=10, padx=10)
            
        # Menambahkan Treeview
        self.tree = ttk.Treeview(self, columns=("nopol", "merk", "warna","BahanBakar"), show="headings")
        self.tree.heading("nopol", text="Nopol Mobil")
        self.tree.heading("merk", text="Merk Mobil")
        self.tree.heading("warna", text="Warna Mobil")
        self.tree.heading("BahanBakar", text="Bahan Bakar")
        self.tree.grid(row=5, column=0, columnspan=8, pady=10, padx=10)
            
        # Menambahkan tombol refresh data
        Button(self, text="Refresh Data",command=self.tampilkan_data).grid(row=6, column=0, columnspan=2, pady=10,padx=10)

        #Menambahkan tombol print data
        Button(self, text="Print Data", command=self.cetak_ke_pdf).grid(row=6,column=4, columnspan=2, pady=10, padx=10)
        
        self.tampilkan_data()
        
    def simpan_data(self):
        nopol = self.nopol_entry.get()
        merk = self.merk_entry.get()
        warna = self.warna_entry.get()
        BahanBakar = self.BahanBakar_entry.get("1.0", END)
        
        query = "INSERT INTO mobil (Nopol, merk_mobil, warna_mobil, bahan_bakar) VALUES (%s,%s, %s, %s)"
        values = (nopol, merk, warna, BahanBakar)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            
        self.nopol_entry.delete(0, END)
        self.merk_entry.delete(0, END)
        self.warna_entry.delete(0, END)
        self.BahanBakar_entry.delete("1.0", END)
            
    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Ambil data dari database
        self.cursor.execute("SELECT * FROM mobil")
        data = self.cursor.fetchall()
        # Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def update_data(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diupdate.")
            return
        
        # Ambil data terpilih dari treeview
        data = self.tree.item(selected_item[0], 'values')
        

        # Tampilkan form update dengan data terpilih
        self.nopol_entry.insert(0, data[0])
        self.merk_entry.insert(0, data[1])
        self.warna_entry.insert(0, data[2])
        self.BahanBakar_entry.insert("1.0", data[3])

        self.nopol_entry.delete(0, END)
        self.merk_entry.delete(0, END)
        self.warna_entry.delete(0, END)
        self.BahanBakar_entry.delete("1.0", END)

        # Menambahkan tombol update di form
        Button(self, text="Update", command=lambda:
        self.proses_update(data[0])).grid(row=4, column=1, columnspan=2, pady=10)
        
    def proses_update(self, nis_to_update):
        nopol = self.nopol_entry.get()
        merk = self.merk_entry.get()
        warna = self.warna_entry.get()
        BahanBakar = self.BahanBakar_entry.get("1.0", END)
        query = "UPDATE mobil SET Nopol=%s, merk_mobil=%s, warna_mobil=%s, bahan_bakar=%s WHERE Nopol=%s"
        values = (nopol, merk, warna, BahanBakar, nis_to_update)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Bersihkan form setelah update
        self.nopol_entry.delete(0, END)
        self.merk_entry.delete(0, END)
        self.warna_entry.delete(0, END)
        self.BahanBakar_entry.delete("1.0", END)

        # Tampilkan kembali data setelah diupdate
        self.tampilkan_data()

    def cetak_ke_pdf(self):
        doc = SimpleDocTemplate("data_mobil.pdf", pagesize=letter)
        styles = getSampleStyleSheet()

        # Membuat data untuk tabel PDF
        data = [["Nopol Mobil", "Merk Mobil", "Warna Mobil", "Bahan Bakar"]]

        for row_id in self.tree.get_children():
            row_data = [self.tree.item(row_id, 'values')[0],
                        self.tree.item(row_id, 'values')[1],
                        self.tree.item(row_id, 'values')[2],
                        self.tree.item(row_id, 'values')[3]]
            data.append(row_data)

        # Membuat tabel PDF
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Menambahkan tabel ke dokumen PDF
        doc.build([table])

        messagebox.showinfo("Sukses", "Data berhasil dicetak ke PDF(data_mobil.pdf).")

    def hapus_data(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus.")
            return
        
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")

        if confirmation:
            for item in selected_item:
                data = self.tree.item(item, 'values')
                nis_to_delete = data[0]

            query = "DELETE FROM mobil WHERE Nopol = %s"
            values = (nis_to_delete,)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        except Exception as e:
             messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        
        self.tampilkan_data()

if __name__ == "__main__":
    app = Data_Mobil()
    app.mainloop()