set runtimepath+=joint/ide/vim
au BufRead,BufNewFile *.idl set filetype=joint

let g:cpp_plugin.indexer.builder.autoBuild = 1
call g:buildsystem.setAvailableBuildConfigs( { 'host': CMakeBuildConfig(4, './build/') } )
