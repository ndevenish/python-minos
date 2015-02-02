# - Try to find Minossoft base release, otherwise prepare for base compilation
# Defines:
#   MINOS_FOUND - System has prerequisites for minos compilation
#   MINOS_INCLUDE_DIRS - Required MINOS include directories
#   MINOS_LIBRARY_DIRS - Required Library include directories
#   MINOS_CFLAGS - additional definitions
#   MINOS_TESTREL - is a test release

include(CMakeParseArguments)
# Find required libraries
find_package(ROOT REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_search_module(SIGC REQUIRED sigc++-1.2)

# Pull the environments SRT_PUBLIC_CONTEXT if set
if (NOT SRT_PUBLIC_CONTEXT AND ENV{SRT_PUBLIC_CONTEXT})
  SET(SRT_PUBLIC_CONTEXT $ENV{SRT_PUBLIC_CONTEXT} CACHE PATH "Base Minossoft Install")
  if (${SRT_PUBLIC_CONTEXT} STREQUAL ${CMAKE_SOURCE_DIR})
    MESSAGE(STATUS "Found SRT_PUBLIC_CONTEXT equivalent to local directory; Building base release")
    SET(MINOS_TESTREL FALSE)
  else()
    MESSAGE(STATUS "Found SRT_PUBLIC_CONTEXT. Building test release.")
    SET(MINOS_TESTREL TRUE)
  endif()
elseif(NOT SRT_PUBLIC_CONTEXT)
  SET(SRT_PUBLIC_CONTEXT ${CMAKE_SOURCE_DIR} CACHE PATH "Base Minossoft Install")
  MESSAGE(STATUS "No Prior SRT_PUBLIC_CONTEXT. Building base release")
endif()

# If the public context is structured with an include directory, use that
if (IS_DIRECTORY "${SRT_PUBLIC_CONTEXT}/include")
  SET(_SRT_INCLUDE "${SRT_PUBLIC_CONTEXT}/include")
else()
  SET(_SRT_INCLUDE "${SRT_PUBLIC_CONTEXT}")
endif()

set(MINOS_CFLAGS -DSITE_HAS_SIGC)
set(MINOS_LIBRARY_DIRS ${ROOT_LIBRARY_DIR} ${SIGC_LIBRARY_DIRS} ${SRT_PUBLIC_CONTEXT}/lib )
set(MINOS_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR} ${_SRT_INCLUDE} ${ROOT_INCLUDE_DIR} ${SIGC_INCLUDE_DIRS} )

FIND_PACKAGE_HANDLE_STANDARD_ARGS( MINOS DEFAULT_MSG SRT_PUBLIC_CONTEXT SIGC_FOUND ROOT_FOUND )

# Macros
macro (MINOS_ADD_LIBRARY PACKAGE_NAME)
  set (OPTIONS ROOTCINT SIGC )
  set (MULTITARGETS HEADERS SOURCES CINTSOURCES)
  CMAKE_PARSE_ARGUMENTS(MIN "${OPTIONS}" "" "${MULTITARGETS}" ${ARGN})

  # Build a list of CINT sources from the source list
  if ( ${MIN_ROOTCINT} AND ("${MIN_CINTSOURCES}" STREQUAL ""))
    set ( MIN_CINTSOURCES *.h )
  endif()

  include_directories ( ${SIGC_INCLUDE_DIRS} )

  # Put this at the front, otherwise the wrong LinkDef.h may be found
  include_directories ( BEFORE ${CMAKE_CURRENT_SOURCE_DIR} )
  
  # Build the dictionary from the source files
  if ( ${MIN_ROOTCINT} )
      ROOT_GENERATE_DICTIONARY( ${PACKAGE_NAME}.cint
                                ${MIN_CINTSOURCES}
                                OPTIONS -p
                                LINKDEF LinkDef.h )
    LIST(APPEND MIN_SOURCES ${PACKAGE_NAME}.cint.cxx )
  endif()


  add_library ( ${PACKAGE_NAME} SHARED ${MIN_SOURCES} )

  if (${MIN_SIGC})
    # Add the package directory to the search path
    link_directories ( ${SIGC_LIBRARY_DIRS} )
    target_link_libraries( ${PACKAGE_NAME} ${SIGC_LIBRARIES})
  endif()
  # All packages should compile unexplicitly for now
  # set_target_properties( ${PACKAGE_NAME} PROPERTIES LINK_FLAGS "-undefined dynamic_lookup" )
endmacro()

#get_cmake_property(_variableNames VARIABLES)
#foreach (_variableName ${_variableNames})
#    message(STATUS "${_variableName}=${${_variableName}}")
#endforeach()
