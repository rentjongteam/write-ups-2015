# Saw this-1

**Kategori:** Reverse
**Points:** 100
**Deskripsi**

> Survive and get the flag!
>
> Note: This challenge contains two flags, one of them is easier to
> fetch, the other is harder. The easier flag will be clearly indicated
> as "Flag 1", the harder flag as "Flag 2". Submit the easier (Flag 1)
> here.
>
> Server running here:
>
> nc 87.107.123.3 31337


## Write-up

Saya hanya berhasil menyelesaikan flag yang mudah. Kita diminta menebak tiap bilangan yang diberikan.
Untuk bisa menebak dengan benar, kita perlu tahu nilai seed. Untungnya ada leak jika kita mengirimkan username 64 karakter.

Saya sebenarnya sudah mencoba membuat program dalam C, tapi entah kenapa hasil randomnya berbeda.
Karena tidak ingin mendebug, saya manfaatkan saja kode yang sudah ada di dalam program leach dengan memanfaatkan
preload (set.c). Intinya preload tersebut mengeset seed dari environment variable.

Dengan menjalankan `saw.py` didapatkan flag: `Flag 1: ASIS{109096cca8948d1cebee782a11d2472b}`
