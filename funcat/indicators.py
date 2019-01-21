# -*- coding: utf-8 -*-

from .api import (
    OPEN, HIGH, LOW, CLOSE, VOLUME, VOL,
    ABS, MAX, HHV, LLV,
    REF, IF, SUM, STD,
    MA, EMA, SMA,
    AVEDEV,
    COUNT,
    MIN,
    AMOUNT,
    SQRT,
    ADVANCE,
    DECLINE,
    CAPITAL,
    DMA,
    INDEXO,
    INDEXH,
    INDEXL,
    INDEXC,
    INDEXV,
)


def KDJ(N=9, M1=3, M2=3):
    """
    KDJ 随机指标
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2

    return K, D, J


def DMI(M1=14, M2=6):
    """
    DMI 趋向指标
    """
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
    HD = HIGH - REF(HIGH, 1)
    LD = REF(LOW, 1) - LOW

    DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
    DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
    DI1 = DMP * 100 / TR
    DI2 = DMM * 100 / TR
    ADX = MA(ABS(DI2 - DI1) / (DI1 + DI2) * 100, M2)
    ADXR = (ADX + REF(ADX, M2)) / 2

    return DI1, DI2, ADX, ADXR


def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIF, M)
    MACD = (DIF - DEA) * 2

    return MACD


def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100

    return RSI1, RSI2, RSI3


def BOLL(N=20, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P

    return UPPER, MID, LOWER


def WR(N=10, N1=6):
    """
    W&R 威廉指标
    """
    WR1 = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR2 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100

    return WR1, WR2


def BIAS(L1=5, L4=3, L5=10):
    """
    BIAS 乖离率
    """
    BIAS = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L4)) / MA(CLOSE, L4) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L5)) / MA(CLOSE, L5) * 100

    return BIAS, BIAS2, BIAS3


def ASI(M1=26, M2=10):
    """
    ASI 震动升降指标
    """
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    BB = ABS(LOW - LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))
    R = IF((AA > BB) & (AA > CC), AA + BB / 2 + DD / 4, IF((BB > CC) & (BB > AA), BB + AA / 2 + DD / 4, CC + DD / 4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))
    SI = X * 16 / R * MAX(AA, BB)
    ASI = SUM(SI, M1)
    ASIT = MA(ASI, M2)

    return ASI, ASIT


def VR(M1=26):
    """
    VR容量比率
    """
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOL, 0), M1) / SUM(IF(CLOSE <= LC, VOL, 0), M1) * 100

    return VR


def BRAR(N=26):
    """
    BRAR人气意愿指标
    """
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), N) / SUM(MAX(0, REF(CLOSE, 1) - LOW), N) * 100
    AR = SUM(HIGH - OPEN, N) / SUM(OPEN - LOW, N) * 100

    return BR, AR


def DPO(M1=20, M2=10, M3=6):
    DPO = CLOSE - REF(MA(CLOSE, M1), M2)
    MADPO = MA(DPO, M3)

    return DPO, MADPO


def TRIX(M1=12, M2=20):
    TR = EMA(EMA(EMA(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    TRMA = MA(TRIX, M2)

    return TRIX, TRMA


def ATR(N=14):
    MTR = MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW))
    ATR = MA(MTR, N)

    return ATR


def CCI(N=14):
    TYP = (HIGH + LOW + CLOSE) / 3
    CCI = (TYP - MA(TYP, N)) / (0.015 * AVEDEV(TYP, N))

    return CCI

def PSY(N=12, M=6):
    PSY = COUNT(CLOSE > REF(CLOSE, 1), N) / N * 100
    PSYMA = MA(PSY, M)

    return PSYMA

def EXPMA(M1=12, M2=50):
    EXP1 = EMA(CLOSE, M1)
    EXP2 = EMA(CLOSE, M2)

    return EXP1, EXP2

def XS(N=13):
    VAR2 = CLOSE * VOL
    VAR3 = EMA((EMA(VAR2, 3) / EMA(VOL, 3) + EMA(VAR2, 6) / EMA(VOL, 6) + EMA(VAR2, 12) / EMA(VOL, 12) + EMA(VAR2,24)
                / EMA(VOL, 24)) / 4, N)
    SUP = 1.06 * VAR3
    SDN = VAR3 * 0.94
    VAR4 = EMA(CLOSE, 9)
    LUP = EMA(VAR4 * 1.14, 5)
    LDN = EMA(VAR4 * 0.86, 5)

    return SUP, SDN, LUP, LDN

def CYR(M=5, N=13):
    DIVE = 0.01 * EMA(AMOUNT, N) / EMA(VOL, N)
    CYR = (DIVE / REF(DIVE, 1) - 1) * 100
    MACYR = MA(CYR, M)

    return MACYR

def CYW():
    VAR1 = CLOSE - LOW
    VAR2 = HIGH - LOW
    VAR3 = CLOSE - HIGH
    VAR4 = IF(HIGH > LOW, (VAR1 / VAR2 + VAR3 / VAR2) * VOL, 0)
    CYW = SUM(VAR4, 10) / 10000

    return CYW

def HISV(N=60):
    HSIV = STD(CLOSE, N) * SQRT(250) * 100.0

    return HSIV

def ARMS(N=21, INDEX='000300.XSHG'):
    ARMS = EMA(ADVANCE / DECLINE, N)

    return ARMS

def FSL():
    """
    若数据源为tushare，则只能拿到2016-08-09之后的流通股数，在此之前的流通股为np.nan
    :return:
    """
    SWL = (EMA(CLOSE, 5) * 7 + EMA(CLOSE, 10) * 3) / 10
    SWS = DMA(EMA(CLOSE, 12), MAX(1, 100 * (SUM(VOL, 5) / (3 * CAPITAL))))

    return SWL, SWS


def HMA(M1=6, M2=12, M3=30, M4=72, M5=144):
    HMA1 = MA(HIGH, M1)
    HMA2 = MA(HIGH, M2)
    HMA3 = MA(HIGH, M3)
    HMA4 = MA(HIGH, M4)
    HMA5 = MA(HIGH, M5)

    return HMA1, HMA2, HMA3, HMA4, HMA5


def LMA(M1=6, M2=12, M3=30, M4=72, M5=144):
    LMA1 = MA(LOW, M1)
    LMA2 = MA(LOW, M2)
    LMA3 = MA(LOW, M3)
    LMA4 = MA(LOW, M4)
    LMA5 = MA(LOW, M5)

    return LMA1, LMA2, LMA3, LMA4, LMA5


def AMV(M1=5, M2=13, M3=34, M4=60):
    AMOV = VOL * (OPEN + CLOSE) / 2
    AMV1 = SUM(AMOV, M1) / SUM(VOL, M1)
    AMV2 = SUM(AMOV, M2) / SUM(VOL, M2)
    AMV3 = SUM(AMOV, M3) / SUM(VOL, M3)
    AMV4 = SUM(AMOV, M4) / SUM(VOL, M4)

    return AMV1, AMV2, AMV3, AMV4


def ABI(M=10):
    ABI = 100 * ABS(ADVANCE - DECLINE) / (ADVANCE + DECLINE)
    MAABI = EMA(ABI, M)

    return ABI, MAABI


def MCL(N1=19, N2=39):
    DIF = ADVANCE - DECLINE
    EMA1 = EMA(DIF, N1)
    EMA2 = EMA(DIF, N2)
    MCL = EMA1 - EMA2
    MAMCL1 = EMA1
    MAMCL2 = EMA2

    return MCL, MAMCL1, MAMCL2


def MIKE(N=10):
    HLC = REF(MA((HIGH + LOW + CLOSE) / 3, N), 1)
    HV = EMA(HHV(HIGH, N), 3)
    LV = EMA(LLV(LOW, N), 3)
    STOR = EMA(2 * HV - LV, 3)
    MIDR = EMA(HLC + HV - LV, 3)
    WEKR = EMA(HLC * 2 - LV, 3)
    WEKS = EMA(HLC * 2 - HV, 3)
    MIDS = EMA(HLC - HV + LV, 3)
    STOS = EMA(2 * LV - HV, 3)

    return STOR, MIDR, WEKR, WEKS, MIDS, STOS


def CR(N=26):
    MID = REF(HIGH + LOW, 1) / 2
    CR = SUM(MAX(0, HIGH - MID), N) / SUM(MAX(0, MID - LOW), N) * 100

    return CR


def ROC(N=12, M=6):
    ROC = 100 * (CLOSE - REF(CLOSE, N)) / REF(CLOSE, N)
    MAROC = MA(ROC, M)

    return ROC, MAROC

def ZLMM():
    LC = REF(CLOSE, 1)
    RSI2 = SMA(MAX(CLOSE - LC, 0), 12, 1) / SMA(ABS(CLOSE - LC), 12, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), 18, 1) / SMA(ABS(CLOSE - LC), 18, 1) * 100
    MMS = MA(3 * RSI2 - 2 * SMA(MAX(CLOSE - LC, 0), 16, 1) / SMA(ABS(CLOSE - LC), 16, 1) * 100, 3)
    MMM = EMA(MMS, 8)
    MML = MA(3 * RSI3 - 2 * SMA(MAX(CLOSE - LC, 0), 12, 1) / SMA(ABS(CLOSE - LC), 12, 1) * 100, 5)

    return MMS, MMM, MML


def LB():
    ZY2 = VOL / INDEXV * 1000

    return ZY2

def XDT(M=5, N=10):
    QR = CLOSE / INDEXC * 1000
    MQR1 = MA(QR, M)
    MQR2 = MA(QR, N)

    return QR, MQR1, MQR2


def SMX(N=50):
    ZY = CLOSE / INDEXC * 2000
    ZY1 = EMA(ZY, 3)
    ZY2 = EMA(ZY, 17)
    ZY3 = EMA(ZY, 34)

    return ZY1, ZY2, ZY3


def RAD(D=3, S=30, M=30):
    SM = (OPEN + HIGH + CLOSE + LOW) / 4
    SMID = MA(SM, D)
    IM = (INDEXO + INDEXH + INDEXL + INDEXC) / 4
    IMID = MA(IM, D)
    SI1 = (SMID - REF(SMID, 1)) / SMID
    II = (IMID - REF(IMID, 1)) / IMID
    RADER1 = SUM((SI1 - II) * 2, S) * 1000
    RADERMA = SMA(RADER1, M, 1)

    return RADER1, RADERMA