
build/fma_gemm:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64
    1004:	48 83 ec 08          	sub    rsp,0x8
    1008:	48 8b 05 d9 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd9]        # 3fe8 <__gmon_start__@Base>
    100f:	48 85 c0             	test   rax,rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   rax
    1016:	48 83 c4 08          	add    rsp,0x8
    101a:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 52 2f 00 00    	push   QWORD PTR [rip+0x2f52]        # 3f78 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	f2 ff 25 53 2f 00 00 	bnd jmp QWORD PTR [rip+0x2f53]        # 3f80 <_GLOBAL_OFFSET_TABLE_+0x10>
    102d:	0f 1f 00             	nop    DWORD PTR [rax]
    1030:	f3 0f 1e fa          	endbr64
    1034:	68 00 00 00 00       	push   0x0
    1039:	f2 e9 e1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    103f:	90                   	nop
    1040:	f3 0f 1e fa          	endbr64
    1044:	68 01 00 00 00       	push   0x1
    1049:	f2 e9 d1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    104f:	90                   	nop
    1050:	f3 0f 1e fa          	endbr64
    1054:	68 02 00 00 00       	push   0x2
    1059:	f2 e9 c1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    105f:	90                   	nop
    1060:	f3 0f 1e fa          	endbr64
    1064:	68 03 00 00 00       	push   0x3
    1069:	f2 e9 b1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    106f:	90                   	nop
    1070:	f3 0f 1e fa          	endbr64
    1074:	68 04 00 00 00       	push   0x4
    1079:	f2 e9 a1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    107f:	90                   	nop
    1080:	f3 0f 1e fa          	endbr64
    1084:	68 05 00 00 00       	push   0x5
    1089:	f2 e9 91 ff ff ff    	bnd jmp 1020 <_init+0x20>
    108f:	90                   	nop
    1090:	f3 0f 1e fa          	endbr64
    1094:	68 06 00 00 00       	push   0x6
    1099:	f2 e9 81 ff ff ff    	bnd jmp 1020 <_init+0x20>
    109f:	90                   	nop
    10a0:	f3 0f 1e fa          	endbr64
    10a4:	68 07 00 00 00       	push   0x7
    10a9:	f2 e9 71 ff ff ff    	bnd jmp 1020 <_init+0x20>
    10af:	90                   	nop
    10b0:	f3 0f 1e fa          	endbr64
    10b4:	68 08 00 00 00       	push   0x8
    10b9:	f2 e9 61 ff ff ff    	bnd jmp 1020 <_init+0x20>
    10bf:	90                   	nop

Disassembly of section .plt.got:

00000000000010c0 <__cxa_finalize@plt>:
    10c0:	f3 0f 1e fa          	endbr64
    10c4:	f2 ff 25 05 2f 00 00 	bnd jmp QWORD PTR [rip+0x2f05]        # 3fd0 <__cxa_finalize@GLIBC_2.2.5>
    10cb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

Disassembly of section .plt.sec:

00000000000010d0 <strlen@plt>:
    10d0:	f3 0f 1e fa          	endbr64
    10d4:	f2 ff 25 ad 2e 00 00 	bnd jmp QWORD PTR [rip+0x2ead]        # 3f88 <strlen@GLIBC_2.2.5>
    10db:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

00000000000010e0 <__cxa_atexit@plt>:
    10e0:	f3 0f 1e fa          	endbr64
    10e4:	f2 ff 25 a5 2e 00 00 	bnd jmp QWORD PTR [rip+0x2ea5]        # 3f90 <__cxa_atexit@GLIBC_2.2.5>
    10eb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

