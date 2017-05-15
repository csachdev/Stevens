import csv
from datetime import datetime
from collections import OrderedDict
import collections
from operator import itemgetter

class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)



    def __init__(self, list_of_lists, header=True):

         if header:
            duplicate_header=list_of_lists[0]
            self.header = list_of_lists[0]
            print self.header
            temp_data=[]
            temp_data_spaces=list_of_lists[1:]
            #removing leading and trailing white spaces
            for item in  temp_data_spaces:
                item = [x.strip(' ') for x in item]
                temp_data.append(item)
            #print temp_data

            #checking whether headers are unique if not then throwing exception
            if len(duplicate_header)!=len(set(duplicate_header)):
                raise Exception("Headers are not unique")
            self.data = temp_data
            #print self.data





         else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists[0])]
            self.data = list_of_lists
         self.sort_data=temp_data
         self.data = [OrderedDict(zip(self.header, row)) for row in self.data]



    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            
            #BOOLEAN INDEXING

            return_data=[]
            if item=='Price':
               return_data=Series([int(row[item].replace(",","")) for row in self.data])
            elif item=='Transaction_date' or item=='Account_Created' or item=='Last_Login':
               return_data = Series([datetime.strptime(row[item],'%m/%d/%y %H:%M') for row in self.data])

            else:
               return_data = Series([row[item]for row in self.data])
            #i = 0
            #print type(return_data)

            return return_data
            #return temp_data
            # this is for rows and columns
        elif isinstance(item, tuple):

            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]





    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    # Sorting Function
    def sort_by(self,column_name,reverse):

        index1 = self.header.index(column_name)

        print index1
        if (index1==0 or index1==8 or index1==9):
           if reverse:
             print sorted(self.sort_data,
                            key=lambda k: datetime.strptime(k[index1], '%m/%d/%y %H:%M'),
                            reverse=True)


           else:
              print sorted(self.sort_data,
                            key=lambda k: datetime.strptime(k[index1], '%m/%d/%y %H:%M'),
                            reverse=False)

        elif index1==2 or index1==10 or index1==11:
             self.sort_data_temp=[]
             for l in self.sort_data:
               temp=str(l[index1])
               temp=temp.replace(",","")
               l[index1]=float(temp)
               self.sort_data_temp.append(l)

             if reverse:
                 print sorted(self.sort_data_temp, key=itemgetter(index1), reverse=True)
             else:
                 print sorted(self.sort_data_temp, key=itemgetter(index1))

        else:
             if reverse:
                 print sorted(self.sort_data, key=itemgetter(index1), reverse=True)
             else:
                 print sorted(self.sort_data, key=itemgetter(index1))

class Series(list):
    def __init__(self,list_of_values):
        self.data=list_of_values
    def __eq__(self, other):
        ret_list=[]
        temp_list=[]
        try:
            other=datetime.strptime(other,'%m/%d/%y %H:%M')
        except:
            pass

        print type(other)
        for item in self.data:

            temp_list.append(item==other)
        j=0
        for i in temp_list.__iter__():
            if i:
                ret_list.append(df.sort_data[j])
            j=j+1

        return ret_list

        #print ret_list

        return ret_list
    def __ne__(self, other):
        ret_list=[]
        temp_list=[]
        try:
            other=datetime.strptime(other,'%m/%d/%y %H:%M')
        except:
            pass
        for item in self.data:
            temp_list.append(item!=other)
        j = 0
        for i in temp_list.__iter__():
            if i:
                ret_list.append(df.sort_data[j])
            j = j + 1

        return ret_list
    def __ge__(self, other):
        ret_list = []
        temp_list=[]
        try:
            other=datetime.strptime(other,'%m/%d/%y %H:%M')
        except:
            pass

        for item in self.data:
            temp_list.append(item >= other)
        j = 0
        for i in temp_list.__iter__():
            if i:
                ret_list.append(df.sort_data[j])
            j = j + 1

        return ret_list

    def __le__(self, other):
        ret_list = []
        temp_list=[]
        try:
            other=datetime.strptime(other,'%m/%d/%y %H:%M')
        except:
            pass

        for item in self.data:
            temp_list.append(item <= other)
        j = 0
        for i in temp_list.__iter__():
            if i:
                ret_list.append(df.sort_data[j])
            j = j + 1

        return ret_list

    def __lt__(self, other):
        ret_list = []
        temp_list=[]
        for item in self.data:
            temp_list.append(item < other)
        j = 0
        for i in temp_list.__iter__():
            if i:
                ret_list.append(df.sort_data[j])
            j = j + 1

        return ret_list

    def __gt__(self, other):
        ret_list = []
        temp_list=[]
        for item in self.data:
          temp_list.append(item > other)
        j = 0
        for i in temp_list.__iter__():
             if i:
                 ret_list.append(df.sort_data[j])
             j = j + 1

        return ret_list

infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]


df = DataFrame(list_of_lists=data)

#TASK 1: Checking the Sort Function
print df.sort_by('Name',True)

#TASK 2: Comparison of Columns
print df['Transaction_date']>='1/31/09 21:50'



