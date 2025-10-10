from netCDF4 import Dataset
from numpy import ma


"""This is a development tool for nc file comparison"""

root = "C:/Users/Jeffrey/Downloads/swson"

org_file = root+"/HadISST_sst.nc"
file = root+"/HadISST_sst_point_2p0_0p1.nc"

# with Dataset(org_file) as src, Dataset(file, "w") as dst:
#     # copy global attributes all at once via dictionary
#     dst.setncatts(src.__dict__)
#     # copy dimensions
#     for name, dimension in src.dimensions.items():
#         dst.createDimension(
#             name, (len(dimension) if not dimension.isunlimited() else None))
#     # copy all file data except for the excluded
#     for name, variable in src.variables.items():
#         print(name)
#         print(src[name].ncattrs())
#
#         dst.createVariable(name, variable.datatype, variable.dimensions)
#         dst[name].setncatts(src[name].__dict__)
#         dst[name][:] = src[name][:]
#         # copy variable attributes all at once via dictionary

old_nc = Dataset(org_file, "r")
new_nc = Dataset(file, "r")

if old_nc.variables.keys() != new_nc.variables.keys():
    print("WRONG!")
print(new_nc["sst"][:].shape)
# for key in old_nc.variables.keys():
#     print(key)
#     if old_nc[key].ncattrs() != new_nc[key].ncattrs():
#         print("WRONG!")
#     old_list = old_nc[key][:].flatten()
#     new_list = new_nc[key][:].flatten()
#     old_list.mask = ma.nomask
#     new_list.mask = ma.nomask
#
#     cnt = 0
#     for x in range(len(old_list)):
#         if old_list[x] != new_list[x]:
#             print("index", x, "old", old_list[x], "new", new_list[x])
#             cnt += 1
#
#     print(cnt)