00000000000010f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>:
    10f0:	f3 0f 1e fa          	endbr64
    10f4:	f2 ff 25 9d 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e9d]        # 3f98 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@GLIBCXX_3.4>
    10fb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001100 <__stack_chk_fail@plt>:
    1100:	f3 0f 1e fa          	endbr64
    1104:	f2 ff 25 95 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e95]        # 3fa0 <__stack_chk_fail@GLIBC_2.4>
    110b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>:
    1110:	f3 0f 1e fa          	endbr64
    1114:	f2 ff 25 8d 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e8d]        # 3fa8 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@GLIBCXX_3.4.9>
    111b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001120 <_ZNSt8ios_base4InitC1Ev@plt>:
    1120:	f3 0f 1e fa          	endbr64
    1124:	f2 ff 25 85 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e85]        # 3fb0 <_ZNSt8ios_base4InitC1Ev@GLIBCXX_3.4>
    112b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001130 <_ZNSo9_M_insertIdEERSoT_@plt>:
    1130:	f3 0f 1e fa          	endbr64
    1134:	f2 ff 25 7d 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e7d]        # 3fb8 <_ZNSo9_M_insertIdEERSoT_@GLIBCXX_3.4.9>
    113b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001140 <_ZNSt9basic_iosIcSt11char_traitsIcEE5clearESt12_Ios_Iostate@plt>:
    1140:	f3 0f 1e fa          	endbr64
    1144:	f2 ff 25 75 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e75]        # 3fc0 <_ZNSt9basic_iosIcSt11char_traitsIcEE5clearESt12_Ios_Iostate@GLIBCXX_3.4>
    114b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001150 <_ZNSolsEi@plt>:
    1150:	f3 0f 1e fa          	endbr64
    1154:	f2 ff 25 6d 2e 00 00 	bnd jmp QWORD PTR [rip+0x2e6d]        # 3fc8 <_ZNSolsEi@GLIBCXX_3.4>
    115b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000001160 <main>:
    1160:	f3 0f 1e fa          	endbr64
    1164:	41 57                	push   r15
    1166:	b9 10 00 00 00       	mov    ecx,0x10
    116b:	4c 8d 3d ce 2e 00 00 	lea    r15,[rip+0x2ece]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    1172:	31 f6                	xor    esi,esi
    1174:	41 56                	push   r14
    1176:	41 55                	push   r13
    1178:	41 bd 20 00 00 00    	mov    r13d,0x20
    117e:	41 54                	push   r12
    1180:	55                   	push   rbp
    1181:	31 ed                	xor    ebp,ebp
    1183:	53                   	push   rbx
    1184:	48 81 ec a8 01 00 00 	sub    rsp,0x1a8
    118b:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1192:	00 00
    1194:	48 89 84 24 98 01 00 	mov    QWORD PTR [rsp+0x198],rax
    119b:	00
    119c:	31 c0                	xor    eax,eax
    119e:	48 8d 7c 24 10       	lea    rdi,[rsp+0x10]
    11a3:	4c 8d 64 24 10       	lea    r12,[rsp+0x10]
    11a8:	4c 8d b4 24 90 00 00 	lea    r14,[rsp+0x90]
    11af:	00
    11b0:	f3 48 ab             	rep stos QWORD PTR es:[rdi],rax
    11b3:	48 8d bc 24 90 00 00 	lea    rdi,[rsp+0x90]
    11ba:	00
    11bb:	b9 10 00 00 00       	mov    ecx,0x10
    11c0:	f3 48 ab             	rep stos QWORD PTR es:[rdi],rax
    11c3:	48 8b 05 76 2e 00 00 	mov    rax,QWORD PTR [rip+0x2e76]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    11ca:	4c 89 e7             	mov    rdi,r12
    11cd:	48 8b 50 e8          	mov    rdx,QWORD PTR [rax-0x18]
    11d1:	4c 01 fa             	add    rdx,r15
    11d4:	8b 42 18             	mov    eax,DWORD PTR [rdx+0x18]
    11d7:	48 c7 42 08 02 00 00 	mov    QWORD PTR [rdx+0x8],0x2
    11de:	00
    11df:	25 fb fe ff ff       	and    eax,0xfffffefb
    11e4:	83 c8 04             	or     eax,0x4
    11e7:	89 42 18             	mov    DWORD PTR [rdx+0x18],eax
    11ea:	e8 d1 04 00 00       	call   16c0 <_Z8gemm_fmaRA4_A4_db>
    11ef:	be 01 00 00 00       	mov    esi,0x1
    11f4:	4c 89 f7             	mov    rdi,r14
    11f7:	e8 c4 04 00 00       	call   16c0 <_Z8gemm_fmaRA4_A4_db>
    11fc:	4c 89 e6             	mov    rsi,r12
    11ff:	48 8d 3d 41 0e 00 00 	lea    rdi,[rip+0xe41]        # 2047 <_IO_stdin_used+0x47>
    1206:	e8 15 07 00 00       	call   1920 <_Z12print_matrixPKcRA4_A4_Kd>
    120b:	4c 89 f6             	mov    rsi,r14
    120e:	48 8d 3d 43 0e 00 00 	lea    rdi,[rip+0xe43]        # 2058 <_IO_stdin_used+0x58>
    1215:	e8 06 07 00 00       	call   1920 <_Z12print_matrixPKcRA4_A4_Kd>
    121a:	48 8d 35 46 0e 00 00 	lea    rsi,[rip+0xe46]        # 2067 <_IO_stdin_used+0x67>
    1221:	4c 89 ff             	mov    rdi,r15
    1224:	e8 c7 fe ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1229:	c5 d9 57 e4          	vxorpd xmm4,xmm4,xmm4
    122d:	c5 fb 11 24 24       	vmovsd QWORD PTR [rsp],xmm4
    1232:	49 8d 5d e0          	lea    rbx,[r13-0x20]
    1236:	c4 c1 7b 10 04 1e    	vmovsd xmm0,QWORD PTR [r14+rbx*1]
    123c:	31 c0                	xor    eax,eax
    123e:	c4 c1 7b 5c 04 1c    	vsubsd xmm0,xmm0,QWORD PTR [r12+rbx*1]
    1244:	4c 89 ff             	mov    rdi,r15
    1247:	c5 f9 54 0d 21 10 00 	vandpd xmm1,xmm0,XMMWORD PTR [rip+0x1021]        # 2270 <_ZL1A+0x110>
    124e:	00
    124f:	c5 f9 2f 0d b9 0f 00 	vcomisd xmm1,QWORD PTR [rip+0xfb9]        # 2210 <_ZL1A+0xb0>
    1256:	00
    1257:	c5 f3 5f 14 24       	vmaxsd xmm2,xmm1,QWORD PTR [rsp]
    125c:	0f 97 c0             	seta   al
    125f:	48 83 c3 08          	add    rbx,0x8
    1263:	01 c5                	add    ebp,eax
    1265:	49 8b 07             	mov    rax,QWORD PTR [r15]
    1268:	c5 fb 11 14 24       	vmovsd QWORD PTR [rsp],xmm2
    126d:	48 8b 40 e8          	mov    rax,QWORD PTR [rax-0x18]
    1271:	49 c7 44 07 10 0a 00 	mov    QWORD PTR [r15+rax*1+0x10],0xa
    1278:	00 00
    127a:	e8 b1 fe ff ff       	call   1130 <_ZNSo9_M_insertIdEERSoT_@plt>
    127f:	49 39 dd             	cmp    r13,rbx
    1282:	75 b2                	jne    1236 <main+0xd6>
    1284:	ba 01 00 00 00       	mov    edx,0x1
    1289:	48 8d 35 ea 0d 00 00 	lea    rsi,[rip+0xdea]        # 207a <_IO_stdin_used+0x7a>
    1290:	4c 89 ff             	mov    rdi,r15
    1293:	49 83 c5 20          	add    r13,0x20
    1297:	e8 74 fe ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    129c:	49 81 fd a0 00 00 00 	cmp    r13,0xa0
    12a3:	75 8d                	jne    1232 <main+0xd2>
    12a5:	48 8b 05 6c 0f 00 00 	mov    rax,QWORD PTR [rip+0xf6c]        # 2218 <_ZL1A+0xb8>
    12ac:	c5 fb 10 0d 9c 0f 00 	vmovsd xmm1,QWORD PTR [rip+0xf9c]        # 2250 <_ZL1A+0xf0>
    12b3:	00
    12b4:	ba 20 00 00 00       	mov    edx,0x20
    12b9:	31 f6                	xor    esi,esi
    12bb:	c5 fb 10 05 5d 0f 00 	vmovsd xmm0,QWORD PTR [rip+0xf5d]        # 2220 <_ZL1A+0xc0>
    12c2:	00
    12c3:	bb 01 00 00 00       	mov    ebx,0x1
    12c8:	48 89 84 24 18 01 00 	mov    QWORD PTR [rsp+0x118],rax
    12cf:	00
    12d0:	48 8b 05 51 0f 00 00 	mov    rax,QWORD PTR [rip+0xf51]        # 2228 <_ZL1A+0xc8>
    12d7:	c5 fb 11 8c 24 50 01 	vmovsd QWORD PTR [rsp+0x150],xmm1
    12de:	00 00
    12e0:	48 89 84 24 28 01 00 	mov    QWORD PTR [rsp+0x128],rax
    12e7:	00
    12e8:	48 8b 05 41 0f 00 00 	mov    rax,QWORD PTR [rip+0xf41]        # 2230 <_ZL1A+0xd0>
    12ef:	c5 fb 11 8c 24 58 01 	vmovsd QWORD PTR [rsp+0x158],xmm1
    12f6:	00 00
    12f8:	48 89 84 24 30 01 00 	mov    QWORD PTR [rsp+0x130],rax
    12ff:	00
    1300:	48 8b 05 31 0f 00 00 	mov    rax,QWORD PTR [rip+0xf31]        # 2238 <_ZL1A+0xd8>
    1307:	c5 fb 11 8c 24 60 01 	vmovsd QWORD PTR [rsp+0x160],xmm1
    130e:	00 00
    1310:	c5 fb 10 0d 40 0f 00 	vmovsd xmm1,QWORD PTR [rip+0xf40]        # 2258 <_ZL1A+0xf8>
    1317:	00
    1318:	48 89 84 24 38 01 00 	mov    QWORD PTR [rsp+0x138],rax
    131f:	00
    1320:	48 8b 05 19 0f 00 00 	mov    rax,QWORD PTR [rip+0xf19]        # 2240 <_ZL1A+0xe0>
    1327:	c5 fb 11 8c 24 68 01 	vmovsd QWORD PTR [rsp+0x168],xmm1
    132e:	00 00
    1330:	48 89 84 24 40 01 00 	mov    QWORD PTR [rsp+0x140],rax
    1337:	00
    1338:	48 8b 05 09 0f 00 00 	mov    rax,QWORD PTR [rip+0xf09]        # 2248 <_ZL1A+0xe8>
    133f:	c5 fb 11 8c 24 78 01 	vmovsd QWORD PTR [rsp+0x178],xmm1
    1346:	00 00
    1348:	c5 fb 10 0d b8 0e 00 	vmovsd xmm1,QWORD PTR [rip+0xeb8]        # 2208 <_ZL1A+0xa8>
    134f:	00
    1350:	48 89 84 24 48 01 00 	mov    QWORD PTR [rsp+0x148],rax
    1357:	00
    1358:	48 8b 05 01 0f 00 00 	mov    rax,QWORD PTR [rip+0xf01]        # 2260 <_ZL1A+0x100>
    135f:	c5 fb 11 84 24 20 01 	vmovsd QWORD PTR [rsp+0x120],xmm0
    1366:	00 00
    1368:	48 89 84 24 70 01 00 	mov    QWORD PTR [rsp+0x170],rax
    136f:	00
    1370:	c5 fb 11 84 24 80 01 	vmovsd QWORD PTR [rsp+0x180],xmm0
    1377:	00 00
    1379:	c5 fb 11 84 24 88 01 	vmovsd QWORD PTR [rsp+0x188],xmm0
    1380:	00 00
    1382:	48 8d 42 e0          	lea    rax,[rdx-0x20]
    1386:	c4 c1 7b 10 04 04    	vmovsd xmm0,QWORD PTR [r12+rax*1]
    138c:	c5 fb 5c c1          	vsubsd xmm0,xmm0,xmm1
    1390:	c5 f9 54 05 d8 0e 00 	vandpd xmm0,xmm0,XMMWORD PTR [rip+0xed8]        # 2270 <_ZL1A+0x110>
    1397:	00
    1398:	c5 f9 2e 05 70 0e 00 	vucomisd xmm0,QWORD PTR [rip+0xe70]        # 2210 <_ZL1A+0xb0>
    139f:	00
    13a0:	0f 47 de             	cmova  ebx,esi
    13a3:	48 83 c0 08          	add    rax,0x8
    13a7:	48 39 c2             	cmp    rdx,rax
    13aa:	74 14                	je     13c0 <main+0x260>
    13ac:	c5 fb 10 8c 04 10 01 	vmovsd xmm1,QWORD PTR [rsp+rax*1+0x110]
    13b3:	00 00
    13b5:	eb cf                	jmp    1386 <main+0x226>
    13b7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    13be:	00 00
    13c0:	48 81 fa 80 00 00 00 	cmp    rdx,0x80
    13c7:	74 17                	je     13e0 <main+0x280>
    13c9:	c5 fb 10 8c 14 10 01 	vmovsd xmm1,QWORD PTR [rsp+rdx*1+0x110]
    13d0:	00 00
    13d2:	48 83 c2 20          	add    rdx,0x20
    13d6:	eb aa                	jmp    1382 <main+0x222>
    13d8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
    13df:	00
    13e0:	83 fd 01             	cmp    ebp,0x1
    13e3:	0f 84 bd 00 00 00    	je     14a6 <main+0x346>
    13e9:	48 8d 35 8c 0c 00 00 	lea    rsi,[rip+0xc8c]        # 207c <_IO_stdin_used+0x7c>
    13f0:	4c 89 ff             	mov    rdi,r15
    13f3:	e8 f8 fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    13f8:	89 ee                	mov    esi,ebp
    13fa:	48 89 c7             	mov    rdi,rax
    13fd:	e8 4e fd ff ff       	call   1150 <_ZNSolsEi@plt>
    1402:	48 8d 35 87 0c 00 00 	lea    rsi,[rip+0xc87]        # 2090 <_IO_stdin_used+0x90>
    1409:	4c 89 ff             	mov    rdi,r15
    140c:	e8 df fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1411:	c5 fb 10 04 24       	vmovsd xmm0,QWORD PTR [rsp]
    1416:	48 89 c7             	mov    rdi,rax
    1419:	e8 12 fd ff ff       	call   1130 <_ZNSo9_M_insertIdEERSoT_@plt>
    141e:	4c 89 ff             	mov    rdi,r15
    1421:	48 8d 35 7e 0c 00 00 	lea    rsi,[rip+0xc7e]        # 20a6 <_IO_stdin_used+0xa6>
    1428:	e8 c3 fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    142d:	48 89 c7             	mov    rdi,rax
    1430:	84 db                	test   bl,bl
    1432:	0f 84 29 01 00 00    	je     1561 <main+0x401>
    1438:	48 8d 35 fe 0b 00 00 	lea    rsi,[rip+0xbfe]        # 203d <_IO_stdin_used+0x3d>
    143f:	31 ed                	xor    ebp,ebp
    1441:	e8 aa fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1446:	48 8d 35 6b 0c 00 00 	lea    rsi,[rip+0xc6b]        # 20b8 <_IO_stdin_used+0xb8>
    144d:	4c 89 ff             	mov    rdi,r15
    1450:	e8 9b fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1455:	48 8d 35 e6 0b 00 00 	lea    rsi,[rip+0xbe6]        # 2042 <_IO_stdin_used+0x42>
    145c:	48 89 c7             	mov    rdi,rax
    145f:	e8 8c fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1464:	48 8d 35 0f 0c 00 00 	lea    rsi,[rip+0xc0f]        # 207a <_IO_stdin_used+0x7a>
    146b:	48 89 c7             	mov    rdi,rax
    146e:	e8 7d fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1473:	89 d8                	mov    eax,ebx
    1475:	21 e8                	and    eax,ebp
    1477:	83 f0 01             	xor    eax,0x1
    147a:	0f b6 c0             	movzx  eax,al
    147d:	48 8b 94 24 98 01 00 	mov    rdx,QWORD PTR [rsp+0x198]
    1484:	00
    1485:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    148c:	00 00
    148e:	0f 85 f8 00 00 00    	jne    158c <main+0x42c>
    1494:	48 81 c4 a8 01 00 00 	add    rsp,0x1a8
    149b:	5b                   	pop    rbx
    149c:	5d                   	pop    rbp
    149d:	41 5c                	pop    r12
    149f:	41 5d                	pop    r13
    14a1:	41 5e                	pop    r14
    14a3:	41 5f                	pop    r15
    14a5:	c3                   	ret
    14a6:	c5 fb 10 84 24 c0 00 	vmovsd xmm0,QWORD PTR [rsp+0xc0]
    14ad:	00 00
    14af:	c5 fb 5c 44 24 40    	vsubsd xmm0,xmm0,QWORD PTR [rsp+0x40]
    14b5:	48 8d 35 c0 0b 00 00 	lea    rsi,[rip+0xbc0]        # 207c <_IO_stdin_used+0x7c>
    14bc:	4c 89 ff             	mov    rdi,r15
    14bf:	c5 fb 5c 05 39 0d 00 	vsubsd xmm0,xmm0,QWORD PTR [rip+0xd39]        # 2200 <_ZL1A+0xa0>
    14c6:	00
    14c7:	c5 f9 54 2d a1 0d 00 	vandpd xmm5,xmm0,XMMWORD PTR [rip+0xda1]        # 2270 <_ZL1A+0x110>
    14ce:	00
    14cf:	4c 8d 35 6c 0b 00 00 	lea    r14,[rip+0xb6c]        # 2042 <_IO_stdin_used+0x42>
    14d6:	4c 8d 2d 60 0b 00 00 	lea    r13,[rip+0xb60]        # 203d <_IO_stdin_used+0x3d>
    14dd:	c5 fb 11 6c 24 08    	vmovsd QWORD PTR [rsp+0x8],xmm5
    14e3:	e8 08 fc ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    14e8:	be 01 00 00 00       	mov    esi,0x1
    14ed:	48 89 c7             	mov    rdi,rax
    14f0:	e8 5b fc ff ff       	call   1150 <_ZNSolsEi@plt>
    14f5:	48 8d 35 94 0b 00 00 	lea    rsi,[rip+0xb94]        # 2090 <_IO_stdin_used+0x90>
    14fc:	4c 89 ff             	mov    rdi,r15
    14ff:	e8 ec fb ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1504:	c5 fb 10 04 24       	vmovsd xmm0,QWORD PTR [rsp]
    1509:	48 89 c7             	mov    rdi,rax
    150c:	e8 1f fc ff ff       	call   1130 <_ZNSo9_M_insertIdEERSoT_@plt>
    1511:	48 8d 35 8e 0b 00 00 	lea    rsi,[rip+0xb8e]        # 20a6 <_IO_stdin_used+0xa6>
    1518:	4c 89 ff             	mov    rdi,r15
    151b:	e8 d0 fb ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1520:	84 db                	test   bl,bl
    1522:	4c 89 f6             	mov    rsi,r14
    1525:	49 0f 45 f5          	cmovne rsi,r13
    1529:	48 89 c7             	mov    rdi,rax
    152c:	e8 bf fb ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1531:	48 8d 35 80 0b 00 00 	lea    rsi,[rip+0xb80]        # 20b8 <_IO_stdin_used+0xb8>
    1538:	4c 89 ff             	mov    rdi,r15
    153b:	e8 b0 fb ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1540:	c5 fb 10 35 c8 0c 00 	vmovsd xmm6,QWORD PTR [rip+0xcc8]        # 2210 <_ZL1A+0xb0>
    1547:	00
    1548:	4c 89 f6             	mov    rsi,r14
    154b:	c5 f9 2f 74 24 08    	vcomisd xmm6,QWORD PTR [rsp+0x8]
    1551:	48 89 c7             	mov    rdi,rax
    1554:	49 0f 47 f5          	cmova  rsi,r13
    1558:	40 0f 97 c5          	seta   bpl
    155c:	e9 fe fe ff ff       	jmp    145f <main+0x2ff>
    1561:	4c 8d 2d da 0a 00 00 	lea    r13,[rip+0xada]        # 2042 <_IO_stdin_used+0x42>
    1568:	31 ed                	xor    ebp,ebp
    156a:	4c 89 ee             	mov    rsi,r13
    156d:	e8 7e fb ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1572:	48 8d 35 3f 0b 00 00 	lea    rsi,[rip+0xb3f]        # 20b8 <_IO_stdin_used+0xb8>
    1579:	4c 89 ff             	mov    rdi,r15
    157c:	e8 6f fb ff ff       	call   10f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1581:	4c 89 ee             	mov    rsi,r13
    1584:	48 89 c7             	mov    rdi,rax
    1587:	e9 d3 fe ff ff       	jmp    145f <main+0x2ff>
    158c:	e8 6f fb ff ff       	call   1100 <__stack_chk_fail@plt>
    1591:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    1598:	00 00 00 00
    159c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

