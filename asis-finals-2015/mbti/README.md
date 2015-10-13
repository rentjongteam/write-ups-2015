# MBTI

**Kategori:** Forensic
**Points:** 200
**Deskripsi**

> test your personality and tell me about mine.

## Write-up

Kita diberikan file pcap, di mana seluruh pcapnya terenkripsi, jadi tidak ada string yang bisa didapat kecuali hostname: `mbti.asis-ctf.ir`, dan ketika kita kunjungi, kita diminta memasukkan nama dan umur, lalu berikutnya akan ada berbagai [pertanyaan kepribadian](https://en.wikipedia.org/wiki/Myers%E2%80%93Briggs_Type_Indicator). Di akhir kita akan diberi flag. Apapun jawaban kita, akan muncul flag, tapi flag yang salah.

Jika diperhatikan, pertanyaan berikut tergantung dari jawaban saat ini. Dan panjang pertanyaannya berbeda-beda. Lalu di file pcap bisa kita lihat bahwa enkripsi yang digunakan adalah RC4 tanpa padding. Artinya kita bisa tahu dengan tepat berapa ukuran konten yang dikembalikan, sampai ke level byte.

Dengan mengetahui info tersebut, kita bisa merekonstruksi pilihan yang dibuat dalam file pcap. Caranya kita test jawaban '1', jika ukuran responnya tidak sesuai, kita coba jawaban berikutnya.

Kita tidak tahu berapa panjang nama yang dimasukkan di awal. Panjangnya nama menentukan panjang repons (ukuran `Content-length`). Tapi nama ini tidak akan berubah panjangnya, jadi kita tidak akan mencocokkan jumlah byte secara eksak, tapi berapa perbedaan ukuran dokumen yang dikembalikan dibandingkan request sebelumnya.

Langkah pertama: ekstrak panjang `app_data` dari file

```python
import pyshark

cap = pyshark.FileCapture("mbti.pcap")
for i in cap:
    if 'ssl' in i:
        if 'app_data' in dir(i.ssl):
            data = i.ssl.app_data.replace(':', '').decode('hex')    
            print "APP DATA ", i.ip.src, len(data)    

```

Berikut ini beberapa baris awal (saya reqirect outputnye ke file bernama `flow`):

    APP DATA  192.168.110.13 487 
    APP DATA  185.45.192.218 1367
    APP DATA  192.168.110.13 662 
    APP DATA  185.45.192.218 1635
    APP DATA  192.168.110.13 628 
    APP DATA  185.45.192.218 1686
    APP DATA  192.168.110.13 509 
    APP DATA  185.45.192.218 1596
    APP DATA  192.168.110.13 479 
    APP DATA  185.45.192.218 1682
    APP DATA  192.168.110.13 479 
    APP DATA  185.45.192.218 1624
    APP DATA  192.168.110.13 479 
    APP DATA  185.45.192.218 1709
    APP DATA  192.168.110.13 628 
    APP DATA  185.45.192.218 1595
    APP DATA  192.168.110.13 628 


Perhatikan hal lain lagi: tiap langkah jawaban 1 sampai 25, kita akan selalu mengirim jumlah byte yang sama `aanswer=x` (di mana x adalah 0 sampai 4). Di sini saya sempat terkecoh, ada 2 kemungkinan: app_data yang berukuran 479 atau 628, keduanya ada 25 buah. Saya coba dua-duanya. 

Jadi pertama kita asumsikan asumsi bahwa semua yang panjangnya 479 adalah request, dan panjang berikutnya adalah jawaban. Singkat cerita, ternyata ini salah, dan saya coba lagi dengan 628.

Saya buat skrip python untuk mencetak perbedaan tiap request dari file `flow` di atas:

```python
lines = open("flow", "r").readlines()
prev = 1635
#prev = 1596
for i in range(0, len(lines)):
    line = lines[i]
    line = line.strip()
    a,b,c,d,e1 = line.split(" ")
    if int(e1)==628:
    #if int(e1)==479:
        a,b,c,d,e2 = lines[i+1].split(" ")
        print int(e2)-prev, ",", 
        prev = int(e2)
```

Hasilnya 

     #untuk 479
     d = [86 , -58 , 85 , -39 , 16 , -10 , -30 , 3 , 45 , -29 , -26 , 63 , -68 , -20 , 39 , -7 , -5 , 32 , -64 , 70 , -16 , -14 , -47 , -1 , -659]

     #untuk 628
     d = [51 , -91 , -6 , 100 , 26 , -35 , -62 , 46 , -41 , 57 , -17 , 43 , -38 , -50 , 39 , -66 , 33 , -24 , 96 , -104 , 7 , 54 , -20 , -19 , -668]


Setelah mendapatkan informasi ini, saya membuat skrip (`simulate.py`) untuk melakukan request, mendapatkan jawaban, mencocokkan dengan tabel di atas, jika tidak cocok, maka coba jawaban berikutnya, sampai cocok. Tapi ternyata tidak berhasil. Ternyata ada satu soal, di mana 2 jawaban akan menghasilkan panjang konten yang sama.

Akhirnya saya modifikasi skripnya supaya mencoba semua kemungkinan, dan ternyata memang hanya satu soal yang bermasalah.

Ada satu masalah lagi: di akhir ada 5 jawaban, yang semuanya menghasilkan panjang teks yang sama, jadi tetap harus ditebak-tebak. Jadi totalnya saya melakukan banyak tebakan:

* Mengasumsikan panjang request adalah 479, sampai di akhir saya cek 4 flag yang mungkin: tidak berhasil
* Saya cek ternyata ada jawaban yang keduanya menghasilkan panjang yang sama, hasilnya 4 flag lagi saya cek lagi-lagi tidak berhasil
* Mengasumsikan panjang request adalah 628, sampai di akhir, saya cek 4 flag yang mungkin: tidak berhasil
* Saya coba kemungkinan jawaban kedua: sampai diakhir ada 4 flag, saya cek flag 1 gagal, flag 2 gagal, flag 3 BERHASIL

Tadinya saya sudah putus asa dan ingin menyerah, tapi akhirnya flagnya diterima.

    ASIS{01d3c6afe8046b28eef7ac98a19cae85} 
