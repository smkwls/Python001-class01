# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql




class SpidersPipeline:
    def process_item(self, item, spider):
        conn = pymysql.connect(host = 'localhost',
                       port = 3306,
                       user = 'root',
                       password = 'qi123456',
                       database = 'test',
                       charset = 'utf8mb4'
                        )

        values = list(zip(item[title[0:10]],item[year[0:10]],item[category[0:10]]))
        final_data = pd.DataFrame(data)

        try:
            cur = conn.cursor()
            cur.executemany('INSERT INTO  test.test(title,year,category) values(%s,%s,%s)' ,values)
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()



