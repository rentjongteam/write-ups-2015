# Leach

**Kategori:** Reverse
**Points:** 250
**Deskripsi**

> Find the flag in this [file](soal/leach_bc83626319ab77ade5408f6ea222920e.xz).

## Write-up

Ketika file ini dijalankan hasilnya adalah "bola" yang memantul di mode teks:

![tampilan awal](./display.png?raw=true "tampilan awal")


Hasil strace menunjukkan bahwa program ini memakai `sleep` dan memanggil `time` cukup banyak.
Jadi percobaan pertama adalah membuat preload untuk sleep supaya programnya lebih cepat.

```C
unsigned int sleep(unsigned int a)
{
        return 0;
}
```

Dicompile dengan perintah:

    gcc -shared -fPIC -o s.so s.c

Tapi ketika dijalankan:

    LD_PRELOAD=./s.so ./leach

Ternyata hasilnya kacau.

Tanpa membaca programnya, saya mengambil kesimpulan bahwa program memperhatikan waktu, jadi misalnya sekarang t=0,
setelah sleep 10, maka program berharap ketika memanggil time lagi, waktu sudah t=10.
Dengan dugaan itu saya membuat preload baru:


```C
#include <unistd.h>
#include <time.h>

int xtime = 0;

time_t time(time_t *t)
{
        if (t) {
                *t = xtime;
        }
        return xtime;
}

unsigned int sleep(unsigned int a)
{
        xtime += a;
        return 0;
}
```

Dan ketika dijalankan:

         $ LD_PRELOAD=./sleep.so ./leach
        this may take too long time ... :)
        ASIS
        ##############################
        {f18b0b4f1bc6c8af21a4a53ef002f9a2}

Outputnya agak kacau sedikit, tapi flagnya adalah `ASIS{f18b0b4f1bc6c8af21a4a53ef002f9a2}`