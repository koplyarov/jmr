joint_generate_adapters(python joint_adapters.py
    ${IDL_DIR}/IClient.idl
)

add_custom_target(core-adapters-py ALL DEPENDS joint_adapters.py)

joint_make_module_package(core-component-py
    PACKAGE_DIR ${JOINT_MODULE_OUTPUT_DIRECTORY}/core
    MANIFEST Core.jm
    DEPENDS core-adapters-py
)

joint_add_module_content(core-component-py
    DIRECTORY Package
    FILES __init__.py module.py ${CMAKE_CURRENT_BINARY_DIR}/joint_adapters.py
)

joint_add_module_content(core-component-py
    DIRECTORY Package/client
    FILES client/__init__.py client/client_session.py
)

joint_add_module_content(core-component-py
    DIRECTORY Package/operation
    FILES operation/__init__.py operation/map_operation.py operation/map_reduce_operation.py
)

joint_add_module_content(core-component-py
    DIRECTORY Package/storage
    FILES storage/__init__.py storage/memory_storage.py
)

joint_add_module_content(core-component-py
    DIRECTORY Package/tables
    FILES tables/__init__.py tables/row.py tables/row_reader.py tables/row_writer.py
)
