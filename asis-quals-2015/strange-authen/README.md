# Strange Authen

**Kategori:** web
**Points:** 225
**Deskripsi**

> Go [there](http://strangeauthen.asis-ctf.ir/) and find the flag.

## Write-up

Berikut ini adalah tampilan challenge web Strange Authen

![Strange-Authen-Web](./1.png?raw=true "Strange Authen Web")

Web ini sangat sederhana dan fungsi yang berjalan di menu hanya menu login, dan untuk login kita di hadapkan dengan metode http-auth (digest).

Setelah di lakukan sedikit scanning di temukan bahwa web memiliki halaman robots.txt, yang menginformasikan beberapa direktori yang di sembunyikan dari search engine.

![robots.txt](./2.png?raw=true “robots.txt”)

Disitu kita mengetahui bahwa terdapat beberapa direktori dan file, salah satu yang cukup berguna nantinya untuk challenges ini adalah folder misc yang didalamnya terdapat file sample_traffic.pcap

![sample_traffic.pcap](./3.png?raw=true “sample_traffic.pcap”)

file pcap ini sebenarnya tidak sempurna sehingga apabila di buka dengan wireshark tidak akan langsung bisa terbuka tetapi harus di perbaiki terlebih dahulu, untuk mempercepat pekerjaan saya mempergunakan foremost untuk mengekstrak file2 didalamnya, dan ditemukan file jenis html, jpg dan png. Di file2 html inilah didapatkan hasil capture login http-digest-auth dengan user admin dan user factoreal.

![http-digest-auth](./4.png?raw=true “http-digest-auth”)

Dikarenakan dari hasil capture hanya user factoreal yang terlihat mengakses halaman login.php, maka selanjutnya saya mencoba me-replay session yang di pergunakan dan berhasil login tetapi saat mengakses file yang berkemungkinan besar terdapat flag di dalamnya masih belum berhasil, maka saya mencoba untuk melakukan crack terhadap passwordnya dengan `crack.py` dan di dapatkan user factoreal dengan password: secpass

![cracking-user-factorial-password](./5.png?raw=true “cracking user factorial password”)

Kemudian mempergunakan akun tersebut untuk login

![Login](./6.png?raw=true “Login”)

Tetapi saat mencoba mengakses file ternyata masih gagal, dan diarahkan ke halaman login.php?destroysession, setelah beberapa lama dan beberapa percobaan akhirnya saya berhasil masuk ke halaman flag “7he_most_super_s3cr3t_page.php” dengan menggunakan session dan user-agent yang terdapat di file sample_traffic.pcap untuk user factoreal.

![Request](./7.png?raw=true “Request Flag Page”)

Dan Flag tersembunyi di source HTML halaman tersebut :)

![Flag](./8.png?raw=true “Flag”)


