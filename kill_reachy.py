from reachy_sdk import ReachySDK

reachy = ReachySDK(host='localhost')
reachy.turn_on('head')
reachy.turn_off('head')