#!/bin/bash
 head -n 1 data/20160413.export.CSV  | tr '\t' '\n' | awk '{print NR-1 " " $0}'
