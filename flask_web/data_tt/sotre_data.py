import json
import os
import datetime
import xlrd
import pandas as pd
from bases.lib_database import getDBSchema
from data_tt.base_data import base_data


class StoreData(object):
    item_code = ''
    item_code2 = ''
    category = ''
    desc = ''
    unit = ''
    qty = ''

class AdminStore(base_data):
    def clear(self, tmp):
        result = str(tmp).replace('-', '').replace(',', '').replace('.0', '').strip()
        if result == '':
            result = '0'
        return result

    def haveIMA(self, item_code):
        result = False
        db_name = getDBSchema('d6part2', True)
        sql = """select * from {db_name}.ima_file where ima01 = '{item_code}'"""
        sql = sql.format(item_code=item_code, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        cursor.fetchall()
        if cursor.rowcount > 0:
            result = True
        return result

    def getStockQty(self, item_code):
        db_name = getDBSchema('d6part2', True)
        sql = """select img01,img10 from {db_name}.img_file where img01 = '{item_code}' and img02 = '002'"""
        sql = sql.format(item_code=item_code, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        result = cursor.fetchone()
        if result is not None:
            result = result[1]
        else:
            result = 0
        return result


    # def read_excel(self, data_date):
    #     print('read_excel:'+data_date)
    #     file = 'D:\\ExcelTemp\\D6Store_{data_date}.xlsx'
    #     file = file.format(data_date=data_date)
    #     if not os.path.exists(file):
    #         return ""
    #
    #     wb = xlrd.open_workbook(filename=file)  # 打开文件
    #     sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
    #     tRows = sheet1.nrows
    #     data_list = []
    #
    #     tt_data = self.getTTData(data_date)
    #     for r in range(tRows):
    #         row = sheet1.row_values(r)
    #         item_code = str(row[1]).replace('.0', '')
    #         barcode = str(row[2]).replace('.0', '')
    #         qty = row[17]
    #         if len(str(row[0])) > 0 and len(item_code) == 10 and qty != 0:
    #             data = {}
    #
    #             data['item_code'] = item_code
    #             data['barcode'] = barcode
    #             data['category'] = row[3]
    #             data['desc'] = row[4]
    #             data['unit'] = row[5]
    #             data['qty'] = qty
    #             data['price'] = row[18]
    #
    #             data['tt_name'] = 'N/A'
    #             data['tt_spec'] = 'N/A'
    #             data['tt_qty'] = 'N/A'
    #             data['tt_unit'] = 'N/A'
    #             result_msg = ''
    #             for tt_row in tt_data:
    #                 if tt_row['INB04'] == item_code:
    #                     tt_qty = tt_row['INB16']
    #                     data['tt_name'] = tt_row['IMA02']
    #                     data['tt_spec'] = tt_row['IMA021']
    #                     data['tt_qty'] = tt_qty
    #                     data['tt_unit'] = tt_row['INB08']
    #
    #             if data['tt_qty'] == 'N/A':
    #                 if self.haveIMA(item_code):
    #                     result_msg += "TT aimt301 No Data,"
    #                 else:
    #                     result_msg += "TT No Item Code,"
    #             else:
    #                 if qty != tt_qty:
    #                     result_msg += "Qty Incorrect,"
    #
    #                 if tt_row['INAPOST'] == 'N' and self.getStockQty(item_code) < tt_qty:
    #                     result_msg += "TT No Stock Qty,"
    #             if len(result_msg) > 0:
    #                 result_msg = result_msg[:-1]
    #             else:
    #                 result_msg = "OK"
    #             data['result_msg'] = result_msg
    #             data_list.append(data)
    #             print(row)
    #
    #     return data_list

    def getTTData(self, data_date):
        db_name = getDBSchema('d6part2', True)
        sql = """select inb04,ima02,ima021,inb08,inapost,sum(inb16) inb16 from {db_name}.ina_file a, {db_name}.inb_file b,{db_name}.ima_file c
                 where ina01 = inb01 and ina02 = to_date('{data_date}','yyyymmdd') and b.inb04 = c.ima01 group by inb04,ima02,ima021,inb08,inapost"""
        sql = sql.format(sql, data_date=data_date, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        query_result = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

        return query_result

    def getTTStockData(self):
        db_name = getDBSchema('d6part2', True)
        sql = """select img01,img10 from {db_name}.img_file where img02 = '002'"""
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)

        results = {}

        for row in cursor.fetchall():
            results[row[0]] = row[1]
        return results

    def get_sheet_name(self, data_date):
        month_map = {"01": "JANUARY", "02": "FEBRUARY", "03": "MARCH", "04": "APRIL", "05": "MAY", "06": "JUNE",
                     "07": "JULY", "08": "AUGUST", "09": "SEPTEMBER", "10": "OCTOBER", "11": "NOVEMBER", "12": "DECEMBER"}
        month_day_map = {"01": " 16-31", "02": " 16-28", "03": " 16-31", "04": " 16-30", "05": " 16-31", "06": " 16-30",
                     "07": " 16-31", "08": " 16-31", "09": " 16-30", "10": " 16-31", "11": " 16-30",
                     "12": " 16-31"}

        yyyy = data_date[0:4]
        mm = data_date[4:6]
        dd = data_date[6:8]
        sheet_url = ""

        if yyyy == "2020":
            sheet_url = "https://docs.google.com/spreadsheets/d/1JTVtkilTHeRNrrFrthjPWUBraOMb3RwKSgkx0NUw7ps/edit#gid=1395785703"
        elif yyyy == "2021":
            sheet_url = "https://docs.google.com/spreadsheets/d/1--c_l18X4Z01GmXrEGB8S7fLNOENjfGcSI5IanUBoO8/edit#gid=172355127"

        if int(dd) > 15:
            t_dd = month_day_map[mm]
            move_index = (int(dd)-15 - 1) * 2
        else:
            t_dd = " 1-15"
            move_index = (int(dd) - 1) * 2

        return month_map[mm] + t_dd, move_index, sheet_url

    def google_excel(self, data_date):
        import pygsheets

        yesterday = (datetime.date.today() + datetime.timedelta(-1)).strftime("%d")

        sheet_name, move_index, sheet_url = self.get_sheet_name(data_date)

        gc = pygsheets.authorize(service_file='D:\\ExcelTemp\\box_chang.json')
        sht = gc.open_by_url(
            sheet_url
        )
        #wks_list = sht.worksheets()
        worksheet = sht.worksheet_by_title(sheet_name)
        #worksheet = sht.get_worksheet(23)
        print(worksheet)
        df = worksheet.get_as_df()

        stock_index = self.get_stock_key(df)
        cash_index = self.get_start_key(df)+move_index

        tRows, tCols = df.shape
        data_list = []

        tt_data = self.getTTData(data_date)
        tt_stock_data = self.getTTStockData()

        for r in range(tRows):
            item_code = str(df.iloc[r, 1]).replace('.0', '')
            barcode = str(df.iloc[r, 2]).replace('.0', '')
            qty = df.iloc[r, cash_index] #計算出昨天的位置

            if len(item_code) == 10 and qty != 0 and str(qty).strip() != '-':
                data = {}

                data['item_code'] = item_code
                data['barcode'] = barcode
                data['category'] = df.iloc[r, 3]
                data['desc'] = df.iloc[r, 4]
                data['unit'] = df.iloc[r, 5]
                data['qty'] = self.clear(qty)
                data['price'] = df.iloc[r, cash_index+1]

                data['tt_name'] = 'N/A'
                data['tt_spec'] = 'N/A'
                data['tt_qty'] = 'N/A'
                data['tt_unit'] = 'N/A'
                data['tt_stock'] = 'N/A'
                data['exl_stock'] = 'N/A'
                result_msg = ''

                #取得TT的資料
                for tt_row in tt_data:
                    if tt_row['INB04'] == item_code:
                        tt_qty = int(tt_row['INB16'])
                        data['tt_name'] = tt_row['IMA02']
                        data['tt_spec'] = tt_row['IMA021']
                        data['tt_qty'] = tt_qty
                        data['tt_unit'] = tt_row['INB08']

                #若資料是昨天，就比對庫存
                #if data_date[6:8] == yesterday and tt_row['INAPOST'] == 'Y':
                if data_date[6:8] == yesterday:
                    if len(tt_data) > 0:
                        if tt_row['INAPOST'] == 'Y':
                            data['tt_stock'] = self.clear(tt_stock_data[item_code])
                            data['exl_stock'] = self.clear(df.iloc[r, stock_index])
                        else:
                            if tt_stock_data[item_code] is None:
                                tt_stock_qty = 0
                            else:
                                tt_stock_qty = int(tt_stock_data[item_code])
                            data['tt_stock'] = self.clear(tt_stock_qty-tt_qty)
                            data['exl_stock'] = self.clear(df.iloc[r, stock_index])


                if data['tt_qty'] == 'N/A':
                    if self.haveIMA(item_code):
                        result_msg += "TT aimt301 No Data,"
                    else:
                        result_msg += "TT No Item Code,"
                else:
                    if self.clear(str(qty)) != str(tt_qty):
                        result_msg += "Qty Incorrect,"

                    if tt_row['INAPOST'] == 'N' and (tt_stock_data[item_code] is None or int(tt_stock_data[item_code]) < int(tt_qty)):
                        result_msg += "TT No Stock Qty,"

                    if str(data['tt_stock']) != str(data['exl_stock']):
                        result_msg += "Stock Gap,"

                if len(result_msg) > 0:
                    result_msg = result_msg[:-1]
                else:
                    result_msg = "OK"
                data['result_msg'] = result_msg
                data_list.append(data)

        return data_list

    def get_start_key(self, df):
        rows, cols = df.shape
        for col in range(cols):
            if df.iloc[0, col] == "CASH\nOUT":
                return col
        return 0

    def get_stock_key(self, df):
        index = 0
        df_cols = list(df.columns.values)
        for col in df_cols:
            if col == "REMAINING BALANCE":
                break
            index += 1
        return index

# ad = AdminStore()
# ad.google_excel('20210301')