#Simple Algorithm


**Kategori:** Crypto
**Points:** 100
**Deskripsi**
> The flag is encrypted by this [code](soal/simple_algorithm_5a0058082857cf27d6e51c095ac59bd5), can you decrypt it after finding the system?


## Write-up

Algoritma yang digunakan untuk mengenkripsi cukup sederhana,
pertama flag dijadikan hex lalu diubah menjadi integer, tapi karakter pertama diabaikan (lihat hflag[2:],
artinya dua hex pertama diabaikan):

```python
hflag = flag.encode('hex')
iflag = int(hflag[2:], 16)
```

Setelah itu ada fungsi `FAN` yang akan memetakan integer ke integer lain. Kita tidak perlu mengerti detailnya. Berikutnya:

```python
i = 0
r = ''
while i < len(str(iflag)):
    d = str(iflag)[i:i+2]
    nf = FAN(int(d), 3)
    r += str(nf)
    i += 2
```

Untuk tiap dua karakter desimal (`iflag` berisi desimal), kita petakan dengan fungsi FAN, dengan m=3.
Karena cuma ada 99 kemungkinan (00-99), saya bisa membuat tabelnya untuk mencari kebalikannya:

```python
for i in range(0, 99):
    print '"%s":%d, ' % (FAN(i, 3), i)
```

Setelah dirapikan sedikit, tabelnya seperti ini:


```python
a = {"0":"0", "1":"01", "3":"02", "8":"03", "9":"04", "10":"05",
     "24":"06", "26":"07", "27":"08", "28":"09", "30":"10", "71":"11",
     "72":"12", "73":"13", "78":"14", "80":"15", "81":"16", "82":"17",
     "84":"18", "89":"19", "90":"20", "91":"21", "213":"22", "215":"23",
     "216":"24", "217":"25", "219":"26", "233":"27", "234":"28", "235":"29",
     "240":"30", "242":"31", "243":"32", "244":"33", "246":"34", "251":"35",
     "252":"36", "253":"37", "267":"38", "269":"39", "270":"40", "271":"41",
     "273":"42", "638":"43", "639":"44", "640":"45", "645":"46", "647":"47",
     "648":"48", "649":"49", "651":"50", "656":"51", "657":"52", "658":"53",
     "699":"54", "701":"55", "702":"56", "703":"57", "705":"58", "719":"59",
     "720":"60", "721":"61", "726":"62", "728":"63", "729":"64", "730":"65",
     "732":"66", "737":"67", "738":"68", "739":"69", "753":"70", "755":"71",
     "756":"72", "757":"73", "759":"74", "800":"75", "801":"76", "802":"77",
     "807":"78", "809":"79", "810":"80", "811":"81", "813":"82", "818":"83",
     "819":"84", "820":"85", "1914":"86", "1916":"87", "1917":"88",
     "1918":"89", "1920":"90", "1934":"91", "1935":"92", "1936":"93",
     "1941":"94", "1943":"95", "1944":"96", "1945":"97",      "1947":"98"}
```

Tabel ini bisa untuk mendekrip hasil. Contoh: jika kita enkrip 'Xab', maka hasilnya 21619360.
Nilai ini bisa di pecah menjadi 216, 1936, dan 0. Cara pemisahan ini adalah dengan melihat tabel di atas,
kita tidak mungkin memisahkan menjadi: 2 dan 16 (karena 2 dan 16 tidak ada di tabel).
Setelah tahu angka: 216, 1936, dan 0, itu bisa kita petakan balik menjadi:
24, 93, 0 yang jika digabungkan menjadi: 24930 yang jika dijadikan hex 0x6162,
dan jika didecode menjadi `ab`.


Sekarang setelah tahu pemetaannya, kita buka file `enc.txt` yang perlu didekrip:

     2712733801194381163880124319146586498182192151917719248224681364019142438188097307292437016388011943193619457377217328473027324319178428

Perhatikan bahwa karena sistem enkripsi ini tidak memakai pemisah, agak sulit memisahkan string menjadi bagian-bagianya, ada kerancuan.
Kita mulai dari bebereapa angka di awal:

     271

Angka itu bisa dihasilkan dari: "27" dan "1" atau "271". Dengan mengenkrip flag sample: 'ASIS{b026324c6904b2a9cb4b88d6d61c81d1}',
bisa didapatkan pemetaan beberapa huruf awal, dan sisanya manual, perhatikan tanda '*',
itu artinya saya tidak yakin karena ada lebih dari satu interpretasi.

```python
b = "271 273 3 801 1943 811 638 *801 *243 1914 658 649 818 219 215 1917 719 24 82 246 *813 640 1914 *243 *818 *809 *730 *729 *243 701 638 *801 1943 1936 1945 737 *721 732 84 730 *273 *243 1917 84 28".replace("*", "").split(" ")
```

Dengan menjalankan `dec.py`, didapatkan output:

    SIS{a9ab115c488a311896dac4e8bc20a6d7}

Perhatikan bahwa huruf pertama hilang (sesuai kode program),
jadi kita perlu tambahkan A di depan, flagnya menjadi `ASIS{a9ab115c488a311896dac4e8bc20a6d7}`

