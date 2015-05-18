#define _GNU_SOURCE

#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
#include <sys/types.h>
#include <sys/socket.h>

const char *msg = "print key\n";


ssize_t send(int sockfd, const void *buf, size_t len, int flags)
{
	ssize_t (*orig_send)(int sockfd, const void *buf, size_t len, int flags);
        orig_send = dlsym(RTLD_NEXT, "send");
	printf("LEN=%d\n", len);
	ssize_t r = orig_send(sockfd, buf, len, flags);
	printf("SEND %d %s\n", r, buf);
	return r;

}

int (*chal)(char *a1, char *res);
int (*chal2)(char *a2);

char mem[10];
char chalres[10];

ssize_t recv(int sockfd, void *buf, size_t len, int flags)
{
	ssize_t (*orig_recv)(int sockfd, void *buf, size_t len, int flags);
        orig_recv = dlsym(RTLD_NEXT, "recv");
	ssize_t (*orig_send)(int sockfd, const void *buf, size_t len, int flags);
        orig_send = dlsym(RTLD_NEXT, "send");
	
	ssize_t r = orig_recv(sockfd, buf, len, flags);
	printf("READ %d %s\n", r, buf);
	if (strstr(buf, "what would you like")) {
		len = 100;
		//printf("requesting 2nd lin\n");
		//ssize_t r = orig_recv(sockfd, buf, len, flags);
		//printf("READx2 %d %s\n", r, buf);

		printf("REQUESTING KEY \n");
		ssize_t x = orig_send(sockfd, msg, strlen(msg), flags);
		r = orig_recv(sockfd, buf, len, flags);
		printf("read challenge %d %s\n", r, buf);
		char *xc = buf + 11;
		memcpy(mem, xc, 5);

		printf ("chal = '%s'\n", mem);

		r = orig_recv(sockfd, buf, len, flags);
		printf("read 'answer?' %d %s\n", r, buf);

		chal = 0x8048EAB;
		*(int *)0x804B04C=7;

		chal(mem, chalres);
		chal2 = 0x8048F67;
		chal2(chalres);
		strcat(chalres, "\n");
		printf ("sending response\n");
		x = orig_send(sockfd, chalres, strlen(chalres), flags);
		printf ("receiving again");
		r = orig_recv(sockfd, buf, len, flags);
		printf("read flag  %d: %s\n", r, buf);

		exit(0);	
	
	}
	return r;
}
