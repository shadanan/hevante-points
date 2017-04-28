#!/usr/bin/env python
import itertools

actions = ["to send",
           "to add",
           "to give"]

points_dests = ["{Points} points to {Dest}",
                "{Dest} {Points} points"]

srcs = ["from {Source}"]

reason_preps = ["for",
                "because"]

reasons = ["{donuts|Reason}",
           "{help|Reason}",
           "{helping|Reason}",
           "{graphs|Reason}",
           "{changes|Reason}",
           "{metrics|Reason}",
           "{code review|Reason}",
           "{being helpful|Reason}",
           "{feather boa|Reason}",
           "{bringing donuts|Reason}",
           "{quick code review|Reason}",
           "{help with task|Reason}",
           "{helping with task|Reason}",
           "{helping with code|Reason}",
           "{lack of feather boa|Reason}",
           "{helping with a task|Reason}",
           "{help with a task|Reason}",
           "{spending all day helping|Reason}",
           "{spending all day helping me|Reason}",
           "{spending all day working with dynamo DB|Reason}"]


utterances = []

for utterance in itertools.product(actions, points_dests, srcs, reason_preps, reasons):
    utterances.append('SendHevantePoints %s' % ' '.join(utterance))

for utterance in itertools.product(actions, points_dests, reason_preps, reasons, srcs):
    utterances.append('SendHevantePoints %s' % ' '.join(utterance))

for utterance in itertools.product(actions, points_dests):
    utterances.append('SendHevantePoints %s' % ' '.join(utterance))

for utterance in itertools.product(actions, points_dests, reason_preps, reasons):
    utterances.append('SendHevantePoints %s' % ' '.join(utterance))

for utterance in itertools.product(actions, points_dests, srcs):
    utterances.append('SendHevantePoints %s' % ' '.join(utterance))

utterances.append('GetName {Name}')
utterances.append('GetName to {Name}')
utterances.append('GetName from {Name}')

utterances.append('GetPoints {Points}')
utterances.append('GetPoints {Points} points')

for utterance in itertools.product(reason_preps, reasons):
    utterances.append('GetReason %s' % ' '.join(utterance))

print('\n'.join(utterances))
