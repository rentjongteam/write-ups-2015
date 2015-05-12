# Dark

**Kategori:** Reverse
**Points:** 125
**Deskripsi**

> Find the flag in this [file](soal/dark_aba92f5882a156452b18b895c722cea6.tar.xz).

## Write-up

File ini adalah enkriptor, dan kita diberikan file flag.enc untuk didekrip.
Sebelum saya membaca kodenya, saya melakukan beberapa eksperimen: 
sepertinya berapapun jumlah karakter yang dienkrip (saya mencoba beberapa karakter) hasil enkripsinya 30215 byte.

Karena belum mendapatkan clue, saya mencoba melakukan tracing dengan ltrace. File input saya hanya berisi `abcdefghij`

        yohanes@olivia:~/dark$ ltrace ./dark a b1
        __libc_start_main(0x400715, 3, 0x7ffffb6ce468, 0x400980 <unfinished ...>
        fopen("a", "r")                                  = 0x1fde010
        fopen("b1", "wb")                                = 0x1fde250
        fread(0x7ffffb6c6cd0, 1, 30215, 0x1fde010)       = 11
        sprintf("00", "%02x", 0)                         = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 0
        sprintf("00", "%02x", 0)                         = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 0
        sprintf("00", "%02x", 0)                         = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 0
        sprintf("00", "%02x", 0)                         = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 0
        sprintf("00", "%02x", 0)                         = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 0
        sprintf("0a", "%02x", 0xa)                       = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 160
        sprintf("6a", "%02x", 0x6a)                      = 2
        strtol(0x7ffffb6ce300, 0, 16, 2)                 = 166
        sprintf("69", "%02x", 0x69)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 150
        sprintf("68", "%02x", 0x68)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 134
        sprintf("67", "%02x", 0x67)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 118
        sprintf("66", "%02x", 0x66)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 102
        sprintf("65", "%02x", 0x65)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 86
        sprintf("64", "%02x", 0x64)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 70
        sprintf("63", "%02x", 0x63)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 54
        sprintf("62", "%02x", 0x62)                      = 2
        strtol(0x7fffaf6a21f0, 0, 16, 2)                 = 38
        sprintf("61", "%02x", 0x61)                      = 2
        strtol(0x7fff53ae8010, 0, 16, 2)                 = 22
        sprintf("00", "%02x", 0)                         = 2
        strtol(0x7fff53ae8010, 0, 16, 2)                 = 0


Heksa untuk 'a' adaah 0x61, 'b' adalah 0x62, dst. Berikutnya dipanggil fungsi `strtol` terhadap sebuah string, ketika dibaca hasil decompiler:

```C
        sprintf(&s, "%02x", v15);
        nptr = printfres;
        v11 = s;
        ival = strtol(&nptr, 0LL, 16);
```

Seharusnya setelah `sprintf`, hasilnya diubah menjadi integer dengan `strtol`, tapi ternyata tidak demikian di assemblynya:


        .text:00000000004008A0                 movzx   eax, [rbp+printfres]
        .text:00000000004008A4                 mov     [rbp+nptr], al
        .text:00000000004008A7                 movzx   eax, [rbp+s]
        .text:00000000004008AB                 mov     [rbp+nptr_1], al
        .text:00000000004008AE                 lea     rax, [rbp+nptr]
        .text:00000000004008B2                 mov     edx, 10h        ; base
        .text:00000000004008B7                 mov     esi, 0          ; endptr
        .text:00000000004008BC                 mov     rdi, rax        ; nptr
        .text:00000000004008BF                 call    _strtol

Ternyata karakternya dibalik dulu, ini menjelaskan output di atas, jadi '61' (hex) dibalik nibblenya menjadi '16' (hex), lalu dikonversi menjadi desimal menjadi 22. 

Bagian decompiler yang lain cukup valid, jadi saya bisa membuat tool untuk mendecodenya menggunakan Python. Di assembly perkalian 32 bit akan menghasilkan 64 bit, dan bisa kita ekstrak 32 bitnya, tapi python menggunakan big integer, saya malas mendebugnya. Saya buat dulu file yang isinya byte 00:

         dd if=/dev/zero bs=30215 of=empty count=1
         
Karena A xor 0 = A, maka kita bisa membuat kunci enkripsi dari file itu:

         ./dark empty key.bin

Berikutnya dekripsi dilakukan dengan skrip Python ini:

```python
import sys

f1 = open(sys.argv[1], "rb").read()
f2 = open(sys.argv[2], "rb").read()
f3 = open(sys.argv[3], "wb")

def rev(x):
	m = "%02x" % ord(x)
	n = m[1] + m[0]
	return int(n, 16)

res = ""
ctr = 0 
resx = ""
for i in range(0, len(f1)):
	resx =  chr(rev(f1[i]) ^ rev(f2[i]))+ resx
	if ctr==15:
		res += resx
		resx = ""
		ctr = 0
		continue
	ctr += 1

f3.write(res)
f3.close()
```

Saya jalankan dengan:

     python xor.py flag.enc key.bin result.pdf
     

Output flag bisa dilihat di file [result.pdf](result.pdf)
