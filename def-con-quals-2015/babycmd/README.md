# Babycmd

**Kategori:** Baby's first
**Points:** 1
**Deskripsi**

## Write-up

Kita diberikan sebuah file, ketika dijalankan, kita bisa memilih untuk melakukan `ping`, `dig`, atau `host`. Sepertinya semua input dicek dengan benar. Pada tahap pertama, semua input dicek apakah mengandung karakter special `|`, `&`, `*`, `!`, dan `'`.

Untuk perintah `ping`, selain inputnya dicek, input juga dikonversi menjadi bentuk biner dengan `inet_aton`, dan dikembalikan menjadi string dengan `inet_ntoa`. Jadi ini benar-benar aman.

Untuk perintah `dig`, jika inputnya berupa alamat ip, maka akan dilakukan `dig -x alamat_ip`, jika inputnya host name, maka akan dilakukan pemeriksaan hostnamenya valid atau tidak, lalu `dig 'namahost'` akan dipanggil. Perhatikan ada kutip tunggal di situ, di shell, apapun dalam petik tunggal tidak akan diekspansi, dan karena petik tunggal (`'`) juga difilter, maka kita tidak akan bisa melakukan apapun.

Terakhir pada perintah `host` pemeriksaan yang sama dilakukan, tapi kali ini yang dipakai adalah petik ganda: `host "namahost"`. Karena petik ganda (`"`) digunakan, maka di dalam nama host dilakukan ekspansi, jadi kita bisa melakukan `host $(ls)` untuk menjalankan `ls`. Tapi ternyata ada pengecekan ekstra di karakter pertama dan terakhir, jadi perintah perlu diberi sesuatu di depan/belakangnya, misalnya `host a$(ls)b`, di output kita akan ada ekstra `a` di awal dan `b` di akhir, yang bisa kita abaikan. 

Dengan perintah `host a$(cat${IFS}/home/babycmd/flag)b` didapatkan:

       The flag is: Pretty easy eh!!~ Now let's try something hArd3r, shallwe??.


