import pandas as pd
import numpy as np
import openpyxl as opx

def data(path):
    df=pd.read_csv(path, skiprows=1, usecols=[0,4], header=None, names=['q','i'])
    return df

def theory_sphere(I0, R, sigma, q_min, q_max, points, sigma_resol):

    qq=np.logspace(q_min, q_max, points)

    def Intensity():
        #intensity from spheres
        def sphere_vol(R):
            return (4/3)*np.pi*R**3

        def Int(i0, R, q):
            qR=q*R
            return i0*sphere_vol(R)**2*(3*(np.sin(qR)-qR*np.cos(qR))/qR**3)**2
        
        #gaussian distribution
        def gaussian(x):
            return np.exp(-x**2/2)/np.sqrt(2*np.pi)

        def vol_av(R, sigma):
            return (((4/3)*np.pi)**2)*(R**6+15*R**4*sigma**2+45*R**2*sigma**4+15*sigma**6)

        #listbox for intensities
        Int_li=[]

        #gaussian list
        xx=np.linspace(-3,3, 2*sigma_resol+1)
        gaussian_li=gaussian(xx)

        Ri_li=sigma*xx+R

        for i in qq:
            Ints=Int(I0, Ri_li, i)
            Int_av=(np.dot(Ints, gaussian_li))*(3/sigma_resol)
            Int_li.append(Int_av/(vol_av(R, sigma)))
        
        return Int_li
    
    return qq, Intensity()

def export(data, params, path):
    df=pd.DataFrame(data, index=["q", "I(q)"])
    dfT=df.T
    df2 = pd.json_normalize(params)
    
    workbook = opx.Workbook()
    workbook.save(path+'.xlsx')
    
    with pd.ExcelWriter(path+'.xlsx') as writer:
        dfT.to_excel(writer, index=None, sheet_name='profile')
        df2.to_excel(writer, sheet_name='parmeters', index=False)
    



"""
def MW_Mn(I0):
    return """
