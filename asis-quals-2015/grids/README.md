# Grids

**Kategori:** Programming
**Points:** 300

**Deskripsi**
> In each stage send the maximun size of area that can be covered by given points as a vertex of polygon in 2D.
>
> nc 217.218.48.84 12433
>
> mirror 1 : nc 217.218.48.84 12432
>
> mirror 2 : nc 217.218.48.84 12434
>
> mirror 2 : nc 217.218.48.84 12429

## Write-up

Mencari luas bisa dilakukan dengan [Shoelace Formula](https://en.wikipedia.org/wiki/Shoelace_formula), 
tapi syaratnya semua titik harus terurut searah jarum jam (atau berlawanan arah jarum jam). 
Di soal tidak disebutkan apakah setiap titik harus masuk dalam vertex polygon, dan setelah dicoba, 
ternyata tidak semua titik harus dipakai.

Dipakai atau tidak dipakainya titik menentukan besar area maksimum polygon. 
Misalnya kita punya 5 titik, empat sudut bujur sangkar dan satu titik di tengah. 
Jika kita abaikan titik yang di tengah, maka luas polygon hanyalah panjang kali lebarnya. 
Jika titik di tengah harus jadi vertex (jadi titik sudut garis), maka luasnya akan berkurang.
 
Tadinya kode yang saya coba adalah dari [sini](https://code.activestate.com/recipes/578047-area-of-polygon-using-shoelace-formula/), tapi jawaban dianggap salah ketika titik lebih dari 4. 
Jadi akhirnya saya mengambil kesimpulan bahwa ini adalah permasalahan untuk menemukan [Convex Hull](https://en.wikipedia.org/wiki/Convex_hull), lalu mencari luasnya.

Untuk menemukan Convex Hull, saya menggunakan Scipy/Numpy, dan saya menggunakan algoritma luas yang sudah saya sebutkan linknya di atas.

 ```python
import numpy as np
from scipy.spatial import ConvexHull

def CVArea(points):
        hull = ConvexHull(points)
        verts = hull.vertices.tolist()
        newpoints = []
        for v in verts:
                newpoints.append(points[v])
        print "old ", points, " np ", newpoints
        return PolygonArea(newpoints)
```

Setelah 100 pertanyaan, didapatkan flag `ASIS{f3a8369f4194c5e44c03e5fcefb8ddf6}` 
