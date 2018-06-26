#!/usr/bin/env bash
# This method takes an URL then performs a curl request against it and records time_taken
tt_url_test(){
URL=$1
    test=$(curl -w "@curl-format.txt" -o /dev/null -s ${URL})
    return ${test}
}
