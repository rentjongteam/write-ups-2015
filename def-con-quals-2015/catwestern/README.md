# Catwestern

**Kategori:** Coding Challenge
**Points:** 1
**Deskripsi**

> catwestern_631d7907670909fc4df2defc13f2057c.quals.shallweplayaga.me 9999

## Write-up

Ketika melakukan koneksi ke server yang diberikan, maka akan muncul register 64 bit dan teks yang menyatakan bahwa N bytes akan dikirimkan, 

	****Initial Register State****
	rax=0x69e0dbcfd32015d0
	rbx=0x2166ec821bc521f4
	rcx=0x4a820a0ac809a526
	rdx=0x85515cf720ee692c
	rsi=0xaafe23d2eac425f3
	rdi=0xbd45b8a1f3b1dd64
	r8=0xda54d5e5745ebaa1
	r9=0xf69e2e991ee965c2
	r10=0xa77d65d3de30d57e
	r11=0x1a1e2f8100f1cd06
	r12=0xb6db4a0298640150
	r13=0x635f71fbe34a256d
	r14=0xa50dc7183347a21
	r15=0x9f25bfbd20205642
	****Send Solution In The Same Format****
	About to send 99 bytes: 

Dari situ bisa diduga bahwa kita diminta mengeksekusi byte-byte yang dikirimkan, dengan menggunakan nilai awal register yang diberikan. Ada banyak cara untuk melakukan ini, jadi saya ambil pendekatan yang termudah bagi saya. Pertama saya perlu membentuk kode yang akan dieksekusi, saya melakukan ini:

 * Saya buat file `test.asm`, dengan teks `bits 64` untuk menyatakan bahwa instruksi berikutnya adalah untuk arsitektur 64 bit
 * Saya masukkan semua nilai register dalam bentuk `mov rname, value`
 * Saya masukkan byte-byte yang harus dieksekusi dalam bentuk `db nilai`
 * assemble file dengan `nasm`
 
Hasil kompilasi adalah binary yang *naked*, tidak bisa dijalankan. Saya menggunakan pendekatan berikut untuk menjalankan binary yang dihasilkan

 * buat file main.c yang isinya penuh dengan `nop`
 * compile menjadi template: `gcc main.c -o template`
 * Baca isi binary `test`  ke memori, hapus `0xc3` (opcode untuk RET) di paling akhir
 * Buat salinan `template` menjadi `code` (ini ternyata tidak perlu karena kita cuma diminta mengeksekusi kode sekali saja)
 * Replace `nop` yang ada di main menjadi kode yang ada di file `test` (yang akan kita eksekusi)
 
Sekarang bagian berikutnya adalah: bagaimana mendapatkan nilai register setelah ekskeusi? Saya membuat skrip gdb yang melakukan ini:

 * membuat breakpoint di akhir fungsi main sebelum ret
 * memprint isi register dengan `info registers`
 
Isi skripnya (alamat mungkin perlu diadjust tergantung versi compiler Anda):

	set prompt 
	break *0x0000000000400789
	run
	info registers
	quit


Berikutnya saya tinggal mengeksekusi ini:

```python
os.system("gdb -q ./code  < gdb-script  > out.txt")
```

Lalu outputnya diparse. Berikut ini contoh ketika skripnya berjalan:

     yohanes@sophie:/data/yohanes/coding-defcon$ python code.py 
     ****Initial Register State****
     rax=0xd7b7a33257d522a7
     rbx=0xb9cc68e157426a29
     rcx=0xc47a1d30481318b3
     rdx=0xdcceaaa1527d03c0
     rsi=0x471fc7c0b0cea37c
     rdi=0xd71779364cfe9b4e
     r8=0x213b9c079705db52
     r9=0xe4fe3c0ac11c9d4
     r10=0xec4dd35b56654380
     r11=0xccc4813eb4b242ea
     r12=0xe7666edec0397cb8
     r13=0x5e6102204b72027b
     r14=0x3cb96d4455a98c6a
     r15=0xea683236cdfe0d7e
     ****Send Solution In The Same Format****
     About to send 89 bytes: 
     89 bytes: 

     receiving  89
     LEN  89
     4d01e34881ea5cfbdd024d87ed4981e7b8d67b4d4981cb15c8285a4981ee9645800548ffc84981c1ef00e06e490fa5f64d87c848f7d190480facd10549f7e54c0fadf9490fa4ff0b4d09e84981eb78b3cb274c01c149f7e2c3
     update code  228
     rax=0x825557aa6148a700
     rbx=0xb9cc68e157426a29
     rcx=0x5e6fe3f4ba74d903
     rdx=0x35f8634ef19ab8e2
     rsi=0x471fc7c0b0cea37c
     rdi=0xd71779364cfe9b4e
     r8=0x5e6fe3e15bf3cafb
     r9=0x213b9c079705db52
     r10=0xec4dd35b56654380
     r11=0xb42af01d57204c3f
     r12=0xe7666edec0397cb8
     r13=0x5e6102204b72027b
     r14=0x36a238fe3e058675
     r15=0x26bd021c6b8
     ----
     rax=0x825557aa6148a700
     rbx=0xb9cc68e157426a29
     rcx=0x5e6fe3f4ba74d903
     rdx=0x35f8634ef19ab8e2
     rsi=0x471fc7c0b0cea37c
     rdi=0xd71779364cfe9b4e
     r8=0x5e6fe3e15bf3cafb
     r9=0x213b9c079705db52
     r10=0xec4dd35b56654380
     r11=0xb42af01d57204c3f
     r12=0xe7666edec0397cb8
     r13=0x5e6102204b72027b
     r14=0x36a238fe3e058675
     r15=0x26bd021c6b8

     The flag is: Cats with frickin lazer beamz on top of their heads!

Jadi flagnya adalah:

     Cats with frickin lazer beamz on top of their heads!
