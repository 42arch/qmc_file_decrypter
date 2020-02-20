## 介绍

* 此工具可以将QQ音乐下载的加密的VIP歌曲🎵文件（后缀以**qmc**开头的文件），如 **qmcogg**、**qmcflac**、**qmc0**等，转换成一般播放器可以识别的**ogg**、**flac**和**mp3**格式等。

* 文件解密算法在decrypt.py中，程序GUI使用tkinter构建。

## 下载使用

* 可直接在[release页面]( https://github.com/ingen42/qcm_file_decrypter/releases )下载可执行文件（qq音乐VIP歌曲转换器.exe）
* 也可以下载源代码，在代码路径下使用pyinstaller工具运行命令`pyinstaller -F qmc_decrypter.py -w `编译成可执行文件(在dist目录下)。
* 打开工具，在操作菜单下分别添加文件和指定输出文件的路径，点击“开始转换”按钮，全部转换完成后，打开输出路径，即可找到对应的解密后的文件。
* 注：腾讯电脑管家可能会报毒😓...，出现这样的情况请将程序文件添加到信任区。
