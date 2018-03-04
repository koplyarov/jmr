set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(JOINT_MODULE_OUTPUT_DIRECTORY "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

################################################################################

set(DEPLOY_DIR "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/jmr_web_client")

joint_generate_adapters(python joint_adapters.py ${IDL_FILES})
add_custom_target(jmr_web_client_adapters_py ALL DEPENDS joint_adapters.py)

set(WEB_CLIENT_FILES
    web_client.py
    fake_db_activity.py
    templates/base.html
    templates/navigation-dir.html
    templates/navigation-table.html
    templates/operations.html
    templates/version.html
)

add_custom_target(
    jmr_web_client ALL
    DEPENDS jmr_web_client_adapters_py
)

add_custom_command(
    TARGET jmr_web_client 
    COMMAND ${CMAKE_COMMAND} -E copy_if_different joint_adapters.py ${DEPLOY_DIR}/joint_adapters.py
)

foreach(F ${WEB_CLIENT_FILES})
    add_custom_command(
        TARGET jmr_web_client 
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/${F} ${DEPLOY_DIR}/${F}
    )
endforeach()
