model BrowserFlight "Coast from 6 m/s with level hover thrust"
  // An experiment around the SAME Quadrotor equations; no duplicated physics.
  extends Quadrotor(T=m*g, tau=0, vx(start=6));
end BrowserFlight;
