__author__ = 'mjohnpayne'

import numpy
import glob
import matplotlib.pyplot as plt

pat = '/Volumes/MP_HD/Pm_Ts_Tf_Pf_comparison/orthomcl_run/orthomcl_data/CDS_files/syn_distance_out'

indata = glob.glob(pat + '/*.meg')


pfpml = []
pftfl = []
pmtfl = []
pftsl = []
pmtsl = []
tftsl = []

c = 0
for i in indata:
    if c%1000 == 0:
        print c
    infile = open(i,'r').readlines()
    pmaa = infile[35][9:].strip('\n')
    pfpm = float(infile[41][5:15].strip('\n'))
    pfpml.append(pfpm)
    pftf = float(infile[42][5:15].strip('\n'))
    pftfl.append(pftf)
    pmtf = float(infile[42][16:].strip('\n'))
    pmtfl.append(pmtf)
    pfts = float(infile[43][5:15].strip('\n'))
    pftsl.append(pfts)
    pmts = float(infile[43][16:26].strip('\n'))
    pmtsl.append(pmts)
    tfts = float(infile[43][27:].strip('\n'))
    tftsl.append(tfts)
    c +=1

inf = [pfpml,pftfl,pmtfl,pftsl,pmtsl,tftsl]
data = {'pfpm':pfpml,'pftf':pftfl,'pmtf':pmtfl,'pfts':pftsl,'pmts':pmtsl,'tfts':tfts}
name = ['pfpm','pftf','pmtf','pfts','pmts','tfts']
av = []
std = []
for x in data:
    # name += [x]
    av += [numpy.average(data[x])]
    std += [numpy.std(data[x])]

ax = plt.axes()
plt.boxplot(inf)
ax.set_xticklabels(name)
plt.savefig('/Volumes/MP_HD/Pm_Ts_Tf_Pf_comparison/orthomcl_run/orthomcl_data/CDS_files/boxplots_syn_mut_prop.pdf',dpi=400)

print name
print av
# c = 1
# for i in infile:
#     print c
#     print itfts
#     c+=1
