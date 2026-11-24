import numpy as np

def simulate(Kp, Ki, Kd, setpoint=10.0, t_end=3.0, K=1.0, tau=0.5, dt=0.01,
             umax=12.0, dz=1.5, fric=0.5, q=0.05, noise=0.02, delay=True, seed=0):
    """Closed-loop simulation of a motor with real-world effects.
    Set umax=np.inf, dz=0, fric=0, q=0, noise=0, delay=False to switch effects off."""
    rng = np.random.default_rng(seed)
    n = int(t_end / dt)
    t = np.arange(n) * dt
    y = np.zeros(n)                 # true motor speed
    u_log = np.zeros(n)             # controller output
    omega = 0.0                     # motor speed state
    integral = 0.0
    prev_e = 0.0
    u_prev = 0.0

    for k in range(n):
        # --- sensor: noise, then quantization (smallest step the encoder can see)
        meas = omega + (rng.normal(0, noise) if noise > 0 else 0.0)
        if q > 0:
            meas = np.round(meas / q) * q

        # --- controller (discrete PID)
        e = setpoint - meas
        integral += e * dt
        d = 0.0 if k == 0 else (e - prev_e) / dt
        prev_e = e
        u = Kp * e + Ki * integral + Kd * d
        u = np.clip(u, -umax, umax)             # saturation
        u_log[k] = u

        # --- one-sample delay between controller and motor
        u_apply = u_prev if delay else u
        u_prev = u

        # --- deadband and friction (friction simplified as lost drive)
        if abs(u_apply) < dz:
            u_eff = 0.0
        else:
            u_eff = u_apply - fric * np.sign(u_apply)

        # --- motor dynamics: Euler integration, 10 sub-steps of 1 ms per sample
        for _ in range(10):
            omega += (-omega + K * u_eff) / tau * (dt / 10)
        y[k] = omega

    return t, y, u_log
