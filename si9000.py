import ctypes
from models import BEMCalcProgressStructure, BEMCalcResultStructure, BEMErrorStructure

# 加载DLL
si9000 = ctypes.CDLL('lib/CalcEngineBEMDll.dll')

si9000.CalcEngineBEMDLLClaimFlexLicence.argtypes = [ctypes.c_long]
si9000.CalcEngineBEMDLLClaimFlexLicence.restype = ctypes.c_long

si9000.CalcEngineBEMDLLIsCalculationModelAllowed.argtypes = [ctypes.c_long , ctypes.c_long]
si9000.CalcEngineBEMDLLIsCalculationModelAllowed.restype = ctypes.c_long

si9000.CalcEngineBEMDLLQueryCalculationFinished.argtypes = [ctypes.POINTER(BEMCalcProgressStructure)]
si9000.CalcEngineBEMDLLQueryCalculationFinished.restype = ctypes.c_bool

si9000.CalcEngineBEMDLLQueryCalculationResult.argtypes = [ctypes.POINTER(BEMCalcResultStructure)]
si9000.CalcEngineBEMDLLQueryCalculationResult.restype = ctypes.c_bool 

# 外层单线
si9000.CalcEngineBEMDLLCoatedMicrostrip1B.argtypes = [ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_long]
si9000.CalcEngineBEMDLLCoatedMicrostrip1B.restype = ctypes.c_long

# 外层单线共面
si9000.CalcEngineBEMDLLCoatedCoplanarWaveguideWithLowerGnd1B.argtypes = [ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_long]
si9000.CalcEngineBEMDLLCoatedCoplanarWaveguideWithLowerGnd1B.restype = ctypes.c_long

# 内层单线不共面
si9000.CalcEngineBEMDLLOffsetStripline1B1A.argtypes = [ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_long]
si9000.CalcEngineBEMDLLOffsetStripline1B1A.restype = ctypes.c_long

# 内层单线对地
si9000.CalcEngineBEMDLLOffsetCoplanarWaveguide1B1A.argtypes = [ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_long]
si9000.CalcEngineBEMDLLOffsetCoplanarWaveguide1B1A.restype = ctypes.c_long

# 外层双线不对地
si9000.CalcEngineBEMDLLDiffEdgeCoupledCoatedMicrostrip1B.argtypes = [ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_double,
                                                   ctypes.c_long]
si9000.CalcEngineBEMDLLDiffEdgeCoupledCoatedMicrostrip1B.restype = ctypes.c_long

# 内层双线不对地
si9000.CalcEngineBEMDLLDiffOffsetStripline1B1A.argtypes = [ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_long]
si9000.CalcEngineBEMDLLDiffOffsetStripline1B1A.restype = ctypes.c_long

# 外层双线对地
si9000.CalcEngineBEMDLLDiffCoatedCoplanarWaveguideWithLowerGnd1B.argtypes = [ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_long]
si9000.CalcEngineBEMDLLDiffCoatedCoplanarWaveguideWithLowerGnd1B.restype = ctypes.c_long

# 内层双线对地
si9000.CalcEngineBEMDLLDiffOffsetCoplanarWaveguide1B1A.argtypes = [ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_double,
                                                                  ctypes.c_long]
si9000.CalcEngineBEMDLLDiffOffsetCoplanarWaveguide1B1A.restype = ctypes.c_long

si9000.CalcEngineBEMDLLGetErrorAsString.argtypes = [ctypes.POINTER(BEMErrorStructure), ctypes.POINTER(ctypes.c_byte), ctypes.c_long]
si9000.CalcEngineBEMDLLCoatedMicrostrip1B.restype = ctypes.c_long