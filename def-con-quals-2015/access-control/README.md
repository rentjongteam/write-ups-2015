# Access control

**Kategori:** Reverse Engineering
**Points:** 1
**Deskripsi**

> It's all about who you know and what you want.
>
> access_control_server_f380fcad6e9b2cdb3c73c651824222dc.quals.shallweplayaga.me:17069
>
> [Download Client](http://downloads.notmalware.ru/client_197010ce28dffd35bf00ffc56e3aeb9f)

## Write-up

Kita diberikan binary yang merupakan client untuk sebuah server. Pertama kita diminta memasukkan message, dari reversing bisa dilihat bahwa teks yang diminta adalah `hack the world`. Dengan user bawaan (`grumpy`), bisa login, tapi tidak boleh membaca key. 


	yohanes@olivia:~$ ./client_197010ce28dffd35bf00ffc56e3aeb9f 54.84.39.118
	Socket created
	Enter message : hack the world
	<< connection ID: o2v]"6gvOb3N*4


	*** Welcome to the ACME data retrieval service ***
	what version is your client?

	<< hello...who is this?
	<< 

	<< enter user password

	<< hello grumpy, what would you like to do?

	<< grumpy
	<< 
	mrvito
	gynophage
	selir
	jymbolia
	sirgoon
	duchess
	deadwood
	hello grumpy, what would you like to do?

	<< the key is not accessible from this account. your administrator has been notified.


Di situ terlihat ada beberapa user yang mungkin. Dengan patching sederhana, kita bisa mencoba user `selir` dan `mrvito` tanpa perlu reversing algoritma autentikasi. Kedua user tersebut gampang karena panjang stringnya kurang atau sama dengan `grumpy`. Untuk user yang lain, saya ubah dulu pointernya, saya timpa string `Send failed` dengan nama user, lalu saya jalankan.

Setelah mencoba-coba semua user, user yang diperbolehkan membaca key adalah `duchess`. Tapi ternyata ketika `print key`, diminta challenge. Saya agak malas mengimplementasikan ulang algoritma challenge dan algoritma autentikasi, jadi saya memakai teknik LD_PRELOAD jadi saya bisa menggunakan kode yang ada, dan cukup memanggil kode yang sudah ada.

	gcc  -shared -m32 recv.c -ldl -fPIC -o rec.so

Untuk menjalankannya, saya menggunakan client yang sudah saya patch menjadi `client_duchess`

         LD_PRELOAD=./rec.so ./client_duchess 52.74.123.29

Inilah patch yang saya lakukan di level assembly:

```diff
--- c_grumpy    2015-05-18 19:05:02.026886379 +0700
+++ c_duchess   2015-05-18 19:05:15.484154070 +0700
@@ -1,5 +1,5 @@

-client_197010ce28dffd35bf00ffc56e3aeb9f:     file format elf32-i386
+client_duchess:     file format elf32-i386


 Disassembly of section .init:
@@ -339,7 +339,7 @@
  8048939:      e9 96 03 00 00          jmp    8048cd4 <send@plt+0x6d4>
  804893e:      c7 04 24 64 91 04 08    movl   $0x8049164,(%esp)
  8048945:      e8 f4 04 00 00          call   8048e3e <send@plt+0x83e>
- 804894a:      b8 6c 91 04 08          mov    $0x804916c,%eax
+ 804894a:      b8 2e 92 04 08          mov    $0x804922e,%eax
  804894f:      8b 10                   mov    (%eax),%edx
  8048951:      89 15 72 b4 04 08       mov    %edx,0x804b472
  8048957:      0f b7 50 04             movzwl 0x4(%eax),%edx
@@ -357,7 +357,7 @@
  8048994:      66 c7 40 04 00 00       movw   $0x0,0x4(%eax)
  804899a:      8d 84 24 80 00 00 00    lea    0x80(%esp),%eax
  80489a1:      89 44 24 04             mov    %eax,0x4(%esp)
- 80489a5:      c7 04 24 6c 91 04 08    movl   $0x804916c,(%esp)
+ 80489a5:      c7 04 24 2e 92 04 08    movl   $0x804922e,(%esp)
  80489ac:      e8 fa 04 00 00          call   8048eab <send@plt+0x8ab>
  80489b1:      8d 84 24 80 00 00 00    lea    0x80(%esp),%eax
  80489b8:      89 04 24                mov    %eax,(%esp)
```

