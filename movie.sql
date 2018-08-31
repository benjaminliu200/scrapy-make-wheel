CREATE TABLE Movie (
  id         INT           NOT NULL PRIMARY KEY AUTO_INCREMENT
  COMMENT '自增 id',
  name       VARCHAR(1024) NOT NULL
  COMMENT '电影名称',
  movieInfo  VARCHAR(1024) NOT NULL
  COMMENT '电影详情',
  star       VARCHAR(16)                        DEFAULT NULL
  COMMENT '豆瓣评分',
  quote      VARCHAR(1024)                      DEFAULT NULL
  COMMENT '经典台词',
  createtime DATETIME                           DEFAULT CURRENT_TIMESTAMP
  COMMENT '添加时间'
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;