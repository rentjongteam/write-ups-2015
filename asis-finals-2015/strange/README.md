# Strange

**Kategori:** Forensic
**Points:** 150
**Deskripsi**

> I lost my glasses! help me!!

## Write-up

Kita diberikan file PNG yang besar sekali:

    file strang.png
    strange.png: PNG image data, 344987 x 344987, 1-bit colormap, non-interlaced

Sesuai petunjuknya, "I lost my glasses", kemungkinan ada sesuatu yang sangat kecil di gambar yang sangat besar. Karena saya tidak menemukan tools melihat gambar sebesar itu, saya buatkan tools dalam C untuk mengekstrak datanya (data PNG dikompres dengan zlib). Offset ini saya dapatkan manual dari blok `IDAT`:

```C
        const char *rr = memblock + 0x3b;
```

Compile dengan:

    gcc strange.c -std=c99 -lz
    
Catatan: awalnya saya langsung memprint kode ke layar, baru setelah tahu bahwa ada blok non zero di tengah, saya print yang itu saja. 

Setelah didapatkan isi yang relevan, saatnya melihat isi tersebut. Format gambar termudah untuk hitam putih adalah PBM. Saya cukup menambahkan header:

    P1
    320 14

Dan menuliskan teks `0` dan `1`. Ini saya lakukan dengan python (lihat skrip `strange.py`). Untuk membuat filenya:

    python strange.py > flag.pbm
    
    

Setelah itu gambar bisa mudah dilihat menggunakan editor gambar apa saja (saya memakai editor Emacs sehingga filenya bisa langsung saya buka di editor tersebut).

![flag](./flag.png?raw=true "Flag")
