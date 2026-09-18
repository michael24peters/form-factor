"""
plot_style.py

Shared plot style for this notebook's figures: colorblind-safe palette,
axis chrome, and font setup. Trimmed down from the fitting-code version of
this module to just the pieces relevant here (no stats-box/margin/save
helpers, since this isn't a fit-result-JSON-driven workflow).
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Shared fit-plot palette. primary/secondary/tertiary validated pairwise
# colorblind-safe (dataviz skill's validate_palette.js, all-pairs, light mode).
COLORS = {
    'data':       '#000000',
    'primary':    '#2a78d6',
    'secondary':  '#1baf7a',
    'tertiary':   '#eb6834',
    'reference':  '#898781',
}

def style_axes(ax, minor_y=True, n_minor=None, integer_y=False):
    """Inward, mirrored major+minor ticks on all four sides, and heavier
    spines -- shared chrome for every panel of a fit plot. Set minor_y=False
    to omit minor ticks on the y-axis only (e.g. the pull panel's integer
    scale has no need for them). n_minor caps the minor-tick subdivisions per
    major interval on both axes (matplotlib's automatic default is denser).
    integer_y restricts y-axis major ticks to whole numbers, dropping the
    decimal tick labels."""
    ax.minorticks_on()
    if not minor_y:
        ax.yaxis.set_minor_locator(mticker.NullLocator())
    elif n_minor is not None:
        ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(n_minor))
        ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(n_minor))
    if integer_y:
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.tick_params(which='major', direction='in', top=True, right=True, width=1.6, length=7.0)
    ax.tick_params(which='minor', direction='in', top=True, right=True, width=1.2, length=4.0)
    for spine in ax.spines.values():
        spine.set_linewidth(2.0)

def apply_font():
    """Set up the Inter font (falling back to the default sans-serif if it's
    not installed) and the shared figure/savefig DPI for all plots."""
    family = 'Inter'
    try:
        import matplotlib.font_manager as fm
        fm.findfont('Inter', fallback_to_default=False)
    except Exception:
        print('[INFO] Inter font not found, falling back to default sans-serif.')
        family = 'sans-serif'
    plt.rcParams['font.family'] = family
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
