#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <zlib.h>
#include <assert.h>


#define handle_error(msg) \
  do { perror(msg); exit(EXIT_FAILURE); } while (0)

int main(int argc, char *argv[])
{
    z_stream strm;
    int ret;

 strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;
    strm.avail_in = 0;
    strm.next_in = Z_NULL;
    ret = inflateInit(&strm);
    if (ret != Z_OK)
        return ret;

   const char *memblock;
   int fd;
   struct stat sb;

   fd = open(argv[1], O_RDONLY);
   fstat(fd, &sb);
   printf("Size: %lu\n", (uint64_t)sb.st_size);

   memblock = mmap(NULL, sb.st_size, PROT_READ, MAP_SHARED, fd, 0);
   if (memblock == MAP_FAILED) handle_error("mmap");

   for(uint64_t i = 0; i < 10; i++)
   {
     printf("[%lu]=%X ", i, memblock[i]);
   }

   printf("\n");

   fflush(stdout);

   int CHUNK = 2048;

   int avail = sb.st_size;
   const char *rr = memblock + 0x3b;

   for(uint64_t i = 0; i < 10; i++)
   {
     printf("[%lu]=%X ", i, rr[i]);
   }

   fflush(stdout);

   printf ("\n");

   char out[CHUNK];

   int bytecount = 0;
   int in_non_zero = 0;
   do {
           int rd = CHUNK;
           if (rd>avail) {
                   rd = avail;
           }
           avail -= rd;
           strm.avail_in = rd;
           strm.next_in = rr;
           rr += rd;
           /* run inflate() on input until output buffer not full */
           do {
                   strm.avail_out = CHUNK;
                   strm.next_out = out;
                   ret = inflate(&strm, Z_NO_FLUSH);
                   assert(ret != Z_STREAM_ERROR);  /* state not clobbered */
                   switch (ret) {
                   case Z_NEED_DICT:
                           printf("ERROR dict");
                           ret = Z_DATA_ERROR;     /* and fall through */
                   case Z_DATA_ERROR:
                           printf("ERROR data");
                   case Z_MEM_ERROR:
                           (void)inflateEnd(&strm);
                           printf("ERROR mem");
                           return ret;
                   }
                   int have = CHUNK - strm.avail_out;
                   int nz = 0;
                   for (int i = 0; i < have; i++) {
                           if (out[i]!=0) {
                                   nz = 1;
                                   if (!in_non_zero) {
                                           printf("[");
                                   }
                                   printf("0x%02x, ", (unsigned char) out[i]);
                                   fflush(stdout);
                                   in_non_zero = 1;
                           } else {
                                   if (in_non_zero) {
                                           printf("],\n");
                                   }
                                   in_non_zero = 0;
                           }
                   }
                   /* if (nz) { */
                   /*         for (int i = 0; i < have; i++) { */
                   /*                 printf("%02x", (unsigned char)out[i]); */
                   /*         } */
                   /*         printf("\n"); */
                   /* } */
                   bytecount += have;
           } while (strm.avail_out == 0);
           //printf("bytecount = %d\n", bytecount);4
           
   } while (ret != Z_STREAM_END);

   return 0;
}