Dan inilah jika dilihat di level hex (lihat string `grumpy` menjadi `duchess`):

```diff
yohanes@ubuntu:~$ diff -ruN c1 c2
--- c1  2015-05-18 19:08:10.720494512 +0700
+++ c2  2015-05-18 19:09:37.932867132 +0700
@@ -146,13 +146,13 @@
 00000910  04 24 3e 91 04 08 e8 23  05 00 00 c7 04 24 4f 91  |.$>....#.....$O.|
 00000920  04 08 e8 d3 03 00 00 85  c0 0f 84 a5 03 00 00 c7  |................|
 00000930  05 68 b4 04 08 01 00 00  00 e9 96 03 00 00 c7 04  |.h..............|
-00000940  24 64 91 04 08 e8 f4 04  00 00 b8 6c 91 04 08 8b  |$d.........l....|
+00000940  24 64 91 04 08 e8 f4 04  00 00 b8 2e 92 04 08 8b  |$d..............|
 00000950  10 89 15 72 b4 04 08 0f  b7 50 04 66 89 15 76 b4  |...r.....P.f..v.|
 00000960  04 08 0f b6 40 06 a2 78  b4 04 08 c7 04 24 73 91  |....@..x.....$s.|
 00000970  04 08 e8 83 03 00 00 c7  04 24 73 91 04 08 e8 77  |.........$s....w|
 00000980  03 00 00 85 c0 74 73 8d  84 24 80 00 00 00 c7 00  |.....ts..$......|
 00000990  00 00 00 00 66 c7 40 04  00 00 8d 84 24 80 00 00  |....f.@.....$...|
-000009a0  00 89 44 24 04 c7 04 24  6c 91 04 08 e8 fa 04 00  |..D$...$l.......|
+000009a0  00 89 44 24 04 c7 04 24  2e 92 04 08 e8 fa 04 00  |..D$...$........|
 000009b0  00 8d 84 24 80 00 00 00  89 04 24 e8 a7 05 00 00  |...$......$.....|
 000009c0  c6 84 24 85 00 00 00 00  b8 87 91 04 08 8d 94 24  |..$............$|
 000009d0  80 00 00 00 89 54 24 08  89 44 24 04 8d 84 24 80  |.....T$..D$...$.|
@@ -276,7 +276,7 @@
 00001130  20 79 6f 75 72 20 63 6c  69 65 6e 74 3f 00 76 65  | your client?.ve|
 00001140  72 73 69 6f 6e 20 33 2e  31 31 2e 35 34 0a 00 68  |rsion 3.11.54..h|
 00001150  65 6c 6c 6f 2e 2e 2e 77  68 6f 20 69 73 20 74 68  |ello...who is th|
-00001160  69 73 3f 00 67 72 75 6d  70 79 0a 00 67 72 75 6d  |is?.grumpy..grum|
+00001160  69 73 3f 00 64 75 63 68  65 73 73 0a 00 00 00 6d  |is?.duchess....m|
 00001170  70 79 00 65 6e 74 65 72  20 75 73 65 72 20 70 61  |py.enter user pa|
 00001180  73 73 77 6f 72 64 00 25  73 0a 00 00 68 65 6c 6c  |ssword.%s...hell|
 00001190  6f 20 25 73 2c 20 77 68  61 74 20 77 6f 75 6c 64  |o %s, what would|
@@ -288,8 +288,8 @@
 000011f0  72 65 63 76 20 66 61 69  6c 65 64 00 3c 3c 20 25  |recv failed.<< %|
 00001200  73 0a 00 63 6f 6e 6e 65  63 74 69 6f 6e 20 49 44  |s..connection ID|
 00001210  3a 00 63 6f 6e 6e 65 63  74 69 6f 6e 20 49 44 3a  |:.connection ID:|
-00001220  20 00 63 68 61 6c 6c 65  6e 67 65 3a 20 00 53 65  | .challenge: .Se|
-00001230  6e 64 20 66 61 69 6c 65  64 00 00 00 01 1b 03 3b  |nd failed......;|
+00001220  20 00 63 68 61 6c 6c 65  6e 67 65 3a 20 00 64 75  | .challenge: .du|
+00001230  63 68 65 73 73 00 00 00  64 00 00 00 01 1b 03 3b  |chess...d......;|
 00001240  50 00 00 00 09 00 00 00  b4 f2 ff ff 6c 00 00 00  |P...........l...|
 00001250  88 f4 ff ff 90 00 00 00  be fa ff ff c0 00 00 00  |................|
 00001260  02 fc ff ff ec 00 00 00  6f fc ff ff 10 01 00 00  |........o.......|
```

