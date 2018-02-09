#!/bin/bash
set -evx

mkdir ~/.pushicore

# safety check
if [ ! -f ~/.pushicore/.pushi.conf ]; then
  cp share/pushi.conf.example ~/.pushicore/pushi.conf
fi
