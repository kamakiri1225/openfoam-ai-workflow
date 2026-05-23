
from os import path
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def boundary_def(case, boundary_dict):
    def velocity_func(name, velocity):# 速度規定
        # ======== U =================
        velocity = f'({velocity[0]} {velocity[1]} {velocity[2]})'
        UFile = {}
        UFile["type"] = 'fixedValue'
        UFile["value"] = "uniform " + str(velocity)
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'zeroGradient'
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'fixedValue'
        kFile["value"] = "$internalField"
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'fixedValue'
        epsilonFile["value"] = "$internalField"
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'fixedValue'
        omegaFile["value"] = "$internalField"
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'calculated'
        nutFile["value"] = "$internalField"
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================
        
        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()
            
    def massflowRate_func(name, massflow, rho):# 質量流れ
        # ======== U =================
        UFile = {}
        UFile["type"] = 'flowRateInletVelocity'
        UFile["massFlowRate"] = "constant " + str(massflow)
        UFile["rhoInlet"] = str(rho)
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'zeroGradient'
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'fixedValue'
        kFile["value"] = "$internalField"
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'fixedValue'
        epsilonFile["value"] = "$internalField"
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'fixedValue'
        omegaFile["value"] = "$internalField"
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'calculated'
        nutFile["value"] = "$internalField"
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================
        
        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()
        
    def fluxRate_func(name, volumeflowrate):# 体積流量
        # ======== U =================
        UFile = {}
        UFile["type"] = 'flowRateInletVelocity'
        UFile["volumetricFlowRate"] = "constant " + str(volumeflowrate)
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'zeroGradient'
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'fixedValue'
        kFile["value"] = "$internalField"
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'fixedValue'
        epsilonFile["value"] = "$internalField"
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'fixedValue'
        omegaFile["value"] = "$internalField"
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'calculated'
        nutFile["value"] = "$internalField"
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================

        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()

    def surfaceNormalVelocity_func(name, vmag):# 法線方向流速
        # ======== U =================
        UFile = {}
        UFile["type"] = 'surfaceNormalFixedValue'
        UFile["refValue"] = "uniform " + str(vmag)
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'zeroGradient'
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'fixedValue'
        kFile["value"] = "$internalField"
        boundary_dict['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'fixedValue'
        epsilonFile["value"] = "$internalField"
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'fixedValue'
        omegaFile["value"] = "$internalField"
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'zeroGradient'
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================
        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()

    def staticPressure_func(name, press):# 静止圧
        # ======== U =================
        UFile = {}
        UFile["type"] = 'zeroGradient'
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'fixedValue'
        pFile["value"] = "uniform " + str(press)
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'zeroGradient'
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'zeroGradient'
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'zeroGradient'
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'zeroGradient'
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================

        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()
        
    def pressureInletOutletVelocity_func(name, press_velocity):# 自然流出流入
        # ======== U =================
        UFile = {}
        UFile["type"] = 'pressureInletOutletVelocity'
        UFile["value"] = "uniform " + f"({press_velocity[1]} {press_velocity[2]} {press_velocity[3]})"
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'totalPressure'
        pFile["p0"] = "uniform " + str(press_velocity[0])
        pFile["value"] = "uniform " + str(press_velocity[0])
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'inletOutlet'
        kFile["inletValue"] = "$internalField"
        kFile["value"] = "$internalField"
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'inletOutlet'
        epsilonFile["inletValue"] = "$internalField"
        epsilonFile["value"] = "$internalField"
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'inletOutlet'
        omegaFile["inletValue"] = "$internalField"
        omegaFile["value"] = "$internalField"
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'calculated'
        nutFile["value"] = "$internalField"
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================

        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()
        
    def noSlip_func(name):# 静止壁
        # ======== U =================
        UFile = {}
        UFile["type"] = 'fixedValue'
        UFile["value"] = "uniform " + "(0 0 0)"
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'zeroGradient'
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'kqRWallFunction'
        kFile["value"] = "uniform " + "0"
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'epsilonWallFunction'
        epsilonFile["value"] = "uniform " + "0"
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'omegaWallFunction'
        omegaFile["value"] = "uniform " + "0"
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'nutkWallFunction'
        nutFile["value"] = "uniform " + "0"
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================
        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()

    def slip_func(name):# 滑り条件
        # ======== U =================
        UFile = {}
        UFile["type"] = 'slip'
        boundary_filed['U']["boundaryField"][name] = UFile
        # ======== p =================
        pFile = {}
        pFile["type"] = 'zeroGradient'
        boundary_filed['p']["boundaryField"][name] = pFile
        # ======== k =================
        kFile = {}
        kFile["type"] = 'zeroGradient'
        boundary_filed['k']["boundaryField"][name] = kFile
        # ======== epsilon =================
        epsilonFile = {}
        epsilonFile["type"] = 'zeroGradient'
        boundary_filed['epsilon']["boundaryField"][name] = epsilonFile
        # ======== omega =================
        omegaFile = {}
        omegaFile["type"] = 'zeroGradient'
        boundary_filed['omega']["boundaryField"][name] = omegaFile
        # ======== nut =================
        nutFile = {}
        nutFile["type"] = 'zeroGradient'
        boundary_filed['nut']["boundaryField"][name] = nutFile
        # =========================
        for filed_ in boundary_filed:
            boundary_filed[filed_].writeFile()

    # ========= main ==========================================================
    boundary_filed = {}
    print(f'case={case}')
    
    boundary_filed['U'] = ParsedParameterFile(path.join(case, "0", 'U'))
    boundary_filed['p'] = ParsedParameterFile(path.join(case, "0", 'p'))
    boundary_filed['k'] = ParsedParameterFile(path.join(case, "0", 'k'))
    boundary_filed['epsilon'] = ParsedParameterFile(path.join(case, "0", 'epsilon'))
    boundary_filed['omega'] = ParsedParameterFile(path.join(case, "0", 'omega'))
    boundary_filed['nut'] = ParsedParameterFile(path.join(case, "0", 'nut'))

    if boundary_dict['bounaryType'] == '流速指定':
        velocity_func(boundary_dict['patchName'], boundary_dict['value'])# 速度規定
        print("="*40)

    elif boundary_dict['bounaryType'] == '質量流':
        massflowRate_func(boundary_dict['patchName'], boundary_dict['value'][0], boundary_dict['value'][2])# 質量流れ
        print("="*40)  

    elif boundary_dict['bounaryType'] == '体積流量指定':
        fluxRate_func(boundary_dict['patchName'], boundary_dict['value'][0])# 体積流量
        print("="*40)

    elif boundary_dict['bounaryType'] == '法線方向流速':
        surfaceNormalVelocity_func(boundary_dict['patchName'], boundary_dict['value'][0])# 法線方向流速
        print("="*40)   
    elif boundary_dict['bounaryType'] == '静止圧指定':
        staticPressure_func(boundary_dict['patchName'], boundary_dict['value'][0])# 静止圧
        print("="*40)

    elif boundary_dict['bounaryType'] == '全圧指定':
        pass
    
    elif boundary_dict['bounaryType'] == '自然流出流入':
        pressureInletOutletVelocity_func(boundary_dict['patchName'], boundary_dict['value'])# 自然流出流入
        print("="*40)

    elif boundary_dict['bounaryType'] == '静止壁':
        noSlip_func(boundary_dict['patchName']) # 静止壁
        print("="*40)

    elif boundary_dict['bounaryType'] == '滑り条件':
         slip_func(boundary_dict['patchName']) # 滑り
         print("="*40)   
    else:
        print(f"境界条件:{boundary_dict['patchName']}。境界条件の指定がありません。")
        print(f"静止壁で定義します。")
        print("="*40)