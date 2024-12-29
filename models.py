import ctypes

class BEMCalcProgressStructure(ctypes.Structure):
    """
    计算进度结构体结构体
    """
    _fields_ = [
        ("nCurrentCalculationStep", ctypes.c_long), # ' nCurrentCalculationStep - Current step count
        ("nCurrentCalculationStepMax", ctypes.c_long), # ' nCurrentCalculationStepMax - Estimate of maximum step
        ("nCurrentGoalSeekIteration", ctypes.c_long), # ' nCurrentGoalSeekIteration - Current interation (Goal Seeker)
        ("nCurrentGoalSeekIterationMax", ctypes.c_long), # ' nCurrentGoalSeekIterationMax - Maximum interation (Goal Seeker)
        ("dPrevGoalValue", ctypes.c_double), # ' dPrevGoalValue - Previous Goal value (Goal Seeker)
        ("dPrevImpedance", ctypes.c_double) # ' dPrevImpedance - Previous Impedance value (Goal Seeker)
    ]

    def __init__(self, nCurrentCalculationStep=0, nCurrentCalculationStepMax=0, 
                 nCurrentGoalSeekIteration=0, nCurrentGoalSeekIterationMax=0, 
                 dPrevGoalValue=0.0, dPrevImpedance=0.0):
        super().__init__(nCurrentCalculationStep, nCurrentCalculationStepMax, 
                         nCurrentGoalSeekIteration, nCurrentGoalSeekIterationMax, 
                         dPrevGoalValue, dPrevImpedance)

class BEMCalcResultStructure(ctypes.Structure):
    """
    计算返回结果结构体
    """
    _fields_ = [
        ("dResultValid", ctypes.c_double),       # dResultValid 0 == invalid result
        ("dImpedance", ctypes.c_double),          # dImpedance Calculated impedance (Ohms)
        ("dDelay", ctypes.c_double),              # dDelay Calculated time delay (ps)
        ("dErEff", ctypes.c_double),              # dErEff Calculated effect Er
        ("dInductance", ctypes.c_double),         # dInductance Calculated inductance (nH/m)
        ("dCer", ctypes.c_double)                # dCer Calculated capacitance (pF/m)
    ]

    def __init__(self, dResultValid=0.0, dImpedance=0.0, dDelay=0.0, dErEff=0.0, 
                 dInductance=0.0, dCer=0.0):
        super().__init__(dResultValid, dImpedance, dDelay, dErEff, 
                         dInductance, dCer)

    def __str__(self):
        return (f"BEMCalcResultStructure(dResultValid={self.dResultValid}, "
                f"dImpedance={self.dImpedance}, dDelay={self.dDelay}, "
                f"dErEff={self.dErEff}, dInductance={self.dInductance}, "
                f"dCer={self.dCer})")
    
class BEMErrorStructure(ctypes.Structure):
    """
    计算错误结果结构体
    """
    _fields_ = [
        ("nError", ctypes.c_long),   
        ("nErrParam1", ctypes.c_long),  
        ("nErrParam2", ctypes.c_long),         
        ("nErrorParamForVB", ctypes.c_int),   
        ("dErrParam3", ctypes.c_double),         
        ("dErrParam4", ctypes.c_double)          
    ]

    def __init__(self, nError=0, nErrParam1=0, nErrParam2=0, nErrorParamForVB=0, 
                 dErrParam3=0.0, dErrParam4=0.0):
        super().__init__(nError, nErrParam1, nErrParam2, nErrorParamForVB, 
                         dErrParam3, dErrParam4)

    def __str__(self):
        return (f"BEMErrorStructure(nError={self.nError}, "
                f"nErrParam1={self.nErrParam1}, nErrParam2={self.nErrParam2}, "
                f"nErrorParamForVB={self.nErrorParamForVB}, dErrParam3={self.dErrParam3}, "
                f"dErrParam4={self.dErrParam4})")

