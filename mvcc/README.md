# MVCC Protocol

## Description

MVCC merupakan salah satu protokol dalam concurrency control. Pada program ini, diimplementasikan variansi MVCC dengan timestamp ordering. MVCC menyimpan data item/record Q dengan satu atau lebih versi.   Dengan suatu versi dari item data mengandung content yang merupakan nilai atau value dari data item atau record versi Qk, Write timestamp (WTS) Qk yang merupakan timestamp dari transaksi yang berhasil melakukan write data item/record versi Qk tersebut, Read Timestamp (RTS) Qk yang merupakan timestamp terbesar dari sebuah transaksi yang berhasil membaca nilai data item/record versi Qk. Proses read tidak harus menunggu karena dapat langsung membaca versi data item Qk.

Pada implementasinya, transaksi akan memilih versi tertentu atau membuat versi baru atas data item Qk. Transaksi tersebut akan memilih data item Qk yang memiliki nilai write timestamp terbesar akan tetapi masih tidak melebihi nilai dari timestamp transaksi tersebut (WTS(Qk) <= TS(Ti)). Pada proses read, nilai R-TS dari Qk diubah nilainya didapatkan dari nilai maksimal timestamp transaksi dan nilai R-TS(Qk) sebelumnya. Sedangkan pada proses write, dilakukan beberapa pengecekan. Apabila nilai timestamp transaksi lebih kecil dari R-TS (Qk) maka proses write tidak dapat dilanjutkan dan transaksi harus melakukan rollback. Jika didapatkan nilai timestamp transaksi sama dengan nilai W-TS dari Qk maka transaksi dapat secara langsung melakukan overwrite nilai atau value data. Selain itu, transaksi akan membuat sebuah versi data item baru dengan nilai W-TS (Qi) dan R-TS (Qi)  berupa nilai timestamp dari transaksi.


## How to Run
- Masukkan file test ke dalam folder test
- Pastika file test sudah sesuai dengan format yang diminta program -> contoh dapat dilihat pada file di folder test
- Jalankan program
  ```
  py main.py test/<file-name>
  ```

