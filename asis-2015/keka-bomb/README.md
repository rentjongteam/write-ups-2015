# Keka Bomb

**Kategori:** Forensik
**Points:** 75

**Deskripsi**

> Find the flag in this [file](soal/keka_bomb_9e0f1863259c578f3231b5cfbc10e258).
  
## Write-up

Seperti biasa, semua file yang diberikan berformat .xz, setelah diekstrak didapatkan file 7z. 
Untuk memudahkan, file ini saya rename menjadi keka.7z
            
    $ 7z l keka.7z

    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=utf8,Utf16=on,HugeFiles=on,8 CPUs)
    
    Listing archive: keka.7z
    
    --
    Path = keka.7z
    Type = 7z
    Method = LZMA
    Solid = -
    Blocks = 16
    Physical Size = 9508910
    Headers Size = 210
    
       Date      Time    Attr         Size   Compressed  Name
    ------------------- ----- ------------ ------------  ------------------------
    2015-04-30 08:46:35 ....A   4194304000       594004  001.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  002.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  003.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  004.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  005.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  006.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  007.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  008.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  009.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  010.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  011.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  012.7z
    2015-04-30 08:46:35 ....A   4194304000       598640  013.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  014.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  015.7z
    2015-04-30 08:46:35 ....A   4194304000       594004  016.7z
    ------------------- ----- ------------ ------------  ------------------------
                               67108864000      9508700  16 files, 0 folders


Sesuai namanya, ini merupakan sejenis [Zip Bomb](https://en.wikipedia.org/wiki/Zip_bomb). 
Saya coba ekstrak file pertama, ternyata isinya 7z bomb lagi. Saya butuh strategi baru. Pertama saya cek CRC filenya:

    $ 7z -slt l keka.7z
    
    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=utf8,Utf16=on,HugeFiles=on,8 CPUs)
    
    Listing archive: keka.7z
    
    --
    Path = keka.7z
    Type = 7z
    Method = LZMA
    Solid = -
    Blocks = 16
    Physical Size = 9508910
    Headers Size = 210
    
    ----------
    Path = 001.7z
    Size = 4194304000
    Packed Size = 594004
    Modified = 2015-04-30 08:46:35
    Attributes = ....A
    CRC = ED145EFF
    Encrypted = -
    Method = LZMA:24
    Block = 0
    
    Path = 002.7z
    Size = 4194304000
    Packed Size = 594004
    Modified = 2015-04-30 08:46:35
    Attributes = ....A
    CRC = ED145EFF
    Encrypted = -
    Method = LZMA:24
    Block = 1
    
    ... dst 
            
Tidak mungkin semua file sama, jadi saya cek apakah CRC-nya sama:

    $ 7z -slt l keka.7z| grep CRC
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = 36EB76E2
    CRC = ED145EFF
    CRC = ED145EFF
    CRC = ED145EFF

Perhatikan semua file CRC-nya sama, tapi Ketika sampai file ke 13, dia beda sendiri 

    Path = 013.7z
    Size = 4194304000
    Packed Size = 598640
    Modified = 2015-04-30 08:46:35
    Attributes = ....A
    CRC = 36EB76E2
    Encrypted = -
    Method = LZMA:24
    Block = 12

Jadi saya ekstrak file ini, tapi tidak sampai penuh 

    $ 7z x keka.7z 013.7z
            
Ketika sudah beberapa detik berjalan, saya tekan control-C untuk membatalkan ekstraksi. Ketika dicek, ternyata isinya mirip dengan sebelumnya:

    $ 7z l 013.7z 
    
    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=utf8,Utf16=on,HugeFiles=on,8 CPUs)
    
    Listing archive: 013.7z
    
    --
    Path = 013.7z
    Type = 7z
    Method = LZMA
    Solid = -
    Blocks = 16
    Physical Size = 9497888
    Headers Size = 209
    
       Date      Time    Attr         Size   Compressed  Name
    ------------------- ----- ------------ ------------  ------------------------
    2015-04-30 01:32:54 ....A   4194304000       593444  0001.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0002.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0003.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0004.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0005.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0006.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0007.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0008.7z
    2015-04-30 01:32:54 ....A   4194304000       596019  0009.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0010.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0011.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0012.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0013.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0014.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0015.7z
    2015-04-30 01:32:54 ....A   4194304000       593444  0016.7z
    ------------------- ----- ------------ ------------  ------------------------
                               67108864000      9497679  16 files, 0 folders


            
Jadi teknik yang sama bisa dipakai, file `0009.7z` diekstrak, lalu di dalamnya ada `0000007.7z`, 
di dalamnya lagi ada `0000000008.7z`. Di file terakhir ini isinya berbeda:
             
     $ 7z l 0000000008.7z            
     
     7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
     p7zip Version 9.20 (locale=utf8,Utf16=on,HugeFiles=on,8 CPUs)
     
     Listing archive: 0000000008.7z
     
     --
     Path = 0000000008.7z
     Type = 7z
     Method = LZMA
     Solid = -
     Blocks = 16
     Physical Size = 9467826
     Headers Size = 212
     
        Date      Time    Attr         Size   Compressed  Name
     ------------------- ----- ------------ ------------  ------------------------
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_00
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_01
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_02
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_03
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_04
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_05
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_06
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_07
     2015-04-27 14:20:03 ....A   4194304000       591769  bomb_08
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_09
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_10
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_11
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_12
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_13
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_14
     2015-04-27 14:20:03 ....A   4194304000       591723  bomb_15
     ------------------- ----- ------------ ------------  ------------------------
                                67108864000      9467614  16 files, 0 folders
            
Dan file yang CRC-nya berbeda adalah `bomb_08`. 
File ini jika diekstrak akan butuh space sangat besar, jadi saya pipe saja ke `hexdump`. Saya memilih `hexdump` 
karena akan menampilkan hanya baris yang ada isinya saja. Di offset sekitar 2GB baru ketemu flagnya:
 
     7z x 0000000008.7z bomb_08 -so | hexdump -C
     
     7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
     p7zip Version 9.20 (locale=utf8,Utf16=on,HugeFiles=on,8 CPUs)
     
     Processing archive: 0000000008.7z
     
     Extracting  bomb_0800000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
     *
     7d000000  41 53 49 53 7b 66 39 37  34 64 61 33 32 30 33 64  |ASIS{f974da3203d|
     7d000010  31 35 35 38 32 36 39 37  34 66 34 61 36 36 37 33  |155826974f4a6673|
     7d000020  35 61 32 30 62 7d 0a 00  00 00 00 00 00 00 00 00  |5a20b}..........|
     7d000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
     *
     ^C
     
     
     Break signaled

Jadi flagnya adalah `ASIS{f974da3203d155826974f4a66735a20b}`
