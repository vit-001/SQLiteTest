# -*- coding: utf-8 -*-
__author__ = 'Vit'

if __name__ == "__main__":
    from gymboomreader import GymBoomReader
    from model_classes import Statistic,CreateTable
    from gb_base import Base
    from dbconvert import DBConvert
    from model_classes import ExportXLS

    gb= GymBoomReader('base/1.gb')
    base= Base()

    DBConvert(gb, base)

    # base.export()

    # base.stat()

    Statistic.proceed(base)

    ex = ExportXLS(base)


    ex.proceed_to_xls('out.xlsx')
    # with open('out.csv', 'w') as fd:
    #     # base.export_csv(fd)
    #     CreateTable.proceed(base,fd)


