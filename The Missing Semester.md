# The Missing Semester
## Shell 入门
`date echo which man ls cd cat sort uniq head tail grep set find awk sleep`
- `uniq` 需要注意的是，它只会消除连续出现的重复行，对于连续的4中间夹了一个3,就会变为4 3 4
- `sort` 默认是按照字典序排序的，可以通过 `-u` 参数实现去重功能
- `head tail` 默认输出10行，可以通过 `-n` 参数指定输出行数
- `grep` 用于在文件中搜索特定模式，实际上就是通过正则表达式，可以使用 `-r` 参数递归搜索目录中的文件，`-i` 参数忽略大小写，`-v` 参数反转匹配结果，`-l` 参数只输出匹配的文件名，`-P` 参数使用 Perl 兼容的正则表达式

- `sed` 是一个流编辑器，可以对文本进行替换、删除、插入等操作，常用的命令有 `s` 用于替换，`d` 用于删除，`i` 用于插入，for example `sed 's/old/new/g' file.txt` 会将 file.txt 中的所有 old 替换为 new
- `find` 用于在目录中查找文件，在指定位置搜索符合条件的文件，常用的参数有 `-name` 用于按照文件名搜索，`-type` 用于按照文件类型搜索，`-size` 用于按照文件大小搜索，`-exec` 用于对找到的文件执行命令
- `awk` 用于解析文件，默认用空白字符和行来分割文件，使用 `-F` 可以改变分隔符，`awk '{print $1}' file.txt` 会输出 file.txt 中的第一列
- `|` 管道符号
- `>` 输出重定向，需要注意的是，`>` 会覆盖原有文件内容，而 `>>` 则会在原有文件内容的基础上追加内容
- 在 shell 中 0 代表成功，非 0 代表失败，这一点与其他编程语言不同
- `if for while` 等控制结构在 shell 中也有对应的语法，例如 `if [ condition ]; then ... fi`，`for var in list; do ... done`，`while [ condition ]; do ... done` 
再例如 `for i in $(seq 1 10); do echo $i; done` 会输出1到10的数字
- `sleep` 用于暂停执行一段时间，例如 `sleep 5` 会暂停5秒钟
## 命令行环境
`* ? && || ps kill fg bg jobs ssh scp wc ripgrep`
- glob - `*` 匹配任意数量的字符
- 一段命令程序的的输出实际为两个，一个是标准输出流，一个是标准错误流，默认情况下它们都输出到终端，但可以通过重定向将它们分别输出到不同的文件，例如 `command > output.txt 2> error.txt` 会将标准输出流重定向到 output.txt 文件，将标准错误流重定向到 error.txt 文件
- 在 shell 中，`foo=bar`，然后通过`echo $foo` 可以输出 bar，注意在 shell 中变量赋值时不能有空格！如果想要子进程也能访问这个变量，需要使用 `export foo=bar` 来导出变量
- `echo $?` 可以查看上一个命令的退出状态码，0 代表成功，1 代表失败，2 代表命令未找到
- `&& ||` 用于连接多个命令，`command1 && command2` 表示如果 command1 成功执行，则执行 command2，`command1 || command2` 表示如果 command1 执行失败，则执行 command2
- 关于进程，`ps` 命令可以查看当前系统中的进程，`kill` 命令可以终止一个进程，例如 `kill -9 pid` 会强制终止 pid 对应的进程，`ctrl + z` 可以将当前正在运行的命令暂停，`fg` 可以将暂停的命令恢复到前台继续执行，`bg` 可以将暂停的命令放到后台继续执行，`jobs` 可以查看当前的后台任务
- `ssh` 用于远程登录到另一台计算机，例如 `ssh user@hostname` 会登录到 hostname 这台计算机，使用 user 这个用户名，登录后可以执行命令，就像在本地一样，通常我们使用 ssh key 来实现免密登陆
- `scp` 用于在本地和远程计算机之间复制文件，例如 `scp file.txt user@hostname:/path/to/destination` 会将本地的 file.txt 文件复制到 hostname 这台计算机的 /path/to/destination 目录下，使用 user 这个用户名
- `wc` 用于统计文件中的行数、字数和字符数，例如 `wc -l file.txt` 会输出 file.txt 中的行数，`wc -w file.txt` 会输出 file.txt 中的字数，`wc -c file.txt` 会输出 file.txt 中的字符数
- `ripgrep` 是一个快速的文本搜索工具，类似于 `grep`，但性能更好，支持正则表达式，可以递归搜索目录中的文件，例如 `rg pattern` 会在当前目录及其子目录中搜索包含 pattern 的文件，并输出匹配的行
## 开发环境与工具
`vim vscode AI-power`
## 调试与性能分析
`journalctl gdb lldb RR strace bpftrace`
- `journalctl` 是一个用于查看和管理系统日志的工具
- `RR` 是一个用于记录和重放程序执行的工具，可以帮助我们分析程序的性能问题，例如 `rr record ./my_program` 会记录 my_program 的执行过程，`rr replay` 会重放记录的执行过程，并且可以在其中使用 gdb 进行调试，`reverse-continue` 用于反向继续执行程序
- `gdb` 是 GNU 调试器，可以用于调试 C/C++ 程序，例如 `gdb my_program` 会启动 gdb 并加载 my_program，`break main` 会在 main 函数设置一个断点，`run` 会开始执行程序，`next` 会执行下一行代码，`print variable` 会打印变量的值
- `lldb` 是一个用于调试程序的工具，类似于 `gdb`，但主要用于 macOS 和 iOS 开发
- `strace` 是一个用于跟踪系统调用和信号的工具，可以帮助我们分析程序的性能问题，例如 `strace -p pid` 会跟踪 pid 对应的进程的系统调用，`strace -c -p pid` 会统计 pid 对应的进程的系统调用的时间和次数
- `bpftrace` 是一个用于跟踪内核事件的工具，可以帮助我们分析系统的性能问题，例如 `bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("openat called by %s\n", comm); }'` 会跟踪 openat 系统调用，并打印调用该系统调用的进程的名称
## 版本控制与Git
`git`
- `git init`
- `git add [files]`
- `git commit -m [message]`
- `git log`: 默认只显示当前分支下的 snapshot  `git log --graph --all`: 显示所有分支的 snapshot，并且以图形化的方式展示它们之间的关系 `git log -p`: 显示每个提交的差异
- `git branch [name]` `git branch -d [branch]` `git branch [name] [commit]`: 创建一个新的分支，指向指定的 commit，默认是当前分支的最新 commit 
- `git switch [branch]`
- `git merge [branch]`
- `git checkout [branch or commit's hash]`: 可以切换到指定的分支或者提交，例如 `git checkout master` 会切换到 master 分支，`git checkout abc123` 会切换到提交 hash 为 abc123 的提交 
- `git remote add [name] [url]`: 添加一个远程仓库，例如 `git remote add origin https://github.com/user/repo.git`
- `git push`: 将本地的提交推送到远程仓库
- `git fetch`: 从远程仓库获取最新的提交和分支信息，但不会自动合并到当前分支
- `git pull`: 从远程仓库获取最新的提交和分支信息，并自动合并到当前分支
- `git diff`: 显示工作区文件与暂存区文件的差异
- `git stash`: 将当前工作区的修改保存到一个临时区域，并恢复到上一次提交的状态，例如 `git stash save "message"` 会将当前工作区的修改保存到 stash 中，并且添加一个 message 作为备注
## 代码打包与分发
当我们在处理不同的程序时，其所需要的依赖库可能会不同，不同的以来之间还可能存在冲突，因此我们需要通过分离环境的方式来解决这个问题，常用的工具有 `venv` `conda` 和 `docker`
python 的打包生态相当复杂，有多种工具都实现了打包逻辑，最熟悉的就是 `pip`，它是 Python 的包管理工具，可以用于安装和管理 Python 包，目前最容易上手使用的是 `uv`
- `venv` 是 Python 内置的一个工具，可以用于创建虚拟环境，例如 `python -m venv myenv` 会在当前目录下创建一个名为 myenv 的虚拟环境，`source myenv/bin/activate` 会激活这个虚拟环境，之后安装的依赖库都会安装到这个虚拟环境中，而不会影响到全局环境
- `uv`： uv 集成了很多的 python 工具，例如 `uv pip` 用于安装和管理 Python 包，`uv venv` 用于创建和管理虚拟环境，`uv build` 用于构建 Python 包，`uv publish` 用于发布 Python 包到 PyPI，使用 uv 可以简化很多的操作，例如 `uv pip install package` 会在当前虚拟环境中安装 package 包，`uv run` 会在当前虚拟环境中运行 Python 程序，同时自动安装程序所需要的依赖库

