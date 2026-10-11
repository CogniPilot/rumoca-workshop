import Generated

/-!
Scoped exact-real proofs for the workshop's generated quadrotor RHS.
These are mathematical invariants, not a certification of a flight controller,
floating-point integrator, parameter fit, NLP global optimum, or Rumoca itself.
-/

namespace Workshop
noncomputable section

def drag (kl kq eps v : ℝ) : ℝ :=
  -kl * v - kq * Real.sqrt (v*v + eps*eps) * v

def physicsRhs (s : State) (u : Control) (p : Params) : State :=
  { x := s.vx, z := s.vz, theta := s.omega,
    vx := (u.T * Real.sin s.theta + drag p.k_linear p.k_quad p.eps s.vx) / p.m,
    vz := (u.T * Real.cos s.theta - p.m*p.g + drag p.k_linear p.k_quad p.eps s.vz) / p.m,
    omega := (u.tau - p.damping*s.omega) / p.Iyy }

/-- The actual exported Solve RHS equals the displayed workshop equations. -/
theorem generated_matches_physics (t : ℝ) (s : State) (u : Control) (p : Params) :
    generatedRhs t s u p = physicsRhs s u p := by
  cases s
  simp [generatedRhs, physicsRhs, drag, sub_eq_add_neg, add_assoc]

/-- Drag is zero at zero velocity, despite smoothing. -/
theorem drag_zero (kl kq eps : ℝ) : drag kl kq eps 0 = 0 := by
  simp [drag]

/-- Drag is odd: reversing velocity reverses the force. -/
theorem drag_odd (kl kq eps v : ℝ) : drag kl kq eps (-v) = -drag kl kq eps v := by
  simp only [drag, neg_mul_neg]
  ring

/-- Drag power has the expected nonpositive quadratic form. -/
theorem drag_power (kl kq eps v : ℝ) :
    v * drag kl kq eps v = -(kl*v^2 + kq*Real.sqrt (v*v+eps*eps)*v^2) := by
  unfold drag
  ring

/-- Nonnegative coefficients guarantee that drag never injects energy. -/
theorem drag_dissipative (kl kq eps v : ℝ) (hl : 0 ≤ kl) (hq : 0 ≤ kq) :
    v * drag kl kq eps v ≤ 0 := by
  rw [drag_power]
  have h : 0 ≤ kl*v^2 + kq*Real.sqrt (v*v+eps*eps)*v^2 := by positivity
  linarith

/-- Smoothing with positive epsilon avoids the square-root singularity. -/
theorem smooth_magnitude_positive (eps v : ℝ) (he : 0 < eps) :
    0 < Real.sqrt (v*v + eps*eps) := by
  apply Real.sqrt_pos.2
  nlinarith [sq_nonneg v, sq_pos_of_pos he]

/-- The regularized drag has a derivative at every real speed. -/
theorem drag_differentiable (kl kq eps : ℝ) (he : 0 < eps) :
    Differentiable ℝ (drag kl kq eps) := by
  intro v
  have hs : DifferentiableAt ℝ (fun w : ℝ => Real.sqrt (w*w + eps*eps)) v := by
    apply DifferentiableAt.sqrt
    · fun_prop
    · nlinarith [sq_nonneg v, sq_pos_of_pos he]
  unfold drag
  exact ((differentiableAt_const (-kl)).mul differentiableAt_id).sub
    (((differentiableAt_const kq).mul hs).mul differentiableAt_id)

/-- Ideal nonzero-speed force observations yield the linear regression row. -/
theorem normalized_drag (kl kq eps v : ℝ) (hv : v ≠ 0) :
    -drag kl kq eps v / v = kl + kq*Real.sqrt (v*v+eps*eps) := by
  unfold drag
  field_simp [hv]
  ring

/-- The illustrative left/right rotor-pair allocation reconstructs thrust/torque. -/
theorem rotor_allocation (T tau arm : ℝ) (ha : arm ≠ 0) :
    (T+tau/arm)/2 + (T-tau/arm)/2 = T ∧
    arm*((T+tau/arm)/2 - (T-tau/arm)/2) = tau := by
  constructor
  · ring
  · field_simp [ha]
    ring

