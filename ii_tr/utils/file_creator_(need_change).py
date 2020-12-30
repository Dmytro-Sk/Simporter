import pandas as pd
import csv


class TRInfo:
    def __init__(self, args):
        self.file_path = args.get('tr_file_path')
        self.file_name = args.get('tr_file_name')
        self.sheet_name = args.get('sheet_name')
        self.slicer1 = args.get('slicer1')
        self.slicer2 = args.get('slicer2')
        self.column_name = args.get('column_name')
        self.df = pd.read_excel(f'{self.file_path}{self.file_name}', self.sheet_name, engine='openpyxl').fillna('-')

    def data_from_df(self):
        if self.column_name is None:
            return self.df.columns[self.slicer1:self.slicer2]
        else:
            return self.df[f'{self.column_name}'][self.slicer1:self.slicer2]


class FileCreator:
    def __init__(self, args):
        self.conv_data_file_path = args.get('conv_data_file_path')
        self.conv_data_file_name = args.get('conv_data_file_name')
        self.url_list_file_path = args.get('url_list_file_path')
        self.url_list_file_name = args.get('url_list_file_name')
        self.initial_url = args.get('initial_url')
        self.result_file_path = args.get('result_file_path')
        self.result_file_name = args.get('result_file_name')

    def write_column(self, data_list, func) -> None:
        with open(self.conv_data_file_path + self.conv_data_file_name, 'a') as f:
            f.write(self.conv_def_name(func))
            f.writelines('\n'.join(data_list) + '\n' * 3)

    def write_row(self, data_list, func) -> None:
        with open(self.conv_data_file_path + self.conv_data_file_name, 'a') as f:
            f.write(self.conv_def_name(func))
            f.write(f'[{", ".join(data_list)}]' + '\n' * 3)

    def create_url_list(self) -> None:
        pd.DataFrame([self.initial_url], columns=[]).to_csv(
            self.url_list_file_path + self.url_list_file_name)

    def create_final_table(self, data_list) -> None:
        columns_names_list = []
        columns_names_list.extend([i for i in data_list])
        with open(self.result_file_path + self.result_file_name, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=columns_names_list)
            csv_writer.writeheader()

    @staticmethod
    def conv_def_name(func):
        conv_def_name = f' {func.__name__.replace("_", " ").upper()} '.center(50, "-") + '\n' * 2
        return conv_def_name


class Converter:
    @staticmethod
    def get_locators(data_list):
        converted_locators_list = []
        for locator in data_list:
            converted_locator = locator.replace(' ', '_').upper() + ' = \'\''
            converted_locators_list.append(converted_locator)
        return converted_locators_list

    @staticmethod
    def get_elements_names_for_parse(data_list):
        converted_elements_names_list = ['items = ProjectNameItem', '\n' * 2]
        for element_name in data_list:
            converted_element_name = f"{element_name.replace(' ', '_').lower()} = response.xpath(Locators.{element_name.replace(' ', '_').upper()}).get()"
            converted_elements_names_list.append(converted_element_name)
        return converted_elements_names_list

    @staticmethod
    def get_elements_names_for_result(data_list):
        converted_elements_names_list = ['self.url_index = url_index', 'self.url = url']
        for element_name in data_list:
            converted_element_name = f'self.{element_name.replace(" ", "_").lower()}'
            converted_elements_names_list.append(converted_element_name)
        return converted_elements_names_list

    @staticmethod
    def get_columns_names(data_list):
        columns_names_list = ['index', 'url']
        for column in data_list:
            converted_column = column.lower().replace('_', ' ').title()
            columns_names_list.append(converted_column)
        return columns_names_list


"""Put and initial data"""

data = {
    'url_list_file_path': '../',
    'url_list_file_name': './url_list.xlsx',
    'initial_url': 'https://www.dresslily.com/hoodies-c-181.html',
    'conv_data_file_path': './',
    'conv_data_file_name': 'converted_data_reviews.txt',
    'result_file_path': '../../iii_results/',
    'result_file_name': 'final_table_products.csv',
    'tr_file_path': '../',
    'tr_file_name': 'req_data.xlsx',
    'sheet_name': 'Sheet1',
    'slicer1': 0,
    'slicer2': 6,
    'column_name': 'reviews'  # set column name if data from column otherwise set None
}

tr_inf = TRInfo(data)
fc = FileCreator(data)
con = Converter()


"""Create converted_data file"""

# get_locators
fc.write_column(con.get_locators(tr_inf.data_from_df()), con.get_locators)
# get_elements_names_for_parse
fc.write_column(con.get_elements_names_for_parse(tr_inf.data_from_df()), con.get_elements_names_for_parse)





# get_elements_names_for_result
fc.write_row(con.get_elements_names_for_result(tr_inf.data_from_df()), con.get_elements_names_for_result)
# get_columns_names
fc.write_row(con.get_columns_names(tr_inf.data_from_df()), con.get_columns_names)


"""Create url_list and final_table files"""

# ATTENTION, rewrites file.
# fc.create_url_list()   # create_url_list.
# fc.create_final_table(Converter().get_columns_names(tr_inf.data_from_df()))  # create_final_table
