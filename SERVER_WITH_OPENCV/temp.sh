#!/usr/bin/env bash
 export rm=/sys/class/tacho-motor/motor1
 export lm=/sys/class/tacho-motor/motor0
 echo reset > $rm/command
 echo reset > $lm/command
 echo brake > $rm/stop_action
 echo brake > $lm/stop_action
 echo 120   > $rm/speed_sp
 echo -120  > $lm/speed_sp
 echo 402    > $rm/position_sp
 echo -402    > $lm/position_sp
 echo run-to-rel-pos > $rm/command
 echo run-to-rel-pos > $lm/command
