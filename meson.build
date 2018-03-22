pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gas_station_software')
gnome = import('gnome')

gnome.compile_resources('gas-station-software',
  'gas-station-software.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'gas-station-software.in',
  output: 'gas-station-software',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gas_station_software_sources = [
  'gi_composites.py',
  'main.py',
  'Login.py',
  'Sales.py',
  'definitions.py',
  'database_handler.py',
  'calculator.py',
'dips.py',
'double_entry.py',
'debtors.py',
'accounting.py',
'settings.py',
'inventory.py',
]

database =['julaw.db',]

install_data(gas_station_software_sources, install_dir: moduledir)
install_data(database, install_dir: moduledir)
