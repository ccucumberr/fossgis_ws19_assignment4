#!/usr/bin/env python

import grass.script as gscript


def main():
    gscript.run_command('g.region', flags='p')
#import files
    gscript.run_command('v.import', overwrite=True, output='fire', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\fire_incidents\fire_archive_V1_89293.shp")
    gscript.run_command('r.import', overwrite=True, output='landcover', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\corine_landcover_2018\CLC2018_tarragona.tif")
    gscript.run_command('r.import', overwrite=True, output='dem1', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\dem\N40E000.SRTMGL1.hgt\N40E000.hgt")
    gscript.run_command('r.import', overwrite=True, output='dem2', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\dem\N41E000.SRTMGL1.hgt\N41E000.hgt")
    gscript.run_command('r.import', overwrite=True, output='dem3', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\dem\N41E001.SRTMGL1.hgt\N41E001.hgt")
    gscript.run_command('v.import', overwrite=True, output='buildings', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\osm\buildings.geojson")
    gscript.run_command('v.import', overwrite=True, output='firestations', input=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\assignment4_data\assignment4_data\osm\fire_stations.geojson")
#merge dems
    gscript.run_command('r.patch', overwrite=True, output='dem_tarragona', input=['dem1', 'dem2', 'dem3'])
#calculate slope
    gscript.run_command('r.slope.aspect', overwrite=True, elevation='dem_tarragona', slope='slope')
#reclass slope fire categories
    gscript.run_command('r.reclass', overwrite=True, input='slope', output='reclass_slope', rules=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\reclass_slope_fire_rule.txt")
#make result permanent
    gscript.run_command('r.resample', overwrite=True, input='reclass', output='slope_hazardclass')
#reclass landcover
    gscript.run_command('r.reclass', overwrite=True, input='landcover', output='reclass_landcover', rules=r"C:\Users\Eddi\Desktop\FOSSGIS\assignment4_V2\fossgis_ws19_assignment4\reclass_landcover_rule.txt")
#calculate probability for ignition on fire
    gscript.run_command('v.mkgrid', overwrite=True, map='grid', box='1000,1000')
    gscript.run_command('v.vect.stats', overwrite=True, points='wildfire_incidents', areas='grid', method='sum', points_column='cat', count_column='fire_count', stats_column='stat')
    gscript.run_command('v.to.rast', overwrite=True, input='grid3', output='incidents_cells', use='attr', attribute_column='fire_count', label_column='fire_count')
if __name__ == '__main__':
    main()
