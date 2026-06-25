# 实验概览
两个任务
- task 1: 编写 `csim.c` 程序实现和二进制文件 `./csim-ref` 相同的功能，输出 `cache` 的 miss、hit、evictions 次数
- task 2:  编写 `trans.c` 程序，编写出最少 misses 的矩阵转置函数
# PartA
 从零开始编写 C 程序，需要掌握参数读、文件读和内存分配管理的方法，还有 gdb 的使用相关命令 [[bomb]]

## C 语言拾遗
首先我们对于这道题目我们需要定义一个结构体 `cache_line`
```c
typedef struct {
	int valid;
	int tag;
	int time_stamp;
} cache_line;
```
参数读取：使用 `getopt` 函数进行命令行输入的读取
```c
#include <unistd.h>
#include <getopt.h>

int opt;
while ((opt = getopt(argc, argv, "hvs:E:b:t:")) != -1) {
	switch(opt) {
	case 'h':
		printUsage();
		break;
	case 'v':
		v = 1;
		break;
	case 's':
		s = atoi(optarg);
		break;
	...
	}
}
```
文件读取：使用 `fopen` 进行文件打开，使用 `fscanf` 进行文件内容的读取
```c
#include <stdio.h>

FILE *trace_file;
trace_file = fopen(optarg, "r");
while (fscanf(" %c %zx %d\n", &operation, &addr, &size) == 3) {
	...
}
```
内存分配管理：因为我们需要根据传入的参数来创建 `cache` 因此我们需要采用动态分配空间
```c
#include <stdlib.h>

typedef cache_line *set;
set *cache = (set *)malloc(sizeof(set) * (1 << s));
```

## 注意事项
 我们定义了 `set *cache` 因此我们 cache 所存储的是 set 类型变量的地址同时我们定义了 `typedef cache_line *set`，因此 set 类型的变量存储的是 `cache_line` 这个结构体的地址，对于我们使用的 `cache[i][j]` 实际上进行了两次解引用，因此 `cache[i][j]` 就是对应的结构体，所以当我们在试图改变结构体中定义的变量的值的时候不能直接使用 `cache[i][j].valid = 1`; 这样进行改变，需要定义 `set temp = &cache[i][j]`，来进行变量值的改变

# Part B
实验说明中指出在本部分可以使用硬编码来解决，目标为解决三个测试矩阵：
- 32 x 32
- 64 x 64
- 61 x 67
缓存的指标：
- E = 1
- b = 5
- s = 5
一个 block 可以存储 32 字节数据，因此可知可以存储 8 个 int 类型变量
本部分的重点在于如何写出 misses 符合要求的矩阵转置函数，本题还有参数定义数量的限制，规定定义的参数不能超过 12 个，这也是一个提示，除去循环所要用到的 4 个变量，我们还可以定义的临时变量是 8 个
## 临时变量
如果不使用临时变量，程序的执行逻辑是读写交替即 read A → write B → read A ......，一旦遇到对角线或者互相冲突的地址，就会引发 A、B 交替争夺 set
为了避免这种情况的发生，我们引入临时变量储存一个 block 能够存储的 A 的值，连续读取 A 的值，没有任何写入 B 的操作干扰，所以只有第一次 miss，剩下的 7 次都是 hit，当读取结束，对于 B 再统一进行读写，这样大大较少了 miss 的产生
## 分块
如果不分块，以 32 x 32 为例，对于 A 矩阵：每一行在开始的时候都要重新命中，同时当处于对角线时，A B 互踢，导致 cache 的相同 set 来回被占用替换，平均每行要发生 2-3 次的 miss，因此 A 产生的总 Miss 为 32 x 2.5 = 80 次；对于 B 矩阵：因为内层循环 j 走的太远（跨度 32），导致任何缓存在 cache 的 B block 在下一次被使用的时候（外层循环 i 变大）之前，会被冲掉，导致 B 的每一次写入都产生 miss，因此 B 产生的总 Miss 为 32 x 32 = 1024 次

*分块就是当 cache 很小的时候，将装不下的大矩阵切分为小矩阵，当数据刚写入缓存的时候，就在其要被替代前立即使用或者放入寄存器中缓存，从而提高命中率*
## 32 x 32
很明显，在这种排布的矩阵中，每 8 行产生相同的 set 占用，因此我们选用 8 x 8 作为矩阵 A B 的分块大小，通过临时变量处理即可
## 64 x 64
本部分的**重难点**，难点在于此时每 4 行就会产生相同的 set 占用，但是当我们选用 4 x 4 的分块矩阵大小时，不能满足题目要求的 miss 次数，因此我们需要采取一些处理策略，我们依旧采用 8 x 8 的分块模式，我们将其分为 4 个 4 x 4 的小块，4 x 4 的小块完美符合 set 无占用的情况

按照以下步骤进行处理：
	1. 首先处理 A 的上半部分 4 x 8 部分，将左上角部分按照正常步骤转置到 B 的坐上部分，将本来应该放到 B 的左下部分的放到 B 的右上部分
	2. 用临时变量暂存 B 的右上部分，将 A 的左下部分赋值给 B，将暂存的变量赋值给 B 的左下部分
	3. 处理 A、B 的第四部分
	![[Excalidraw/CSAPP.excalidraw.md#^frame=mdxvQkDI|100%]]
## 61 x 67 
由于本题的 miss 限制很宽，使用 16 x 16 的 block 进行分块处理即可通过，但是要注意的是，对于这种不是正方形的矩阵，还要记得处理分块后的部分，而能够使用 16 x 16 的具体原因是，不规则的矩阵尺寸把“对齐冲突陷阱 ”破坏了，即每一行的前 8 个元素的映射没有等差关系了