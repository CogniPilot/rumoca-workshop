"""Generate original diagrams and legible presentation plots from real results."""
from common import *


def build_assets():
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Arc
    import qrcode
    from fit_drag_jax import load_flights
    dest = ROOT/"slides/assets"
    dest.mkdir(exist_ok=True)
    ink, teal, gold, orange = "#131d2a", "#007e87", "#cfb991", "#b65131"
    plt.rcParams.update({"font.size": 19, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 160,
                         "text.color": ink, "axes.labelcolor": ink})
    def save(fig, name):
        fig.savefig(dest/name, facecolor="white", bbox_inches="tight", pad_inches=.18)
        plt.close(fig)
    def canvas(height=4):
        fig, ax = plt.subplots(figsize=(12, height))
        ax.set(xlim=(0, 12), ylim=(0, height))
        ax.axis("off")
        return fig, ax
    def box(ax, x, y, w, h, text, color="#e7f2f3", size=22):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                  facecolor=color, edgecolor="none"))
        ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=size)
    def arrow(ax, a, b):
        ax.annotate("", xy=b, xytext=a, arrowprops={"arrowstyle": "->", "lw": 2.5, "color": teal})
    fig, ax = canvas(4)
    box(ax, .2, 1.6, 2.5, 1.2, "Modelica\nQuadrotor.mo", "#f0e7d5")
    box(ax, 4., 1.6, 2.4, 1.2, "Rumoca\ncompiler")
    box(ax, 8.1, 2.55, 3.3, 1.05, "JAX\nidentify drag")
    box(ax, 8.1, .5, 3.3, 1.05, "CasADi\noptimize flight")
    arrow(ax, (2.9, 2.2), (3.8, 2.2))
    arrow(ax, (6.6, 2.3), (7.9, 3.05))
    arrow(ax, (6.6, 2.1), (7.9, 1.05))
    ax.text(1.45, .8, "VS Code + LSP\nauthoring", ha="center", fontsize=19)
    ax.text(5.2, .6, "Browser/WASM\nmodeling + simulation", ha="center", fontsize=19)
    ax.text(6., 3.75, "Same declared equations; separate numerical workflows", ha="center", fontsize=20)
    save(fig, "architecture.png")
    fig, ax = canvas(4.6)
    ax.set_aspect("equal")
    cx, cz, angle = 6., 2.0, np.pi/6
    dx, dz = 1.5*np.cos(angle), -1.5*np.sin(angle)
    ax.plot([cx-dx, cx+dx], [cz-dz, cz+dz], color=ink, lw=11, solid_capstyle="round")
    rotor_dx, rotor_dz = .5*np.cos(angle), -.5*np.sin(angle)
    for xx, zz in [(cx-dx, cz-dz), (cx+dx, cz+dz)]:
        rotor_x, rotor_z = xx+.18*np.sin(angle), zz+.18*np.cos(angle)
        ax.plot([xx, rotor_x], [zz, rotor_z], lw=5, color=ink)
        ax.plot([rotor_x-rotor_dx, rotor_x+rotor_dx],
                [rotor_z-rotor_dz, rotor_z+rotor_dz], lw=7, color=gold)
    arrow(ax, (cx, cz), (cx+2.4*np.sin(angle), cz+2.4*np.cos(angle)))
    ax.text(cx+1.5, cz+1.6, "T", color=teal, fontsize=30)
    ax.annotate("", xy=(cx, .45), xytext=(cx, cz),
                arrowprops={"arrowstyle": "->", "lw": 3, "color": orange})
    ax.text(cx+.2, .75, "mg", color=orange, fontsize=26)
    ax.plot([cx, cx], [cz, cz+1.25], "--", color="#888888")
    ax.add_patch(Arc((cx, cz), 1.8, 1.8, theta1=60, theta2=90, lw=2, color=ink))
    ax.text(cx+.35, cz+1., r"$\theta$", fontsize=24)
    arrow(ax, (1., .7), (3.2, .7)); arrow(ax, (1., .7), (1., 3.2))
    ax.text(3.3, .65, "x", fontsize=25); ax.text(.9, 3.4, "z", fontsize=25)
    ax.text(9.4, 2.4, "Thrust toward +x\nwhen pitch is positive", ha="center", fontsize=20)
    ax.text(6, 4.4, "Planar motion; ideal aggregate thrust and torque", ha="center", fontsize=20)
    save(fig, "quadrotor.png")
    fig, ax = canvas(3.3)
    ax.text(6, 2.4, r"$D(v)=-k_{\rm linear}v-k_{\rm quad}\sqrt{v^2+\epsilon^2}\,v$",
            ha="center", fontsize=35)
    ax.text(6, 1.3, "Linear: N s/m     Quadratic: N s²/m²     ε = 0.01 m/s", ha="center", fontsize=23)
    ax.text(6, .3, "Nonnegative coefficients ⇒ drag opposes motion", ha="center", fontsize=24, color=teal)
    save(fig, "drag-law.png")
    _, export = compile_model()
    rollout = jax_rollout(export)
    x0, u = maneuver(export, vx0=6.)
    fig, ax = plt.subplots(figsize=(12, 4.2), layout="constrained")
    t = np.arange(len(u)+1)*DT
    for kq, label, color in [(0., "linear only", teal), (.08, "linear + quadratic", orange)]:
        ys = np.array(rollout(parameters(export, k_quad=kq), x0, u))
        ax.plot(t, ys[:, 0], lw=3.5, label=label, color=color)
    ax.set(xlabel="Time [s]", ylabel="Horizontal distance [m]")
    ax.legend(fontsize=20); ax.grid(alpha=.2)
    save(fig, "simulation-hero.png")
    flights = load_flights(ROOT/"data/noisy_flight.csv")
    fig, ax = plt.subplots(figsize=(12, 4.1), layout="constrained")
    for f, color in zip(flights, [teal, gold, orange, "#345fb5"]):
        label = f"Flight {f['id']} · {f['split']}"
        ax.plot(f["t"], f["y"][:, 3], color=color, lw=2.7, label=label)
    ax.set(xlabel="Time [s]", ylabel="Measured horizontal speed [m/s]")
    ax.legend(ncol=2, fontsize=16); ax.grid(alpha=.2)
    save(fig, "data-hero.png")
    fig, ax = canvas(4.2)
    labels = ["Generated RHS\nModelica → JAX", "RK4 rollout\npositive drag", "Data residuals\nscaled by noise", "JAX gradients\nL-BFGS-B"]
    for i, label in enumerate(labels):
        box(ax, .15+i*3., 2.3, 2.55, 1.15, label, size=20)
        if i < 3: arrow(ax, (2.78+i*3, 2.87), (3.02+i*3, 2.87))
    ax.text(6, 1.25, r"$L=\mathrm{mean}\left[\left(\frac{\widehat y-y}{\sigma}\right)^2\right]$",
            ha="center", fontsize=30)
    ax.text(6, .3, r"$k_l/k_{l,\rm ref}=e^a,\quad k_q/k_{q,\rm ref}=e^b$", ha="center", fontsize=27)
    save(fig, "fit-workflow.png")
    fit = json.loads((ROOT/"results/reference/fit_drag.json").read_text())
    assert fit["source_sha256"] == source_hash()
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.3), layout="constrained")
    for ax, f in zip(axs, [flights[2], flights[3]]):
        ax.scatter(f["t"][::3], f["y"][::3, 3], s=18, color="#555555", alpha=.6, label="noisy measurements")
        for coeffs, label, color, ls in [(fit["initial_drag"], "before fit", teal, "--"), (fit["drag"], "after fit", orange, "-")]:
            ys = np.array(rollout(parameters(export, **coeffs), f["y"][0], f["u"]))
            ax.plot(f["t"], ys[:, 3], lw=3, ls=ls, color=color, label=label)
        ax.set(xlabel="Time [s]", ylabel="Horizontal speed [m/s]", title=f["split"].capitalize())
        ax.grid(alpha=.2)
    axs[0].legend(fontsize=14)
    save(fig, "fit-hero.png")
    fig, ax = canvas(4.5)
    box(ax, .2, 2.8, 3.1, 1., "Start hover\n(0, 1) m", "#f0e7d5")
    box(ax, 8.3, 2.8, 3.1, 1., "Target hover\n(4, 2) m", "#e7f2f3")
    arrow(ax, (3.6, 3.3), (8., 3.3))
    ax.text(5.8, 3.65, "6 s", ha="center", fontsize=24)
    ax.text(6, 2., "T: 0–20 N     τ: ±0.35 N m", ha="center", fontsize=24)
    ax.text(6, 1.1, "z: 0.25–4 m     |θ| ≤ 0.55 rad", ha="center", fontsize=24)
    ax.text(6, .25, "60 shooting intervals · node pitch margin · independent reintegration", ha="center", fontsize=19)
    save(fig, "control-problem.png")
    with np.load(ROOT/"results/reference/trajectory.npz") as tr:
        xs, us, dt = tr["X"], tr["U"], float(tr["dt"])
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.3), layout="constrained")
    axs[0].plot(xs[0], xs[1], lw=3.5, color=teal)
    axs[0].scatter([0, 4], [1, 2], s=90, color=orange)
    axs[0].set(xlabel="Horizontal position [m]", ylabel="Altitude [m]", title="Move between hovers")
    tt = np.arange(xs.shape[1])*dt
    axs[1].plot(tt, xs[2], lw=3, color=teal, label="pitch")
    for limit in [-.55, .55]: axs[1].axhline(limit, color=orange, ls="--")
    axs[1].set(xlabel="Time [s]", ylabel="Pitch [rad]", title="Tilt, then brake")
    axs[1].legend(fontsize=17)
    for ax in axs: ax.grid(alpha=.2)
    save(fig, "control-hero.png")
    fig, ax = canvas(3.7)
    labels = ["Declared\nphysics", "Identification\n+ control", "SIL / BIL\nupstream tools", "Aircraft tests\nPURT"]
    for i, label in enumerate(labels):
        box(ax, .15+i*3., 1.5, 2.55, 1.15, label, size=21)
        if i < 3: arrow(ax, (2.78+i*3, 2.07), (3.02+i*3, 2.07))
    ax.annotate("", xy=(.8, 1.2), xytext=(11., 1.2), arrowprops={"arrowstyle": "->", "lw": 2, "connectionstyle": "arc3,rad=-.08", "color": gold})
    ax.text(6, .25, "Measure discrepancies. Improve the model and experiment.", ha="center", fontsize=22)
    save(fig, "research-loop.png")
    qrcode.make("https://github.com/CogniPilot/rumoca_workshop_amc2026").save(dest/"repo-qr.png")
    qrcode.make("https://pylon-racing.geddes.rcac.purdue.edu/").save(dest/"pylon-qr.png")
    qrcode.make("https://github.com/CogniPilot/rumoca_workshop_amc2026/blob/main/COMMUNITY.md").save(dest/"community-qr.png")


if __name__ == "__main__":
    build_assets()
