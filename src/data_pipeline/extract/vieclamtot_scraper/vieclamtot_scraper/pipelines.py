# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from .items import *
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
import sys
sys.path.append('../../..')
from data_pipeline.transform.processing.transform_colab import *
from data_pipeline.load.load_airtable import *
from data_pipeline.load.load_airtable_colab import *
from data_pipeline.transform.processing.transformed_item import *

class VieclamtotScraperTransformPipeline:

    def process_item(self, item, spider):
        if isinstance(item, VieclamtotJobScraperItem):
            try:
                return TransformedScraperJobItem(transform_vlt_job(item))
            except Exception as e:
                print(e)
            
        else:
            try:
                return TransformedScraperCompanyItem(transform_vlt_company(item))
            except Exception as e:
                print(e)

class VieclamtotScraperLoadPipeline:

    def open_spider(self, spider):
        self.n_job = 0
        self.n_company = 0

        self.job = []
        self.company = []
        self.base = base

    def process_item(self, item, spider):

        if isinstance(item, TransformedScraperJobItem):
            self.n_job += 1
            if self.n_job == 10:
                load_job(self.job, base)
                self.n_job = 0
                self.job = []
            else:
                self.job.append(dict(item))
            
        else:
            self.n_company += 1
            if self.n_company == 10:
                load_company(self.company, base)
                self.n_company = 0
                self.company = []
            else:
                self.company.append(dict(item))
    
    def close_spider(self, spider):
        if len(self.job) != 0:
            load_job(self.job, base)
        if len(self.company) != 0:
            load_company(self.company, base)


class VieclamtotScraperPreprocessPipeline:

    def __init__(self) -> None:
        self.first_item = True
        self.metadata = None
        self.data_job = []
        self.data_company = []

    # def open_spider(self, spider):
    #     self.start = time.time()
        # print('---------- Opening Main Pipeline ----------')
        # self.file_job = open('../vieclamtot_scraper/data/job.json', 'w')
        # self.file_job = open('/code/vieclamtot_scraper/data/job.json', 'w')

        # self.file_company = open('../vieclamtot_scraper/data/company.json', 'w')
        # self.file_company = open('/code/vieclamtot_scraper/data/company.json', 'w')
        # print('---------- Opened Main Pipeline ----------')

    # def close_spider(self, spider):
    #     self.end = time.time()
    #     print(self.end - self.start)
        # print('---------- Closing Main Pipeline ----------')
        # json.dump(self.data_job, self.file_job, indent=4)
        # self.file_job.close()

        # json.dump(self.data_company, self.file_company, indent=4)
        # self.file_company.close()
        # print('---------- Closed Main Pipeline ----------')

    def process_item(self, item, spider):
        
        if isinstance(item, VieclamtotJobScraperItem):
            # print('---------- Processing Job ----------')
            return self.process_job(item)
            
            # return self.process_job_item(item)
            
        return item

    def process_job(self, item):

        item = ItemAdapter(item)

        # if re.match('\d+, .+', item['age_range']) is None:
        #     item['age_range'] = re.findall('\d+', item['age_range'])[0] + '+'
        
        # if re.match('.+, \d+', item['age_range']) is None:
        #     item['age_range'] = re.findall('\d+', item['age_range'])[0] + '-'

        if item['preferred_education'] == 'None':
            item['preferred_education'] = 'Không yêu cầu'

        if item['preferred_gender'] == 'None':
            item['preferred_gender'] = 'Không yêu cầu'

        if item['preferred_working_experience'] == 'None':
            item['preferred_working_experience'] = 'Không yêu cầu'

        if item['skills'] == 'None':
            item['skills'] = 'Không yêu cầu'

        # self.data_job.append(item.asdict())

        # print(item.asdict())

        return VieclamtotJobScraperItem(item)


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def open_spider(self, spider):
        # print('---------- Opening Duplicate Pipeline ----------')
        pass
    
    def close_spider(self, spider):
        # print('---------- Closing Dupilicate Pipeline ----------')
        pass

    def process_item(self, item, spider):
        # print('---------- Filtering Duplicate ----------')
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem()
        else:
            self.ids_seen.add(adapter['id'])
            return item