"""
阻抗计算调用方法
"""
from si9000 import ctypes,BEMCalcProgressStructure,BEMCalcResultStructure,si9000
from models import ModelAllowedSpecificCode, BEMErrorStructure
from loguru import logger


class Calc:
    """
    阻抗计算实例
    """

    __nLicenceType = 3
    """
    NONE   = 0, SI8000 = 1, SI8OEM = 2\r\n
    SI9000 = 3, SI9OEM = 4
    """
    def __init__(self):
        si9000.CalcEngineBEMDLLClaimFlexLicence(ctypes.c_long(self.__nLicenceType))
        # logger.debug("初始化完成...")

    def __calcAllowedType(self,type:int):
        """
        指定计算模型
        """
        lngFreqDependantCalc = 1
        if self.__nLicenceType == 1 or self.__nLicenceType == 2:
            lngFreqDependantCalc = 0
        allowed = si9000.CalcEngineBEMDLLIsCalculationModelAllowed(ctypes.c_long(type),ctypes.c_long(lngFreqDependantCalc))
        if allowed == 0:
            logger.debug("计算模型不允许")

    def 外层单线不对地(self,H1:float,Er1:float,
                W1:float,T1:float,C1:float=0.04,
                C2:float=0.012,CEr:float=3.5) -> float:
        if C1 is None:
            C1 = 0.04  # 手动设置为默认值
        if C2 is None:
            C2 = 0.012  # 手动设置为默认值
        if CEr is None:
            CEr = 3.5  # 手动设置为默认值

        self.__calcAllowedType(ModelAllowedSpecificCode.glngCOATEDMICROSTRIP1B)
        res = si9000.CalcEngineBEMDLLCoatedMicrostrip1B(ctypes.c_double((W1/0.0254)-1.0),
                                                        ctypes.c_double(W1/0.0254),
                                                        ctypes.c_double(T1/0.0254),
                                                        ctypes.c_double(H1/0.0254),
                                                        ctypes.c_double(Er1),
                                                        ctypes.c_double(C2/0.0254),
                                                        ctypes.c_double(C1/0.0254),
                                                        ctypes.c_double(CEr),
                                                        ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0

        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            # logger.debug(udtBEMCalcProgress.nCurrentCalculationStep,"/",udtBEMCalcProgress.nCurrentCalculationStepMax)
            pass
        # logger.debug("CalculationFinished OK！")

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[外层单线不对地] {:.4f}".format(W1)+"mm 线宽的阻抗为 "+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance
    
    def 外层单线对地(self,H1:float,Er1:float,
                W1:float,D1:float,T1:float,C1:float=0.04,
                C2:float=0.012,CEr:float=3.5) -> float:
        if C1 is None:
            C1 = 0.04  # 手动设置为默认值
        if C2 is None:
            C2 = 0.012  # 手动设置为默认值
        if CEr is None:
            CEr = 3.5  # 手动设置为默认值

        self.__calcAllowedType(ModelAllowedSpecificCode.glngCOATEDCOPLANARSTRIPSWITHLOWERGND1B)
        res = si9000.CalcEngineBEMDLLCoatedCoplanarWaveguideWithLowerGnd1B(ctypes.c_double((W1/0.0254)-1.0),
                                                               ctypes.c_double(W1/0.0254),
                                                               ctypes.c_double(T1/0.0254),
                                                               ctypes.c_double(D1/0.0254),
                                                               ctypes.c_double(H1/0.0254),
                                                               ctypes.c_double(Er1),
                                                               ctypes.c_double(C2/0.0254),
                                                               ctypes.c_double(C1/0.0254),
                                                               ctypes.c_double(CEr),
                                                               ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0

        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[外层单线对地] 线宽{:.4f}".format(W1)+"mm 对地{:.4f}".format(D1)+"mm 的阻抗为","{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance
    
    def 内层单线不对地(self,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,T1:float) -> float:
        """
        内层单线不对地
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        T1:铜厚
        """
        self.__calcAllowedType(ModelAllowedSpecificCode.glngOFFSETSTRIPLINE1B1A)
        res = si9000.CalcEngineBEMDLLOffsetStripline1B1A(ctypes.c_double((W1/0.0254)-1.0),
                                                         ctypes.c_double(W1/0.0254),
                                                         ctypes.c_double(T1/0.0254),
                                                         ctypes.c_double(H1/0.0254),
                                                         ctypes.c_double(Er1),
                                                         ctypes.c_double(H2/0.0254),
                                                         ctypes.c_double(Er2),
                                                         ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0
        
        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[内层单线不对地] 线宽{:.4f}".format(W1)+"mm 的阻抗为"+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance

    def 内层单线对地(self,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,D1:float,T1:float) -> float:
        """
        内层单线对地
        """
        self.__calcAllowedType(ModelAllowedSpecificCode.glngOFFSETCOPLANARWAVEGUIDE1B1A)
        res = si9000.CalcEngineBEMDLLOffsetCoplanarWaveguide1B1A(ctypes.c_double((W1/0.0254)-1.0),
                                                         ctypes.c_double(W1/0.0254),
                                                         ctypes.c_double(T1/0.0254),
                                                         ctypes.c_double(D1/0.0254),
                                                         ctypes.c_double(H1/0.0254),
                                                         ctypes.c_double(Er1),
                                                         ctypes.c_double(H2/0.0254),
                                                         ctypes.c_double(Er2),
                                                         ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0

        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[内层单线对地] 线宽{:.4f}".format(W1)+"mm 的阻抗为"+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance

    def 外层双线不对地(self,H1:float,Er1:float,
                W1:float,S1:float,T1:float,
                C1:float=0.04,C2:float=0.012,C3:float=0.04,CEr:float=3.5) -> float:
        """
        外层双线不对地
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        S1:线间距
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        C3:基材油墨厚度
        CEr:油墨介电常数
        """
        if C1 is None:
            C1 = 0.04  # 手动设置为默认值
        if C2 is None:
            C2 = 0.012  # 手动设置为默认值
        if C3 is None:
            C3 = 0.04  # 手动设置为默认值
        if CEr is None:
            CEr = 3.5  # 手动设置为默认值

        # self.__calcAllowedType(ModelAllowedSpecificCode.glngEDGECOUPLEDCOATEDMICROSTRIP1B)  不校验模型允许
        res = si9000.CalcEngineBEMDLLDiffEdgeCoupledCoatedMicrostrip1B(ctypes.c_double((W1/0.0254)-1.0),
                                                                       ctypes.c_double(W1/0.0254),
                                                                       ctypes.c_double(T1/0.0254),
                                                                       ctypes.c_double(S1/0.0254),
                                                                       ctypes.c_double(H1/0.0254),
                                                                       ctypes.c_double(Er1),
                                                                       ctypes.c_double(C2/0.0254),
                                                                       ctypes.c_double(C1/0.0254),
                                                                       ctypes.c_double(C3/0.0254),
                                                                       ctypes.c_double(CEr),
                                                                       ctypes.c_double(3),  # 计算模式
                                                                       ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0
        
        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[外层双线不对地] 线宽{:.4f}".format(W1)+"mm 的阻抗为"+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance

    def 内层双线不对地(self,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,S1:float,T1:float) -> float:
        """
        内层双线不对地
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        S1:线间距
        T1:铜厚
        """
        #self.__calcAllowedType(ModelAllowedSpecificCode.glngEDGECOUPLEDCOATEDMICROSTRIP1B) 不校验模型允许
        res = si9000.CalcEngineBEMDLLDiffOffsetStripline1B1A(ctypes.c_double((W1/0.0254)-1.0),
                                                                   ctypes.c_double(W1/0.0254),
                                                                   ctypes.c_double(T1/0.0254),
                                                                   ctypes.c_double(S1/0.0254),
                                                                   ctypes.c_double(H1/0.0254),
                                                                   ctypes.c_double(Er1),
                                                                   ctypes.c_double(H2/0.0254),
                                                                   ctypes.c_double(Er2),
                                                                   ctypes.c_double(3),
                                                                   ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0
        
        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[内层双线不对地] 线宽{:.4f}".format(W1)+"mm 的阻抗为"+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance

    def 外层双线对地(self,H1:float,Er1:float,
                W1:float,S1:float,D1:float,T1:float,
                C1:float=0.04,C2:float=0.012,C3:float=0.04,CEr:float=3.5) -> float:
        """
        外层双线对地
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        S1:线间距
        D1:对地距离
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        C3:基材油墨厚度
        CEr:油墨介电常数
        """
        if C1 is None:
            C1 = 0.04  # 手动设置为默认值
        if C2 is None:
            C2 = 0.012  # 手动设置为默认值
        if C3 is None:
            C3 = 0.04  # 手动设置为默认值
        if CEr is None:
            CEr = 3.5  # 手动设置为默认值

        res = si9000.CalcEngineBEMDLLDiffCoatedCoplanarWaveguideWithLowerGnd1B(ctypes.c_double((W1/0.0254)-1.0),
                                                                       ctypes.c_double(W1/0.0254),
                                                                       ctypes.c_double(T1/0.0254),
                                                                       ctypes.c_double(S1/0.0254),
                                                                       ctypes.c_double(D1/0.0254),
                                                                       ctypes.c_double(H1/0.0254),
                                                                       ctypes.c_double(Er1),
                                                                       ctypes.c_double(C2/0.0254),
                                                                       ctypes.c_double(C1/0.0254),
                                                                       ctypes.c_double(C3/0.0254),
                                                                       ctypes.c_double(CEr),
                                                                       ctypes.c_double(3),
                                                                       ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0
        
        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[外层双线对地] 线宽{:.4f}".format(W1)+"mm 的阻抗为"+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance

    def 内层双线对地(self,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,S1:float,D1:float,T1:float):
        """
        内层双线对地
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        S1:线间距
        D1:对地距离
        T1:铜厚
        """
        res = si9000.CalcEngineBEMDLLDiffOffsetCoplanarWaveguide1B1A(ctypes.c_double((W1/0.0254)-1.0),
                                                                   ctypes.c_double(W1/0.0254),
                                                                   ctypes.c_double(T1/0.0254),
                                                                   ctypes.c_double(S1/0.0254),
                                                                   ctypes.c_double(D1/0.0254),
                                                                   ctypes.c_double(H1/0.0254),
                                                                   ctypes.c_double(Er1),
                                                                   ctypes.c_double(H2/0.0254),
                                                                   ctypes.c_double(Er2),
                                                                   ctypes.c_double(3),
                                                                   ctypes.c_long(0))
        if res == 0:
            udtBEMErrorStructure = BEMErrorStructure()
            error_code = ctypes.c_byte(0) 
            si9000.CalcEngineBEMDLLGetErrorAsString(ctypes.byref(udtBEMErrorStructure), ctypes.byref(error_code), 255)
            logger.debug(udtBEMErrorStructure)
            logger.debug("阻抗计算失败，请检查参数|",res,"|",udtBEMErrorStructure)
            return 0
        
        udtBEMCalcProgress = BEMCalcProgressStructure()
        while si9000.CalcEngineBEMDLLQueryCalculationFinished(ctypes.byref(udtBEMCalcProgress)) == False:
            pass

        udtBEMCalcResults = BEMCalcResultStructure()
        si9000.CalcEngineBEMDLLQueryCalculationResult(ctypes.byref(udtBEMCalcResults))
        logger.info("[内层双线对地] 线宽{:.4f}".format(W1)+"mm 的阻抗为"+"{:.4f}".format(udtBEMCalcResults.dImpedance)+"Ω")
        return udtBEMCalcResults.dImpedance


class Calc_Plus(Calc):
    """
    阻抗计算扩展
    """
    def 外层单线不对地s(self,H1:float,Er1:float,
                W1:float,T1:float,C1:float=0.04,
                C2:float=0.012,CEr:float=3.5,Count:int=10,Step:float=0.01):
        """
        外层单线不对地批量计算
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        CEr:油墨介电常数
        Count:计算次数
        Step:步进值
        """
        ohms:list = [] # 返回值2
        name_lists:list = [] # 返回值1

        count:int = round(Count / 2)*2 # 只允许偶数
        halb:int = round(count / 2)
        i:int = 0
        W1_Orig:float = W1

        # 向下减
        W1 = W1_Orig - (Step * halb)
        while i < halb:
            i = i + 1
            ohms.append(self.外层单线不对地(H1,Er1,W1,T1,C1,C2,CEr))
            name_lists.append(W1)
            W1 = W1 + Step
            if W1 <= 0.01:
                logger.debug("向下调整到极限，无法继续调整！")
                break
        i = 0
        W1 = W1_Orig
        # 向上加
        while i < halb:
            i = i + 1
            ohms.append(self.外层单线不对地(H1,Er1,W1,T1,C1,C2,CEr))
            name_lists.append(W1)
            W1 = W1 + Step
        return name_lists,ohms
    
    def 外层单线不对地reverse(self,Z:float,H1:float,Er1:float,
                W1:float,T1:float,C1:float=0.04,
                C2:float=0.012,CEr:float=3.5):
        """
        外层单线不对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        CEr:油墨介电常数
        """
        current_W = W1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.外层单线不对地(H1,Er1,current_W,T1,C1,C2,CEr)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的线宽: {current_W:.4f}mm, 对应阻抗值: {current_Z:.2f}Ω")
                return current_W
                
            # 确定调整方向（修正后的逻辑）
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01:
                logger.info(f"警告：线宽已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return 0.01
            if new_W > 10:
                logger.info(f"警告：线宽已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return 10
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终线宽: {current_W:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W
                
            # 更新线宽
            current_W = new_W
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终线宽: {current_W:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W
            
    def 外层单线对地reverse(self,Z:float,H1:float,Er1:float,
                W1:float,D1:float,T1:float,C1:float=0.04,
                C2:float=0.012,CEr:float=3.5):
        """
        外层单线对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        D1:对地距离
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        CEr:油墨介电常数
        """
        current_W = W1
        current_D = D1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.外层单线对地(H1,Er1,current_W,current_D,T1,C1,C2,CEr)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W, current_D
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的参数: 线宽 {current_W:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
                
            # 确定调整方向（修正后的逻辑）
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
                # 计算新的对地距离（线宽减小，对地距离增加）
                abs_change = abs(new_W - current_W)
                new_D = current_D + abs_change/2.0
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                # 计算新的对地距离（线宽增加，对地距离减小）
                abs_change = abs(new_W - current_W)
                new_D = current_D - abs_change/2.0
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01 or new_D < 0.01:
                logger.info(f"警告：尺寸已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
            if new_W > 10 or new_D > 10:
                logger.info(f"警告：尺寸已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终参数: 线宽 {current_W:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
                
            # 更新参数
            current_W = new_W
            current_D = new_D
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终参数: 线宽 {current_W:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
            
    def 内层单线不对地reverse(self,Z:float,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,T1:float):
        """
        内层单线不对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        T1:铜厚
        """
        current_W = W1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.内层单线不对地(H1,Er1,H2,Er2,current_W,T1)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的线宽: {current_W:.4f}mm, 对应阻抗值: {current_Z:.2f}Ω")
                return current_W
                
            # 确定调整方向
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01:
                logger.info(f"警告：线宽已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return 0.01
            if new_W > 10:
                logger.info(f"警告：线宽已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return 10
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终线宽: {current_W:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W
                
            # 更新线宽
            current_W = new_W
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终线宽: {current_W:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W
            
    def 内层单线对地reverse(self,Z:float,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,D1:float,T1:float):
        """
        内层单线对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        D1:对地距离
        T1:铜厚
        """
        current_W = W1
        current_D = D1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.内层单线对地(H1,Er1,H2,Er2,current_W,current_D,T1)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W, current_D
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的参数: 线宽 {current_W:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
                
            # 确定调整方向
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
                # 计算新的对地距离（线宽减小，对地距离增加）
                abs_change = abs(new_W - current_W)
                new_D = current_D + abs_change/2.0
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                # 计算新的对地距离（线宽增加，对地距离减小）
                abs_change = abs(new_W - current_W)
                new_D = current_D - abs_change/2.0
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01 or new_D < 0.01:
                logger.info(f"警告：尺寸已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
            if new_W > 10 or new_D > 10:
                logger.info(f"警告：尺寸已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终参数: 线宽 {current_W:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
                
            # 更新参数
            current_W = new_W
            current_D = new_D
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终参数: 线宽 {current_W:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_D
            
    def 外层双线不对地reverse(self,Z:float,H1:float,Er1:float,
                W1:float,S1:float,T1:float,C1:float=0.04,
                C2:float=0.012,C3:float=0.04,CEr:float=3.5):
        """
        外层双线不对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        S1:线距
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        C3:基材油墨厚度
        CEr:油墨介电常数
        """
        current_W = W1
        current_S = S1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.外层双线不对地(H1,Er1,current_W,current_S,T1,C1,C2,C3,CEr)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W, current_S
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
                
            # 确定调整方向
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
                # 计算新的线距（线宽减小，线距增加）
                abs_change = abs(new_W - current_W)
                new_S = current_S + abs_change  # 注意这里是加上完整的变化量
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                # 计算新的线距（线宽增加，线距减小）
                abs_change = abs(new_W - current_W)
                new_S = current_S - abs_change  # 注意这里是减去完整的变化量
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01 or new_S < 0.01:
                logger.info(f"警告：尺寸已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
            if new_W > 10 or new_S > 10:
                logger.info(f"警告：尺寸已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
                
            # 更新参数
            current_W = new_W
            current_S = new_S
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S

    def 内层双线不对地reverse(self,Z:float,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,S1:float,T1:float):
        """
        内层双线不对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        S1:线距
        T1:铜厚
        """
        current_W = W1
        current_S = S1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.内层双线不对地(H1,Er1,H2,Er2,current_W,current_S,T1)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W, current_S
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
                
            # 确定调整方向
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
                # 计算新的线距（线宽减小，线距增加）
                abs_change = abs(new_W - current_W)
                new_S = current_S + abs_change  # 线宽变化多少，线距变化相同的量
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                # 计算新的线距（线宽增加，线距减小）
                abs_change = abs(new_W - current_W)
                new_S = current_S - abs_change  # 线宽变化多少，线距变化相同的量
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01 or new_S < 0.01:
                logger.info(f"警告：尺寸已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
            if new_W > 10 or new_S > 10:
                logger.info(f"警告：尺寸已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
                
            # 更新参数
            current_W = new_W
            current_S = new_S
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S
            
    def 外层双线对地reverse(self,Z:float,H1:float,Er1:float,
                W1:float,S1:float,D1:float,T1:float,C1:float=0.04,
                C2:float=0.012,C3:float=0.04,CEr:float=3.5):
        """
        外层双线对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        W1:线宽
        S1:线距
        D1:对地距离
        T1:铜厚
        C1:基材油墨厚度
        C2:铜皮油墨厚度
        C3:基材油墨厚度
        CEr:油墨介电常数
        """
        current_W = W1
        current_S = S1
        current_D = D1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.外层双线对地(H1,Er1,current_W,current_S,current_D,T1,C1,C2,C3,CEr)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W, current_S, current_D
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
                
            # 确定调整方向
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
                # 计算新的线距和对地距离（线宽减小，线距和对地距离增加）
                abs_change = abs(new_W - current_W)
                new_S = current_S + abs_change  # 线距变化量等于线宽变化量
                new_D = current_D + abs_change/2.0  # 对地距离变化量为线宽变化量的一半
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                # 计算新的线距和对地距离（线宽增加，线距和对地距离减小）
                abs_change = abs(new_W - current_W)
                new_S = current_S - abs_change  # 线距变化量等于线宽变化量
                new_D = current_D - abs_change/2.0  # 对地距离变化量为线宽变化量的一半
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01 or new_S < 0.01 or new_D < 0.01:
                logger.info(f"警告：尺寸已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
            if new_W > 10 or new_S > 10 or new_D > 10:
                logger.info(f"警告：尺寸已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
                
            # 更新参数
            current_W = new_W
            current_S = new_S
            current_D = new_D
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
            
    def 内层双线对地reverse(self,Z:float,H1:float,Er1:float,
                H2:float,Er2:float,W1:float,S1:float,D1:float,T1:float):
        """
        内层双线对地反算
        Z:要求阻抗值
        H1:介质厚度
        Er1:介质介电常数
        H2:PP+铜厚
        Er2:PP介电常数
        W1:线宽
        S1:线距
        D1:对地距离
        T1:铜厚
        """
        current_W = W1
        current_S = S1
        current_D = D1
        step = W1 * 0.1  # 初始步长为线宽的10%
        last_direction = 0  # 记录上一次调整方向: 1为增加，-1为减少
        direction_changes = 0  # 记录方向改变次数
        
        while True:
            # 计算当前阻抗值
            current_Z = self.内层双线对地(H1,Er1,H2,Er2,current_W,current_S,current_D,T1)
            
            # 检查计算是否失败
            if current_Z == 0:
                logger.info(f"警告：阻抗计算失败，请检查参数")
                return current_W, current_S, current_D
                
            # 检查是否在允许范围内
            if abs(current_Z - Z) <= 0.3:
                logger.info(f"找到满足条件的参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
                
            # 确定调整方向
            if current_Z < Z:  # 阻抗值过小，需要减小线宽
                current_direction = -1
                new_W = current_W - step
                # 计算新的线距和对地距离（线宽减小，线距和对地距离增加）
                abs_change = abs(new_W - current_W)
                new_S = current_S + abs_change  # 线距变化量等于线宽变化量
                new_D = current_D + abs_change/2.0  # 对地距离变化量为线宽变化量的一半
            else:  # 阻抗值过大，需要增加线宽
                current_direction = 1
                new_W = current_W + step
                # 计算新的线距和对地距离（线宽增加，线距和对地距离减小）
                abs_change = abs(new_W - current_W)
                new_S = current_S - abs_change  # 线距变化量等于线宽变化量
                new_D = current_D - abs_change/2.0  # 对地距离变化量为线宽变化量的一半
                
            # 检查是否发生方向改变
            if last_direction != 0 and current_direction != last_direction:
                direction_changes += 1
                step = step * 0.5  # 每次方向改变时，步长减半
                logger.debug(f"减小步长至: {step:.6f}mm")
                
            # 更新方向记录
            last_direction = current_direction
                
            # 检查是否超出物理限制
            if new_W < 0.01 or new_S < 0.01 or new_D < 0.01:
                logger.info(f"警告：尺寸已达到最小限制(0.01mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
            if new_W > 10 or new_S > 10 or new_D > 10:
                logger.info(f"警告：尺寸已达到最大限制(10mm)，当前阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
                
            # 检查步长是否太小
            if step < 0.0001:  # 如果步长小于0.1微米
                logger.info(f"步长已经很小，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
                
            # 更新参数
            current_W = new_W
            current_S = new_S
            current_D = new_D
            
            # 防止无限循环
            if direction_changes > 10:
                logger.info(f"调整方向改变次数过多，停止调整。最终参数: 线宽 {current_W:.4f}mm, 线距 {current_S:.4f}mm, 对地距离 {current_D:.4f}mm, 阻抗值: {current_Z:.2f}Ω")
                return current_W, current_S, current_D