/-- Thrust projection preserves force magnitude for every pitch angle. -/
theorem thrust_projection_norm (T theta : ℝ) :
    (T*Real.sin theta)^2 + (T*Real.cos theta)^2 = T^2 := by
  calc
    _ = T^2 * ((Real.sin theta)^2 + (Real.cos theta)^2) := by ring
    _ = T^2 := by rw [Real.sin_sq_add_cos_sq]; ring

/-- T=m*g, zero tilt/rates/velocities is an equilibrium at any position. -/
theorem hover_equilibrium (t x z : ℝ) (p : Params) :
    generatedRhs t ⟨x,z,0,0,0,0⟩ ⟨p.m*p.g,0⟩ p = ⟨0,0,0,0,0,0⟩ := by
  rw [generated_matches_physics]
  simp [physicsRhs, drag]

def energyRate (s r : State) (p : Params) : ℝ :=
  p.m * (s.vx*r.vx + s.vz*r.vz) + p.m*p.g*r.z + p.Iyy*s.omega*r.omega

/-- Chain-rule energy rate: thrust/torque input power minus drag/damping. -/
theorem mechanical_energy_balance (t : ℝ) (s : State) (u : Control) (p : Params)
    (hm : p.m ≠ 0) (hI : p.Iyy ≠ 0) :
    energyRate s (generatedRhs t s u p) p =
      u.T*(s.vx*Real.sin s.theta + s.vz*Real.cos s.theta) + u.tau*s.omega
      + s.vx*drag p.k_linear p.k_quad p.eps s.vx
      + s.vz*drag p.k_linear p.k_quad p.eps s.vz - p.damping*s.omega^2 := by
  rw [generated_matches_physics]
  unfold energyRate physicsRhs
  dsimp
  field_simp [hm, hI]
  ring

/-- With controls off, total mechanical energy cannot increase. -/
theorem unforced_energy_dissipative (t : ℝ) (s : State) (p : Params)
    (hm : p.m ≠ 0) (hI : p.Iyy ≠ 0)
    (hl : 0 ≤ p.k_linear) (hq : 0 ≤ p.k_quad) (hd : 0 ≤ p.damping) :
    energyRate s (generatedRhs t s ⟨0,0⟩ p) p ≤ 0 := by
  rw [mechanical_energy_balance t s ⟨0,0⟩ p hm hI]
  dsimp
  have hx := drag_dissipative p.k_linear p.k_quad p.eps s.vx hl hq
  have hz := drag_dissipative p.k_linear p.k_quad p.eps s.vz hl hq
  have hw : 0 ≤ p.damping*s.omega^2 := by positivity
  nlinarith

/-- Ideal force samples at two distinct smooth speed magnitudes separate kl/kq.
This is an algebraic excitation result, not a noisy-data confidence theorem. -/
theorem two_speed_coefficients_unique (a b kl₁ kq₁ kl₂ kq₂ : ℝ)
    (hab : a ≠ b)
    (ha : kl₁ + kq₁*a = kl₂ + kq₂*a)
    (hb : kl₁ + kq₁*b = kl₂ + kq₂*b) :
    kl₁ = kl₂ ∧ kq₁ = kq₂ := by
  have h : (kq₁-kq₂)*(a-b) = 0 := by nlinarith [ha, hb]
  have hq : kq₁ = kq₂ := by
    rcases mul_eq_zero.mp h with hq | hbad
    · linarith
    · exact False.elim (hab (by linarith))
  constructor
  · rw [hq] at ha
    linarith
  · exact hq

/-- Positive parameterization used by the fitting script. -/
theorem log_parameters_positive (a b : ℝ) : 0 < Real.exp a ∧ 0 < Real.exp b := by
  exact ⟨Real.exp_pos a, Real.exp_pos b⟩

end
end Workshop

#print axioms Workshop.generated_matches_physics
#print axioms Workshop.drag_dissipative
#print axioms Workshop.drag_differentiable
#print axioms Workshop.normalized_drag
#print axioms Workshop.rotor_allocation
#print axioms Workshop.mechanical_energy_balance
#print axioms Workshop.unforced_energy_dissipative
#print axioms Workshop.two_speed_coefficients_unique
