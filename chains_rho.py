import numpy as np
from soliket.szlike import KSZLikelihood, TSZLikelihood
from cobaya.yaml import yaml_load_file
from cobaya.samplers.mcmc import plot_progress
from cobaya.output import get_output
from cobaya.model import get_model
from cobaya.sampler import get_sampler
import matplotlib.pyplot as plt
import getdist.plots as gdplt
import time
from cobaya.run import run
import os

identity = 'FFT_transform'
print("-----------------------------------------------------------")
print("This run is for rho %s"%identity)

info_from_yaml = yaml_load_file("chains_rho.yaml")

model = get_model(info_from_yaml)
out = get_output(prefix="chains/ksz_%s"%identity,resume=False,force=True)
info_sampler = info_from_yaml["sampler"]
mcmc = get_sampler(info_sampler,model=model,output=out)
start = time.time()
mcmc.run()
end = time.time()
print("finished sampling, it took %.2f minutes = %.2f hours to converge to R-1 = 0.01"%(((end-start)/60.),((end-start)/3600.)))

plot_progress("chains/ksz_%s"%identity)
plt.tight_layout()
plt.savefig('ksz_%s_progress.png'%identity) 
plt.close() 

print("------------------------------------------------------------")
print("Now finding the best fit parameters")
updated_info_minimizer, minimizer = run(info_from_yaml, minimize=True, force=True)
minimum = minimizer.products()["minimum"]
best_rho0 = minimum['gnfw_rho0']
best_bt = minimum['gnfw_bt_ksz']
best_A2h = minimum['gnfw_A2h_ksz']

folder,name = os.path.split(os.path.abspath(info_from_yaml["output"]))
gdplot = gdplt.get_subplot_plotter(chain_dir=folder)
gdplot.settings.title_limit_fontsize=14
gdplot.triangle_plot(name,['gnfw_rho0','gnfw_bt_ksz','gnfw_A2h_ksz'],filled=True,title_limit=1,markers={'gnfw_rho0':best_rho0,'gnfw_bt_ksz':best_bt,'gnfw_A2h_ksz':best_A2h})
plt.savefig('ksz_%s_corner_labels.png'%identity,bbox_inches='tight')
plt.close()


'''
#old way
info_from_yaml = yaml_load_file("chains_rho.yaml")
info_from_yaml["likelihood"]["ksz"] = KSZLikelihood

updated_info, sampler = run(info_from_yaml,resume=False,force=True)
'''
