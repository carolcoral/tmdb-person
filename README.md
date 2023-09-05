# tmdb-person

根据nfo文件信息刮削相关演员信息及图片

## example
> emby 存储于metadata/peopel 中的数据示例

> 电视剧tvs 和 电影movies 的保存 `.nfo` 命名格式不一样。movies的 `.nfo` 文件以电影名为前缀， tvs 统一以 `tvshow.nfo` 命名

* a: 英文演员信息
* 张: 中文演员信息
* person.nfo
* tvshow.nfo

## data
> 实际刮削的演员信息存放路径

## 接口
> https://developer.themoviedb.org/

1. 演员信息刮削：https://developer.themoviedb.org/reference/person-details
2. 图片统一前缀路径：https://www.themoviedb.org/t/p/original