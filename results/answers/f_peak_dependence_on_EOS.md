# What is f_peak and how does it depend on the nuclear EOS?

The peak frequency $f_\mathrm{peak}$ of gravitational wave (GW) signals from core-collapse supernovae (CCSNe) is a characteristic frequency of the postbounce oscillations of the protoneutron star (PNS). It encodes information about the nuclear equation of state (EOS) and the properties of the PNS core.

In the slow rotation regime ($T/|W| \lesssim 0.06$), $f_\mathrm{peak}$ is primarily determined by the PNS dynamical frequency, which scales with the square root of the central density $\rho_c$:

$$
f_\mathrm{peak} \propto \sqrt{G\rho_c}
$$

where $G$ is the gravitational constant. Different EOS lead to different central densities, resulting in variations in $f_\mathrm{peak}$ of approximately 150 Hz in the slow rotation regime [literature/md/richers2017.md:L200-L205 § Equation of State Effects on Gravitational Waves from Rotating Core Collapse].

This dependence is most pronounced in the slow rotation regime, where the EOS effects are parameterized by the PNS central density. When normalized by the dynamical frequency $\sqrt{G\bar{\rho}_c}$, the differences between EOS are drastically reduced, indicating that the effect of the EOS on $f_\mathrm{peak}$ is essentially parameterized by the PNS central density [literature/md/richers2017.md:L200-L205 § Equation of State Effects on Gravitational Waves from Rotating Core Collapse].

In rapidly rotating models ($T/|W| \gtrsim 0.06$), the behavior of $f_\mathrm{peak}$ becomes more complex due to the influence of rotation, and it is described by a different scaling relation [literature/md/abdikamalov_review2022.md:L263 § Review of Gravitational Wave Emission from Core-Collapse Supernovae].

In the context of asteroseismology, the peak frequency of g-modes depends on the gravity at the source, while f-modes depend on the square root of the mean density of the star [literature/md/mezzacappa_zanolin2024.md:L287-L293 § Asteroseismology of Protoneutron Stars in Core-Collapse Supernovae].

## Verification

- `grep -A5 -B5 "f_peak.*EOS\|EOS.*f_peak" literature/md/richers2017.md` — shows that f_peak varies by ~150 Hz between EOS in the slow rotation regime.
- `grep -A5 -B5 "f_peak.*EOS\|EOS.*f_peak" literature/md/dimmelmeier2008.md` — shows that switching from Shen to LS EOS produces a Δf_max = +34 Hz difference.
- `grep -A5 -B5 "f_peak.*EOS\|EOS.*f_peak" literature/md/pastormarcos2024.md` — confirms that f_peak ∝ √(Gρ_c) in the slow rotation regime.
- `grep -A5 -B5 "f_peak.*EOS\|EOS.*f_peak" literature/md/abdikamalov_review2022.md` — shows that f_peak scaling changes in rapid rotation regime.
- `grep -A5 -B5 "f_peak.*EOS\|EOS.*f_peak" literature/md/mezzacappa_zanolin2024.md` — shows the relationship between f_peak and stellar structure for g- and f-modes.