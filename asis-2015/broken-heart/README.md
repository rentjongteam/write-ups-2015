#My Heart

**Kategori:** Forensik
**Points:** 100
**Deskripsi**
> Find the flag in this [file](soal/myheart_7cb6daec0c45b566b9584f98642a7123.pcap.xz).

## Write-up

Dalam file PCAP yang diberikan, terdapat beberapa HTTP request dengan range yang berbeda-beda.
Kita bisa menggabungkan ini secara manual, tapi saya menggunakan `tshark` dan skrip python untuk menyatukannya.

Untuk memecahkan filenya

     for((i=0;i<23;i++)) ;
        do tshark -2 -r ../myheart_7cb6daec0c45b566b9584f98642a7123.pcap -z follow,tcp,hex,$i > $i;
     done

Saya mengetahui ada 22 segment dari perintah:

     tshark -r myheart_7cb6daec0c45b566b9584f98642a7123.pcap -T fields -e tcp.streams

Perhatikan bahwa ada beberapa byte hilang di depan, tapi dari string "IDAT" dan "HDR",
kita bisa menebak bahwa ini file PNG, jadi kita tambahkan saja header PNG.

![flag](./output.png?raw=true "Output")
