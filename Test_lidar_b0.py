# -*- coding: utf-8 -*-

import os
cd=os.path.dirname(__file__)
import utils as utl
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import warnings
import matplotlib
import glob

warnings.filterwarnings('ignore')
plt.close('all')

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm' 
matplotlib.rcParams['font.size'] = 12

#%% Inputs
source=os.path.join(cd,'data/public')
scan_sel='sc1*b0*ground.stats3d'#enter here wildcard identifier for the scan (*b0*inflow.turb, *b0*meand, *b0*inflow.stats, *b0*wake.stats3d, *b0*farmwake, *b0*bloc, sc1*b0*ground.stats3d, sh*b0*ground.stats3d)
D=127#[m] turbine diameter

#%% Initialization
try:
    file=glob.glob(os.path.join(source,scan_sel+'*.nc'))[0]
except:
    print('Could not load file. Please check file path.')

Data=xr.open_dataset(file)

#%% Main

#coordinates
r=Data['range'].values
time=Data['time'].values

X=Data['x'].mean(dim='scanID').values
Y=Data['y'].mean(dim='scanID').values
Z=Data['z'].mean(dim='scanID').values

X_all=Data['x'].values
Y_all=Data['y'].values
Z_all=Data['z'].values

#wind speed
rws=Data['wind_speed'].values
rws_qc=Data['wind_speed'].where(Data['qc_wind_speed']==0).values

#other
scan_mode=Data.attrs['scan_mode']
qc=Data['qc_wind_speed'].values

#%% Plots

#define domain limits
reals=Data['qc_wind_speed'].values==0
xlim=[np.round(np.nanpercentile(X_all[reals]/D, 1)),np.round(np.nanpercentile(X_all[reals]/D, 99))]
ylim=[np.round(np.nanpercentile(Y_all[reals]/D, 1)),np.round(np.nanpercentile(Y_all[reals]/D, 99))]
zlim=[np.round(np.nanpercentile(Z_all[reals]/D, 1)),np.round(np.nanpercentile(Z_all[reals]/D, 99))]

xlim_wide=[np.round(np.nanpercentile(X_all/D, 1)),np.round(np.nanpercentile(X_all/D, 99))]
ylim_wide=[np.round(np.nanpercentile(Y_all/D, 1)),np.round(np.nanpercentile(Y_all/D, 99))]
zlim_wide=[np.round(np.nanpercentile(Z_all/D, 1)),np.round(np.nanpercentile(Z_all/D, 99))]

#all data
plt.figure(figsize=(18,8))
plt.subplot(2,1,1)
for rep in range(len(time[0,:])):
    plt.pcolor(time[:,rep],r,rws[:,:,rep],cmap='coolwarm',vmin=np.nanpercentile(rws_qc,10)-1,vmax=np.nanpercentile(rws_qc,90)+1)
    plt.plot([time[0,rep],time[0,rep]],[r[0],r[-1]],'--k',linewidth=1)
plt.xlabel('Time (UTC)')
plt.ylabel('Range [m]')
plt.grid()
plt.title(os.path.basename(file))
plt.colorbar(label='Raw radial wind speed [m s$^{-1}$]')   

plt.subplot(2,1,2)
for rep in range(len(time[0,:])):
    plt.pcolor(time[:,rep],r,rws_qc[:,:,rep],cmap='coolwarm',vmin=np.nanpercentile(rws_qc,10)-1,vmax=np.nanpercentile(rws_qc,90)+1)
    plt.plot([time[0,rep],time[0,rep]],[r[0],r[-1]],'--k',linewidth=1)
plt.xlabel('Time (UTC)')
plt.ylabel('Range [m]')
plt.grid()
plt.colorbar(label='QC radial wind speed [m s$^{-1}$]')   

plt.tight_layout()
fig_name=os.path.join(cd,'figures',os.path.basename(file)[:-3],os.path.basename(file).replace('.nc','_rws_all.png'))
utl.mkdir(os.path.dirname(fig_name))
plt.savefig(fig_name)
plt.close()

