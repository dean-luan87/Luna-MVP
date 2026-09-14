# -*- coding: utf-8 -*-
"""Field Profiles — 场不是 scene label，是期望实体/行为/信息/风险 v1."""

from __future__ import annotations

from typing import Any, Dict

FIELD_PROFILES: Dict[str, Dict[str, Any]] = {
    "home_furniture_store": {
        "field_candidate": "home_furniture_retail_area",
        "field_properties": {
            "expected_entities": ["folding_furniture", "display_racks", "price_tags", "customers", "staff"],
            "expected_behaviors": ["browsing", "shopping", "comparing_products"],
            "expected_information": ["product_label", "price", "promotion"],
            "risk_patterns": ["glass_display", "heavy_furniture", "narrow_aisle"],
        },
    },
    "construction_site": {
        "field_candidate": "construction_work_zone",
        "field_properties": {
            "expected_entities": ["scaffolding", "metal_frames", "workers", "machinery", "safety_signs"],
            "expected_behaviors": ["construction_work", "material_transport", "equipment_operation"],
            "expected_information": ["safety_warning", "zone_boundary", "equipment_status"],
            "risk_patterns": ["falling_objects", "moving_machinery", "unauthorized_entry"],
        },
    },
    "shopping_mall_public_area": {
        "field_candidate": "shopping_mall_public_area",
        "field_properties": {
            "expected_entities": ["shops", "signs", "advertisements", "customers", "staff", "decorative_installations", "navigation_signage"],
            "expected_behaviors": ["walking", "queuing", "shopping", "wayfinding"],
            "expected_information": ["shop_sign", "floor_guide", "promotion", "exit_direction"],
            "risk_patterns": ["crowd", "stairs", "glass_door", "moving_people"],
        },
    },
    "greenery_maintenance_zone": {
        "field_candidate": "urban_greenery_maintenance",
        "field_properties": {
            "expected_entities": ["pruning_tools", "ladders", "water_pipes", "landscaping_workers", "plants"],
            "expected_behaviors": ["pruning", "watering", "lawn_mowing", "maintenance"],
            "expected_information": ["work_zone_sign", "equipment_label"],
            "risk_patterns": ["moving_equipment", "falling_branches"],
        },
    },
    "barber_shop": {
        "field_candidate": "barber_service_area",
        "field_properties": {
            "expected_entities": ["haircut_chairs", "mirrors", "scissor_machines", "barbers", "customers"],
            "expected_behaviors": ["haircutting", "waiting", "grooming"],
            "expected_information": ["price_list", "service_menu"],
            "risk_patterns": ["sharp_tools_near_customer"],
        },
    },
    "subway_platform": {
        "field_candidate": "subway_transit_platform",
        "field_properties": {
            "expected_entities": ["direction_signs", "platform_edge", "passengers", "advertisement_screens"],
            "expected_behaviors": ["waiting", "boarding", "wayfinding"],
            "expected_information": ["direction_text", "exit_sign", "transfer_info"],
            "risk_patterns": ["platform_edge", "crowd", "moving_train"],
        },
    },
    "restaurant_dining": {
        "field_candidate": "restaurant_service_area",
        "field_properties": {
            "expected_entities": ["menu_boards", "ordering_screens", "tables", "staff", "customers"],
            "expected_behaviors": ["ordering", "dining", "queuing", "payment"],
            "expected_information": ["menu", "price", "queue_number", "pickup_counter"],
            "risk_patterns": ["hot_food", "crowd", "wet_floor"],
        },
    },
    "hospital_public_area": {
        "field_candidate": "hospital_public_corridor",
        "field_properties": {
            "expected_entities": ["medical_staff", "patients", "wheelchairs", "guidance_desks", "pharmacy_windows"],
            "expected_behaviors": ["patient_transport", "consultation", "waiting"],
            "expected_information": ["department_sign", "registration_info", "pharmacy_hours"],
            "risk_patterns": ["medical_emergency", "crowd", "wet_floor"],
        },
    },
    "street_intersection": {
        "field_candidate": "urban_street_intersection",
        "field_properties": {
            "expected_entities": ["vehicles", "traffic_lights", "pedestrians", "road_signs"],
            "expected_behaviors": ["crossing", "driving", "waiting_at_light"],
            "expected_information": ["traffic_signal", "street_name", "crosswalk"],
            "risk_patterns": ["moving_vehicle", "crowd_congestion", "curb_edge"],
        },
    },
    "fire_safety_zone": {
        "field_candidate": "fire_safety_equipment_zone",
        "field_properties": {
            "expected_entities": ["fire_extinguisher", "alarm_box", "exit_sign", "safety_equipment"],
            "expected_behaviors": ["inspection", "emergency_response"],
            "expected_information": ["safety_instruction", "exit_direction"],
            "risk_patterns": ["blocked_exit", "equipment_obstruction"],
        },
    },
}


def get_field_profile(field_key: str) -> Dict[str, Any]:
    profile = FIELD_PROFILES.get(field_key, FIELD_PROFILES["shopping_mall_public_area"])
    return {
        "field_candidate": profile.get("field_candidate"),
        "field_properties": profile.get("field_properties"),
        "field_not_scene_label": True,
        "candidate_only": True,
        "not_fact": True,
    }
