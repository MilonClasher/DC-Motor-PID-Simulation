## Definitions
1. Error: Difference between setpoint (deisred target value) and current state of process variable.
2. Setpoint: The desired target value that the process variable (a controlled variable) is meant to reach and maintain.
3. Closed-loop/Feedback control system: Type of control system that measures actual output and feeds that measurement back to adjust its control action until the output matches the setpoint.
4. Overshoot: When a system's output temporarily rises above its target or final steady-state value before settling.
5. Settling time: Time it takes for a system's output to reach and stay within a specified percentage band of its final steady-state value after a step input is added.
6. Steady-state error: Difference between setpoint and actual output of a stable control system after transient response has died out.
7. Transient response: Temporary change in a control system's output right after a change in input, initial condition or disturbance before it settles into a steady state.
8. Step input: A signal that jumps instantaneously from one constant value to another at a specific time. 
9. Proportional gain (Kp): Scales output to current error for faster response.
10. Integral gain (Ki): Sums past error to remove steady-state error
11. Derivative gain (Kd): Reacts to rate of error change to damp overshoot and oscillation.

## Numbers
01.
P   Kp=1    Ki=0    Kd=0    OS=  0.0%  rise=0.550s  settle=0.980s  sse=0.500
P   Kp=5    Ki=0    Kd=0    OS=  0.0%  rise=0.185s  settle=0.330s  sse=0.167
P   Kp=20   Ki=0    Kd=0    OS=  0.0%  rise=0.050s  settle=0.095s  sse=0.048
PI  Kp=5    Ki=10   Kd=0    OS=  0.0%  rise=0.220s  settle=0.395s  sse=-0.000
PI  Kp=5    Ki=50   Kd=0    OS= 19.4%  rise=0.105s  settle=0.490s  sse=0.000
PI  Kp=5    Ki=100  Kd=0    OS= 30.8%  rise=0.080s  settle=0.550s  sse=0.000
PD  Kp=5    Ki=0    Kd=0    OS=  0.0%  rise=0.185s  settle=0.330s  sse=0.167
PD  Kp=5    Ki=0    Kd=0.1  OS=  0.0%  rise=0.210s  settle=0.370s  sse=0.167
PD  Kp=5    Ki=0    Kd=0.3  OS=  0.0%  rise=0.230s  settle=0.445s  sse=0.167
PID Kp=5    Ki=50   Kd=0    OS= 19.4%  rise=0.105s  settle=0.490s  sse=0.000
PID Kp=5    Ki=50   Kd=0.1  OS= 17.9%  rise=0.130s  settle=0.760s  sse=0.000
PID Kp=5    Ki=50   Kd=0.3  OS= 15.6%  rise=0.155s  settle=0.915s  sse=0.000

02. 
Z-N gains: Kp=12.58, Ki=126.31, Kd=0.313

L estimated: 0.05  (model value 0.05)
T estimated: 0.522  (model value 0.5)

all off                OS=  0.0%  rise=0.210s  settle=0.370s  final=10.00
deadband, dz=11        OS=  2.0%  rise=0.200s  settle=2.990s  final=9.89
P only, no friction    OS=  0.0%  rise=0.180s  settle=0.300s  final=8.33
P only, friction=2     OS=  0.0%  rise=0.180s  settle=0.300s  final=8.00
saturation, umax=12    OS= 14.5%  rise=0.690s  settle=2.700s  final=10.26
high gains, no delay   OS= 10.9%  rise=0.030s  settle=0.240s  final=10.00
high gains, delay      OS= 33.0%  rise=0.010s  settle=0.220s  final=10.00

2. 
Ki=10  no anti-windup  OS= 14.5%  settle=2.70s  final=10.26
Ki=10  clamping        OS=  0.0%  settle=1.60s  final=9.99
Ki=50  no anti-windup  OS= 15.4%  settle=2.97s  final=10.36
Ki=50  clamping        OS=  0.8%  settle=0.86s  final=10.00

## Graph:
1. Motor step response: The motor takes time to reach full speed after switching on. Tau is how long that takes.
2. P only: Like cruise control: the further below target speed, the harder it pushes. The push weakens near the target, so it stops short. Your numbers: gap of 0.500, 0.167, 0.048 at Kp 1, 5, 20.
3. Adding I: The controller remembers the past gap and keeps pushing until the gap is zero. Too much memory overshoots, as in your 30.8% at Ki = 100.
4. Adding D: The controller eases off when it sees the gap closing fast. This trims overshoot a little and slows the response.
5. Ziegler-Nichols: A recipe that turns two measurements of the motor into gains. It is aggressive, so it overshoots more.
6. Deadband (11 V): The motor does not move until the voltage is high enough, so the speed hunts around the target. Settling went from 0.37 s to 2.99 s.
7. Friction (P only): Friction steals a constant amount of push, so the motor ends at 8.00 instead of 8.33.
8. Delay: Reacting late makes the controller swing past the target. Overshoot rose from 10.9% to 33.0%.
9. Anti-windup: While the controller is maxed out, its memory keeps piling up, then releases as overshoot. Clamping stops the pile-up.

1. Motor step response

I switched the motor on with a sudden full command.
Its speed rose gradually and reached 63% of its final value after 0.5 s.
The motor has inertia, so it cannot change speed instantly. Tau is the size of that lag.

2. P only

I raised Kp from 1 to 5 to 20.
Rise time fell from 0.550 s to 0.050 s, and the final gap to the target fell from 0.500 to 0.167 to 0.048 but never reached zero.
The push is proportional to the gap, so it fades as the gap closes and the motor stops just short of the target.

3. Adding I

I added Ki and raised it from 10 to 50 to 100.
The final gap became zero, and overshoot went from 0% to 19.4% to 30.8%.
The controller stores the past gap and keeps pushing until the gap is zero. A large stored amount pushes the motor past the target before it unwinds.

4. Adding D

I raised Kd from 0 to 0.1 to 0.3 in the PID case.
Overshoot fell from 19.4% to 15.6%, and settling time grew from 0.490 s to 0.915 s.
Kd reacts to how fast the gap is closing and eases off the push. That reduces the swing past the target, and it also slows the approach.

5. Ziegler-Nichols

Instead of choosing gains by hand, I measured two properties of the motor (its delay and its response time) and let the recipe compute the gains.
It rose fastest, in 0.060 s against 0.096 s, and overshot more, at 79.1% against 4.1%.
The recipe aims for a fast response and accepts a swing past the target to get it.

6. Deadband (11 V)

I raised the dead zone from 1.5 V to 11 V.
Settling time went from 0.37 s to 2.99 s, with 2.0% overshoot, and the speed hunted around the target.
The motor ignores any command below 11 V, so the controller must build up a large push before anything moves. Then the motor jumps past the target, and the cycle repeats.

7. Friction (P only)

I raised friction from 0 to 2, with a P-only controller.
The final speed fell from 8.33 to 8.00.
Friction takes away a constant amount of push. A P-only controller has no memory to make up the loss, so the gap stays.

8. Delay

I added a one-sample delay (10 ms) with high gains, Kp = 20 and Ki = 200.
Overshoot rose from 10.9% to 33.0%.
The controller acts on old information. It keeps pushing after the motor has already reached the target, so the motor swings past it.

9. Anti-windup

I limited the output to 12 V and turned on clamping, which stops the stored push from growing while the output is maxed out.
Overshoot fell from 14.5% to 0.0%, and settling time from 2.70 s to 1.60 s.
Without clamping, the stored push keeps growing while the controller is maxed out, and it releases as overshoot once the motor catches up.