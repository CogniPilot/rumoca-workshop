-- Generated from models/Quadrotor.mo by Rumoca 0.10.2
-- Model SHA256: 3864d44035bd894931586749afc60c33a4190e6810b3b81b69fde9c52fddb56a

-- Real-arithmetic interpretation of the checked scalar Solve program.
-- Floating-point execution, compiler correctness, and this template are outside the proof.
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic

namespace Workshop
noncomputable section

structure State where
  x : ℝ
  z : ℝ
  theta : ℝ
  vx : ℝ
  vz : ℝ
  omega : ℝ

structure Params where
  m : ℝ
  Iyy : ℝ
  g : ℝ
  k_linear : ℝ
  k_quad : ℝ
  damping : ℝ
  eps : ℝ

structure Control where
  T : ℝ
  tau : ℝ

def generatedRhs (_t : ℝ) (s : State) (u : Control) (p : Params) : State :=
  let r0 := s.vx
  let o0 := r0
  let r0 := s.vz
  let o1 := r0
  let r0 := s.omega
  let o2 := r0
  let r0 := u.T
  let r1 := s.theta
  let r2 := Real.sin r1
  let r3 := r0 * r2
  let r4 := p.k_linear
  let r5 := s.vx
  let r6 := r4 * r5
  let r7 := r3 - r6
  let r8 := p.k_quad
  let r9 := s.vx
  let r10 := s.vx
  let r11 := r9 * r10
  let r12 := p.eps
  let r13 := p.eps
  let r14 := r12 * r13
  let r15 := r11 + r14
  let r16 := Real.sqrt r15
  let r17 := r8 * r16
  let r18 := s.vx
  let r19 := r17 * r18
  let r20 := r7 - r19
  let r21 := p.m
  let r22 := r20 / r21
  let o3 := r22
  let r0 := u.T
  let r1 := s.theta
  let r2 := Real.cos r1
  let r3 := r0 * r2
  let r4 := p.m
  let r5 := p.g
  let r6 := r4 * r5
  let r7 := r3 - r6
  let r8 := p.k_linear
  let r9 := s.vz
  let r10 := r8 * r9
  let r11 := r7 - r10
  let r12 := p.k_quad
  let r13 := s.vz
  let r14 := s.vz
  let r15 := r13 * r14
  let r16 := p.eps
  let r17 := p.eps
  let r18 := r16 * r17
  let r19 := r15 + r18
  let r20 := Real.sqrt r19
  let r21 := r12 * r20
  let r22 := s.vz
  let r23 := r21 * r22
  let r24 := r11 - r23
  let r25 := p.m
  let r26 := r24 / r25
  let o4 := r26
  let r0 := u.tau
  let r1 := p.damping
  let r2 := s.omega
  let r3 := r1 * r2
  let r4 := r0 - r3
  let r5 := p.Iyy
  let r6 := r4 / r5
  let o5 := r6
  { x := o0, z := o1, theta := o2, vx := o3, vz := o4, omega := o5 }

end
end Workshop
