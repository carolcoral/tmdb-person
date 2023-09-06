# tmdb-person

![](https://img.shields.io/badge/Python-3.8-green)
![](https://img.shields.io/badge/TMDB-V3-blue)

根据nfo文件信息刮削相关演员信息及图片

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
* 环境：Python3.8

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
**`方法一:`**

修改 `person.py` 文件中 `if __name__ == '__main__':` 方法中 `__dir_path` 参数值和 `__output` 参数值

**`方法二:`**

> 通过命令行方式设置参数

```python
python3 person.py {"__dir_path":"/volume1/video/movies", "__output":"/volume1/metadata/person"}
```

