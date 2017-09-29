#!/bin/bash

#run python validator
find ../ -name '*.py' | xargs pep8  --max-line-length=200
