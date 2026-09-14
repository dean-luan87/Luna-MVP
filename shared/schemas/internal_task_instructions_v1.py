# -*- coding: utf-8 -*-
"""
内部任务指令 id（v1 机器语言）。

完整语义与映射表见：docs/architecture/task/LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md
"""

from __future__ import annotations


class Navigation:
    START = "navigation.start"
    PAUSE = "navigation.pause"
    RESUME = "navigation.resume"
    STOP = "navigation.stop"
    REROUTE = "navigation.reroute"
    ADD_WAYPOINT = "navigation.add_waypoint"
    REMOVE_WAYPOINT = "navigation.remove_waypoint"
    SWITCH_DESTINATION = "navigation.switch_destination"
    QUERY_PROGRESS = "navigation.query_progress"
    QUERY_ETA = "navigation.query_eta"
    QUERY_LOCATION = "navigation.query_location"
    QUERY_ROUTE_STATUS = "navigation.query_route_status"


class Observation:
    SCAN_ONCE = "observation.scan_once"
    SCAN_CONTINUOUS = "observation.scan_continuous"
    FIND_OBJECT = "observation.find_object"
    FIND_SIGN = "observation.find_sign"
    FIND_PLACE = "observation.find_place"
    DESCRIBE_SCENE = "observation.describe_scene"
    QUERY_FRONT = "observation.query_front"
    QUERY_LEFT = "observation.query_left"
    QUERY_RIGHT = "observation.query_right"
    QUERY_NEARBY = "observation.query_nearby"
    STOP_SCAN = "observation.stop_scan"


class Task:
    START = "task.start"
    PAUSE = "task.pause"
    RESUME = "task.resume"
    STOP = "task.stop"
    CANCEL = "task.cancel"
    SWITCH = "task.switch"
    INSERT_TEMPORARY = "task.insert_temporary"
    RESTORE_PREVIOUS = "task.restore_previous"
    QUERY_CURRENT = "task.query_current"
    QUERY_NEXT_STEP = "task.query_next_step"


class Device:
    VOLUME_UP = "device.volume_up"
    VOLUME_DOWN = "device.volume_down"
    MUTE = "device.mute"
    UNMUTE = "device.unmute"
    SLEEP = "device.sleep"
    SHUTDOWN = "device.shutdown"
    STATUS_QUERY = "device.status_query"
    UPDATE_QUERY = "device.update_query"


class Confirmation:
    ACCEPT = "confirmation.accept"
    REJECT = "confirmation.reject"
    MODIFY = "confirmation.modify"


class Feedback:
    STOP_CURRENT_DIALOGUE = "feedback.stop_current_dialogue"
    NOT_UNDERSTOOD = "feedback.not_understood"
    RETRY = "feedback.retry"


class CasualObservation:
    QUERY_ONCE = "casual_observation.query_once"
    QUERY_NEARBY = "casual_observation.query_nearby"
    DESCRIBE_CURRENT_SCENE = "casual_observation.describe_current_scene"
