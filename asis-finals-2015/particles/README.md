# Particles

**Kategori:** Forensic
**Points:** 175
**Deskripsi**

> I had a bet with Gordon Kane of Michigan University that the Higgs particle wouldn't be found.
> - Stephen Hawking

## Write-up

Kita diberi sebuah file pcap. Di dalamnya ada transfer dengan protokol [zsync](http://zsync.moria.org.uk/). Setelah menghabiskan waktu cukup lama mempelajari detail file zsync, ternyata semua tidak terlalu berguna.

Cara kerja zsync cukup sederhana: protokol ini gunanya untuk mengupdate file yang ada di komputer lokal kita dengan file di remote. Pertama kita perlu mendownload file zsync yang merupakan "ringkasan" file yang ada di server. Tepatnya isi file zsync adalah checksum tiap blok. Jika ada blok yang tidak sama dengan lokal, maka kita minta ke server blok itu saja.

Pertanyaan pertama adalah: file apa yang sudah ada di lokal yang perlu dipatch? dari stream 0, kita mendapatkan SHA1: 9be3800b49e84e0c014852977557f21bcde2a775. Ternyata ini file malware: <https://github.com/eset/malware-ioc/blob/master/potao/README.adoc>. Silakan digoogle lebih lanjut untuk menemukan filenya (tidak akan saya link/upload langsung di sini).

Berikutnya yang perlu dilakukan adalah mempatch malware itu dengan potongan konten http parsial. Setelah selesai, rename `out5.bin` menjadi `out.exe`, lalu jalankan. Akan keluar error message yang merupakan flagnya.

    ASIS{c295c4f709efc00a54e77a027e36860c}


Catatan: sebelum CTF ini berakhir, ada orang yang mengupload filenya ke sever, jadi orang lain gampang menemukan jawabannya <http://www.ibrahim-elsayed.com/?p=124>

Tapi saya yang solve pertama, jadi ketika saya solve, file itu belum ada:

![pertama](./particles.jpg?raw=true Pertama")
