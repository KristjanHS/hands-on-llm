#!/bin/bash
# Run black on the provided files
black "$@"
# Stage the changes
git add "$@"
