// GENERATED bundle; physics source: models/Quadrotor.mo
// Source SHA256: 3864d44035bd894931586749afc60c33a4190e6810b3b81b69fde9c52fddb56a
// Paste all text in the playground. Create Scenario; set Model name BrowserFlight, end time 8 s; Run Simulation.
model Quadrotor "Planar quadrotor: one physics source for JAX and CasADi"
  // World x is right, z is up. Positive theta tilts thrust toward +x.
  // Aggregate thrust/torque omit rotor dynamics, yaw, roll, and ground contact.
  parameter Real m(unit="kg") = 1.2 "Mass";
  parameter Real Iyy(unit="kg.m2") = 0.025 "Pitch inertia";
  parameter Real g(unit="m/s2") = 9.81 "Gravity";
  parameter Real k_linear(unit="N.s/m") = 0.18 "Linear world-axis drag";
  parameter Real k_quad(unit="N.s2/m2") = 0.0 "EXERCISE: change to 0.08";
  parameter Real damping(unit="N.m.s/rad") = 0.04 "Pitch-rate damping";
  parameter Real eps(unit="m/s") = 0.01 "Smooth speed magnitude near zero";

  input Real T(unit="N", start=11.772) "Total thrust; hover at m*g";
  input Real tau(unit="N.m", start=0) "Pitch torque";
  Real x(unit="m", start=0, fixed=true) "Horizontal position";
  Real z(unit="m", start=1, fixed=true) "Altitude";
  Real theta(unit="rad", start=0, fixed=true) "Pitch, zero at hover";
  Real vx(unit="m/s", start=0, fixed=true) "Horizontal velocity";
  Real vz(unit="m/s", start=0, fixed=true) "Vertical velocity";
  Real omega(unit="rad/s", start=0, fixed=true) "Pitch rate";
equation
  der(x) = vx;
  der(z) = vz;
  der(theta) = omega;
  // Force = thrust projection + linear drag + smooth quadratic drag.
  der(vx) = (T*sin(theta) - k_linear*vx
             - k_quad*sqrt(vx*vx + eps*eps)*vx)/m;
  der(vz) = (T*cos(theta) - m*g - k_linear*vz
             - k_quad*sqrt(vz*vz + eps*eps)*vz)/m;
  der(omega) = (tau - damping*omega)/Iyy;
end Quadrotor;

model BrowserFlight "Coast from 6 m/s with level hover thrust"
  // An experiment around the SAME Quadrotor equations; no duplicated physics.
  extends Quadrotor(T=m*g, tau=0, vx(start=6));
end BrowserFlight;
