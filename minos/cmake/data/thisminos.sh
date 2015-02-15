# Source this script to set up the MINOS build that this script is part of.

drop_from_path()
{
   # Assert that we got enough arguments
   if test $# -ne 2 ; then
      echo "drop_from_path: needs 2 arguments"
      return 1
   fi

   p=$1
   drop=$2

   newpath=`echo $p | sed -e "s;:${drop}:;:;g" \
                          -e "s;:${drop};;g"   \
                          -e "s;${drop}:;;g"   \
                          -e "s;${drop};;g"`
}

drop_contexts()
{
   if [ -n "${LD_LIBRARY_PATH}" ]; then
      drop_from_path $LD_LIBRARY_PATH $1/_build/lib
      LD_LIBRARY_PATH=$newpath
   fi
   if [ -n "${DYLD_LIBRARY_PATH}" ]; then
      drop_from_path $DYLD_LIBRARY_PATH $1/_build/lib
      DYLD_LIBRARY_PATH=$newpath
   fi
}

add_export()
{
  #echo "Exporting: ${1}"
  if [ -z "${LD_LIBRARY_PATH}" ]; then
    LD_LIBRARY_PATH=$1/_build/lib; export LD_LIBRARY_PATH       # Linux, ELF HP-UX
  else
    LD_LIBRARY_PATH=$1/_build/lib:$LD_LIBRARY_PATH; export LD_LIBRARY_PATH
  fi

  if [ -z "${DYLD_LIBRARY_PATH}" ]; then
    DYLD_LIBRARY_PATH=$1/_build/lib; export DYLD_LIBRARY_PATH   # Mac OS X
  else
    DYLD_LIBRARY_PATH=$1/_build/lib:$DYLD_LIBRARY_PATH; export DYLD_LIBRARY_PATH
  fi
}

determine_script_directory()
{
  # Get the script directory
  if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f thisminos.sh ]; then
      echo ERROR: must "cd where/minos/is" before calling ". thistest.sh" for this version of bash!
      SRT_PRIVATE_CONTEXT=; export SRT_PRIVATE_CONTEXT
      return 1
    fi
    DIR="$PWD"
  else
    DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  fi
}

determine_script_directory
#echo "Running from $DIR"

# Different behaviour depending if we are a base or a test release
if [ -s $DIR/.base_release ]; then
  echo "Loading test release $DIR" >&2
  # File exists AND has contents. We are a test release.
  # Chain to the parent base release if at all possible
  POTENTIAL_PRIVATE=${DIR}
  if [ -f $(cat $DIR/.base_release)/thisminos.sh ]; then
    echo "Chain-loading base release $(cat $DIR/.base_release)" >&2
    source $(cat $DIR/.base_release)/thisminos.sh
  else
    echo "ERROR: Base release needs to have a thisminos.sh script"
    exit
  fi 
  # Clear any existing private context variable
  if [ -n "${SRT_PRIVATE_CONTEXT}" ]; then
    drop_contexts $SRT_PRIVATE_CONTEXT
  fi
  export SRT_PRIVATE_CONTEXT=$POTENTIAL_PRIVATE
  add_export $SRT_PRIVATE_CONTEXT
else
  # Base release file does not exist, or is empty. We are a base release.
  # Drop everything, as we will be resetting public
  if [ -n "${SRT_PUBLIC_CONTEXT}" ]; then
    drop_contexts $SRT_PUBLIC_CONTEXT
  fi
  if [ -n "${SRT_PRIVATE_CONTEXT}" ]; then
    drop_contexts $SRT_PRIVATE_CONTEXT
  fi
  # Set the new public context
  export SRT_PUBLIC_CONTEXT=${DIR}
  add_export $SRT_PUBLIC_CONTEXT
fi

# Look at importing ROOT
if [ -s $DIR/.base_root ]; then
  echo "Using ROOT at $(cat $DIR/.base_root)" >&2
  source $(cat $DIR/.base_root)/bin/thisroot.sh
fi

unset DIR


export ENV_TSQL_PSWD=minos_db
export ENV_TSQL_USER=reader
export ENV_TSQL_URL='mysql:odbc://minos-db1.fnal.gov/temp;mysql:odbc://minos-db1.fnal.gov/offline'
