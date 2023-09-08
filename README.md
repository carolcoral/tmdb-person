# tmdb-person
![Python](https://img.shields.io/badge/Python-AtLeast3.8-green)
![TMDB](https://img.shields.io/badge/TMDB-V3-blue)
![https://blog.cnkj.site](https://img.shields.io/badge/Blog-blog.cnkj.site-blue)
> 根据nfo文件信息刮削相关演员信息及图片
> 
> 解决docker部署的emby服务无法正常刮削到视频演员信息问题(通过nastool可以正常刮削到视频信息)


## 数据
### example
> emby 存储于metadata/peopel 中的数据示例

> 电视剧tvs 和 电影movies 的保存 `.nfo` 命名格式不一样。movies的 `.nfo` 文件以电影名为前缀， tvs 统一以 `tvshow.nfo` 命名

* example/metadata/person/a: 英文演员信息
* example/metadata/person/张: 中文演员信息
* example/metadata/person/person.nfo: 演员元数据
* example/tvs/一生一世/tvshow.nfo: 电视剧元数据
* example/movies/神出鬼没 (2023) - 2160p.nfo: 电影元数据

### data
> 实际刮削的演员信息存放路径

## 接口
> https://developer.themoviedb.org/

1. 演员信息刮削：https://developer.themoviedb.org/reference/person-details
2. 图片统一前缀路径：https://www.themoviedb.org/t/p/original

## 使用
* 环境：Python3.9
> 最低要求`Python3.8`，如果需要xml中生成`standalone`参数则必须使用`Python3.9` 及以上版本

### 安装相关pip依赖包

```python
pip3 install requests
pip3 install os
pip3 install xml
pip3 install json
```

### 说明

**`参数说明`**
* __dir_path: 目标文件夹路径
  * 例如电影存放于 `./movies/` 下，则该路径填写 `./movies` 的完整路径。
  * 为了兼容 `电视剧` 中不刮削 `季` 中的 `.nfo` 内容，因此只刮削 `__dir_path` 路径下一层文件夹及当前层下的 `.nfo` 文件(兼容./movies 下同级存放的视频及.nfo文件)
* __output: 演员信息、图片输出路径
* __tmdb_token: TMDB 开发者API调用token
  * 登录 [TMDB](https://www.themoviedb.org/login)
  * 访问 [API](https://www.themoviedb.org/settings/api)
  * 复制 `API 读访问令牌`

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

#### 直接修改脚本文件方式
1. 修改 `main.py` 文件中 `if __name__ == '__main__':` 方法中 `__dir_path` 、 `__output` 、 `__tmdb_token` 参数值
2. 执行脚本
```python
python3 main.py
```

#### 命令行执行
> 注意参数 `--dir_path` 的值如果需要配置多个，请使用英文半角逗号拼接，不要有空格

```python
python3 main.py --dir_path "example/movies","example/tvs" --output data/metadata/person --tmdb_token
```

### 补充
1. 运行提示 `no module name requests` 但是实际python环境中又安装了的：
* 查看当前执行的python版本：```python --version```
* 例如 ```python3 --version``` 显示的是3.8，但是实际又3.9版本的环境，可以使用 ```python3.9 -m pip install requests``` 进行指定python版本的依赖包安装
