# 微博等信息流数据处理、聚合工具

### 功能
对微博 weibo、长毛象 mastodon 的 follow 数据进行抓取，并进行信息的过滤、整合、分组。

### 自动执行
需要在 crontab 中配置定式任务，让程序定期执行。
```commandline
crontab -e
```

### 各程序入口
- main.py 主程序
- data_cleaner.py 数据清理程序，可单独运行
- auto_notify.py 网络监控、通知程序，当无法正常访问 api 时，会发送微信消息通知
- ping_test.py ping 接口的程序，快速检测接口是否能 ping 通
- fbw_manager.py forbidden_words.txt 的文件操作接口，可以在终端中以命令行的方式操作 forbidden_words.txt 文件数据

### 资源文件
- config.ini 配置文件
- focus_user.ini weibo的关注列表，并且对进行的输出的分组，在对应分组内添加用户的 id
- forbidden_words.txt 屏蔽词列表。当 weibo 数据中出现屏蔽词时，予以屏蔽。

### 其他
- export 数据输出目录
- logs 日志文件
- test 测试