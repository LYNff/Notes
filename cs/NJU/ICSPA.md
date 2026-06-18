---
type: project
status: plan
---

# NJUPA

## Makefile 基础知识
Makefile 基于规则运行，一条规则主要包含三个部分：
```Makefile
Target: Dependencies
    Command
```
- Target: 通常是要生成的文件名，也可以是一个动作的名称如(clean)
- Dependencies: 生成目标文件所需的文件，如果依赖文件比目标文件更新，或者目标文件不存在，就会执行 Command
- Command: make需要执行的shell命令

使用变量可以让Makefile更加优雅
当项目变大时，重复写gcc或相同的文件名会很麻烦，我们可以使用变量；
同时Makefile提供了一些符号来简化规则中的命令：
- $@：代表当前的目标文件
- $^：代表所有依赖文件（空格分隔）
- $<：代表第一个依赖文件

运用这两种方式，我们可以书写一个比较精简的Makefile文件：
```Makefile
CC = gcc
CFLAGS = -Wall -g
TARGET = my_program
OBJS = main.o utils.o

$(TARGET): $(OBJS)
    $(CC) $(CFLAGS) -o $@ $^

%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

clean:
    rm -f $(OBJS) $(TARGET)
```
在上述代码中，clean是一个动作，但是如果项目目录下恰好有一个名为clean的文件，执行make clean时，make会发现clean文件已经存在且没有以来，从而拒绝执行清理命令
为了防止这种情况，我们需要生命clean是一个“伪目标”
```Makefile
.PHONY: clean

clean: 
    rm -f *.o my_program
```



