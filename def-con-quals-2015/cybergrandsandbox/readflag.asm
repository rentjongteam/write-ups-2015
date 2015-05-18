    bits 32
    nop
    nop
    nop
    nop
    sub ecx, 100 
    mov eax, 3
    mov ebx, 3
    mov edx, 90
    mov esi,0
    int 0x80
    mov ebx, 1
    mov eax, 2
    int 0x80
    x:
    jmp x