当我们想要将一个程序分发给其他人使用时，比如我们写了一个`greeting.py`，依赖 `typer` 来实现命令行交互，我们可以编写一个 `pyproject.toml` 文件来描述这个程序的元数据和依赖关系，例如：

```toml
[project]
name = "greeting"
version = "0.1.0"
description = "A simple greeting library"
dependencies = [
    "typer>=0.9"
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project.scripts]
gree = "greeting:cli"
```
than we can use `uv build` 来构建这个程序，构建完成后会在 dist 目录下生成一个 wheel 文件，例如 `greeting-0.1.0-py3-none-any.whl`，我们可以将这个文件分发给其他人使用，他们可以通过 `pip install greeting-0.1.0-py3-none-any.whl` 来安装这个程序

we can use `uv lock` 来生成一个 `uv.lock` 文件来锁定依赖库的版本，例如 `uv lock` 会扫描当前虚拟环境中的依赖库，并将它们的版本信息写入 uv.lock 文件中，这样其他人安装这个程序时就可以确保安装的依赖库版本与我们开发时使用的版本一致，避免了依赖库版本不兼容的问题，然后使用 `uv sync` 来安装 uv.lock 文件中锁定的依赖库版本，例如 `uv sync` 会读取 uv.lock 文件中的依赖库版本信息，并安装这些版本的依赖库到当前虚拟环境中

