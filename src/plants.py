import numpy as np

def simulate(Kp, Ki, Kd, setpoint=10.0, t_end=3.0, K=1.0, tau=0.5, dt=0.01,
             umax=12.0, dz=1.5, fric=0.5, q=0.05, noise=0.02, delay=True,
             antiwindup=False, d_tau=0.0, seed=0):
    """Closed-loop simulation of a motor with real-world effects.
    Set umax=np.inf, dz=0, fric=0, q=0, noise=0, delay=False to switch effects off.
    antiwindup=True stops the integral growing while the output is saturated.
    d_tau is the derivative filter time constant in seconds (0 = no filter)."""
    rng = np.random.default_rng(seed)
    n = int(t_end / dt)
    t = np.arange(n) * dt
    y = np.zeros(n)
    u_log = np.zeros(n)
    omega = 0.0
    integral = 0.0
    prev_e = 0.0
    d_filt = 0.0
    u_prev = 0.0
    alpha = d_tau / (d_tau + dt)          # 0 means no filtering

    for k in range(n):
        # sensor: noise, then quantization
        meas = omega + (rng.normal(0, noise) if noise > 0 else 0.0)
        if q > 0:
            meas = np.round(meas / q) * q

        # discrete PID
        e = setpoint - meas
        d_raw = 0.0 if k == 0 else (e - prev_e) / dt
        prev_e = e
        d_filt = alpha * d_filt + (1 - alpha) * d_raw     # low-pass filter on D

        integral_new = integral + e * dt
        u_raw = Kp * e + Ki * integral_new + Kd * d_filt
        u = np.clip(u_raw, -umax, umax)                    # saturation

        # clamping: skip the integral update if clipped AND error pushes deeper
        pushing_deeper = (u != u_raw) and (np.sign(e) == np.sign(u_raw))
        if not (antiwindup and pushing_deeper):
            integral = integral_new
        u_log[k] = u

        # one-sample delay
        u_apply = u_prev if delay else u
        u_prev = u

        # deadband and friction
        if abs(u_apply) < dz:
            u_eff = 0.0
        else:
            u_eff = u_apply - fric * np.sign(u_apply)

        # motor dynamics: 10 Euler sub-steps per sample
        for _ in range(10):
            omega += (-omega + K * u_eff) / tau * (dt / 10)
        y[k] = omega

    return t, y, u_log
