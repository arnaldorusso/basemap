from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset, date2index, num2date
import numpy as np
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable
# create datetime object for desired time
date = datetime.datetime(2007,12,15,0)
# open dataset.
dataset =\
Dataset('http://nomads.ncdc.noaa.gov/thredds/dodsC/oisst2/totalAmsrAgg')
# find index of desired time.
time = dataset.variables['time']
nt = date2index(date, time, calendar='standard')
# read sst.  Will automatically create a masked array using
# missing_value variable attribute.
sst = dataset.variables['sst'][nt]
# read ice.
ice = dataset.variables['ice'][nt]
# read lats and lons (representing centers of grid boxes).
lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]
# shift lats, lons so values represent edges of grid boxes
# (as pcolor expects).
delon = lons[1]-lons[0]; delat = lats[1]-lats[0]
lons = (lons - 0.5*delon).tolist()
lons.append(lons[-1]+delon)
lons = np.array(lons,np.float64)
lats = (lats - 0.5*delat).tolist()
lats.append(lats[-1]+delat)
lats = np.array(lats,np.float64)
# creat figure, axes instances.
fig = plt.figure()
ax = fig.add_axes([0.05,0.05,0.9,0.9])
# create Basemap instance for Robinson projection.
# coastlines not used, so resolution set to None to skip
# continent processing (this speeds things up a bit)
m = Basemap(projection='robin',lon_0=lons.mean(),resolution=None)
# compute map projection coordinates of grid.
x, y = m(*np.meshgrid(lons, lats))
# draw line around map projection limb.
# color background of map projection region.
# missing values over land will show up this color.
m.drawmapboundary(fill_color='0.3')
# plot sst, then ice with pcolor
im1 = m.pcolor(x,y,sst,shading='flat',cmap=plt.cm.jet)
im2 = m.pcolor(x,y,ice,shading='flat',cmap=plt.cm.gist_gray)
# draw parallels and meridians, but don't bother labelling them.
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,420.,60.))
# use axes_grid toolkit to make colorbar axes.
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.1)
cb = plt.colorbar(im1,orientation='horizontal',cax=cax)
# add a title.
ax.set_title('SST and ICE analysis for %s'%date)
plt.savefig('plotsst.png')
