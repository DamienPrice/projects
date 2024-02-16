import os
import numpy as np
from numpy import multiply as mult
from numpy import power as pwr
from numpy import divide as div
from numpy import add as add
from numpy import pi as pi
from numpy import exp as exp
from numpy import log as log
from numpy import sqrt as sqrt
from numpy import square as squ
from scipy.integrate import quad
tpis = 2*pi**2

#retrieving data and file creation
cwd = os.getcwd()
particle_file = 'particleData_pdg2016plusnew_demo' #particle data
chempot_file = 'chemical_potentials_demo' #chempot data
filename = 'ihrgPressures_pdg2016plusnew' #output filename
particles = np.genfromtxt(os.path.join(cwd,particle_file)).astype('float128')
chempot = np.genfromtxt(os.path.join(cwd,chempot_file)).astype('float128')
with open(os.path.join(cwd,filename),'w') as f: #to verify file can be made
    pass

#remove photon from particle data
col = particles[:,0]
ind22 = np.where(col==22)[0]
particles = np.delete(particles,ind22,axis=0)

#columns to arrays of particles data
mi,di,bi,si,qi = particles[:,2],particles[:,4],particles[:,5],particles[:,6],particles[:,10]

#pre-integration components
pi = mult(pwr(-1,bi+1),div(di,tpis)) #pre-integral w/o temp array
xi = pwr(-1,bi+1) #pre-exponent array

#main calculation
## integrand
def integrand(p,xi,mi,ei,t):
    return mult(p**2,log(add(1,mult(xi,exp(div(ei-sqrt(p**2+squ(mi)),t))))))

## integration
def integrate(xi,mi,ei,t):
    return quad(integrand,0,np.inf,args=(xi,mi,ei,t))[0]
integrate_vec = np.vectorize(integrate)

## main function
def main(row): #takes in each smash row
    t = row[0]
    pit = mult(pi,pwr(t,-3)) #pre-integral with temp array, it's T^-3 bc we want P/T^4
    bei,sei,qei = mult(bi,row[1]),mult(si,row[2]),mult(qi,row[3]) #components of end of integral 
    cei = np.array([bei,sei,qei])
    ei = np.sum(cei,axis=0) #end of integral sum array
    grals = integrate_vec(xi,mi,ei,t) #array of all the integrals per row in particles data
    pitgrals = mult(pit,grals) #array of complete quantities to be summed
    fullsum = np.sum(pitgrals,axis=0)#sum of all complete quantities w/ all particle rows w/ 1 temp
    return fullsum

# create table
#%%time #used in jupyter notebook
res = map(main,chempot) #results of all summing with integrations; most time consuming part
pressure = np.array(list(res)) #pressure array
temps = np.round(chempot[:,0],decimals=3) #this is done bc for an unknown reason savetxt alters values; this forces the correct value
allvalues = np.array([temps,chempot[:,1],chempot[:,2],chempot[:,3],pressure]) #T,muB,muS,muQ,P
table = np.transpose(allvalues)

# create file
path = os.path.join(cwd,filename)
np.savetxt(path,table,fmt='%1.3f\t%1.15e\t%1.15e\t%1.15e\t%1.15e')
print('Task Complete')