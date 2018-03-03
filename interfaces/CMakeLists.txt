set(IDL_FILES_LOCAL
    IClient.idl
    fs/IFsClient.idl
    fs/INode.idl
    io/IRow.idl
    io/IRowReader.idl
    io/IRowWriter.idl
    operations/IOperation.idl
    operations/Operations.idl
)

set(IDL_FILES_LOCAL_PATH_FIXED "")
foreach(F ${IDL_FILES_LOCAL})
    list(APPEND IDL_FILES_LOCAL_PATH_FIXED "${CMAKE_CURRENT_SOURCE_DIR}/${F}")
endforeach()
set(IDL_FILES ${IDL_FILES_LOCAL_PATH_FIXED} PARENT_SCOPE)

