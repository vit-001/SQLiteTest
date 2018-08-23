# -*- coding: utf-8 -*-
__author__ = 'Vit'

if __name__ == "__main__":
    from gymboomreader import GymBoomReader
    from model_classes import Base
    from dbconvert import DBConvert

    gb= GymBoomReader('base/1.gb')
    base= Base()

    DBConvert(gb, base)



    base.export()



