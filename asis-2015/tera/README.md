# Tera

**Kategori:** Reverse
**Points:** 100
**Deskripsi**

> Be patient and find the flag in this [file](soal/tera_85021482a68d6ed21892ea99b84f13f3.7z).

## Write-up

Pertama program ini berusaha mengambil file dari:

<http://darksky.slac.stanford.edu/simulations/ds14_a/ds14_a_1.0000>

File ini sangat besar (31 TB), jadi tidak mungkin bisa selesai didownload:

    yohanes@olivia:~$ curl -vX HEAD http://darksky.slac.stanford.edu/simulations/ds14_a/ds14_a_1.0000
    * Hostname was NOT found in DNS cache
    *   Trying 134.79.129.105...
    * Connected to darksky.slac.stanford.edu (134.79.129.105) port 80 (#0)
    > HEAD /simulations/ds14_a/ds14_a_1.0000 HTTP/1.1
    > User-Agent: curl/7.38.0
    > Host: darksky.slac.stanford.edu
    > Accept: */*
    >
    < HTTP/1.1 200 OK
    < Date: Mon, 11 May 2015 14:11:58 GMT
    * Server Apache/2.2.15 (Red Hat) is not blacklisted
    < Server: Apache/2.2.15 (Red Hat)
    < Last-Modified: Sat, 19 Apr 2014 23:47:45 GMT
    < ETag: "94a2a-1f40001809e0-4f76de4904a40"
    < Accept-Ranges: bytes
    < Content-Length: 34359739943392
    < Connection: close
    < Content-Type: text/plain; charset=UTF-8
    <
    * transfer closed with 34359739943392 bytes remaining to read
    * Closing connection 0

Karena tidak mungkinen membaca keseluruhan file, yang bisa kita lakukan adalah membaca kodenya.
Dari situ diketahui bahwa hanya beberapa byte saja yang dibutuhkan.

Algoritma utama kira-kira seperti ini:

```C
    for ( int ctr = 0L; ctr  <38 ; ctr++ )
      printf("%c\n", data[part1[ctr]] ^ part2[ctr]);
```

Hanya 38 byte saja yang dibutuhkan, posisinya ada di array yang saya namai `part1`, dengan mendebug programnya, didapatkan:

```python
pos = [328722382068L, 776146083715L, 980754983019L, 1334227399919L, 1664205831863L, 1785233229436L, 2912527502593L,
4712637162590L, 5281978082788L, 5508543602302L, 5918889626198L, 6310063578552L, 7884852176274L, 7962574521598L,
11157883577120L, 11492064033694L, 12517044052811L, 12758809613532L, 12941959162425L, 13721415896150L, 13769404316555L,
13822604251414L, 14925211032255L, 15812887435840L, 16731474797160L, 17281968741663L, 17698815972253L, 17730345173865L,
18592839134451L, 18948381646949L, 21051597915215L, 23068371246140L, 24563512564370L, 25552729883713L, 30361378460532L,
30412896480654L, 30691556101950L, 30776204217856L, 140737488347792L, 140737267607296L]
```

Dengan menggunakan library `requests`, saya bisa mengambil byte dalam posisi itu menggunakan header `Range`:

```python
import requests

for p in pos:

    headers = {
        "Range": "bytes=%d-%d" % (p,p)
    }

    r = requests.get("http://darksky.slac.stanford.edu/simulations/ds14_a/ds14_a_1.0000", headers=headers)

    print r.content.encode("hex")

```

Isi byte part2:

```python
a = [0xf2,0x9a,0x83,0x12,0x39,0x45,0xe7,0xf4,0x6f,0xa1,0x06,0xe7,0x95,0xf3,0x90,0xf2,0xf0,
    0x6b,0x33,0xe3,0xa8,0x78,0x37,0xd5,0x44,0x39,0x61,0x8a,0xfb,0x22,0xfa,0x9e,0xe7,0x11,
    0x39,0xa6,0xf3,0x33]
```

Jika di-xorkan dengan hasil pertama:

```python
a = [0xf2,0x9a,0x83,0x12,0x39,0x45,0xe7,0xf4,0x6f,0xa1,0x06,0xe7,0x95,0xf3,0x90,0xf2,0xf0,0x6b,
     0x33,0xe3,0xa8,0x78,0x37,0xd5,0x44,0x39,0x61,0x8a,0xfb,0x22,0xfa,0x9e,0xe7,0x11,0x39,0xa6,0xf3,0x33]

b = [0xb3,0xc9,0xca,0x41,0x42,0x76,0xd6,0xc0,0x56,0xc0,0x62,0xd2,0xf1,0xc0,0xa6,0xc0,0xc9,0x5e,
     0x0b,0xd2,0xca,0x49,0x00,0xe7,0x73,0x00,0x02,0xe9,0xc3,0x1a,0xc3,0xac,0xd5,0x23,0x5b,0x9f,0xc0,0x4e]

r = ""
for i in range(0, len(a)):
    r +=  chr(a[i]^b[i])

print r

```

Hasilnya: `ASIS{3149ad5d3629581b17279cc889222b93}`
