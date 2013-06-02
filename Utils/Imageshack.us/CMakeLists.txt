## http://nowardev.wordpress.com/2012/05/16/create-debian-package-for-script-and-simple-project-with-cmake-and-cpack/
## http://www.simonschneegans.de/?p=346

cmake_minimum_required(VERSION 2.6)

project(umageshack.us)
SET (CMAKE_PROJECT_NAME "imageshackus")

set(VERSION "0.0.1")

#search for the minimal version of kde 4.0
find_package(KDE4 4.0.0 REQUIRED)
include(KDE4Defaults)

# add_executable(src/imageshack.us.pyo src/imageshack.us.py)

# add_custom_command(OUTPUT "${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.pyo"
#                    COMMAND python2.7 ARGS -OO -m compileall "${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.py")

## This works:
# add_custom_command(OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/custom_command_output.txt" COMMAND echo "cmake echo output qwerty" > "${CMAKE_CURRENT_BINARY_DIR}/custom_command_output.txt")
# add_custom_target(custom_command_output_txt ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/custom_command_output.txt")

# add_custom_command(OUTPUT custom-command-touch COMMAND /usr/bin/touch "${CMAKE_CURRENT_BINARY_DIR}/custom-command-touch")

# add_custom_target(output ALL  /usr/bin/python2.7 -OO -m compileall "${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.py" COMMAND mv "${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.pyo" "${CMAKE_CURRENT_BINARY_DIR}/imageshack.us")


message("CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
message("CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("ICONS DIR: ${ICON_INSTALL_DIR}")
message("BIN DIR: ${BIN_INSTALL_DIR}")

message("")

## Building executable:
message("Building executable ${BIN_INSTALL_DIR}/imageshack.us ...")
add_custom_command(OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/imageshack.us" COMMAND sh "${CMAKE_CURRENT_SOURCE_DIR}/compilepy.sh" "${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.py" "${CMAKE_CURRENT_BINARY_DIR}/imageshack.us")
# add_executable("${CMAKE_CURRENT_BINARY_DIR}/imageshack.us" "${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.py")
add_custom_target(imageshack.us.bin ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/imageshack.us")
## Installing byte-compiled executable: 
message("Executable will be installed to ${BIN_INSTALL_DIR}/imageshack.us")
INSTALL(PROGRAMS "${CMAKE_CURRENT_BINARY_DIR}/imageshack.us" DESTINATION bin)

## Generating icons:
message("Generating icons ...")
add_custom_command(OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/icons" COMMAND sh "${CMAKE_CURRENT_SOURCE_DIR}/iconsgen.sh" "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}")
add_custom_target(icons ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/icons")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/icons/hicolor/16x16/apps/ImageShack.png DESTINATION "${ICON_INSTALL_DIR}/hicolor/16x16/apps")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/icons/hicolor/22x22/apps/ImageShack.png DESTINATION "${ICON_INSTALL_DIR}/hicolor/22x22/apps")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/icons/hicolor/24x24/apps/ImageShack.png DESTINATION "${ICON_INSTALL_DIR}/hicolor/24x24/apps")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/icons/hicolor/32x32/apps/ImageShack.png DESTINATION "${ICON_INSTALL_DIR}/hicolor/32x32/apps")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/icons/hicolor/48x48/apps/ImageShack.png DESTINATION "${ICON_INSTALL_DIR}/hicolor/48x48/apps")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/icons/hicolor/64x64/apps/ImageShack.png DESTINATION "${ICON_INSTALL_DIR}/hicolor/64x64/apps")


## Install the service menu:
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/imageshack.us.desktop DESTINATION ${SERVICES_INSTALL_DIR}/ServiceMenus)

## Install screenshot script
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/screenshot DESTINATION ${BIN_INSTALL_DIR})

SET(MAJOR_VERSION "0")
SET(MINOR_VERSION "0")
SET(PATCH_VERSION "1")

IF(EXISTS "${CMAKE_ROOT}/Modules/CPack.cmake")
INCLUDE(InstallRequiredSystemLibraries)

SET(CPACK_SET_DESTDIR "on")
SET(CPACK_PACKAGING_INSTALL_PREFIX "/tmp")
SET(CPACK_GENERATOR "DEB")

SET(CPACK_PACKAGE_DESCRIPTION "Imageshack.us service menu for uploading pictures.")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "It's a service menu for Dolphin (or other file manager for KDE, for example the Krusader) that allow you to upload pictures to the http://umageshack.us . After uploading, it places link to the clipboard. Also You can use <imageshack.us file.jpg> command from console to upload pictures.")
SET(CPACK_PACKAGE_VENDOR "BrainFucker")
SET(CPACK_PACKAGE_CONTACT "BrainFucker <retratserif@gmail.com>")
SET(CPACK_PACKAGE_VERSION_MAJOR "${MAJOR_VERSION}")
SET(CPACK_PACKAGE_VERSION_MINOR "${MINOR_VERSION}")
SET(CPACK_PACKAGE_VERSION_PATCH "${PATCH_VERSION}")
SET(CPACK_PACKAGE_FILE_NAME "${CMAKE_PROJECT_NAME}_${MAJOR_VERSION}.${MINOR_VERSION}.${CPACK_PACKAGE_VERSION_PATCH}")
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "${CMAKE_PROJECT_NAME}_${MAJOR_VERSION}.${MINOR_VERSION}.${CPACK_PACKAGE_VERSION_PATCH}")
#demo dependencies
#SET(CPACK_DEBIAN_PACKAGE_DEPENDS " kate , plasma-desktop, libc6 (>= 2.1.3) ")

#dependencies for this service menu
SET(CPACK_DEBIAN_PACKAGE_DEPENDS "libkdecore5, kde-runtime, libkonq5abi1, xclip, python2.7, python-simplejson, python-requests, scrot")
 
SET(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
SET(CPACK_DEBIAN_PACKAGE_SECTION "kde")
SET(CPACK_DEBIAN_ARCHITECTURE ${CMAKE_SYSTEM_PROCESSOR})

SET(CPACK_COMPONENTS_ALL Libraries ApplicationData)
INCLUDE(CPack)

ENDIF(EXISTS "${CMAKE_ROOT}/Modules/CPack.cmake")
