# !/usr/bin/env python3
# Plot Dalitz plot from ROOT tree.
# Usage:
#   python plot_dalitz.py input.root --type dalitz
#   python plot_dalitz.py input.root --type phsp

import argparse
import numpy as np
import matplotlib.pyplot as plt
import uproot

def parse_args():

    parser = argparse.ArgumentParser(description="Dalitz plot from ROOT tree.")
    parser.add_argument("input", help="Input ROOT file")
    parser.add_argument(
        "--type", dest="plot_type", choices=["dalitz", "phsp"], default="dalitz",
        help="Plot type: 'dalitz' -> dalitz_dalitz.png, 'phsp' -> dalitz-phsp.png"
    )
    return parser.parse_args()

def invariant_mass2(px1, py1, pz1, e1, px2, py2, pz2, e2):
    """Compute M^2 of the sum of two 4-vectors."""
    e  = e1  + e2
    px = px1 + px2
    py = py1 + py2
    pz = pz1 + pz2
    return e**2 - px**2 - py**2 - pz**2

args = parse_args()

outfile = "out/dalitz_dalitz.png" if args.plot_type == "dalitz" else "out/dalitz_phsp.png"
print(f"[INFO] Reading from {args.input} and writing to {outfile}.")

# Read tree with uproot.
with uproot.open(args.input) as f:
    tree = f["tree"]
    branches = tree.arrays(
        ["mc_pid", "mc_px", "mc_py", "mc_pz", "mc_e"],
        library="np"
    )

# Define variables for m^2(gamma, mu+) and m^2(mu+, mu-).
# mc contains all MC particles, including the eta and its daughters. We need to
# loop over events and find the gamma, mu+, and mu- for each event to compute
# the invariant masses.
pids = branches["mc_pid"]
pxs = branches["mc_px"]
pys = branches["mc_py"]
pzs = branches["mc_pz"]
es = branches["mc_e"]

m12s = []
m23s = []

for i in range(len(pids)):
    p1 = p2 = p3 = None  # gamma, mu+, mu-

    for j, pid in enumerate(pids[i]):
        # Convert from MeV to GeV
        px = pxs[i][j] / 1000.
        py = pys[i][j] / 1000.
        pz = pzs[i][j] / 1000.
        e = es[i][j] / 1000.

        if pid == 22: p1 = (px, py, pz, e)
        elif pid == -13: p2 = (px, py, pz, e)
        elif pid == 13: p3 = (px, py, pz, e)

    if None not in (p1, p2, p3):
        m12 = invariant_mass2(*p1, *p2)   # m^2(gamma, mu+)
        m23 = invariant_mass2(*p2, *p3)   # m^2(mu+, mu-)
        m12s.append(m12)
        m23s.append(m23)

m12s = np.array(m12s)
m23s = np.array(m23s)

print(f"m12 range: [{m12s.min():.4f}, {m12s.max():.4f}]")
print(f"m23 range: [{m23s.min():.4f}, {m23s.max():.4f}]")

# Plot.
fig, ax = plt.subplots(figsize=(7, 6))
h, xedges, yedges = np.histogram2d(m12s, m23s, bins=100,
                                    range=[[0, 0.20], [0, 0.30]])
# Mask empty bins so they appear white.
# Also mask bins with very low entries to reduce noise (which is likely caused
# by some errors anyway).
# Keep in mind that this will include some background (error) particles that
# are correctly pid identified but are not from eta candidate.
h_masked = np.ma.masked_where(h <= 1, h)

mesh = ax.pcolormesh(xedges, yedges, h_masked.T, cmap="viridis")
fig.colorbar(mesh, ax=ax, label="Entries")

ax.set_xlabel(r"$m^2_{\gamma,\mu^+}$ [GeV$^2$]")
ax.set_ylabel(r"$m^2_{\mu^+,\mu^-}$ [GeV$^2$]")
ax.set_title(r"$\eta \to \mu\mu\gamma$ Dalitz plot")

ax.text(0.025, 0.95, "Requires > 1 entry/bin to show",
        transform=ax.transAxes,
        verticalalignment='top',
)

fig.tight_layout()
fig.savefig(outfile, dpi=150)
print(f"Saved: {outfile}")
