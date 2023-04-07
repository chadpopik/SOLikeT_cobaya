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

identity = 'Hankel_transform_0.001'
print("---------------------------------------------------")
print("This run is for pth %s"%identity)

info_from_yaml = yaml_load_file("chains_pth.yaml")
'''
model = get_model(info_from_yaml)
out = get_output(prefix="chains/tsz_%s"%identity,resume=False,force=True)
info_sampler = info_from_yaml["sampler"]
mcmc = get_sampler(info_sampler,model=model,output=out)
start =	time.time()
mcmc.run()
end = time.time()
print("finished sampling, it took %.2f minutes = %.2f hours to converge to R-1 = 0.01"%(((end-start)/60.),((end-start)/3600.)))

plot_progress("chains/tsz_%s"%identity)
plt.tight_layout()
plt.savefig('tsz_%s_progress.png'%identity)
plt.close()
'''
print("---------------------------------------------------")
print("Now finding the best fit parameters")
updated_info_minimizer, minimizer = run(info_from_yaml, minimize=True, force=True)
minimum = minimizer.products()["minimum"]
best_P0 = minimum['gnfw_P0']
best_bt = minimum['gnfw_bt_tsz']
best_A2h = minimum['gnfw_A2h_tsz']

folder,name = os.path.split(os.path.abspath(info_from_yaml["output"]))
gdplot = gdplt.get_subplot_plotter(chain_dir=folder)
gdplot.settings.title_limit_fontsize=14
gdplot.triangle_plot(name,['gnfw_P0','gnfw_bt_tsz','gnfw_A2h_tsz'],filled=True,title_limit=1,markers={'gnfw_P0':best_P0,'gnfw_bt_tsz':best_bt,'gnfw_A2h_tsz':best_A2h})
plt.savefig('tsz_%s_corner_labels.png'%identity,bbox_inches='tight')
plt.close()

