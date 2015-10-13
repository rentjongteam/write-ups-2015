# What's example flag?

**Kategori:** Misc
**Points:** 1
**Deskripsi**

> Confessions of a flag...

## Write-up

Soal ini tentunya paling gampang, tapi agak mengecoh, karena flag di halaman rules adalah:

    ASIS{476f20676f6f2e676c2f67776a625466}

Tapi ternyata bukan itu flagnya. Jika kita decode hexnya:


    >>> "476f20676f6f2e676c2f67776a625466".decode("hex")
    'Go goo.gl/gwjbTf'

ternyata ada URLnya  yang menuju: 

    http://0bin.asis.io/paste/wYO8nWC1#Fef7-CVtrDG7NIb0e1W77+t2jtMF8GSbVHuo6Ajm5RQ
    
Dan teksnya:

    hi all, the flag is: ASIS{c0966ad97f120b58299cf2a727f9ca59}

Saya cukup yakin sudah melakukan ini, tapi flagnya tidak diterima. Ketika saya coba lagi beberapa jam kemudian, flagnya diterima, mungkin ada error ketika CTF baru dimulai.