#snapshots
if scan_mode=='PPI':
    for rep in range(len(time[0,:])):
        plt.figure(figsize=(18,8))
        pc=plt.pcolor(X/D,Y/D,rws_qc[:,:,rep],cmap='coolwarm',vmin=np.nanpercentile(rws_qc,10)-1,vmax=np.nanpercentile(rws_qc,90)+1)
        plt.xlabel(r'$x/D$')
        plt.ylabel(r'$y/D$')
        ax=plt.gca()
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xticks(np.arange(xlim[0],xlim[1]+1,2))
        ax.set_yticks(np.arange(ylim[0],ylim[1]+1,2))
        plt.grid()
        utl.axis_equal()
        plt.colorbar(label='QC radial wind speed [m s$^{-1}$]')   
        
        plt.title('Rep #'+str(rep)+': '+str(time[0,rep])[:-10].replace('T',' ')+' - '+str(time[-1,rep])[:-10].replace('T',' '))
    
        fig_name=os.path.join(cd,'figures',os.path.basename(file)[:-3],os.path.basename(file).replace('.nc','{i:02d}'.format(i=rep)+'.png'))
        plt.savefig(fig_name)
        plt.close()
        
    print('Figures saved in '+(os.path.dirname(fig_name)))


    #QC insight
    plt.figure(figsize=(18,10))
    for qc_sel in range(12):
        ax=plt.subplot(4,3,qc_sel+1)    
        sel=~np.isnan(X_all+Y_all+qc)*(qc==qc_sel)
        if qc_sel==0:
            plt.gca().scatter(X_all[sel]/D,Y_all[sel]/D,s=2,c='g',alpha=0.05)
            plt.title('Good')
        else:
            plt.gca().scatter(X_all[sel]/D,Y_all[sel]/D,s=2,c='r',alpha=0.05)
            plt.title(Data['qc_wind_speed'].attrs['bit_{qc_sel}_description'.format(qc_sel=qc_sel)].replace('Value rejected due to ','')[:-1])
        plt.xlabel(r'$x/D$')
        plt.ylabel(r'$y/D$')
        ax=plt.gca()
        ax.set_xlim(xlim_wide)
        ax.set_ylim(ylim_wide)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.grid()
        utl.axis_equal()

    plt.tight_layout()
    fig_name=os.path.join(cd,'figures',os.path.basename(file)[:-3],os.path.basename(file).replace('.nc','_qc.png'))
    plt.savefig(fig_name)
    plt.close()
    
if scan_mode=='3D':
    
    for rep in range(len(time[0,:])):
        fig=plt.figure(figsize=(12,6))
        ax=plt.subplot(1,1,1, projection='3d')
        sc=ax.scatter(X/D,Y/D,Z/D,s=2,c=rws_qc[:,:,rep],cmap='coolwarm',vmin=np.nanpercentile(rws_qc,10)-1,vmax=np.nanpercentile(rws_qc,90)+1)
        ax.set_xlabel(r'$x/D$')
        ax.set_ylabel(r'$y/D$')
        ax.set_zlabel(r'$z/D$')
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)
        ax.set_xticks(np.arange(xlim[0],xlim[1]+1,2))
        ax.set_yticks(np.arange(ylim[0],ylim[1]+1,2))
        ax.set_zticks(np.arange(zlim[0],zlim[1]+1,2))
        plt.grid()
        
        utl.axis_equal()
        plt.title('Rep #'+str(rep)+': '+str(time[0,rep])[:-10].replace('T',' ')+' - '+str(time[-1,rep])[:-10].replace('T',' '))
        
        cax=fig.add_axes([ax.get_position().x0+ax.get_position().width+0.075,ax.get_position().y0,0.015,ax.get_position().height])
        cbar = plt.colorbar(sc, cax=cax,label='QC radial radial wind speed [m s$^{-1}$]')
        
        fig_name=os.path.join(cd,'figures',os.path.basename(file)[:-3],os.path.basename(file).replace('.nc','{i:02d}'.format(i=rep)+'.png'))
        plt.savefig(fig_name)
        plt.close()
        
    print('Figures saved in '+(os.path.dirname(fig_name)))


    #QC insight
    plt.figure(figsize=(18,10))
    for qc_sel in range(12):
        ax=plt.subplot(4,3,qc_sel+1, projection='3d')  
        sel=~np.isnan(X_all+Y_all+qc)*(qc==qc_sel)
        if qc_sel==0:
            sc=ax.scatter(X_all[sel]/D,Y_all[sel]/D,Z_all[sel]/D,s=2,c='g',alpha=0.05)
            plt.title('Good')
        else:
            ax.scatter(X_all[sel]/D,Y_all[sel]/D,Z_all[sel]/D,s=2,c='r',alpha=0.05)
            plt.title(Data['qc_wind_speed'].attrs['bit_{qc_sel}_description'.format(qc_sel=qc_sel)].replace('Value rejected due to ','')[:-1])
        
        ax.set_xlabel(r'$x/D$')
        ax.set_ylabel(r'$y/D$')
        ax.set_zlabel(r'$z/D$')
        plt.grid()
        ax.set_xlim(xlim_wide)
        ax.set_ylim(ylim_wide)
        ax.set_zlim(zlim_wide)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        utl.axis_equal()

    plt.tight_layout()
    fig_name=os.path.join(cd,'figures',os.path.basename(file)[:-3],os.path.basename(file).replace('.nc','_qc.png'))
    plt.savefig(fig_name)
    plt.close()