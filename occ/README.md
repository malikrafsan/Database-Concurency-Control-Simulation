# Simple Locking Protocol

## Description

Optimistic Concurrency Control adalah metode concurrency control yang diterapkan pada sistem transactional seperti sistem manajemen basis data relasional dan software transactional memory. OCC mengasumsikan bahwa banyak transaksi seringkali dapat diselesaikan tanpa mengganggu satu sama lain. Saat berjalan, transaksi menggunakan resources data tanpa memperoleh lock dari resources tersebut. Sebelum melakukan commit, setiap transaksi memverifikasi bahwa tidak ada transaksi lain yang mengubah data yang sudah dibaca. Jika ternyata ada conflicting modifications, maka transaksi akan di roll back dan diulang
OCC umumnya digunakan di environments dengan pertentangan data yang rendah. Ketika conflict jarang terjadi, transaksi bisa selesai tanpa biaya untuk mengelola lock dan tanpa harus menunggu lock transaksi lain untuk selesai sehingga bisa menghasilkan throughput yang lebih tinggi dibandingkan metode concurrency control lainnya. Namun jika conflict yang terjadi cukup sering, maka cost untuk terus-menerus mengulang transaksi akan membuat performance menjadi sangat buruk sehingga metode concurrency control lain lebih cocok digunakan daripada OCC.



## How to Run
- Masukkan file test ke dalam folder occ dalam bentuk file .txt
- Sudah diberikan contoh file untuk testing program. Pastikan directory terminal sudah berada didalam folder occ
- Jalankan program
  ```
  py main.py <file-name>
  ```

