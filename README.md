# tmdb-person

![Version](https://img.shields.io/badge/version-1.0.5-blue)
![Python](https://img.shields.io/badge/Python-3.9-green)
![TMDB](https://img.shields.io/badge/TMDB-V3-orign)
![https://blog.cnkj.site](https://img.shields.io/badge/Blog-blog.cnkj.site-blue)

> 根据nfo文件信息刮削相关演员信息及图片

> 解决docker部署的emby服务无法正常刮削到视频演员信息问题(通过nastool可以正常刮削到视频信息)

## ⚠️注意
> 1. 建议使用linux环境或macOS环境进行执行(windows环境执行的数据结果在导入metadata中后可能会被识别成乱码).
> 2. 受不同国家语言限制，部分刮削内容可能出现`"GBK"`异常提示，请使用 **`MacOS`** 或者 **`Linux`** 环境执行脚本即可.
> 3. 如果采用非批量的执行方式，即直接使用 `scrape` 模式进行刮削而没有先进行 `collect` 模式进行元数据收集后再进行刮削.
> 该情况下为避免重名文件导致的跳过刮削, 请注释 [scrape.py](utils%2Fscrape.py) 文件中第 `70` 行代码:
```python
shutil.copy(__file_path, "complete/")
```

## 目录说明
> 电视剧tvs 和 电影movies 的保存 `.nfo` 命名格式不一样。movies的 `.nfo` 文件以电影名为前缀， tvs 统一以 `tvshow.nfo` 命名

### data
> 根据实际配置的 `__output` 路径自动生成.实际刮削后的演员信息和图片的存放路径.

### complete
> 自动生成.存放完成刮削后被转移过来的元数据信息.

### redo
> 自动生成.存放刮削过程中出现异常的元数据记录.

### logs
> 自动生成.存放脚本执行过程中产生的日志文件, 可通过配置进行修改.

### utils
> 主程序下各个脚本子程序代码.

## 调用接口
> https://developer.themoviedb.org/

1. 演员信息刮削：https://developer.themoviedb.org/reference/person-details
2. 图片统一前缀路径：https://www.themoviedb.org/t/p/original

## 使用
* 环境：Python3.9
> 最低要求`Python3.8`，如果需要xml中生成`standalone`参数则必须至少使用`Python3.9` 及以上版本

### 安装相关pip依赖包

```python
pip3 install requests
pip3 install os
pip3 install xml
pip3 install json
```
OR/或

```python
pip3 install -r requirements.txt
```

### 相关说明

**`参数说明`**
* __dir_path: 目标文件夹路径. 绝对路径.
  * 例如电影存放于 `./movies/` 下，则该路径填写 `./movies` 的完整路径
  * 为了兼容 `电视剧` 中不刮削 `季` 中的 `.nfo` 内容，因此只刮削 `__dir_path` 路径下一层文件夹及当前层下的 `.nfo` 文件(兼容./movies 下同级存放的视频及.nfo文件)
* __output: 演员信息、图片输出路径. 绝对路径.
* __tmdb_token: TMDB 开发者API调用token
  * 登录 [TMDB](https://www.themoviedb.org/login)
  * 访问 [API](https://www.themoviedb.org/settings/api)
  * 复制 `API 读访问令牌`
* __mode: 脚本执行模式, 可选参数. 命令行执行脚本使用```--mode collect``` 调用
  * scrape: 刮削模式.从扫描目录直接识别nfo文件并刮削元数据和图片到输出目录中
  * collect: 转移模式.从扫描目录收集所有nfo文件并复制到输出目录中(不执行刮削操作)
  * redo: 重做模式.执行正常刮削数据中出现的异常进行重新处理
  * check: 检查模式.检查指定路径下的全部文件夹中演员元数据`person.nfo` 和 演员图片`folder.jpg` 是否存在并分别记录到 [no_nfo_tmdb_ids.txt](./check/no_nfo_tmdb_ids.txt) 和 [no_image_tmdb_ids.txt](./check/no_image_tmdb_ids.txt) 日志文件中
    * `scan_path` 扫描目录路径使用 `__output` 路径

**`目录结构说明`**
- ./movies
  - 流浪地球.mkv (不刮削)
  - 流浪地球.nfo (刮削)
  - 流浪地球2
    - 流浪地球2.mkv (不刮削)
    - 流浪地球2.nfo (刮削)

- ./tvs
  - 三体
    - tvshow.nfo (刮削)
    - Season 1 (不刮削)

### 运行
> 参数 `__mode` 为可选参数，具体请参考`参数说明`内容

#### 1. 直接修改脚本文件方式
1. 修改 `main.py` 文件中 `if __name__ == '__main__':` 方法中 `__dir_path` 、 `__output` 、 `__tmdb_token` 、 `__mode`参数值
2. 执行脚本
```python
python3 main.py
```

#### 2. 命令行执行
> 注意参数 `--dir_path` 的值如果需要配置多个，请使用英文半角逗号拼接，不要有空格

```python
python3 main.py --dir_path "example/movies","example/tvs" --output data/metadata/person --tmdb_token tmdb_token --mode collect
```

#### 3. 后台执行
> 可以结合前两种执行方式使用

```shell
nohup python3 main.py > nohup.log 2>&1 & echo &! > run.pid
```

### 多线程刮削
> 前置要求：需要先执行main.py脚本的"collect"模式收集nfo元数据文件

#### 1. 直接修改脚本文件方式
1. 修改 `multi_thread.py` 文件中 `if __name__ == '__main__':` 方法中 `__dir_path` 、 `__output` 、 `__tmdb_token` 参数值
2. 执行脚本
```python
python3 multi_thread.py
```

#### 2. 命令行执行
> 注意参数 `--dir_path` 的值如果需要配置多个，请使用英文半角逗号拼接，不要有空格

```python
python3 multi_thread.py --dir_path "example/movies","example/tvs" --output data/metadata/person --tmdb_token tmdb_token
```

#### 3. 后台执行
> 可以结合前两种执行方式使用

```shell
nohup python3 multi_thread.py > nohup.log 2>&1 & echo &! > run.pid
```



### 补充
1. 运行提示 `no module name requests` 但是实际python环境中又安装了的：
* 查看当前执行的python版本：```python --version```
* 例如 ```python3 --version``` 显示的是3.8，但是实际有3.9版本的环境，可以使用 ```python3.9 -m pip install requests``` 进行指定python版本的依赖包安装
