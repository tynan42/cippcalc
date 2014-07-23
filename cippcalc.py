from math import trunc, exp, pi

class LinerManager(object):
    '''Instances of the LinerManager class take a dictionary of keys and
    values and determine the thickness of the CIPP liner'''
    # Standard live load table for AASHTO H20 highway loads,# Cooper E-80
    # rail, or 180 kip airplane gear load. Impact factors have already been
    # integrated.
    live_load_hwy = {
        2:5.56, 3:4.17, 4:2.78, 5:1.74, 6:1.39, 7:1.22, 8:0.69
        }
    live_load_rail = {
        2:26.39, 3:23.61, 4:18.4, 5:16.67, 6:15.63, 7:12.15,
        8: 11.11, 10:7.64, 12:5.56, 14:4.17, 16:3.47, 18:2.78,
        20:2.08, 22:1.91, 24:1.74, 26:1.39, 28:1.04, 30:0.69
        }
    live_load_arpt = {
        2:13.14, 3:12.28, 4:11.27, 5:10.09, 6:8.79, 7:7.85,
        8:6.93, 10:6.09, 12:4.76, 14:3.06, 16:2.29, 18:1.91,
        20:1.53, 22:1.14, 24:1.05
        }
        
    def __init__(self, vardict):
        # The enhancement_factor and soil_mod are submitted exclusivly with
        # the dictionary. The following if statements prevent key failures
        if 'enhancement_factor' not in vardict:
            vardict['enhancement_factor'] = ''
        if 'soil_mod' not in vardict:
            vardict['soil_mod'] = ''
            
        # If value is left blank, assume default (ASTM)

        default_values = {
            'design_modulus':250000, 'design_flexural_strength':4500,
            'safety_factor':2.0, 'ret_factor':50, 'ovality':3.0,
            'enhancement_factor':7.0, 'gw_level':0.0, 'soil_density':140,
            'poissons':0.3, 'soil_mod':700, 'n_host':0.013, 'n_liner':0.010,
            'host_age':45
            }
        
        for key, value in vardict.items():
            if vardict[key] == '':
                vardict[key] = default_values[key]
        
        #tempvardict = {}
        
        #for key, value in vardict.items():
            #tempvardict['self.'+key] = vardict[key]
        
        #vardict = tempvardict
        
        for key, value in vardict.items():
            try:
                float(vardict[key])
                vardict[key] = float(vardict[key])
            except:
                vardict[key] = vardict[key]
                
        self.vardict = vardict
                
        # Calculated variables
        self.vardict['soil_depth'] = (vardict['surface_to_invert']
                                      -(vardict['host_diameter'])/12)
        self.vardict['gw_head'] = (vardict['surface_to_invert']
                                   - vardict['gw_level'])
        if self.vardict['gw_head'] <= 0:
            self.vardict['gw_head'] = 0
        self.vardict['ov_red_fact'] = (((1-(vardict['ovality']/100))/((1+(
                                       vardict['ovality']/100))**2))**3)
        self.vardict['lng_term_modulus'] = ((vardict['ret_factor']/100)
                                            *vardict['design_modulus'])
        self.vardict['lng_term_flex_strength'] = (
                                        (vardict['ret_factor']/100)
                                         *vardict['design_flexural_strength'])
        self.vardict['gw_load'] = self.vardict['gw_head']/2.31

 
    def x1p1(self):
        '''X1.1 - Partially deteriorated gravity pipe condition support
        hydraulic load of groundwater'''
        # Pull variables from dictionary
        dia = self.vardict['host_diameter']
        ef = self.vardict['enhancement_factor']
        mod = self.vardict['lng_term_modulus']
        oval = self.vardict['ov_red_fact']
        mu = self.vardict['poissons']
        FS = self.vardict['safety_factor']
        gwload = self.vardict['gw_load']
        
        # Calculate
        sdr = (((2*ef*mod*oval)/((1-(mu**2))*gwload*FS))**(1.0/3.0))
        liner_thickness_x1p1 = dia/sdr
        return liner_thickness_x1p1

    def x1p2(self):
        '''X1.2 - If there is no groundwater above the pipe, the CIPP should 
        have a maximum SDR of 100'''
        # Pull variables from dictionary
        dia = self.vardict['host_diameter']        
        gwhead = self.vardict['gw_head']
        
        # Calculate
        if (gwhead <= 0):
            liner_thickness_x1p2 = dia/100
            return liner_thickness_x1p2
        else:
            return 0

    def x1p2p1p1(self):
        '''X1.2.1.1 - if the original pipe is oval, the design from X1.1 shall
        have a minimum thickness as calculated by:'''
        # Pull variables from dictionary
        dia = self.vardict['host_diameter'] 
        oval = self.vardict['ov_red_fact']
        flex = self.vardict['lng_term_flex_strength']
        FS = self.vardict['safety_factor']
        gwload = self.vardict['gw_load']
        
        # Calculate
        pythag_A = (1.5*(oval/100))*(1+(oval/100))
        pythag_B = (-0.5*(1+((oval/100))))
        pythag_C = -flex/(gwload*FS)
        root_1 = (-pythag_B+((pythag_B**2)-(4*pythag_A*pythag_C))**(0.5))/(2*pythag_A)
        root_2 = (-pythag_B-((pythag_B**2)-(4*pythag_A*pythag_C))**(0.5))/(2*pythag_A)
        if (root_1 < 0):
            root_1 = 999
        if (root_2 < 0):
            root_2 = 999
        root = min(root_1, root_2)
        liner_thickness_x1p2p1p1 = dia/root
        return liner_thickness_x1p2p1p1

    

    """ For non-standard live loads, or concentrated load, use eq. and impact factors.
        Load eq.
        Pp = 3*Ps / 2*pi*(C^2)*((1+((d/c)^2))^2.5)
        Pp = pressure transmitted to pipe
        Ps = Load at surface (lbs)
        C = depth of cover (in for psi, ft for psf)
        d = horiz. offset distance from pipe to line of application of surface load (in for psi, ft for psf)

    #Impact factor - if less than x, y. If over x>3 use y4.
    imp_fact_hwy = { 1:1.5, 2:1.35, 3:1.15, 100:1.0 }
    imp_fact_rail = { 1:1.75, 2:1.5, 3:1.5, 100:1.35 }
    imp_fact_arpt = { 1:1.5, 2:1.35, 3:1.35, 100:1.15 }

    # Triggers for specialized investigation if load area > 10 sq ft and:
        # 500 psf for pre-1941 pipelines
        # 1000 psf for 12-inch diameter or larger
        # 1500 psf for pipelines smaller than 12-inch dia
    """

    def live_load_determination(self):
        ''' X1.2.2 - Fully deteriorated gravity pipe. Designed to support hydraulic, soil, and live loads.
            Live load calculation method must be determined
            Standard using AASHTO charts'''
        # Pull variables from dictionary
        location = self.vardict['location']
        depth = self.vardict['soil_depth']

        # Determine Live Load
        if (location == 'Highway'):
            if (depth >= 10):
                live_load = 0
            elif (depth >8 and depth < 10):
                live_load = 0.69
            elif (depth < 2):
                live_load = 5.56
            else:
                live_load_index = trunc(depth)
                live_load = self.live_load_hwy[live_load_index]
        elif (location == 'Rail'):
            if (depth > 30):
                live_load = 0
            elif (depth >8 and depth <= 30):
                live_load_index = 2*trunc(0.5*depth)
                live_load = self.live_load_rail[live_load_index]
            elif (depth < 2):
                live_load = 26.39
            else:
                live_load_index = trunc(depth)
                live_load = self.live_load_rail[live_load_index]
        elif (location == 'Airport'):
            if (depth > 24):
                live_load = 0
            elif (depth >8 and depth <= 24):
                live_load_index = 2*trunc(0.5*depth)
                live_load = self.live_load_arpt[live_load_index]
            elif (depth < 2):
                live_load = 13.14
            else:
                live_load_index = trunc(depth)
                live_load = self.live_load_arpt[live_load_index]
        else:
            live_load = None
        return live_load

    def x1p2p2(self):
        # Pull variables from dictionary
        dia = self.vardict['host_diameter']
        gwhead = self.vardict['gw_head']
        depth = self.vardict['soil_depth']
        W = self.vardict['soil_density']
        FS = self.vardict['safety_factor']
        smod = self.vardict['soil_mod']
        oval = self.vardict['ov_red_fact']
        mod = self.vardict['lng_term_modulus']
        
        # Calculate
        adjusted_gwhead = gwhead - (dia/12)
        Rw_calc = 1.0-(0.33*(adjusted_gwhead/depth))
        Rw_min = 0.67
        Rw_max = 1.0
        Rw = min(Rw_calc, Rw_min)
        Rw = Rw_max if Rw > Rw_max else Rw #Water buoyancy factor
        Qt = ((0.433*adjusted_gwhead)+((W*depth*Rw)/144)
              +self.live_load_determination())
        B_prime = 1/(1+(4*(exp(-0.065*depth)))) #Coef of elastic support
        mom_inert = ((dia**3)*((FS*Qt)**2))/(32*Rw*B_prime*smod*oval*mod)
        liner_thickness_x1p2p2 = (12*mom_inert)**(1/3)
        return liner_thickness_x1p2p2

    def x1p2p2p1(self):
        # Pull variables from dictionary
        dia = self.vardict['host_diameter']
        des_mod = self.vardict['design_modulus']
        
        # Calculate
        mom_inert_min = (0.093*(dia**3))/des_mod
        liner_thickness_x1p2p2p1 = (12.0*mom_inert_min)**(1/3)
        return liner_thickness_x1p2p2p1 
    
    def thickness_calc(self):
        # Pull variables from dictionary
        condition = self.vardict['design_condition']
        gwload = self.vardict['gw_load']
        
        # Calculate
        if (condition == 'Partially Deteriorated'):
            if (gwload <= 0):
                liner_thickness = 'No hydraulic loading, design as fully deteriorated or use minimum thickness.'
            else:
                liner_thickness = str('{0:.2f}'.format(round(max(self.x1p1(), self.x1p2(), self.x1p2p1p1())*25.4,2)))
        elif (condition == 'Fully Deteriorated'):
            liner_thickness = str('{0:.2f}'.format(round(max(self.x1p2p2(), self.x1p2p2p1())*25.4,2)))
        else:
            liner_thickness = 'error'
        
        return liner_thickness
    
    def thickness_check(self):
        # Pull variables from dictionary
        dia_mm = 25.4*self.vardict['host_diameter']
        liner_mm = float(self.thickness_calc())
        new_dia = dia_mm - (2*liner_mm)
        area_lost = (pi*(dia_mm**2)/4) - (pi*(new_dia**2)/4)
        area_lost_percent = ((pi*(dia_mm**2)/4) - area_lost)/(pi*(dia_mm**2)/4)
        
        # Check against pipe size
        return (1-area_lost_percent)*100
        
        
    def output_dict(self):
        # Convert input variables to nice format
        round_down_to0 = [
            'design_modulus', 'design_flexural_strength', 'ret_factor',
            'soil_density', 'soil_mod', 'host_age'
            ]
        round_down_to1 = [
            'safety_factor', 'ovality', 'enhancement_factor', 'gw_level'
            ]
        round_down_to2 = ['poissons']
        round_down_to3 = ['n_host', 'n_liner']
        
        for i in round_down_to0:
            self.vardict[i] = round(self.vardict[i])
        for i in round_down_to1:
            self.vardict[i] = str('{0:.1f}'.format(round(self.vardict[i],1)))
        for i in round_down_to2:
            self.vardict[i] = str('{0:.2f}'.format(round(self.vardict[i],2)))
        for i in round_down_to3:
            self.vardict[i] = str('{0:.3f}'.format(round(self.vardict[i],3)))
        
        # Future - send out for calculations of flow reduction, add to dict
        
        return self.vardict

    

def LM_run(input):
    lm = LinerManager(input)
    thickness = lm.thickness_calc()
    area_lost = lm.thickness_check()
    return(thickness, area_lost, lm.output_dict())


