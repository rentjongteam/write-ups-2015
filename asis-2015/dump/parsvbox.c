#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct SSMFILEHDR
{
    /** Magic string which identifies this file as a version of VBox saved state
     *  file format (SSMFILEHDR_MAGIC_V2_0). */
    char            szMagic[32];
    /** The major version number. */
    uint16_t        u16VerMajor;
    /** The minor version number. */
    uint16_t        u16VerMinor;
    /** The build number. */
    uint32_t        u32VerBuild;
    /** The SVN revision. */
    uint32_t        u32SvnRev;
    /** 32 or 64 depending on the host. */
    uint8_t         cHostBits;
    /** The size of RTGCPHYS. */
    uint8_t         cbGCPhys;
    /** The size of RTGCPTR. */
    uint8_t         cbGCPtr;
    /** Reserved header space - must be zero. */
    uint8_t         u8Reserved;
    /** The number of units that (may) have stored data in the file. */
    uint32_t        cUnits;
    /** Flags, see SSMFILEHDR_FLAGS_XXX.  */
    uint32_t        fFlags;
    /** The maximum size of decompressed data. */
    uint32_t        cbMaxDecompr;
    /** The checksum of this header.
     * This field is set to zero when calculating the checksum. */
    uint32_t        u32CRC;
}  __attribute__((packed)) SSMFILEHDR;


/**
 * Data unit header.
 */
typedef struct SSMFILEUNITHDRV2
{
    /** Magic (SSMFILEUNITHDR_MAGIC or SSMFILEUNITHDR_END). */
    char            szMagic[8];
    /** The offset in the saved state stream of the start of this unit.
     * This is mainly intended for sanity checking. */
    uint64_t        offStream;
    /** The CRC-in-progress value this unit starts at. */
    uint32_t        u32CurStreamCRC;
    /** The checksum of this structure, including the whole name.
     * Calculated with this field set to zero.  */
    uint32_t        u32CRC;
    /** Data version. */
    uint32_t        u32Version;
    /** Instance number. */
    uint32_t        u32Instance;
    /** Data pass number. */
    uint32_t        u32Pass;
    /** Flags reserved for future extensions. Must be zero. */
    uint32_t        fFlags;
    /** Size of the data unit name including the terminator. (bytes) */
    uint32_t        cbName;
    /** Data unit name, variable size. */
    //char            szName[SSM_MAX_NAME_SIZE];
}  __attribute__((packed)) SSMFILEUNITHDRV2;


static const uint8_t UTF8ExtraBytes[256] = {
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
	2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 3,3,3,3,3,3,3,3,4,4,4,4,5,5,5,5
};

static const uint8_t FirstByteBits[7] = {
	0x00, 0x00, 0xC0, 0xE0, 0xF0, 0xF8, 0xFC
};

static const unsigned long FirstByteMask[6] = {
	0xFF, 0x1F, 0x0F, 0x07, 0x03, 0x03
};


enum {
	Low6Bits = 0x3F,	/* 00111111 */
	High2Bits = 0xC0,	/* 11000000 */
	ByteMask = 0x00BF,	/* 10111111 */
	ContinueBits = 0x80	/* 10xxxxxx */
};


long read_length(FILE *f)
{
	unsigned char ch;
	fread(&ch, 1, 1, f);
	if ((ch & 0x80)==0) {
		return ch;
	} else {
		int extra_bytes = UTF8ExtraBytes[ch];
		char extra[256];
		fread(extra, extra_bytes, 1, f);
		long res = ch & FirstByteMask[extra_bytes];
		unsigned char *src = extra;
		do {
			res <<= 6;
			res |= ((*src++) & Low6Bits);
			if (--extra_bytes == 0)
				break;
		} while (1);
		return res;
	}
}

char buf[16*1024*1024];
char outbuf[32*1024*1024];

unsigned int 
lzf_decompress (const void *const in_data,  unsigned int in_len,
                void             *out_data, unsigned int out_len);

int main(int argc, char *argv[])
{
	SSMFILEHDR head;
	char outname[1024];

	unsigned char c;
	FILE *f = fopen(argv[1], "rb");
	if (!f) {
		printf("cant open file\n");
		return 0;
	}

	fread(&head, sizeof(SSMFILEHDR), 1, f);
	printf("%s %ld\n", head.szMagic, head.cbMaxDecompr);
	SSMFILEUNITHDRV2 unit;

	while (!feof(f) && !ferror(f)) {
		fread(&unit, sizeof(SSMFILEUNITHDRV2), 1, f);
		printf("Magic %s streampos : %lld cbsize: %d\n", unit.szMagic, unit.offStream, unit.cbName);
		memset(buf, 0, sizeof(buf));
		fread(buf, unit.cbName, 1, f);
		char nn[512];
		memset(nn, 0, sizeof(nn));
		memcpy(nn, buf, unit.cbName);

		printf("CBNAME: %s\n", nn);

		sprintf(outname, "%s-%s.out", argv[1], nn);

		printf("outname: %s\n", outname);
		
		FILE *fout = fopen(outname, "wb");

		int rectype;
		while (!feof(f) && !ferror(f)) {
			fread(&c, 1, 1, f);
			printf("C=> %02x\n", c);
			rectype = c & 0xf;
			printf("RECORD TYPE %02x\n", rectype);
			if (rectype==1 || rectype==2 || rectype==3 || rectype==4) {
				long r = read_length(f);
				printf("len %ld\n", r);

				if (rectype==4) {
					int n = fread(buf, 1, 1, f);
					printf("Zero count: %d\n", buf[1]);
				} else {
					buf[r+1] = '\0';
					int n = fread(buf, 1, r, f);
					printf("READ = %d\n", n);
					//printf("BUF: %s\n", buf);
					if (rectype==2) {
						fwrite(buf, r, 1, fout);
					}

					if (rectype==3) {
						int outlen = buf[0]*1024;
						int decres = lzf_decompress(buf+1, r-1, outbuf, outlen);
						printf("Decompress result: %d\n", decres);
						fwrite(outbuf, outlen, 1, fout);
						fflush(fout);
					}
				}

				if (rectype==1) {
					break;
				}
			}
			if (rectype==00) {
				printf("INVALID TYPE\n");
				break;
			}
		}
		fclose(fout);
		if (rectype==00) {
			break;
		}
	}

	return 0;
}
