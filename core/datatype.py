"""定义数据类型"""
import os
import json
import logging
from datetime import date


class MovieInfo:
    def __init__(self, dvdid=None, /, *, cid=None, from_file=None):
        """
        Args:
            dvdid ([str], optional): 番号，要通过其他方式创建实例时此参数应留空
            from_file: 从指定的文件(json格式)中加载数据来创建实例
        """
        arg_count = len([i for i in [dvdid, cid, from_file] if i])
        if arg_count != 1:
            raise TypeError(f'Require 1 parameter but {arg_count} given')
        # 创建类的默认属性
        self.dvdid = dvdid          # DVD ID，即通常的番号
        self.cid = cid              # DMM Content ID
        self.cover = None           # 封面图片（URL）
        self.genre = None           # 影片分类的标签
        self.score = None           # 评分（10分制）
        self.title = None           # 影片标题（不含番号）
        self.magnet = None          # 磁力链接
        self.serial = None          # 系列
        self.actress = None         # 出演女优
        self.director = None        # 导演
        self.duration = None        # 影片时长
        self.producer = None        # 制作商
        self.publisher = None       # 发行商
        self.publish_date = None    # 发布日期
        self.preview_pics = None    # 预览图片（URL）
        self.preview_video = None   # 预览视频（URL）

        if from_file:
            if os.path.isfile(from_file):
                self.load(from_file)
            else:
                raise TypeError(f"Invalid file path: '{from_file}'")

    def __str__(self) -> str:
        d = vars(self)
        if type(d['publish_date']) is date:
            d['publish_date'] = d['publish_date'].isoformat()
        return json.dumps(d, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return __class__.__name__ + f"('{self.dvdid}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def dump(self, filepath) -> None:
        with open(filepath, 'wt', encoding='utf-8') as f:
            f.write(str(self))

    def load(self, filepath) -> None:
        with open(filepath, 'rt', encoding='utf-8') as f:
            d = json.load(f)
        try:
            d['publish_date'] = date.fromisoformat(d['publish_date'])
        except:
            d['publish_date'] = None
        # 更新对象属性
        attrs = vars(self).keys()
        for k, v in d.items():
            if k in attrs:
                self.__setattr__(k, v)


class Movie:
    """用于关联影片文件的类"""
    def __init__(self, dvdid=None, /, *, cid=None) -> None:
        arg_count = len([i for i in (dvdid, cid) if i])
        if arg_count != 1:
            raise TypeError(f'Require 1 parameter but {arg_count} given')
        # 创建类的默认属性
        self.dvdid = dvdid              # DVD ID，即通常的番号
        self.cid = cid                  # DMM Content ID
        self.files = []                 # 关联到此番号的所有影片文件的列表（用于管理带有多个分片的影片）
        self.data_src = 'normal'        # 数据源：不同的数据源将使用不同的爬虫
        self.info = None                # 抓取到的影片信息

    def __repr__(self) -> str:
        return __class__.__name__ + f"('{self.dvdid}')"


class ColoredFormatter(logging.Formatter):
    """为不同level的日志着色"""
    NO_STYLE = '\033[0m'
    COLOR_MAP = {
        logging.DEBUG:    '\033[1;30m', # grey
        logging.WARNING:  '\033[1;33m', # light yellow
        logging.ERROR:    '\033[1;31m', # light red
        logging.CRITICAL: '\033[0;31m', # red
    }

    def __init__(self, fmt='%(levelname)-8s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', style='%', validate=True) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)

    def format(self, record):
        raw = super().format(record)
        color = self.COLOR_MAP.get(record.levelno, self.NO_STYLE)
        return color + raw + self.NO_STYLE