00000000000015a0 <_GLOBAL__sub_I__Z8gemm_fmaRA4_A4_db>:
    15a0:	f3 0f 1e fa          	endbr64
    15a4:	55                   	push   rbp
    15a5:	48 8d 2d a5 2b 00 00 	lea    rbp,[rip+0x2ba5]        # 4151 <_ZStL8__ioinit>
    15ac:	48 89 ef             	mov    rdi,rbp
    15af:	e8 6c fb ff ff       	call   1120 <_ZNSt8ios_base4InitC1Ev@plt>
    15b4:	48 8b 3d 3d 2a 00 00 	mov    rdi,QWORD PTR [rip+0x2a3d]        # 3ff8 <_ZNSt8ios_base4InitD1Ev@GLIBCXX_3.4>
    15bb:	48 89 ee             	mov    rsi,rbp
    15be:	5d                   	pop    rbp
    15bf:	48 8d 15 42 2a 00 00 	lea    rdx,[rip+0x2a42]        # 4008 <__dso_handle>
    15c6:	e9 15 fb ff ff       	jmp    10e0 <__cxa_atexit@plt>
    15cb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

00000000000015d0 <_start>:
    15d0:	f3 0f 1e fa          	endbr64
    15d4:	31 ed                	xor    ebp,ebp
    15d6:	49 89 d1             	mov    r9,rdx
    15d9:	5e                   	pop    rsi
    15da:	48 89 e2             	mov    rdx,rsp
    15dd:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    15e1:	50                   	push   rax
    15e2:	54                   	push   rsp
    15e3:	45 31 c0             	xor    r8d,r8d
    15e6:	31 c9                	xor    ecx,ecx
    15e8:	48 8d 3d 71 fb ff ff 	lea    rdi,[rip+0xfffffffffffffb71]        # 1160 <main>
    15ef:	ff 15 e3 29 00 00    	call   QWORD PTR [rip+0x29e3]        # 3fd8 <__libc_start_main@GLIBC_2.34>
    15f5:	f4                   	hlt
    15f6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    15fd:	00 00 00

