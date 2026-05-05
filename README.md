# AuAl2 Code

Code for AuAl2, our VEX High Stakes robot.

 It is more like a working notebook of drivetrain experiments, autonomous ideas, subsystem control, and simulator-side prototyping.

## Contents
- `AuAl2 Drive-Train code base/Vex Brain Sim`
  A full V5 brain-screen field sim with a draggable camera, field rendering, robot physics-ish movement, collision bounds, scoring/state display on the controller, and a hand-built visual model of the field. This is probably the weirdest and coolest file in the repo.

- `AuAl2 Drive-Train code base/States Code/All Programs.v5python`
  The best "big picture" file. It bundles the shared comp code and multiple autonomous routines in one place, with comments explaining the approach.

- `AuAl2 Drive-Train code base/v5 human driver class.v5python`
  Custom driver control code for a 6-motor drivetrain, curved joystick mapping, curvature-drive math, and direct subsystem controls for intake, clamp, doinker, and wall stake.

- `AuAl2 Drive-Train code base/States Code/Rework.v5python`
  A more evolved autonomous structure with reusable `head()` / `circ()` movement primitives, PID-based motion control, and several autonomous routines like `FourRing()`, `GoalRush()`, and `Skills()`.

- `AuAl2 Drive-Train code base/States Code/Pure Pursuit.v5python`
  An attempt at pushing farther into odometry and path-following ideas, including arc-based position updates, waypoint handling, and pursuit-style control experiments.

- `AuAl2 Drive-Train code base/IMU filter.py`
  A homemade dual-IMU fusion idea that biases toward the sensor changing more slowly to smooth heading.

- `AuAl2 Drive-Train code base/PID control.py`
- `AuAl2 Drive-Train code base/Jerk Limited accel.py`
- `AuAl2 Drive-Train code base/2Tracker Odometry.py`
  Small focused prototypes for control theory and drivetrain math: PID, jerk-limited acceleration, and tracking-wheel odometry.

