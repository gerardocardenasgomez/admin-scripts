#!/usr/bin/env python
# Currently for yum only


import platform
import rpm


pkgFilter = []

with open("packages.txt", "r") as file:
    for line in file:
        pkgString = line
        pkgFilter.append(pkgString.replace("\n", ""))

distName, distVersion, distID = platform.linux_distribution()
sysType = platform.machine()
sysName = platform.system()
sysRelease = platform.release()

db = rpm.TransactionSet()
mdb = db.dbMatch()

print "-" * 5, " * SYSINFO * ", "-" * 5

print "{0} {1} -- Kernel {2}".format(sysName, sysType, sysRelease)
print "{0} {1} {2}".format(distName, distVersion, distID)

print "-" * 5, " * PACKAGES * ", "-" * 5

for item in mdb:
    pkgName = item['name']
    pkgVersion = item['version']
    pkgRelease = item['release']

    if pkgName in pkgFilter:
        continue
    else:
        print "{0} {1} ({2})".format(pkgName, pkgVersion, pkgRelease)
