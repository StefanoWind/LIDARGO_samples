# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:34:08 2024

@author: sletizia
"""
import numpy as np
from matplotlib import pyplot as plt
import warnings
import matplotlib
import os

warnings.filterwarnings('ignore')
plt.close('all')

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm' 
matplotlib.rcParams['font.size'] = 14

#%% System
def mkdir(path):
    '''
    Makes recursively folder from path, no existance error
    '''
    import os
    path=path.replace('\\','/')
    folders=path.split('/')
    upper=''
    for f in folders:
        try:
            os.mkdir(upper+f)           
        except:
            pass
                
        upper+=f+'/'
        

#%% Error analysys
def plot_lin_fit(x,y,lb=[],ub=[],units=''):
    '''
    Plots linear fit and key error metrics
    '''
      
    from scipy.stats import linregress
    
    reals=~np.isnan(x+y)
    
    if np.sum(reals)<=1:
        print("Insufficent number of valid points for linear regression")
        return
    
    if lb==[]:
        lb=np.nanmin(np.append(x,y))
        
    if ub==[]:
        ub=np.nanmax(np.append(x,y))
        
    lf=np.round(linregress(x[reals],y[reals]),3)
    rho=np.round(np.corrcoef(x[reals],y[reals])[0][1],3)
    bias=np.round(np.nanmean(y[reals]-x[reals]),3)
    err_SD=np.round(np.nanstd(y[reals]-x[reals]),3)

    scatter=plt.plot(x,y,'.k',markersize=5,alpha=0.25)
    
    line1_1=plt.plot([lb,ub],[lb,ub],'--g')
    trendline=plt.plot(np.array([lb,ub]),np.array([lb,ub])*lf[0]+lf[1],'r',linewidth=2)
    
    txt=plt.text(lb+(ub-lb)*0.05,lb+(ub-lb)*0.05,r'$y='+str(lf[1])+r'+'+str(lf[0])+r'~x $'+'\n'+
                 r'$\rho='+str(rho)+r'$'+'\n'+r'$\overline{\epsilon}='+str(bias)+'$ '+units+
             '\n'+r'$\sqrt{\overline{\epsilon^{\prime 2}}}='+str(err_SD)+'$ '+units,color='k',fontsize=15,bbox=dict(facecolor=(1,1,1,0.25), edgecolor='k'))

    axis_equal()
    plt.xticks(plt.gca().get_yticks())
    plt.xlim([lb,ub])
    plt.ylim([lb,ub])
    txt_position=txt.get_window_extent().transformed(plt.gca().transData.inverted())
    txt.set_position((lb+(ub-lb)*0.05,lb+(ub-lb)*0.95-txt_position.height))
    plt.grid()
    
    return lf,rho,bias,err_SD,scatter,line1_1,trendline,txt

#%% Dates
def datenum(string,format="%Y-%m-%d %H:%M:%S.%f"):
    '''
    Turns string date into unix timestamp
    '''
    from datetime import datetime
    num=(datetime.strptime(string, format)-datetime(1970, 1, 1)).total_seconds()
    return num

def datestr(num,format="%Y-%m-%d %H:%M:%S.%f"):
    '''
    Turns Unix timestamp into string
    '''
    from datetime import datetime
    string=datetime.utcfromtimestamp(num).strftime(format)
    return string
    

def dt64_to_num(dt64):
    '''
    Converts Unix timestamp into numpy.datetime64
    '''
    tnum=(dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    return tnum

def num_to_dt64(tnum):
    '''
    Converts numpy.datetime64 into Unix timestamp
    '''
    dt64= np.datetime64('1970-01-01T00:00:00Z')+np.timedelta64(int(tnum*10**9), 'ns')
    return dt64

#%% Trigonometry
def cosd(x):
    return np.cos(x/180*np.pi)

def sind(x):
    return np.sin(x/180*np.pi)
    
def tand(x):
    return np.tan(x/180*np.pi)

def arctand(x):
    return np.arctan(x)*180/np.pi

def arccosd(x):
    return np.arccos(x)*180/np.pi

def arcsind(x):
    return np.arcsin(x)*180/np.pi

#%% Graphics
def axis_equal():
    '''
    Makes axis of plot equal
    '''
    from mpl_toolkits.mplot3d import Axes3D
    ax=plt.gca()
    is_3d = isinstance(ax, Axes3D)
    if is_3d:
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        zlim=ax.get_zlim()
        ax.set_box_aspect((np.diff(xlim)[0],np.diff(ylim)[0],np.diff(zlim)[0]))
    else:
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        ax.set_box_aspect(np.diff(ylim)/np.diff(xlim))
        
        
def remove_labels(fig):
    '''
    Removes duplicated labels from multiplot
    '''
    axs=fig.axes

    for ax in axs:
        loc=ax.get_subplotspec()
        try:
            
            if loc.is_last_row()==False:
                ax.set_xticks(ax.get_xticks(),[])
                ax.set_xlabel('')
            if loc.is_first_col()==False:
                ax.set_yticks(ax.get_yticks(),[])
                ax.set_ylabel('')
        except:
            pass

def save_all_fig(name,cd,newfolder=False,resolution=300):
    '''
    Saves all current figures
    '''
    mkdir(os.path.join(cd,'figures'))
    if newfolder:
        mkdir(os.path.join(cd,'figures',name))
    figs = [plt.figure(n) for n in plt.get_fignums()]
    inc=0
    for fig in figs:
        if newfolder:
            fig.savefig(os.path.join(cd,'figures',name,'{i:02d}'.format(i=inc)+'.png'),dpi=resolution, bbox_inches='tight')
        else:
            fig.savefig(os.path.join(cd,'figures',name+'{i:02d}'.format(i=inc)+'.png'),dpi=resolution, bbox_inches='tight')
        inc+=1
        
def draw_turbine(x,y,D,wd):
    cd=os.path.dirname(__file__)
    import matplotlib.image as mpimg
    from matplotlib import transforms
    from matplotlib import pyplot as plt
    img = mpimg.imread(os.path.join(cd,'Turbine5.png'))
    ax=plt.gca()
    tr = transforms.Affine2D().scale(D/700,D/700).translate(-100*D/700+x,-370*D/700+y).rotate_deg(90-wd)
    ax.imshow(img, transform=tr + ax.transData)

#%% Machine learning
def RF_feature_selector(X,y,test_size=0.8,n_search=30,n_repeats=10,limits={}):
    '''
    Feature importance selector based on random forest. The optimal set of hyperparameters is optimized through a random search.
    Importance is evaluated throuhg the permutation method, which gives higher scores to fatures whose error metrics drops more after reshuffling.
    '''
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.inspection import permutation_importance
    from scipy.stats import randint
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import mean_absolute_error

    #build train/test datasets
    data = np.hstack((X, y.reshape(-1, 1)))

    data = data[~np.isnan(data).any(axis=1)]
    train_set, test_set = train_test_split(data, random_state=42, test_size=test_size)

    X_train = train_set[:,0:-1]
    y_train = train_set[:,-1]

    X_test = test_set[:,0:-1]
    y_test = test_set[:,-1]
    
    #default grid of hyperparamters (Bodini and Optis, 2020)
    if limits=={}:
        p_grid = {'n_estimators': randint(low=10, high=100), # number of trees
                  'max_features': randint(low=1,high= 6), # number of features to consider when looking for the best split
                  'min_samples_split' : randint(low=2, high=11),
                  'max_depth' : randint(low=4, high=10),
                  'min_samples_leaf' : randint(low=1, high=15)
            }
        
    # Choose cross-validation techniques for the inner and outer loops,
    # independently of the dataset.
    forest_reg = RandomForestRegressor()
    rnd_search = RandomizedSearchCV(forest_reg, param_distributions = p_grid, n_jobs = -1,
                                    n_iter=n_search, cv=5, scoring='neg_mean_squared_error')
    rnd_search.fit(X_train, y_train)
    print('Best set of hyperparameters found:')
    print(rnd_search.best_estimator_)

    predicted_test = rnd_search.best_estimator_.predict(X_test)
    test_mae = mean_absolute_error(y_test, predicted_test)
    print("Average testing MAE:", test_mae)

    predicted_train = rnd_search.best_estimator_.predict(X_train)
    train_mae = mean_absolute_error(y_train, predicted_train)
    print("Average training MAE:", train_mae)

    best_params=rnd_search.best_estimator_.get_params()    
        
    #random forest prediction with optimized hyperparameters
    reals=np.sum(np.isnan(np.hstack((X, y.reshape(-1, 1)))),axis=1)==0
    rnd_search.best_estimator_.fit(X[reals,:], y[reals])
        
    y_pred=y+np.nan
    y_pred[reals] = rnd_search.best_estimator_.predict(X[reals])
       
    reals=~np.isnan(y+y_pred)
    result = permutation_importance(rnd_search.best_estimator_, X[reals], y[reals], n_repeats=n_repeats, random_state=42, n_jobs=2)

    importance=result.importances_mean
    importance_std=result.importances_std
    
    return importance,importance_std,y_pred,test_mae,train_mae,best_params
