#define _GNU_SOURCE

#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>

#include <math.h>
void srand(unsigned int r)
{
        void (*origsrand)(unsigned int r);
        origsrand = dlsym(RTLD_NEXT, "srand");
        int rep = atoi(getenv("SRAND"));
        printf("RANDOM %d\n", rep);
        origsrand(rep);
}

static int ctr = 0;

int rand(void)
{
        int (*origrand)(void);
        origrand = dlsym(RTLD_NEXT, "rand");

        int r = origrand();
        double d = (double)r / 2147483647.0;
        if (ctr==0) {
                int n = floor(d * 13.0 + 4.0);
                printf("Ctr = %d\n", n);
                ctr++;
        } else {
                int n = floor(d * 256);
                printf("N = %d\n", n);
                ctr++;

        }
        return r;
}
