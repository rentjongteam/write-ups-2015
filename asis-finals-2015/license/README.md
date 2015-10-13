# license

**Kategori:** reverse
**Points:** 125
**Deskripsi**

> Find the flag in this file.

## Write-up

Program ini cukup sederhana: dia akan membaca sebuah file license dan jika licensenya benar, maka flag akan diprint. Pertama saya mempatch nama file, sehingga tidak mengandung karakter enter (`\n`),  agar gampang diproses dengan tool lain.

Algoritma pengecekan yang dilakukan oleh `license` adalah seperti ini:

```python
def validate(x):
    line = x.split("\n")
    print xor(line[0], line[1])=="iKWoZL" #0x400d24
    print xor3(line[3], line[1], 0x23)=="Vc4LTy"
    print xor(line[2], line[3])=="GrCRed" #compare @0x400dce
    print xor(xor3(line[4], line[3], 0x23), line[2])=="PhfEni" #compare @0x400e3d
    print line[3]=="hgyGxW"
```

Kita bisa membuat file license yang valid dengan membalik prosesnya:

```python
line = ['','','','','']

line[3] = "hgyGxW"
line[2] = xor(line[3], "GrCRed")
line[1] = xor3(line[3], "Vc4LTy", 0x23)
line[0] = xor(line[1], "iKWoZL")
line[4] = xor(xor(xorc(line[3], 0x23), "PhfEni"), line[2])

all = '\n'.join(line)

```

Setelah dijalankan:

     program successfully registered to ASIS{8d2cc30143831881f94cb05dcf0b83e0}
