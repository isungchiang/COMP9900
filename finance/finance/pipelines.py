# -*- coding: utf-8 -*-
import os
import codecs

class FinancePipeline(object):
    yahooh_field_order = ['StockID', 'Corporation', 'Market',
                          'Address','Contact','Sector','Industry','EmployeesNum','Description']
    @staticmethod
    def isEmptyString(s):
        if s.strip() == '' or s == 'N/A' or s == None:
            return True
        return False

    def process_item(self, item, spider):
        if spider.name == 'yahoo':
            output_dir = './crawledData/'
            file_path = output_dir  + 'YahooProfile.csv'
            with codecs.open(file_path, 'a+', 'utf-8') as f:
                outstream = ''
                for field in self.yahooh_field_order:
                    if (self.isEmptyString(str(item[field]))):
                        outstream += 'N/A\t'
                    else:
                        outstream += str(item[field]) + '\t'
                f.write(outstream.strip() + '\n')
            return item