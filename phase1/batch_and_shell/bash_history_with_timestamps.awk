#!/usr/bin/awk -f

/^#/ {
    cmd_time = substr($0, 2)
    getline cmd
    cmd_date = strftime("%Y-%m-%d %H:%M:%S", cmd_time)
    print cmd_date " " cmd
}