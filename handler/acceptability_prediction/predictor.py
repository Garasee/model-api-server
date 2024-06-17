import numpy as np
import pandas as pd

from handler.commons.encoding_handler import handle_encoding

SMALL_LUG_BOOT_THRESHOLD = 7500000
MEDIUM_LUG_BOOT_THRESHOLD = 8000000
BIG_LUG_BOOT_THRESHOLD = 8750000
CATEGORICAL_FEATURES = ['buying', 'maint', 'lug_boot', 'safety']


def predict_acceptability(payload, predicted_price, model, encoders):
    buying_capacity = "high" if predicted_price > 310400000 else "low"
    lug_boot_size = payload["width"] * payload["length"]

    data = {
        "buying": buying_capacity,
        "maint": get_maintenance_cost_class(buying_capacity, payload['isNew']),
        "doors": 6 if payload["doorAmount"] > 4 else payload['doorAmount'],
        "persons": get_seat_capacity(payload["seatCapacity"]),
        "lug_boot": get_lug_boot_class(lug_boot_size),
        "safety": "high" if payload["isNew"] else "med",
    }

    df = pd.DataFrame([data])

    df_encoded = handle_encoding(df, encoders, CATEGORICAL_FEATURES)

    prediction = model.predict(df_encoded)
    result = encoders['class'].inverse_transform(np.round(prediction).astype(int).flatten())

    return result[0] == "acc"


def get_seat_capacity(seat_capacity):
    if seat_capacity <= 2:
        return 2
    if seat_capacity <= 4:
        return 4
    return 6


def get_maintenance_cost_class(buying_capacity, is_new):
    if buying_capacity == 'high' and is_new:
        return 'high'
    if buying_capacity == 'high' and not is_new or buying_capacity == 'low' and is_new:
        return 'med'
    if buying_capacity == 'low' and not is_new:
        return 'low'


def get_lug_boot_class(lug_boot_size):
    if lug_boot_size < SMALL_LUG_BOOT_THRESHOLD:
        return "small"
    if ((SMALL_LUG_BOOT_THRESHOLD < lug_boot_size < MEDIUM_LUG_BOOT_THRESHOLD) or
            (MEDIUM_LUG_BOOT_THRESHOLD < lug_boot_size < BIG_LUG_BOOT_THRESHOLD)):
        return "med"
    if lug_boot_size > BIG_LUG_BOOT_THRESHOLD:
        return "big"