0000000000001600 <deregister_tm_clones>:
    1600:	48 8d 3d 09 2a 00 00 	lea    rdi,[rip+0x2a09]        # 4010 <__TMC_END__>
    1607:	48 8d 05 02 2a 00 00 	lea    rax,[rip+0x2a02]        # 4010 <__TMC_END__>
    160e:	48 39 f8             	cmp    rax,rdi
    1611:	74 15                	je     1628 <deregister_tm_clones+0x28>
    1613:	48 8b 05 c6 29 00 00 	mov    rax,QWORD PTR [rip+0x29c6]        # 3fe0 <_ITM_deregisterTMCloneTable@Base>
    161a:	48 85 c0             	test   rax,rax
    161d:	74 09                	je     1628 <deregister_tm_clones+0x28>
    161f:	ff e0                	jmp    rax
    1621:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1628:	c3                   	ret
    1629:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001630 <register_tm_clones>:
    1630:	48 8d 3d d9 29 00 00 	lea    rdi,[rip+0x29d9]        # 4010 <__TMC_END__>
    1637:	48 8d 35 d2 29 00 00 	lea    rsi,[rip+0x29d2]        # 4010 <__TMC_END__>
    163e:	48 29 fe             	sub    rsi,rdi
    1641:	48 89 f0             	mov    rax,rsi
    1644:	48 c1 ee 3f          	shr    rsi,0x3f
    1648:	48 c1 f8 03          	sar    rax,0x3
    164c:	48 01 c6             	add    rsi,rax
    164f:	48 d1 fe             	sar    rsi,1
    1652:	74 14                	je     1668 <register_tm_clones+0x38>
    1654:	48 8b 05 95 29 00 00 	mov    rax,QWORD PTR [rip+0x2995]        # 3ff0 <_ITM_registerTMCloneTable@Base>
    165b:	48 85 c0             	test   rax,rax
    165e:	74 08                	je     1668 <register_tm_clones+0x38>
    1660:	ff e0                	jmp    rax
    1662:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    1668:	c3                   	ret
    1669:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001670 <__do_global_dtors_aux>:
    1670:	f3 0f 1e fa          	endbr64
    1674:	80 3d d5 2a 00 00 00 	cmp    BYTE PTR [rip+0x2ad5],0x0        # 4150 <completed.0>
    167b:	75 2b                	jne    16a8 <__do_global_dtors_aux+0x38>
    167d:	55                   	push   rbp
    167e:	48 83 3d 4a 29 00 00 	cmp    QWORD PTR [rip+0x294a],0x0        # 3fd0 <__cxa_finalize@GLIBC_2.2.5>
    1685:	00
    1686:	48 89 e5             	mov    rbp,rsp
    1689:	74 0c                	je     1697 <__do_global_dtors_aux+0x27>
    168b:	48 8b 3d 76 29 00 00 	mov    rdi,QWORD PTR [rip+0x2976]        # 4008 <__dso_handle>
    1692:	e8 29 fa ff ff       	call   10c0 <__cxa_finalize@plt>
    1697:	e8 64 ff ff ff       	call   1600 <deregister_tm_clones>
    169c:	c6 05 ad 2a 00 00 01 	mov    BYTE PTR [rip+0x2aad],0x1        # 4150 <completed.0>
    16a3:	5d                   	pop    rbp
    16a4:	c3                   	ret
    16a5:	0f 1f 00             	nop    DWORD PTR [rax]
    16a8:	c3                   	ret
    16a9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000016b0 <frame_dummy>:
    16b0:	f3 0f 1e fa          	endbr64
    16b4:	e9 77 ff ff ff       	jmp    1630 <register_tm_clones>
    16b9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000016c0 <_Z8gemm_fmaRA4_A4_db>:
    16c0:	f3 0f 1e fa          	endbr64
    16c4:	4c 8d 54 24 08       	lea    r10,[rsp+0x8]
    16c9:	48 83 e4 e0          	and    rsp,0xffffffffffffffe0
    16cd:	89 f1                	mov    ecx,esi
    16cf:	41 ff 72 f8          	push   QWORD PTR [r10-0x8]
    16d3:	4c 8d 0d 66 29 00 00 	lea    r9,[rip+0x2966]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    16da:	55                   	push   rbp
    16db:	48 89 e5             	mov    rbp,rsp
    16de:	41 57                	push   r15
    16e0:	49 89 ff             	mov    r15,rdi
    16e3:	41 56                	push   r14
    16e5:	45 31 f6             	xor    r14d,r14d
    16e8:	41 55                	push   r13
    16ea:	41 54                	push   r12
    16ec:	4c 8d 25 6d 0a 00 00 	lea    r12,[rip+0xa6d]        # 2160 <_ZL1A>
    16f3:	41 52                	push   r10
    16f5:	4c 8d 15 08 09 00 00 	lea    r10,[rip+0x908]        # 2004 <_IO_stdin_used+0x4>
    16fc:	53                   	push   rbx
    16fd:	48 83 ec 60          	sub    rsp,0x60
    1701:	c5 fb 10 05 d7 0a 00 	vmovsd xmm0,QWORD PTR [rip+0xad7]        # 21e0 <_ZL1A+0x80>
    1708:	00
    1709:	c5 fd 28 1d cf 0a 00 	vmovapd ymm3,YMMWORD PTR [rip+0xacf]        # 21e0 <_ZL1A+0x80>
    1710:	00
    1711:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1718:	00 00
    171a:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
    171e:	31 c0                	xor    eax,eax
    1720:	41 83 fe 01          	cmp    r14d,0x1
    1724:	c5 fd 28 d3          	vmovapd ymm2,ymm3
    1728:	c5 f1 57 c9          	vxorpd xmm1,xmm1,xmm1
    172c:	bb 01 00 00 00       	mov    ebx,0x1
    1731:	41 0f 94 c5          	sete   r13b
    1735:	c4 e2 7d 19 c0       	vbroadcastsd ymm0,xmm0
    173a:	c4 e2 fd b8 ca       	vfmadd231pd ymm1,ymm0,ymm2
    173f:	41 21 cd             	and    r13d,ecx
    1742:	83 fb 03             	cmp    ebx,0x3
    1745:	75 09                	jne    1750 <_Z8gemm_fmaRA4_A4_db+0x90>
    1747:	45 84 ed             	test   r13b,r13b
    174a:	75 3f                	jne    178b <_Z8gemm_fmaRA4_A4_db+0xcb>
    174c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    1750:	48 83 fb 04          	cmp    rbx,0x4
    1754:	0f 84 6e 01 00 00    	je     18c8 <_Z8gemm_fmaRA4_A4_db+0x208>
    175a:	48 89 d8             	mov    rax,rbx
    175d:	c4 c1 7b 10 04 dc    	vmovsd xmm0,QWORD PTR [r12+rbx*8]
    1763:	48 8d 15 76 09 00 00 	lea    rdx,[rip+0x976]        # 20e0 <_ZL1B>
    176a:	48 83 c3 01          	add    rbx,0x1
    176e:	48 c1 e0 05          	shl    rax,0x5
    1772:	c5 fd 10 14 02       	vmovupd ymm2,YMMWORD PTR [rdx+rax*1]
    1777:	c4 e2 7d 19 c0       	vbroadcastsd ymm0,xmm0
    177c:	c4 e2 fd b8 ca       	vfmadd231pd ymm1,ymm0,ymm2
    1781:	83 fb 03             	cmp    ebx,0x3
    1784:	75 ca                	jne    1750 <_Z8gemm_fmaRA4_A4_db+0x90>
    1786:	45 84 ed             	test   r13b,r13b
    1789:	74 c5                	je     1750 <_Z8gemm_fmaRA4_A4_db+0x90>
    178b:	c5 fd 29 4d 90       	vmovapd YMMWORD PTR [rbp-0x70],ymm1
    1790:	ba 0e 00 00 00       	mov    edx,0xe
    1795:	4c 89 d6             	mov    rsi,r10
    1798:	4c 89 cf             	mov    rdi,r9
    179b:	c4 e3 7d 19 c8 01    	vextractf128 xmm0,ymm1,0x1
    17a1:	c5 fb 58 0d 57 0a 00 	vaddsd xmm1,xmm0,QWORD PTR [rip+0xa57]        # 2200 <_ZL1A+0xa0>
    17a8:	00
    17a9:	88 8d 77 ff ff ff    	mov    BYTE PTR [rbp-0x89],cl
    17af:	c5 fb 11 85 78 ff ff 	vmovsd QWORD PTR [rbp-0x88],xmm0
    17b6:	ff
    17b7:	c5 fb 11 4d a0       	vmovsd QWORD PTR [rbp-0x60],xmm1
    17bc:	c5 fb 11 4d 80       	vmovsd QWORD PTR [rbp-0x80],xmm1
    17c1:	c5 f8 77             	vzeroupper
    17c4:	e8 47 f9 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    17c9:	4c 8d 05 43 08 00 00 	lea    r8,[rip+0x843]        # 2013 <_IO_stdin_used+0x13>
    17d0:	ba 08 00 00 00       	mov    edx,0x8
    17d5:	4c 8d 0d 64 28 00 00 	lea    r9,[rip+0x2864]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    17dc:	4c 89 c6             	mov    rsi,r8
    17df:	4c 89 cf             	mov    rdi,r9
    17e2:	e8 29 f9 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    17e7:	4c 8d 0d 52 28 00 00 	lea    r9,[rip+0x2852]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    17ee:	be 01 00 00 00       	mov    esi,0x1
    17f3:	4c 89 cf             	mov    rdi,r9
    17f6:	e8 55 f9 ff ff       	call   1150 <_ZNSolsEi@plt>
    17fb:	ba 04 00 00 00       	mov    edx,0x4
    1800:	48 8d 35 15 08 00 00 	lea    rsi,[rip+0x815]        # 201c <_IO_stdin_used+0x1c>
    1807:	48 89 c7             	mov    rdi,rax
    180a:	48 89 45 88          	mov    QWORD PTR [rbp-0x78],rax
    180e:	e8 fd f8 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    1813:	48 8b 7d 88          	mov    rdi,QWORD PTR [rbp-0x78]
    1817:	be 02 00 00 00       	mov    esi,0x2
    181c:	e8 2f f9 ff ff       	call   1150 <_ZNSolsEi@plt>
    1821:	ba 08 00 00 00       	mov    edx,0x8
    1826:	48 8d 35 f4 07 00 00 	lea    rsi,[rip+0x7f4]        # 2021 <_IO_stdin_used+0x21>
    182d:	48 89 c7             	mov    rdi,rax
    1830:	48 89 45 88          	mov    QWORD PTR [rbp-0x78],rax
    1834:	e8 d7 f8 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    1839:	48 8b 7d 88          	mov    rdi,QWORD PTR [rbp-0x78]
    183d:	ba 09 00 00 00       	mov    edx,0x9
    1842:	48 8d 35 e1 07 00 00 	lea    rsi,[rip+0x7e1]        # 202a <_IO_stdin_used+0x2a>
    1849:	e8 c2 f8 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    184e:	c5 fb 10 85 78 ff ff 	vmovsd xmm0,QWORD PTR [rbp-0x88]
    1855:	ff
    1856:	48 8b 7d 88          	mov    rdi,QWORD PTR [rbp-0x78]
    185a:	e8 d1 f8 ff ff       	call   1130 <_ZNSo9_M_insertIdEERSoT_@plt>
    185f:	ba 08 00 00 00       	mov    edx,0x8
    1864:	48 8d 35 c9 07 00 00 	lea    rsi,[rip+0x7c9]        # 2034 <_IO_stdin_used+0x34>
    186b:	48 89 c7             	mov    rdi,rax
    186e:	48 89 45 88          	mov    QWORD PTR [rbp-0x78],rax
    1872:	e8 99 f8 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    1877:	c5 fb 10 4d 80       	vmovsd xmm1,QWORD PTR [rbp-0x80]
    187c:	48 8b 7d 88          	mov    rdi,QWORD PTR [rbp-0x78]
    1880:	c5 f3 10 c1          	vmovsd xmm0,xmm1,xmm1
    1884:	e8 a7 f8 ff ff       	call   1130 <_ZNSo9_M_insertIdEERSoT_@plt>
    1889:	ba 01 00 00 00       	mov    edx,0x1
    188e:	48 8d 35 e5 07 00 00 	lea    rsi,[rip+0x7e5]        # 207a <_IO_stdin_used+0x7a>
    1895:	48 89 c7             	mov    rdi,rax
    1898:	e8 73 f8 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    189d:	c5 fd 28 4d 90       	vmovapd ymm1,YMMWORD PTR [rbp-0x70]
    18a2:	0f b6 8d 77 ff ff ff 	movzx  ecx,BYTE PTR [rbp-0x89]
    18a9:	4c 8d 0d 90 27 00 00 	lea    r9,[rip+0x2790]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    18b0:	c5 fd 28 1d 28 09 00 	vmovapd ymm3,YMMWORD PTR [rip+0x928]        # 21e0 <_ZL1A+0x80>
    18b7:	00
    18b8:	4c 8d 15 45 07 00 00 	lea    r10,[rip+0x745]        # 2004 <_IO_stdin_used+0x4>
    18bf:	e9 96 fe ff ff       	jmp    175a <_Z8gemm_fmaRA4_A4_db+0x9a>
    18c4:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    18c8:	41 83 c6 01          	add    r14d,0x1
    18cc:	c4 c1 7d 11 0f       	vmovupd YMMWORD PTR [r15],ymm1
    18d1:	49 83 c4 20          	add    r12,0x20
    18d5:	49 83 c7 20          	add    r15,0x20
    18d9:	41 83 fe 04          	cmp    r14d,0x4
    18dd:	74 11                	je     18f0 <_Z8gemm_fmaRA4_A4_db+0x230>
    18df:	c4 c1 7b 10 04 24    	vmovsd xmm0,QWORD PTR [r12]
    18e5:	e9 36 fe ff ff       	jmp    1720 <_Z8gemm_fmaRA4_A4_db+0x60>
    18ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    18f0:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    18f4:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    18fb:	00 00
    18fd:	75 18                	jne    1917 <_Z8gemm_fmaRA4_A4_db+0x257>
    18ff:	c5 f8 77             	vzeroupper
    1902:	48 83 c4 60          	add    rsp,0x60
    1906:	5b                   	pop    rbx
    1907:	41 5a                	pop    r10
    1909:	41 5c                	pop    r12
    190b:	41 5d                	pop    r13
    190d:	41 5e                	pop    r14
    190f:	41 5f                	pop    r15
    1911:	5d                   	pop    rbp
    1912:	49 8d 62 f8          	lea    rsp,[r10-0x8]
    1916:	c3                   	ret
    1917:	c5 f8 77             	vzeroupper
    191a:	e8 e1 f7 ff ff       	call   1100 <__stack_chk_fail@plt>
    191f:	90                   	nop

