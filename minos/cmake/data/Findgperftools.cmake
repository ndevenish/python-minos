# -*- cmake -*-

# - Find Google perftools
# Find the Google perftools includes and libraries
# This module defines
#  GPERFTOOLS_FOUND, If false, do not try to use Google perftools.
#  GPERFTOOLS_INCLUDE_DIRS, where to find heap-profiler.h, etc.
#  GPERFTOOLS_LIBRARIES, where to find the required libraries.


find_package(PkgConfig)
pkg_check_modules(PC_GPERFTOOLS QUIET libprofiler)

FIND_PATH( GPERFTOOLS_INCLUDE_DIR google/heap-profiler.h
           HINTS ${PC_GPERFTOOLS_INCLUDEDIR} 
           $ENV{GPERFTOOLS_DIR}/include )

#HINTS  ${PC_GSL_INCLUDE_DIRS} ${GSL_DIR}
          
FIND_LIBRARY(GPERFTOOLS_PROFILER_LIBRARY
  NAMES profiler
  HINTS $ENV{GPERFTOOLS_DIR}/lib
        ${PC_GPERFTOOLS_LIBDIR}
        ${PC_GPERFTOOLSLIBRARY_DIRS}
  )

set(GPERFTOOLS_LIBRARIES ${GPERFTOOLS_PROFILER_LIBRARY} )
set(GPERFTOOLS_INCLUDE_DIRS ${GPERFTOOLS_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(GPERFTOOLS DEFAULT_MSG
                                  GPERFTOOLS_PROFILER_LIBRARY GPERFTOOLS_INCLUDE_DIR)
MARK_AS_ADVANCED(
  GPERFTOOLS_PROFILER_LIBRARY
  GPERFTOOLS_INCLUDE_DIR
  )