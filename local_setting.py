class LocalSetting():
    decimal='.'

def fft(f:float)->str:
    return ('%10.2f' % f).replace('.',LocalSetting.decimal)