版本的命名也有一定的规则，通常使用语义化版本规范，格式为 `MAJOR.MINOR.PATCH`，其中 MAJOR 代表重大版本，MINOR 代表次要版本，PATCH 代表修复版本，当我们进行不兼容的 API 修改时，应该增加 MAJOR 版本号，当我们进行向下兼容的功能添加时，应该增加 MINOR 版本号，当我们进行向下兼容的问题修复时，应该增加 PATCH 版本号

`docker` 是一个用于容器化应用程序的工具，可以将应用程序及其依赖库打包到一个容器中，方便分发和部署
- how to build my own image? 使用 Dockerfile 来定义镜像的构建过程, for example:
```Dockerfile
FROM python:3.14
RUN pip install uv
RUN apt-get update
RUN apt-get install -y gcc
COPY greeting/ /app
WORKDIR /app
RUN uv pip install --system /app
```
than we can use `docker build -t greet [文件所在目录]` 来构建这个镜像，例如 `docker build -t greet .` 会在当前目录下寻找 Dockerfile 文件，并根据其中的指令来构建一个名为 greet 的镜像
## 智能体编程
`claude code`
我们可以使用 `claude code` 来辅助我们，通过适当的 prompt 来引导它生成我们需要的代码
智能体编程有许多高级用法：
- 多智能体并行作：可以让多个 agent 在同一个 project 上并行工作，借助`git worktree` 生成多个项目副本，每个 agent 在自己的副本上工作，最后通过 `git merge` 将它们的工作成果合并到主分支上
- 上下文管理: 当上下文过长的时候，可能会产生上下文污染，对模型的性能产生影响，一般会采用比如：`clear` `rewind` `compaction` `llms.txt` `AGENTS.md`