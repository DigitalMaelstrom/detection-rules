#!/bin/bash

 find rules -name '*.toml' -exec cat {} \; | sed -n -e 's/^index = \[\(.*\)\]/\1/p' | sed -n -e 's/, /\n/gp' | sort | uniq