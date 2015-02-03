# - Try to find Neugen3
# Once done this will define
#  NEUGEN3_FOUND - System has LibXml2
#  NEUGEN3_INCLUDE_DIRS - The LibXml2 include directories

#  NEUGEN3_LIBRARIES - The libraries needed to use LibXml2


find_path(NEUGEN3_INCLUDE_DIR stdhep.inc
          HINTS $ENV{NEUGEN3PATH}/inc $ENV{NEUGEN3_DIR}/inc )

find_library(NEUGEN3_LIBRARY NAMES libneugen3.a
             HINTS $ENV{NEUGEN3PATH}/lib $ENV{NEUGEN3_DIR}/lib  )

# Not sure which of these is really required, so just include them all.
# Also, to prevent faffing about, hard-code the fermilab paths for now
SET (FNAL_PATHS /grid/fermiapp/minos/products/prd/NEUGEN3/Linux2.6-GCC_4_5/development/lib
                /grid/fermiapp/minos/products/prd/cern/2005-gfortran/Linux-2-6/lib
                /grid/fermiapp/minos/products/prd/stdhep/v5_04_noshare/Linux+2.6-GCC_4/lib )
find_library(NG3_PDF pdflib804 HINTS ${FNAL_PATHS} )
find_library(NG3_PAW pawlib   HINTS ${FNAL_PATHS} )
find_library(NG3_LAP lapack3  HINTS ${FNAL_PATHS} )
find_library(NG3_BLA blas     HINTS ${FNAL_PATHS} )
find_library(NG3_KRN kernlib  HINTS ${FNAL_PATHS} )
find_library(NG3_HEP stdhep   HINTS ${FNAL_PATHS} )

#-lpdflib804 -lpawlib -llapack3 -lblas 
#-lgraflib -lgrafX11 -lpdflib804 -lpacklib -lmathlib -lkernlib -lcrypt -ldl -lnsl -lstdhep -lgfortran



set(NEUGEN3_LIBRARIES ${NEUGEN3_LIBRARY} ${NG3_PDF} ${NG3_PAW} ${NG3_LAP} ${NG3_BLA} ${NG3_KRN} ${NG3_HEP} )
set(NEUGEN3_INCLUDE_DIRS ${NEUGEN3_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set LIBXML2_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(NEUGEN3  DEFAULT_MSG
                                  NEUGEN3_INCLUDE_DIR
                                  NEUGEN3_LIBRARY)

mark_as_advanced(NEUGEN3_INCLUDE_DIR)
mark_as_advanced(NEUGEN3_LIBRARY)
