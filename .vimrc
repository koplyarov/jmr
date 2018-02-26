let g:cpp_plugin.indexer.builder.autoBuild = 1
call g:buildsystem.setAvailableBuildConfigs( { 'host': CMakeBuildConfig(4, './build/') } )
