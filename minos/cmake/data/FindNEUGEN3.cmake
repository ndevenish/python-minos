# - Try to find Neugen3
# Once done this will define
#  NEUGEN3_FOUND - System has LibXml2
#  NEUGEN3_INCLUDE_DIRS - The LibXml2 include directories

#  NEUGEN3_LIBRARIES - The libraries needed to use LibXml2


find_path(NEUGEN3_INCLUDE_DIR stdhep.inc
          HINTS $ENV{NEUGEN3PATH}/inc $ENV{NEUGEN3_DIR}/inc )

find_library(NEUGEN3_LIBRARY NAMES libneugen3.a
             HINTS $ENV{NEUGEN3PATH}/lib $ENV{NEUGEN3_DIR}/lib  )

set(NEUGEN3_LIBRARIES ${NEUGEN3_LIBRARY} )
set(NEUGEN3_INCLUDE_DIRS ${NEUGEN3_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set LIBXML2_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(NEUGEN3  DEFAULT_MSG
                                  NEUGEN3_INCLUDE_DIR
                                  NEUGEN3_LIBRARY)

mark_as_advanced(NEUGEN3_INCLUDE_DIR)
mark_as_advanced(NEUGEN3_LIBRARY)
