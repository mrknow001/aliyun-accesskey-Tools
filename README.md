# aliyun-accesskey-Tools

此工具用于查询ALIYUN_ACCESSKEY的主机，并且远程执行命令。

对于ALIYUN_ACCESSKEY利用方式可参考文章：[记一次阿里云主机泄露Access Key到Getshell](https://www.freebuf.com/articles/web/255717.html)


## 工具截图 ##

![image](https://github.com/mrknow001/aliyun-accesskey-Tools/blob/main/images/image1.png)

![image](https://github.com/mrknow001/aliyun-accesskey-Tools/blob/main/images/image2.png)

## 安装模块 ##

pip install -r requirements.txt


pyinstaller打包exe命令

pyinstaller --hidden-import=queue -w -F OSSTools.py


由于时间关系，没空写了。策略方面还未完成。
