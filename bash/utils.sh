#!/bin/bash

# Set enviroment variables definied in one or more files
function set_env {
  for envfile in $@
  do
    if [ -f $envfile ]
      then
        set -a            
        source $envfile
        set +a
      fi
  done
}