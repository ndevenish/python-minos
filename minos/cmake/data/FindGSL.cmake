# Try to find gnu scientific library GSL  
# (see http://www.gnu.org/software/gsl/)
#
# Optionally, you can specify GSL_DIR to search
#
# Once done this will define
#  GSL_FOUND - System has GSL
#  GSL_INCLUDE_DIRS - The GSL include directories
#  GSL_LIBRARIES - The libraries needed to use GSL

find_package(PkgConfig)
pkg_check_modules(PC_GSL QUIET gsl)
#set(LIBXML2_DEFINITIONS ${PC_LIBXML_CFLAGS_OTHER})

find_path(GSL_INCLUDE_DIR gsl/gsl_blas.h
          HINTS ${PC_GSL_INCLUDEDIR} ${PC_GSL_INCLUDE_DIRS} ${GSL_DIR}
          PATH_SUFFIXES gsl )

find_library(GSL_LIBRARY NAMES gsl
             HINTS ${PC_GSL_LIBDIR} ${PC_GSL_LIBRARY_DIRS} ${GSL_DIR} )

set(GSL_LIBRARIES     ${GSL_LIBRARY} )
set(GSL_INCLUDE_DIRS  ${GSL_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set LIBXML2_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(GSL DEFAULT_MSG
                                  GSL_LIBRARY GSL_INCLUDE_DIR)

mark_as_advanced( GSL_INCLUDE_DIR GSL_LIBRARY )