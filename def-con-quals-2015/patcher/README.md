# Patcher

**Kategori:** Miscellaneous
**Points:** 3
**Deskripsi**

> Patch the binary from cybergrandsandbox, and submit it [here](http://patcher_2b00042f7481c7b056c4b410d28f33c1.quals.shallweplayaga.me/patcher/)
> [Patch This](http://downloads.notmalware.ru/cybergrandsandbox_e722a7ec2ad46b9fb8472db37cb95713)

## Write-up

Menurut saya ini adalah poin tertinggi untuk soal yang sangat mudah. Dari challenge `cybergrandsandbox` sebelumnya, saya sudah menejlaskan apa masalah binary ini. Cara memperbaiki binary ini yang paling mudah adalah: meningkatkan ukuran buffer, lalu memindahkan agar alamat variabel digeser.

```diff
vagrant@cgc-linux-packer:/vagrant$ diff -ruN cgc-orig cgc
--- cgc-orig    2015-05-18 08:08:23.517608168 +0000
+++ cgc 2015-05-18 08:08:33.997348277 +0000
@@ -1,5 +1,5 @@
 
-cybergrandsandbox_e722a7ec2ad46b9fb8472db37cb95713:     file format cgc32-i386
+patched:     file format cgc32-i386
 
 
 Disassembly of section .text:
@@ -429,7 +429,7 @@
  8048787:      57                      push   %edi
  8048788:      56                      push   %esi
  8048789:      81 ec 3c 20 00 00       sub    $0x203c,%esp
- 804878f:      c7 04 24 00 00 01 00    movl   $0x10000,(%esp)
+ 804878f:      c7 04 24 00 00 09 00    movl   $0x90000,(%esp)
  8048796:      e8 ad 04 00 00          call   0x8048c48
  804879b:      85 c0                   test   %eax,%eax
  804879d:      74 2a                   je     0x80487c9
@@ -437,7 +437,7 @@
  80487a3:      89 44 24 08             mov    %eax,0x8(%esp)
  80487a7:      c7 44 24 04 01 00 00    movl   $0x1,0x4(%esp)
  80487ae:      00 
- 80487af:      c7 04 24 94 13 00 00    movl   $0x1394,(%esp)
+ 80487af:      c7 04 24 94 44 00 00    movl   $0x4494,(%esp)
  80487b6:      e8 51 10 00 00          call   0x804980c
  80487bb:      85 c0                   test   %eax,%eax
  80487bd:      74 28                   je     0x80487e7
@@ -488,7 +488,7 @@
  8048879:      8b 44 24 38             mov    0x38(%esp),%eax
  804887d:      89 80 88 13 00 00       mov    %eax,0x1388(%eax)
  8048883:      8b 44 24 38             mov    0x38(%esp),%eax
- 8048887:      8d 88 88 13 00 00       lea    0x1388(%eax),%ecx
+ 8048887:      8d 88 20 4e 00 00       lea    0x4e20(%eax),%ecx  
  804888d:      89 88 8c 13 00 00       mov    %ecx,0x138c(%eax)
  8048893:      8b 44 24 38             mov    0x38(%esp),%eax
  8048897:      c7 80 90 13 00 00 00    movl   $0x0,0x1390(%eax)
```

Saya gak membabi buta mempatch tiga lokasi sekaligus supaya yakin (dan ternyata benar dalam sekali coba)

Patch pertama: saya tingkatkan alokasi dari 0x10000 menjadi 0x90000 dan 0x1394 menjadi 0x4494. Lalu saya geser asal variabel dari 0x1388 menjadi 0x4e20

Setelah saya patch binarynya, saya menuju ke website yang diminta, lalu mengupload filenya:


	 Uploaded a DECREE executable. Testing functionality.Passed functionality tests.
	 One vulnerability appears to be patched.
	 The flag is: w3 4r3 4ll p47chw0rk, 4nd 50 5h4p3l355 4nd d1v3r53 


	 0
	 
