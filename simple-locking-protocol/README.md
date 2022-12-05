# Simple Locking Protocol

## Description

Simple locking merupakan salah satu protokol dalam concurrency control. Protokol ini merupakan versi sederhana dari two phase locking karena hanya terdapat exclusive lock, berbeda dengan two phase locking yang memiliki dua jenis lock, yaitu shared-lock dan exclusive lock. Selain itu, pada protokol ini, lock hanya dilepas ketika suatu transaksi telah selesai dilakukan, yaitu ketika transaksi tersebut commit. Walaupun begitu, protokol ini tidak memastikan terbebas dari deadlock. Pada implementasinya, simple locking juga memiliki berbagai variansi, termasuk bagaimana ia meng-handle deadlock.

Pada program ini, kami mengimplementasikan deadlock prevention, yaitu skema wound-wait. Skema ini merupakan skema yang preemptive. Pada skema ini, transaksi yang lebih tua akan memaksa transaksi yang lebih muda untuk rollback (wound). Sementara itu, transaksi yang lebih muda akan menunggu transaksi yang lebih tua. Selain saat commit, resource juga akan dibebaskan jika suatu transaksi abort.

Selain itu, pada program ini, kami mengimplementasikan protokol ini, di mana jika terdapat transaksi-transaksi yang berstatus waiting maka semua operasi transaksi-transaksi tersebut akan dikumpulkan secara terurut sesuai kemunculan pada test. Operasi-operasi tersebut akan dicoba dijalankan kembali setiap kali suatu transaksi lain commit, dengan terlebih dahulu mengubah statusnya menjadi available.

Sementara itu, transaksi-transaksi yang di-abort akan dijalankan kembali setelah semua operasi-operasi transaksi non-aborted selesai. Transaksi-transaksi tersebut akan dijalankan secara serial dengan urutan sesuai dengan urutan transaksi tersebut di-abort. Dipilihnya skema serial karena urutan operasi di test sudah tidak relevan untuk digunakan sebagai acuan.


## How to Run
- Masukkan file test ke dalam folder test
- Pastika file test sudah sesuai dengan format yang diminta program -> contoh dapat dilihat pada file di folder test
- Jalankan program
  ```
  py main.py test/<file-name>
  ```