0000000000001920 <_Z12print_matrixPKcRA4_A4_Kd>:
    1920:	f3 0f 1e fa          	endbr64
    1924:	41 56                	push   r14
    1926:	4c 8d 35 4d 07 00 00 	lea    r14,[rip+0x74d]        # 207a <_IO_stdin_used+0x7a>
    192d:	ba 01 00 00 00       	mov    edx,0x1
    1932:	41 55                	push   r13
    1934:	49 89 f5             	mov    r13,rsi
    1937:	4c 89 f6             	mov    rsi,r14
    193a:	41 54                	push   r12
    193c:	49 89 fc             	mov    r12,rdi
    193f:	55                   	push   rbp
    1940:	48 8d 2d f9 26 00 00 	lea    rbp,[rip+0x26f9]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    1947:	53                   	push   rbx
    1948:	48 89 ef             	mov    rdi,rbp
    194b:	e8 c0 f7 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    1950:	4d 85 e4             	test   r12,r12
    1953:	0f 84 87 00 00 00    	je     19e0 <_Z12print_matrixPKcRA4_A4_Kd+0xc0>
    1959:	4c 89 e7             	mov    rdi,r12
    195c:	e8 6f f7 ff ff       	call   10d0 <strlen@plt>
    1961:	4c 89 e6             	mov    rsi,r12
    1964:	48 89 ef             	mov    rdi,rbp
    1967:	48 89 c2             	mov    rdx,rax
    196a:	e8 a1 f7 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    196f:	ba 01 00 00 00       	mov    edx,0x1
    1974:	4c 89 f6             	mov    rsi,r14
    1977:	4d 8d 65 20          	lea    r12,[r13+0x20]
    197b:	48 89 ef             	mov    rdi,rbp
    197e:	e8 8d f7 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    1983:	49 81 c5 a0 00 00 00 	add    r13,0xa0
    198a:	49 8d 5c 24 e0       	lea    rbx,[r12-0x20]
    198f:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
    1993:	c5 fb 10 03          	vmovsd xmm0,QWORD PTR [rbx]
    1997:	48 89 ef             	mov    rdi,rbp
    199a:	48 83 c3 08          	add    rbx,0x8
    199e:	48 8b 40 e8          	mov    rax,QWORD PTR [rax-0x18]
    19a2:	48 c7 44 05 10 0a 00 	mov    QWORD PTR [rbp+rax*1+0x10],0xa
    19a9:	00 00
    19ab:	e8 80 f7 ff ff       	call   1130 <_ZNSo9_M_insertIdEERSoT_@plt>
    19b0:	4c 39 e3             	cmp    rbx,r12
    19b3:	75 da                	jne    198f <_Z12print_matrixPKcRA4_A4_Kd+0x6f>
    19b5:	ba 01 00 00 00       	mov    edx,0x1
    19ba:	4c 89 f6             	mov    rsi,r14
    19bd:	4c 8d 63 20          	lea    r12,[rbx+0x20]
    19c1:	48 89 ef             	mov    rdi,rbp
    19c4:	e8 47 f7 ff ff       	call   1110 <_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l@plt>
    19c9:	4d 39 ec             	cmp    r12,r13
    19cc:	75 bc                	jne    198a <_Z12print_matrixPKcRA4_A4_Kd+0x6a>
    19ce:	5b                   	pop    rbx
    19cf:	5d                   	pop    rbp
    19d0:	41 5c                	pop    r12
    19d2:	41 5d                	pop    r13
    19d4:	41 5e                	pop    r14
    19d6:	c3                   	ret
    19d7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    19de:	00 00
    19e0:	48 8b 05 59 26 00 00 	mov    rax,QWORD PTR [rip+0x2659]        # 4040 <_ZSt4cout@GLIBCXX_3.4>
    19e7:	48 8b 78 e8          	mov    rdi,QWORD PTR [rax-0x18]
    19eb:	48 01 ef             	add    rdi,rbp
    19ee:	8b 77 20             	mov    esi,DWORD PTR [rdi+0x20]
    19f1:	83 ce 01             	or     esi,0x1
    19f4:	e8 47 f7 ff ff       	call   1140 <_ZNSt9basic_iosIcSt11char_traitsIcEE5clearESt12_Ios_Iostate@plt>
    19f9:	e9 71 ff ff ff       	jmp    196f <_Z12print_matrixPKcRA4_A4_Kd+0x4f>

Disassembly of section .fini:

0000000000001a00 <_fini>:
    1a00:	f3 0f 1e fa          	endbr64
    1a04:	48 83 ec 08          	sub    rsp,0x8
    1a08:	48 83 c4 08          	add    rsp,0x8
    1a0c:	c3                   	ret
