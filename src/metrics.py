import numpy as np

def step_metrics(t, y, setpoint=1.0):
    t = np.asarray(t)
    y = np.asarray(y)
    y_final = y[-1]                                   # value the response settles to

    overshoot = max(0.0, (y.max() - y_final) / abs(y_final) * 100)

    i10 = np.argmax(y >= 0.1 * y_final)               # first index above 10%
    i90 = np.argmax(y >= 0.9 * y_final)               # first index above 90%
    rise_time = t[i90] - t[i10]

    outside = np.where(np.abs(y - y_final) > 0.02 * abs(y_final))[0]
    if len(outside) == 0:
        settling_time = 0.0
    elif outside[-1] == len(t) - 1:
        settling_time = np.nan                        # never settled in this window
    else:
        settling_time = t[outside[-1] + 1]            # last time outside the 2% band

    return {"overshoot": overshoot,
            "rise_time": rise_time,
            "settling_time": settling_time,
            "sse": setpoint - y_final}                # steady-state error
