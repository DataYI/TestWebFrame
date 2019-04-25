import pandas as pd
import unittest
from pathlib import Path
from src.config.config import Config


def add_case(ser: pd.Series) -> None:
    '''
    每一行作为一个case处理，添加到上级作用域中的suite对象
    '''
    nonlocal suite
    # path = ser['路径']
    # file_name = ser['文件名']
    # class_name = ser['类名']
    # function_name = ser['方法名']
    import_args = ser[['路径', '文件名', '类名', '方法名']].tolist()
    # 路径的斜杠要转为点
    import_args[0] = Path(import_args[0]).as_posix().replace('/', '.')
    config_way = ser['配置方式']
    # 生成脚本
    if '1' in config_way:
        # 按方法名添加
        script = 'from {0}.{1} import {2}\nsuite.addTest({2}("{3}"))'.format(*import_args)
    elif '2' in config_way:
        # 按类名添加
        script = 'from {0}.{1} import {2}\nsuite.addTest(unittest.TestLoader().loadTestsFromTestCase("{2}"))'.format(*import_args[:-1])
    elif '3' in config_way:
        # 按文件名添加
        script = 'from {0} import {1}\nsuite.addTest(unittest.TestLoader().loadTestFromModule("{1}"))'.format(*import_args[:2])
    elif '4' in config_way:
        # 按路径添加
        script = 'suite.addTest(unittest.TestLoader().discover("{0}"))'.format(import_args[0])
    # 执行脚本
    try:
        exec(script)
    except(ImportError, ModuleNotFoundError):
        print('案例配置有误，详情如下：\n', str(ser)[:-14])


# 读取测试案例配置.xlsx，返回一个或多个suite(取决于配置了多少个sheet页，sheet页之间是多进程并行执行)
def get_suites_by_excel(file: Path) -> list:
    '''
    excel文件中每个sheet中的多个案例组织为一个suite，多个sheet对应多个suite，返回所有suite组成的列表
    '''
    suites = []
    reader = pd.ExcelFile(file)
    sheets = reader.sheet_names

    for sheet in sheets:
        suite = unittest.TestSuite()
        df = pd.read_excel(reader, sheet)
        # 筛选出要执行的案例
        df = df.loc[df['是否执行'].isin(['y', 'Y']), ['路径', '文件名', '类名', '方法名']]
        # 添加案例到suite
        df.apply(add_case, axis=1)
        suites.append(suite)
    return suites


# 读取测试计划配置
def get_test_plan() -> list:
    '''
    读取文件`测试计划配置.xlsx`，得到测试计划列表
    '''
    file_path = Config().plan_file_path
    df = pd.read_excel(file_path)
    ser = df.loc[df['是否执行'].isin(['Y', 'y']), '文件名']
    return ser.tolist()


# 获取执行计划列表
def get_all_test_plan() -> list:
    '''
    调用`get_test_plan`获取测试计划列表，再根据列表，从对应的每个excel文件中获取suites，返回一个包含所有的suites的列表
    '''
    # 所有测试计划文件名的列表
    plan = get_test_plan()
    return [get_suites_by_excel(Path(f)) for f in plan]


if __name__ == '__main__':
    print(get_all_test_plan())