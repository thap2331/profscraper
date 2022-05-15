# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class DepartmentPipeline:

    def open_spider(self, spider):
        try:
            self.read_file = open('database/department.jl', 'r')
            self.write_file = open('database/department.jl', 'w')
        except:
            self.write_file = open('database/department.jl', 'w')

    def close_spider(self, spider):
        try:
            self.read_file.close()
            self.write_file.close()
        except:
            self.write_file.close()

    def process_item(self, item, spider):
        data = list(self.read_file)
        all_url = [i['link'] for i in data]
        if item['link'] not in all_url:
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.write_file.write(line)
            return item

class FacultyPipeline:

    def open_spider(self, spider):
        try:
            self.read_file = open('database/faculty.jl', 'r')
            self.write_file = open('database/faculty.jl', 'w')
        except:
            self.write_file = open('database/faculty.jl', 'w')
            self.read_file = open('database/faculty.jl', 'r')

    def close_spider(self, spider):
        try:
            self.read_file.close()
            self.write_file.close()
        except:
            self.write_file.close()

    def process_item(self, item, spider):
        data = list(self.read_file)
        all_url = [i['link'] for i in data]
        if item['link'] not in all_url:
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.write_file.write(line)
        return item