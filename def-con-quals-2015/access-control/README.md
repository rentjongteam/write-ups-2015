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


TODO: kode yang saya pakai akan ditambahkan.



