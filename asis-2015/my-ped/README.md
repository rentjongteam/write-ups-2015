#My Ped


**Kategori:** Forensik
**Points:** 175

**Deskripsi**


> What you see in my [ped](soal/My_Ped_11ceeee7565e3bbd5c9db2c1a791236f) ?

## Write-up

Setelah diekstraksi, didapatkan file yang tidak dikenal. Setelah file itu dibuka di hex editor, terlihat sepertinya ada beberapa file di dalamnya (PDF, PNG, dsb).


Saya coba cek menggunakan binwalk 

    $ binwalk myped
    
    DECIMAL       HEXADECIMAL     DESCRIPTION
    --------------------------------------------------------------------------------
    33679         0x838F          PDF document, version: "1.5"
    33749         0x83D5          Zlib compressed data, best compression, uncompressed size >= 29980
    39072         0x98A0          Zlib compressed data, best compression, uncompressed size >= 30203
    44751         0xAECF          Zlib compressed data, best compression, uncompressed size >= 22762
    49258         0xC06A          Zlib compressed data, best compression, uncompressed size >= 12619
    51741         0xCA1D          Zlib compressed data, best compression, uncompressed size >= 325
    52146         0xCBB2          Zlib compressed data, best compression, uncompressed size >= 330
    52542         0xCD3E          Zlib compressed data, best compression, uncompressed size >= 600
    52952         0xCED8          Zlib compressed data, best compression, uncompressed size >= 617
    53370         0xD07A          Zlib compressed data, best compression, uncompressed size >= 626
    53815         0xD237          Zlib compressed data, best compression, uncompressed size >= 9117
    61504         0xF040          Zlib compressed data, best compression, uncompressed size >= 760
    61625         0xF0B9          Zlib compressed data, best compression, uncompressed size >= 20161
    73178         0x11DDA         Zlib compressed data, best compression, uncompressed size >= 167
    3299         0x11E53         Zlib compressed data, best compression, uncompressed size >= 5084
    77835         0x1300B         Zlib compressed data, best compression, uncompressed size >= 11
    77958         0x13086         Zlib compressed data, best compression, uncompressed size >= 17860
    82848         0x143A0         Zlib compressed data, best compression, uncompressed size >= 730
    84051         0x14853         PNG image, 323 x 88, 8-bit/color RGB, non-interlaced
    84165         0x148C5         Zlib compressed data, compressed, uncompressed size >= 85360
    88728         0x15A98         PNG image, 651 x 396, 8-bit/color RGBA, non-interlaced
    88842         0x15B0A         Zlib compressed data, compressed, uncompressed size >= 655360
    145843        0x239B3         PNG image, 1737 x 73, 8-bit/color RGBA, non-interlaced


Saya coba ekstrak dengan `binwalk -e`, tapi hasilnya tidak bisa dibaca. Saya coba ekstrak paksa saja file pertama:

    dd if=myped.zpaq of=x.pdf bs=33679 skip=1
    4+1 records in
    4+1 records out
    134911 bytes (135 kB) copied, 0.000437253 s, 309 MB/s

Ternyata file pdfnya bisa dibuka, dan berisi informasi tentang ZPAQ

![ZPAQ](./pdf.png?raw=true "ZPAQ")


Saya segera mencari ZPAQ, dan yang ketemu pertama adalah : [http://mattmahoney.net/dc/zpaq.html](http://mattmahoney.net/dc/zpaq.html)

Saya download filenya, compile, dan saya coba ekstrak:

    ./zpaq extract myped.zpaq -all
    zpaq v7.05 journaling archiver, compiled May 10 2015
    myped.zpaq: 7 versions, 14 files, 8 fragments, 0.168590 MB
    Extracting 0.205479 MB in 6 files -threads 1
    [1..1] -> 30592
    > 0001/flag
    [2..2] -> 43546
    > 0002/flag
    [3..5] -> 49546
    > 0003/flag
    [6..6] -> 3903
    > 0004/flag
    [7..7] -> 55814
    > 0005/flag
    [8..8] -> 22158
    > 0007/flag
    > 0007/
    > 0006/
    > 0005/
    > 0004/
    > 0003/
    > 0002/
    > 0001/

Didapatkan flag bagian 1 di file `007/flag`:

![Flag Bagian 1](./flag-part-1.png?raw=true "Flag Bagian 1")

Sekarang di mana sisanya? Saya coba buka file `0001/flag` yang ternyata merupakan file zpaq juga. Tapi ketika dicoba ekstrak:


    ./zpaq extract flag.zpaq -all 
    zpaq v7.05 journaling archiver, compiled May 11 2015
    flag.zpaq: Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    Unordered fragment tables: expected >= 2 found 1
    17 versions, 34 files, 1 fragments, 0.030580 MB
    zpaq exiting from main: empty block
    0.016 seconds (with errors)


Setelah putus asa, akhirnya saya patch source codenya supaya meneruskan jika error

```diff
--- orig-zpaq/zpaq.cpp	2015-04-18 04:25:12.000000000 +0700
+++ zpaq/zpaq.cpp	2015-05-10 19:44:54.217300070 +0700
@@ -3519,7 +3519,7 @@
   if (block.size()<1) error("archive is empty");
   for (unsigned i=1; i<block.size(); ++i) {
     if (block[i].start<block[i-1].start) error("unordered blocks");
-    if (block[i].start==block[i-1].start) error("empty block");
+    //if (block[i].start==block[i-1].start) error("empty block");
     if (block[i].start<1) error("block starts at fragment 0");
     if (block[i].start>=ht.size()) error("block start too high");
   }
```

TODO: bahas lebih detail proses ekstrasi flagnya.

Flag didapatkan dengan mengekstrak tiap versi file, masing-masing berisi satu karakter flag, sampai karakter terakhir.
 
 
