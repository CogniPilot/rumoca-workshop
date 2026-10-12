model HoverController "Fixed-sample altitude controller for the workshop vehicle"
  constant Real samplePeriod(unit="s") = 0.01 "100 Hz controller tick";
  parameter Real m(unit="kg") = 1.2;
  parameter Real g(unit="m/s2") = 9.81;
  parameter Real kp(unit="N/m") = 2.0 "Altitude feedback";
  parameter Real kd(unit="N.s/m") = 1.0 "Vertical-speed feedback";
  parameter Real minThrust(unit="N") = 0.2;
  parameter Real maxThrust(unit="N") = 25.0;
  input Real z_ref(unit="m", start=1.0);
  input Real z(unit="m", start=1.0);
  input Real vz(unit="m/s", start=0.0);
  discrete output Real T(unit="N", start=11.772);
equation
  when sample(0.0, samplePeriod) then
    T = min(maxThrust, max(minThrust, m*g + kp*(z_ref-z) - kd*vz));
  end when;
end HoverController;