class ModelAllowedSpecificCode():
    # 单线
    glngSURFACEMICROSTRIP1B = 11
    glngSURFACEMICROSTRIP2B = 12
    glngEMBEDDEDMICROSTRIP1B1A = 22
    glngEMBEDDEDMICROSTRIP1B2A = 25
    glngEMBEDDEDMICROSTRIP1E1B2A = 65
    glngEMBEDDEDMICROSTRIP2B1A = 23 
    glngEMBEDDEDMICROSTRIP2B2A = 24
    glngOFFSETSTRIPLINE1B1A = 32
    glngOFFSETSTRIPLINE1B2A = 35
    glngOFFSETSTRIPLINE2B1A = 33
    glngOFFSETSTRIPLINE2B2A = 34
    glngCOATEDMICROSTRIP1B = 51
    glngCOATEDMICROSTRIP2B = 52
    glngDUALCOATEDMICROSTRIP1B = 55

    # 差分
    glngEDGECOUPLEDSURFACEMICROSTRIP1B = 111
    glngEDGECOUPLEDSURFACEMICROSTRIP2B = 112
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP1B1A = 122
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP1B2A = 125
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP1E1B2A = 165
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP2B1A = 123
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP2B2A = 124
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP1B1A1R = 128
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP2B1A1R = 129
    glngEDGECOUPLEDEMBEDDEDMICROSTRIP2B2A1R = 194
    glngEDGECOUPLEDOFFSETSTRIPLINE1B1A = 132
    glngEDGECOUPLEDOFFSETSTRIPLINE1B2A = 135
    glngEDGECOUPLEDOFFSETSTRIPLINE2B1A = 133
    glngEDGECOUPLEDOFFSETSTRIPLINE2B2A = 134
    glngEDGECOUPLEDOFFSETSTRIPLINE1B1A1R = 137
    glngEDGECOUPLEDOFFSETSTRIPLINE2B1A1R = 138
    glngEDGECOUPLEDCOATEDMICROSTRIP1B = 151
    glngEDGECOUPLEDCOATEDMICROSTRIP2B = 152
    glngEDGECOUPLEDDUALCOATEDMICROSTRIP2B = 155
    glngDIFFBROADSIDESTRIPLINE2S = 1132
    glngDIFFBROADSIDESTRIPLINE3S = 1133

    # 单线 共面
    glngSURFACECOPLANARSTRIPS1B = 811
    glngSURFACECOPLANARSTRIPS2B = 812
    glngSURFACECOPLANARSTRIPSWITHLOWERGND1B = 411
    glngSURFACECOPLANARSTRIPSWITHLOWERGND2B = 412
    glngSURFACECOPLANARWAVEGUIDE1B = 611
    glngSURFACECOPLANARWAVEGUIDE2B = 612
    glngSURFACECOPLANARWAVEGUIDEWITHLOWERGROUND1B = 211
    glngSURFACECOPLANARWAVEGUIDEWITHLOWERGROUND2B = 212
    glngCOATEDCOPLANARSTRIPS1B = 851
    glngCOATEDCOPLANARSTRIPS2B = 852
    glngCOATEDCOPLANARSTRIPSWITHLOWERGND1B = 451
    glngCOATEDCOPLANARSTRIPSWITHLOWERGND2B = 452
    glngCOATEDCOPLANARWAVEGUIDE1B = 651
    glngCOATEDCOPLANARWAVEGUIDE2B = 652
    glngCOATEDCOPLANARWAVEGUIDEWITHLOWERGROUND1B = 251
    glngCOATEDCOPLANARWAVEGUIDEWITHLOWERGROUND2B = 252
    glngEMBEDDEDCOPLANARSTRIPS1B1A = 822
    glngEMBEDDEDCOPLANARSTRIPS2B1A = 823
    glngEMBEDDEDCOPLANARSTRIPSWITHLOWERGND1B1A = 422
    glngEMBEDDEDCOPLANARSTRIPSWITHLOWERGND2B1A = 423
    glngEMBEDDEDCOPLANARWAVEGUIDE1B1A = 622
    glngEMBEDDEDCOPLANARWAVEGUIDE2B1A = 623
    glngEMBEDDEDCOPLANARWAVEGUIDEWITHLOWERGROUND1B1A = 222
    glngEMBEDDEDCOPLANARWAVEGUIDEWITHLOWERGROUND2B1A = 223
    glngOFFSETCOPLANARSTRIPS1B1A = 432
    glngOFFSETCOPLANARSTRIPS2B1A = 433
    glngOFFSETCOPLANARWAVEGUIDE1B1A = 232
    glngOFFSETCOPLANARWAVEGUIDE2B1A = 233

    # 差分 共面
    glngDIFFSURFACECOPLANARSTRIPS1B = 911
    glngDIFFSURFACECOPLANARSTRIPS2B = 912
    glngDIFFSURFACECOPLANARSTRIPSWITHLOWERGND1B = 511
    glngDIFFSURFACECOPLANARSTRIPSWITHLOWERGND2B = 512
    glngDIFFSURFACECOPLANARWAVEGUIDE1B = 711
    glngDIFFSURFACECOPLANARWAVEGUIDE2B = 712
    glngDIFFSURFACECOPLANARWAVEGUIDEWITHLOWERGND1B = 311
    glngDIFFSURFACECOPLANARWAVEGUIDEWITHLOWERGND2B = 312
    glngDIFFCOATEDCOPLANARSTRIPS1B = 951
    glngDIFFCOATEDCOPLANARSTRIPS2B = 952
    glngDIFFCOATEDCOPLANARSTRIPSWITHLOWERGND1B = 551
    glngDIFFCOATEDCOPLANARSTRIPSWITHLOWERGND2B = 552
    glngDIFFCOATEDCOPLANARWAVEGUIDE1B = 751
    glngDIFFCOATEDCOPLANARWAVEGUIDE2B = 752
    glngDIFFCOATEDCOPLANARWAVEGUIDEWITHLOWERGND1B = 351
    glngDIFFCOATEDCOPLANARWAVEGUIDEWITHLOWERGND2B = 352
    glngDIFFEMBEDDEDCOPLANARSTRIPS1B1A = 922
    glngDIFFEMBEDDEDCOPLANARSTRIPS2B1A = 923
    glngDIFFEMBEDDEDCOPLANARSTRIPSWITHLOWERGND1B1A = 522
    glngDIFFEMBEDDEDCOPLANARSTRIPSWITHLOWERGND2B1A = 523
    glngDIFFEMBEDDEDCOPLANARWAVEGUIDE1B1A = 722
    glngDIFFEMBEDDEDCOPLANARWAVEGUIDE2B1A = 723
    glngDIFFEMBEDDEDCOPLANARWAVEGUIDEWITHLOWERGND1B1A = 322
    glngDIFFEMBEDDEDCOPLANARWAVEGUIDEWITHLOWERGND2B1A = 323
    glngDIFFOFFSETCOPLANARSTRIPS1B1A = 532
    glngDIFFOFFSETCOPLANARSTRIPS2B1A = 533
    glngDIFFOFFSETCOPLANARWAVEGUIDE1B1A = 332
    glngDIFFOFFSETCOPLANARWAVEGUIDE2B1A = 333