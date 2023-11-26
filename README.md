# 微博等信息流数据处理、聚合工具

### 功能
对微博 weibo、长毛象 mastodon 的 follow 数据进行抓取，并进行信息的过滤、整合、分组。

### 自动执行
只需要在 crontab 中配置定式任务，让程序定期执行。
```commandline
crontab -e
```

### 各程序入口
- main.py 主程序
- data_cleaner.py 数据清理程序，可单独运行
- auto_notify.py 网络监控、通知程序，当无法正常访问 api 时，会发送微信消息通知
- ping_test.py ping 接口的程序，快速检测接口是否能 ping 通
- fbw_manager.py forbidden_words.txt 的文件操作接口，可以在终端中以命令行的方式操作 forbidden_words.txt 文件数据
- config_manager.py 操作config.ini的入口

各程序的执行参数，可以通过 -h 查看。

### 资源文件
- config.ini 配置文件
- focus_user.ini weibo的关注列表，并且对进行的输出的分组，在对应分组内添加用户的 id
- forbidden_words.txt 屏蔽词列表。当 weibo 数据中出现屏蔽词时，予以屏蔽。

### 其他
- export 数据输出目录。数据会 export/weibo/group/2023-07-01/... 这个目录下生成 .html 文件。
- logs 日志文件
- test 测试

### 初次使用注意
需要在 config.ini 中，手动填写好相关配置。其中，created_at 是必须要填的，需要从接口中复制出原始数据，保持相同的数据格式。last_id 则无所谓，可以任意填写。其他参数，按需要填写。
成功运行一次后，每次执行之后，last_id, created_at 值都会自动更新。

使用方法
```commandline
python3 main.py
```

### 其他注意
由于main主程序对数据的处理不够精细，存在数据重复的情况。所以，推荐在 main.py 执行过后，紧接着执行 data_cleaner.py,清理数据。
例如，我在 crontab 中的配置如下
```commandline
0 * * * * /opt/homebrew/bin/python3 /Users/evalcony/coding/py-proj/weibo-proj/main.py >> /Users/evalcony/coding/py-proj/weibo-proj/logs/file.log 2>&1; /opt/homebrew/bin/python3 /Users/evalcony/coding/py-proj/weibo-proj/tools/data_cleaner.py >> /Users/evalcony/coding/py-proj/weibo-proj/logs/file-t.log 2>&1
```
在 main.py 执行过后，紧接着执行 data_cleaner.py。main.py 的日志输出到 logs/file.log 中；data_cleaner.py 的日志输出到 logs/file-t.log 中。

### 生成项目目录结构

```
tree -I 'export|__pycache__|test|test_export|logs' > proj-structure.txt
```