Hasilnya:

	yohanes@ubuntu:~$ LD_PRELOAD=./rec.so ./client_duchess 54.84.39.118
	Socket created
	Enter message : hack the world
	READ 112 connection ID: N:mGnhJ'kw?4V)


	*** Welcome to the ACME data retrieval service ***
	what version is your client?

	<< connection ID: N:mGnhJ'kw?4V)


	*** Welcome to the ACME data retrieval service ***
	what version is your client?

	LEN=16
	SEND 16 version 3.11.54

	READ 20 hello...who is this?
	<< hello...who is this?
	LEN=8
	SEND 8 duchess

	READ 1

	<<

	READ 20 enter user password

	<< enter user password

	LEN=6
	SEND 6 ^8$&-

	READ 42 hello duchess, what would you like to do?

	REQUESTING KEY
	read challenge 17 challenge: *=)O.
	at would you like to do?

	chal = '*=)O.'
	read 'answer?' 8 answer?
	e: *=)O.
	at would you like to do?

	sending response
	receiving againread flag  52: the key is: The only easy day was yesterday. 44564



Berikut ini cara kerja `recv` yang baru, saya akan mengubah flow program setelah menerima string `"what would"`:

```c
	if (strstr(buf, "what would you like")) {
		
	}
```

Di dalam if tersebut, saya paksa untuk mengirim string `"print key"`:

```c
	const char *msg = "print key\n";

        printf("REQUESTING KEY x\n");
        ssize_t x = orig_send(sockfd, msg, strlen(msg), flags);
```		

Balasan ini pasti sebuah teks `challenge: XXXXX`, saya langsung ambil dari karakter ke 11, sebanyak 5 karakter.

```c
	
		r = orig_recv(sockfd, buf, len, flags);
		printf("READ2x %d %s\n", r, buf);
		char *xc = buf + 11;
		memcpy(mem, xc, 5);
		printf ("chal = '%s'\n", mem);
```

Dan berikutnya lagi kita akan membaca teks `"answer?"`

```c
		r = orig_recv(sockfd, buf, len, flags);
		printf("read 'answer?' %d %s\n", r, buf);
```

Dan ini trik utamanya, di executable fungsi untuk komputasi challenge ada di alamat `0x8048EAB` dan `0x8048F67`, dan sebuah variabel global di `0x804B04C` perlu diset jadi `7`, karena kita berjalan di *address space* yang sama, maka fungsi ini bisa dipanggil dari dalam library yang diset di `LD_PRELOAD`

```c
		chal = 0x8048EAB;
		*(int *)0x804B04C=7;

		chal(mem, chalres);
		chal2 = 0x8048F67;
		chal2(chalres);

```

Dan terakhir kita kirimkan flagnya:

```
		strcat(chalres, "\n");
		printf ("sending response\n");
		x = orig_send(sockfd, chalres, strlen(chalres), flags);
		printf ("receiving again");
		r = orig_recv(sockfd, buf, len, flags);
		printf("read flag  %d: %s\n", r, buf);
```

Dan flagnya adalah:

     The only easy day was yesterday. 44564
