#!/bin/bash

set -e

top=$(dirname $0)

# Tests the current script with the demo ap
${top}/venv/bin/python3 ${top}/ipa.py --ipa-path ./test/CarbonIntensityUKDemo.ipa \
    --external-frameworks-input-file-list \
    "test/CarbonIntensityUKDemo/CarbonIntensityUKDemo/Pods/Target Support Files/Pods-CarbonIntensityUKDemo/Pods-CarbonIntensityUKDemo-frameworks-Debug-input-files.xcfilelist" \
    > ${top}/../test/carbon_intensity_uk_ipa_size_report.json