---
key: bag2022_rotation
arxiv: '2110.00486'
title: A novel approach for calculating galaxy rotation curves using spaxel cross-correlation
  and iterative smoothing
authors:
- Satadru Bag
- Arman Shafieloo
- Rory Smith
- Haeun Chung
- Eric V. Linder
- Changbom Park
- Y. Sultan Abylkairov
- Khalykbek Yelshibekov
arxiv_version: 2110.00486v2
method: latex
fetched: '2026-11-01'
---

# A novel approach for calculating galaxy rotation curves using spaxel cross-correlation and iterative smoothing

## Abstract

Precise measurements of the internal dynamics of galaxies have proven of great importance for understanding the internal dark matter distribution of galaxies. We present a novel method for measuring the line-of-sight (LOS) velocities across the face of galaxies by cross-correlation of spectral pixels (spaxels) and an iterative method of smoothing. On simulated data the method can accurately recover the input LOS velocities for different types of spectra (absorption line dominated, emission line dominated, and differing shapes of the continuum), and can handle stellar population radial gradients. Most important of all, it continues to provide reliable measurements of LOS velocities with reasonable uncertainties even when the spectra are very low signal-to-noise (approaching $\sim 1$), which is a challenge for traditional template-fitting approaches. We apply our method to data from a real MaNGA galaxy as a demonstration and find promising results with good precision. This novel approach can be complementary to existing methods primarily based on template fitting.

<span id="firstpage" label="firstpage"></span>

<div class="keywords">

Galaxy: kinematics and dynamics – methods: statistical – methods: data analysis

</div>

# Introduction

The importance of measuring the line-of-sight velocities in astronomy cannot be overstated since they shed light on several key questions in cosmology and astrophysics pertaining to structure formation, galaxy dynamics in clusters (that first revealed the existence of dark matter halos ), distance measures, as well as internal galaxy (and globular cluster) dynamics. In particular, the internal dynamics of galaxies has drawn major amount of interests for decades as this is a fundamental quantity, a part of the empirical scaling properties that almost all galaxies follow, such as the Tully-Fisher (Luminosity vs rotational velocity) , Faber-Jackson (Luminosity vs velocity dispersion) , Fundamental plane (Luminosity vs $R_{\rm eff}$ vs velocity dispersion) . Furthermore, if baryons are in virial equilibrium with the galaxy’s total potential, the dynamics can be used to measure the total mass of the system (the dynamical mass) and the mass-distribution ; see for a review. This is what historically first revealed that dark matter dominates in the outskirts of galaxies . One can also measure the dynamics of baryons that are not in equilibrium, e.g., gas outflows . Therefore, the precise measurement of the internal dynamics of galaxies remains as one of the most important aspects of studying galaxy evolution.

Line-of-sight velocities of baryons are typically measured by Doppler shift of lines in the spectra. For atomic gas the primary line of interest was the 21cm line emission . For stellar components, and ionised gas, one can consider their spectral lines (H$\alpha$ and NII are especially bright lines in the optical part of the spectrum). Traditionally this was done with long slit spectroscopy, resulting in a 1D rotation curve . Spectra also provides valuable information on other properties of stars (other stellar dynamics (e.g., dispersion), stellar populations, ages, metallicities, alpha abundances). Recently, IFUs have become very important. Here spectra are measured in a 2D grid of spaxels across the face of the galaxy. Many large area surveys, e.g. CALIFA (<https://califa.caha.es/>) , MANGA (<https://www.sdss.org/surveys/manga/>) , SAMI (<http://sami-survey.org/>) , and in the future Hector , have databases of thousands of galaxies.

Traditionally matching the spectra is done with template fitting . We get a lot of information from the fit - dynamics, stellar populations, etc . But results are strongly influenced by assumptions built into the templates. Also, when S/N is low, even when it is still possible to measure stellar populations, it becomes difficult to measure line-of-sight velocities with the template fitting approach. S/N can become low in low surface brightness galaxies, or in the outskirts of any galaxy. To overcome this, IFU studies attempt to sum together the spectra from multiple spaxels to try to increase S/N using Voronoi tessellation fields . However, there is still a limit to how far out in radius they can go or how faint galaxies can be. For example, most galaxies in SAMI only have detected stellar dynamics out to one or two effective radii . If the aim is to study dark matter content, this is limiting as it is only beyond $\sim 1 R_{\rm eff}$ that the dark matter begins to dominate the potential . This in turn curtails the possibility for new discoveries from the existing data.

In this article, we seek to explore a template independent method, proposing a novel approach to calculate the velocity differences between the pairs of spaxels. Specifically, we estimate the Doppler shifts using the cross-correlation of the respective spectra, with robust control over both regularization (smoothing) and selection of the particular parts of the spectra. Our method is not dependent on identifying individual features (emission/absorption lines) in the spectra, and of course independent of any template. Therefore, apart from providing a useful crosscheck on traditional methods, it can handle difficult observational conditions (e.g. variation in spectra types, low S/N, etc), as well as realistic complex non-ideal data (incomplete spectra, missing spaxels etc). We demonstrate that this approach allows success even for lower signal to noise spectra than usual, and more robustness as it takes into account the whole spectra, not just predominantly a few features.

The paper is organized as follows. In the next section, we explain the novel technique based on iterative smoothing and computing the cross-correlation between a pair of spectra. We validate the approach on a variety of simulations in section 3 after demonstrating the method on a pair of spaxels. In the following section, we push the method to limit by systematically testing on data with different noise levels from high to very low S/N. In section 5, we validate the method on a MaNGA galaxy and compare the results with that from Marvin. We conclude and put useful discussion in section 6.

# Methodology

<figure id="fig:sch_angles">
<embed src="figs/demo/sch_gal2.pdf" style="width:48.5%" />
<figcaption>The galactic plane is shown by the shaded surface. Suppose the line of sight (LOS) has an angle <span class="math inline"><em>α</em></span> with the rotational axis. The velocity components along the projection of LOS for a point on the galactic plane would be <span class="math inline"><em>v</em>(<em>r</em>)sin <em>β</em></span>. This can be further projected along the LOS by multiplying with the <span class="math inline">sin <em>α</em></span> term.</figcaption>
</figure>

For a galaxy observed with a spectrograph, we obtain spaxel (spectral pixel) for different parts of the galaxy, whether a 2D array in the case of an integral field spectrograph or a line from slit spectroscopy. By comparing one spaxel to another, one can measure wavelength shifts of spectral features in common.

The wavelength shift from spaxel 1 to 2 is directly related to the line of sight velocity difference through the Doppler shift, so $$\begin{equation}
 \label{eq:dv}
 \Delta V= c\ \frac{\lambda_2-\lambda_1}{\lambda_1} \;.
\end{equation}$$ In order to relate this to the galaxy rotation curve (GRC) we must take into account the inclination of the galaxy with respect to the line of sight, with $$\begin{align}
\label{eq:vels}
 V_1&=V_{\rm sys}+ v(r_1)\sin\alpha\, \sin\beta_1\;, \\ \nonumber
 V_2&=V_{\rm sys}+ v(r_2)\sin\alpha\, \sin\beta_2 \;,
\end{align}$$ where the angles are as illustrated in Figure <a href="#fig:sch_angles" data-reference-type="ref" data-reference="fig:sch_angles">1</a>, $V_{\rm sys}$ is the line of sight velocity of the central spaxel, or in the simplest case of the whole galaxy, and $v(r)$ is the rotational velocity of a spaxel at distance $r$ from the galactic centre.

The velocity difference between spaxels as measured by the wavelength shift therefore allows one to build up the galaxy rotation curve $v(r)$ through $$\begin{equation}
\label{eq:vr}
 \Delta V=\sin \alpha\,\left[(v(r_2)\sin \beta_2-v(r_1)\sin \beta_1\right]\;,
\end{equation}$$ given the values of the angles $\alpha$ and $\beta$. One repeats the process for many spaxel pairs, and hence $\Delta V$’s, to construct the GRC.

In this paper we focus on introduction of our technique for measuring $\Delta V$; the extraction of $v(r)$ from those is well established in the literature. Our basic approach is to cross-correlate the spectra from spaxel pairs. Since observed spectra have noise, one needs to avoid spurious features from the noise overwhelming the true wavelength shift. In addition, spectra are sometimes incomplete, missing wavelength regions due to, for example, intervening atmospheric lines.

Therefore we first smooth one spectrum of the pair while leaving that of the other intact; we will then also switch which of the pair is smoothed to compare results and prevent a single high noise spectrum from distorting the estimate. We cross-correlate the spectra pair as a function of offset $\delta V_{\rm off}$ for a wide range of offsets, building up a cross-correlation function $r(\delta V_{\rm off})$. The mode of this curve is expected to be the actual $\Delta V$.

In the next subsections, we go into the technical details of how we carry out the smoothing, estimate the cross-correlation function, and then use it to obtain $\Delta V$.

## Iterative smoothing of the spectra

We smooth an observed spectrum, $F_{\rm obs}(\lambda_i)$, iteratively with a Gaussian kernel following ; these papers establish the criteria for stable, accurate results. The smoothed spectrum in the $n$th step is obtained from the previous step as $$\begin{equation}
\label{eq:smooth}
 F^s_{n}(\lambda)=F^s_{n-1}(\lambda)+ \frac{1}{N(\lambda)} \sum_i\frac{\left(F_{\rm obs}(\lambda_i)-F^s_{n-1}(\lambda_i)\right)}{{\sigma_{\rm obs}}^2(\lambda_i)}\times \exp{\left[-\frac{(\lambda -\lambda_i)^2}{2 \Delta^2} \right]}
\end{equation}$$ where the normalisation term $N(\lambda)$ is given by $$\begin{equation}
 N(\lambda)=\sum_i \left(\frac{1}{{\sigma_{\rm obs}}^2(\lambda_i)}\right) \times \exp{\left[-\frac{(\lambda -\lambda_i)^2}{2 \Delta^2} \right]}\;.
\end{equation}$$ Here $F^s_{n-1}(\lambda)$ is the smoothed spectrum obtained in the previous step, i.e. at the $n-1$ step. We start with an initial guess for the smoothed spectrum, say $F^s_0(\lambda)$= constant in the first step, and continue smoothing for $N_{\rm it}$ number of iterations. For sufficiently number of iteration, the final smoothed spectra should become independent of the initial guess. Note that we have two parameters in this smoothing algorithm: the smoothing scale $\Delta$ and the number of iterations $N_{\rm it}$. These two parameters should be fixed according to the problem at hand. For example, $\Delta\gtrsim \delta \lambda$ where $\delta \lambda$ is the average wavelength resolution in the observed spectrum and $N_{\rm it}\gtrsim 5$ work well for the typical examples we consider in this work. Testing by simulations as described in Section <a href="#sec:validsim" data-reference-type="ref" data-reference="sec:validsim">3</a> establishes that the final results are properly insensitive to the choice of $\Delta$ and $N_{\rm it}$ when they are within reasonable ranges. Also note that in this method we can obtain the smoothed spectrum $F^s$ at any desired values of $\lambda$ in between the observed wavelengths $\lbrace \lambda_i \rbrace$. Thus this smoothing algorithm also serves the purpose of interpolation needed for cross-correlations with any arbitrary Doppler (wavelength) shift.

## Estimating $\Delta V$ using cross-correlation

For different relative velocities ($\Delta V$) we cross-correlate the spectra considering the corresponding Doppler shift in the wavelength (related through equation <a href="#eq:dv" data-reference-type="eqref" data-reference="eq:dv">[eq:dv]</a>), with one of them being smoothed using <a href="#eq:smooth" data-reference-type="eqref" data-reference="eq:smooth">[eq:smooth]</a>. (We also tried initial “supersmoothing”, using a very large $\Delta_{\rm ini}$ to remove the continuum trend; this did not give any advantage over the results we present.) We define the weighted cross-correlation between the spectra of two spaxels (say A and B) as a function of $\Delta V$ as $$\begin{equation}
\label{eq:rab}
 r_{A^sB} (\Delta V)\equiv F^s_A (\lambda+\Delta \lambda)\otimes F_B(\lambda) =\frac{\sum_i w_i \left[ F^s_A(\lambda_i+\Delta \lambda)-\left<F^s_A(\lambda_i+\Delta \lambda)\right>_w \right] \left[ F_B(\lambda_i)-\left<F_B(\lambda_i)\right>_w \right]}{\sqrt{ \sum_i w_i \left[ F^s_A(\lambda_i+\Delta \lambda)-\left<F^s_A(\lambda_i+\Delta \lambda)\right>_w\right]^2} ~\sqrt{\sum_i w_i  \left[ F_B(\lambda_i)-\left<F_B(\lambda_i\right>_w\right]^2 }}\;,
\end{equation}$$ where $\Delta \lambda= \lambda(\Delta V/c)$. The index $i$ runs over the wavelengths sampled in the spectra. We employ inverse variance weighting $w_i=1/{\sigma^2_B}_i$, where ${\sigma_B}_i$ is the uncertainty of the second, unsmoothed spectrum. The correlation coefficient $r_{AB} (\Delta V)$ should have a maximum when $\Delta V$ is the same as the true velocity difference between the two spaxels.

## The algorithm to estimate $\Delta V$

Given these ingredients, the algorithm for obtaining the velocity difference between a pair of spaxels A and B is:

- Smooth the spectra observed in one of the spaxels, say A, calling the smoothed spectrum $F_A^s$.

- Cross-correlate $F_A^s$ and $F_B$ for a large number of relative velocities ($\Delta V$). For added robustness through crosschecks, instead of cross-correlating the whole spectra to give a single answer, we divide the (unsmoothed) spectrum of B into $N_B$ number of bins to utilize information from different parts of the spectrum independently. We determine the cross-correlation <a href="#eq:rab" data-reference-type="eqref" data-reference="eq:rab">[eq:rab]</a> for each bin of $F_B$ separately, i.e. we calculate separate estimates $r_{A^sB_j}(\Delta V)$ for the $j$th bin where $j \in \lbrace 1, N_B \rbrace$.

- Find the global maxima of the correlation coefficients $r_{A^sB_j}(\Delta V)$ for each bin. Let the maximum for the $j$th bin be $r^{\rm max}_{A^sB_j}$, occurring at the velocity difference $\Delta V_{AB_j}$. We will have $N_B$ such velocity estimations corresponding to $N_B$ bins.

- Swap the two spaxels and repeat the same procedure, i.e. evaluate ${r_{B^sA}}_j(\Delta V)$ and find $\Delta V_{BA_j}$ (always using the variance of the unsmoothed spectrum as the weight factor), again separately for each of the $N_B$ bins. We now have $2$$N_B$ number of velocity estimations. We expect $\Delta V_{BA} \approx - \Delta V_{AB}$ for all the bins; this is another crosscheck.

- Estimate the velocity difference from these $2$$N_B$ estimations. As different parts of the spectra may have different signal to noise ratios, different bins can give rise to $\Delta V$ estimation with different degrees of accuracy. To filter out noise we only accept estimates satisfying the symmetry requirement: the velocity estimations $|\Delta V_{AB}|$ and $|\Delta V_{BA}|$ are close to each other, with $|\Delta V_{AB_j}+\Delta V_{BA_j}| \leq 0.05\, |\Delta V_{AB_j}-\Delta V_{BA_j}|$, or $\le10$ km/s[^3].

- From the acceptable estimates determine the final velocity difference $\Delta V_{AB}$ between the spaxels by averaging over these estimates. Estimate the uncertainty $\sigma_{\Delta V_{AB}}$ using the standard deviations.

Cross-correlating one unsmoothed spectrum with another smoothed spectrum helps to increase the effective signal to noise. Without smoothing either spectrum, the correlation coefficient curve $r(\Delta V)$ exhibits wiggles because of random matching of the two spectral noises. This may alter the locations of the maxima of $r(\Delta V)$ for different bins leading to erroneous estimations, especially for low signal to noise cases. Conversely, smoothing both spectra simultaneously leads to neglect of some uncertainties in the data, and hence affects the realistic estimation of the final $\Delta V$. By smoothing each spectrum in sequence in addition we can have a first, basic consistency test between $\Delta V_{AB}$ and $\Delta V_{BA}$ to make sure that we are not fitting noise and both estimations are meaningfully consistent.

# Validating the method using simulation

Our aim is to test the new technique’s ability to measure the shape of a model galaxy’s rotation curve in diverse observational circumstances. Galaxies have different spectra, e.g. red and dead galaxies have absorption lines, while star-forming galaxies may be dominated by emission lines. And galaxies often have differing spectra as a function of radius (e.g. some spiral galaxies have red and dead centres and star formation in their disks). We need to ensure our method is able to successfully recover the input rotation curve even when different types of spectra are considered. Therefore, we test the method through simulations of spectra of galaxies in different scenarios, e.g. with absorption vs emission line dominated spectra, with different noise levels and strengths of features, radially varying spectral properties etc.

In this first work, for simplicity we always simulate the model galaxy to be edge-on and the spaxels are placed on the major axis perpendicular to the line of sight (so $\alpha=\beta=\pi/2$). That is, we demonstrate the procedure in a 1D situation, with the full 2D galaxy data treated in a follow-up paper; this only affects determination of $v(r)$, not $\Delta V$. The velocity difference between two spaxels then simply becomes the difference in their rotational velocities, i.e. $\Delta V_{AB}=v(r_A)-v(r_B)$. We assume an exponential disk for the model galaxy’s stellar disk with an effective radius of $1.5$ kpc. The spaxels are distributed from $-5$ to 5 kpc, and there are 21 spaxels in total such that spaxel 11 is centred on the disk centre. For the line-of-sight dynamics of the stars in each spaxel, we assume a Polyex model : $$\begin{equation}
v_{\rm PE}(r)=v_0\left(1-e^{-r/r_{\rm PE}} \right)\left( 1+\frac{\gamma r}{r_{\rm PE}} \right) \label{eq:vrmodel}
\end{equation}$$ where $v_0$, $r_{\rm PE}$ and $\gamma$ are free parameters that can be varied to alter the shape of the stellar dynamics at each radius. When we carry out validation fits, we take two cases: one where the input dynamics is known (so are these parameters) for testing, in the other it is blinded. We will find that this does not affect the fit quality.

We now build the stellar spectrum of each spaxel. In order to test with realistic spectra, we generate the spectra in the simulations using the observed spectra of ‘benchmark’ spaxels from two rather different MaNGA galaxies, 7991–12701 and 8952–9102[^4]. The spectra in all spaxels for the former galaxy are dominated by strong emission lines; spectra in two spaxels including the central one are shown in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>. On the other hand, the spectra of the MaNGA galaxy 8952–9102 show different properties in different spaxels: the central ones are absorption line dominated while the edge ones have both weak absorption and weak emission lines. Spectra from some of these spaxels are shown in figure <a href="#fig:absorption_spectra_8952-9102" data-reference-type="ref" data-reference="fig:absorption_spectra_8952-9102">3</a>. We then apply a Doppler shift to the spectra, according to the dynamics that the Polyex model provided. We also inject white noise into the MANGA galaxy spectra so that the signal-to-noise in each spaxel will reduce as the surface-brightness of the galaxy’s disk becomes fainter exponentially in the disk outskirts, as occurs in real galaxies.

We carry out the validation procedure in steps, from initially assuming spectral homogeneity and noise homogeneity, then relaxing these conditions one by one. Our model should be considered a toy model for mocking up real IFU observations of galaxies. It allows us to test the method’s ability to recover the input dynamics in a controlled manner, with a realistic set of galaxy spectra, a reasonable choice of rotation curve shapes, and with differing but controlled amounts of noise injected.

We measure the signal to noise ratio (S/N hereafter) of a whole spectrum following . Figure <a href="#fig:S_N_lowNoise" data-reference-type="ref" data-reference="fig:S_N_lowNoise">4</a> shows how S/N of the spectra vary across the spaxels for the different tests that we pursue in this section. The details of the tests involving a variety of different observational conditions are explained below in the respective subsections.

<figure id="fig:emission_spectra_7991-12701">
<embed src="figs/MaNGA_like_simulation/fixed_spectra/manga_7991-12701_spectra21.pdf" />
<figcaption>The MaNGA galaxy 7991–12701 has emission line dominated spectra, shown here from the two spaxels (37,37) and (37,12), given by their coordinates in the 2D IFU grid. The flux observed in MaNGA is in the standard unit of [<span class="math inline">10<sup>−17</sup></span> erg/cm<span class="math inline"><sup>2</sup></span>/s/<span class="math inline">$\AA$</span>] which has been used as the unit of flux in the relevant figures throughout the article. The two spectra exhibit a similar set of features on different continua, and have a slight wavelength shift with respect to each other that is the manifestation of their velocity difference (<span class="math inline"><em>Δ</em><em>V</em> ∼ 168</span> km/s, so the 0.06% shift is difficult to see by eye). The spectra in the central spaxel (37,37) has been used in the simulation for demonstrating the method in section <a href="#sec:demo" data-reference-type="ref" data-reference="sec:demo">3.1.1</a> and for the test presented in section <a href="#sec:1emission" data-reference-type="ref" data-reference="sec:1emission">3.1</a>. The test demonstrated in section <a href="#sec:2emission" data-reference-type="ref" data-reference="sec:2emission">3.3</a> uses both these spectra in the simulation. </figcaption>
</figure>

<figure id="fig:absorption_spectra_8952-9102">
<embed src="figs/MaNGA_like_simulation/fixed_spectra/manga_8952-9102_spectra21.pdf" />
<figcaption>The MaNGA galaxy 8952–9102 has absorption line or weak emission line dominated spectra, shown here from the three spaxels (32,32), (32,37) and (32,43). The spectra for the central spaxel (32,32) has been used for the test demonstrated in section <a href="#sec:1absorption" data-reference-type="ref" data-reference="sec:1absorption">3.2</a>. The spectrum from the spaxels (32,37) and (32,43) are used for the test in section <a href="#sec:absorption_vs_weak_emission" data-reference-type="ref" data-reference="sec:absorption_vs_weak_emission">3.4</a>. </figcaption>
</figure>

<figure id="fig:S_N_lowNoise">
<embed src="figs/S_N_low_noise.pdf" style="width:80.0%" />
<figcaption>Signal to noise ratio (S/N) for fluxes in the spaxels for different tests illustrated in sections <a href="#sec:1emission" data-reference-type="ref" data-reference="sec:1emission">3.1</a>–<a href="#sec:absorption_vs_weak_emission" data-reference-type="ref" data-reference="sec:absorption_vs_weak_emission">3.4</a>. The solid and dotted curves represent two different realizations for each test. Note in the mixed spectra cases (green and red curves) we challenge the method with step function transition in spectra type; we further challenge it in the lowest S/N case (red curve) by flipping the sign of the transition between the two realizations. </figcaption>
</figure>

## Simulation with emission line spectrum

We begin validation by simulating spectra in 21 spaxels located on the major axis of a galaxy, but fixing the properties of all the spectra in different spaxels to that of the spectrum of the central spaxel of MaNGA 7991-12701 (shown in orange in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>). Each is shifted according to the line of sight velocities input in the simulation. The spectra have been observed typically within the wavelength range $\lambda=[3621.6, 10339.5]$ Å with an average interval of $\delta \lambda \approx 1.47$ Å. However, we remove all the data points above $\lambda >9850$ Å due to the telluric contamination arising from the earth’s atmosphere. For this first stage we also keep the noise level low and the same for all the spaxels. Note that even with a uniform noise level, the spectra simulated in the outer/edge spaxels would have worse signal to noise due to the outer disk of a galaxy being fainter.

### Determining the velocity differences

Since we are working with a line of simulated spaxels along the major axis of a galaxy, we can refer to them simply by their second coordinate; this also serves to distinguish simulated spaxels (with a single number) from MaNGA’s observed spaxels (denoted with the 2D IFU coordinates). Consider simulated spectra in a pair of spaxels, $A=7$ and $B=15$, shown in figure <a href="#fig:demo_spectra_cc" data-reference-type="ref" data-reference="fig:demo_spectra_cc">5</a>. They are dominated by strong emission lines and derived from the same underlying spectra that is observed in the central spaxel of the MaNGA 7991-12701 galaxy. The true velocity difference between these spaxels is $326.83$ km/s (the corresponding Doppler shift is evident from the inset which zooms into the spectral region of H$\alpha$ and NII emission lines). For each of $N_B=4$ wavelength bins, we calculate the cross-correlation between one spaxel and the other (smoothed) one as a function of applied velocity shifts.

<figure id="fig:demo_spectra_cc">
<embed src="figs/MaNGA_like_simulation/fixed_spectra/set8_spectra2.pdf" />
<figcaption>Spectra simulated for the initial tests in Section <a href="#sec:1emission" data-reference-type="ref" data-reference="sec:1emission">3.1</a>, in two spaxels, 7 and 15, based on the spectrum observed in the central spaxel of MaNGA 7991-12701 (orange curve in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>). The simulated spectra are shifted according to the input line of sight velocity difference (as shown in the inset which zooms into the spectral range of H<span class="math inline"><em>α</em></span> and NII emission lines) and sampled in equispaced wavelengths. After discarding the <span class="math inline"><em>λ</em> &gt; 9850</span> Å region due to telluric contamination, the rest of the data has been equally divided into 4 bins (each bin encloses the same number of datapoints), shown by the vertical dashed lines. </figcaption>
</figure>

Figure <a href="#fig:demo_cc" data-reference-type="ref" data-reference="fig:demo_cc">6</a> displays the correlation coefficient as a function of the velocity difference, $\Delta V$, between the pair of spaxels. The left and right panels show $r_{A^sB}$ and $r_{B^s A}$ respectively for $4$ bins. For this illustration we use our baseline $\Delta=1.5$ Å and $N_{\rm it}=10$, later showing robustness to variation of these parameters. In both panels we find that $r$ exhibits global maxima at very similar values of $\Delta V$ (taking proper account of the sign), not only for $A^sB$ and $B^sA$, but also for different wavelength bins. Importantly, although the second and the fourth bin do not contain any strong feature, as evident from figure <a href="#fig:demo_spectra_cc" data-reference-type="ref" data-reference="fig:demo_spectra_cc">5</a>, the correlation $r$ shows a prominent peak at the correct $\Delta V$ values; this arises from the presence of many small features in these bins, and holds for both panels of figure <a href="#fig:demo_cc" data-reference-type="ref" data-reference="fig:demo_cc">6</a>. This illustrates the key benefit of this method in that it does not rely on single or few strong identifiable features in the spectra.

The maxima in the left and right panels arise at near-identical absolute values of $\Delta V$, i.e. $\Delta V_{BA} \approx - \Delta V_{AB}$ for all the bins as expected for an accurate shift estimation. Since both the spectra are derived from the same spectra (the central one of MaNGA 7991-12701) and have little noise, all the maxima in this first example have very high values for the correlation coefficient, $r \approx 1$. Following the algorithm described above in section <a href="#sec:algorithm" data-reference-type="ref" data-reference="sec:algorithm">2.3</a>, we find all 4 bins satisfy the selection criteria. Thus we have $4 \times 2=8$ ‘good’ estimations of $\Delta V$ from both the panels.

(Note that the secondary maxima in the third bin are readily identified as due to correlation between the $H\alpha$ line (6564.6 Å restframe) and the NII line (6585.3 Å restframe), giving a $\pm944$ km/s offset relative to the truth. This is an example of using not just statistics, but astrophysical knowledge, in assessing the data.)

From these eight maximum correlations we compute the mean and standard deviation for the velocity difference. The final result is $\Delta V_{AB} \approx 326.94 \pm 0.50$ km/s (for our baseline $\Delta=1.5$ Å, $N_{\rm it}=10$, and 4 bins). This is wholly consistent with the simulation input $\Delta V_{7,15}= 326.83$ km/s, demonstrating validation for this first test.

In table <a href="#table:demo_sim_manga_7991-12701_spaxs" data-reference-type="ref" data-reference="table:demo_sim_manga_7991-12701_spaxs">[table:demo_sim_manga_7991-12701_spaxs]</a>, we present the estimations of $\Delta V$ for the same pair of spaxels as in figure <a href="#fig:demo_cc" data-reference-type="ref" data-reference="fig:demo_cc">6</a> but for various choices of $\Delta$, $N_{\rm it}$, and $N_B$ (number of bins). All our estimations corresponding to these different choices are highly accurate with very small uncertainty and consistent with each other demonstrating the robustness of this approach. We choose as our baseline $\Delta=1.5$ Å, $N_{\rm it}=10$, and $N_B=4$ for the best combination of accuracy, precision, and computational time efficiency.

<figure id="fig:demo_cc">

<figcaption>The correlation coefficient <span class="math inline"><em>r</em>(<em>Δ</em><em>V</em>)</span> plotted as a function of velocity difference <span class="math inline"><em>Δ</em><em>V</em></span> between a pair of spaxels, <span class="math inline"><em>A</em> = 7</span> and <span class="math inline"><em>B</em> = 15</span> from the simulation based on the central spaxel of MaNGA galaxy 7991-12701. The left and right panels show <span class="math inline"><em>r</em><sub><em>A</em><sup><em>s</em></sup><em>B</em></sub></span> and <span class="math inline"><em>r</em><sub><em>B</em><sup><em>s</em></sup><em>A</em></sub></span> respectively for <span class="math inline">4</span> bins, calculated using <a href="#eq:rab" data-reference-type="eqref" data-reference="eq:rab">[eq:rab]</a>. All the bins have maxima at similar <span class="math inline"><em>Δ</em><em>V</em></span> in either panel and at the opposite sign value of the other panel – important crosschecks. </figcaption>
</figure>

<div class="table*">

<table>
<thead>
<tr>
<th style="text-align: center;"><span class="math inline"><em>Δ</em></span> (in Å)</th>
<th colspan="4" style="text-align: center;">Estimated velocity difference (<span class="math inline"><em>Δ</em><em>V</em></span>) in km/s</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>2-5</span></td>
<td colspan="2" style="text-align: center;"><span class="math inline">4</span> bins</td>
<td colspan="2" style="text-align: center;"><span class="math inline">8</span> bins</td>
</tr>
<tr>
<td style="text-align: center;"><span>2-5</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=10$</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=20$</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=10$</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=20$</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">1.5</span></td>
<td style="text-align: center;"><span class="math inline">326.9 ± 0.5</span></td>
<td style="text-align: center;"><span class="math inline">326.8 ± 0.8</span></td>
<td style="text-align: center;"><span class="math inline">326.8 ± 0.6</span></td>
<td style="text-align: center;"><span class="math inline">326.7 ± 1.0</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">2.0</span></td>
<td style="text-align: center;"><span class="math inline">326.8 ± 0.6</span></td>
<td style="text-align: center;"><span class="math inline">326.6 ± 1.1</span></td>
<td style="text-align: center;"><span class="math inline">326.7 ± 0.7</span></td>
<td style="text-align: center;"><span class="math inline">326.5 ± 1.2</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">3.0</span></td>
<td style="text-align: center;"><span class="math inline">327.0 ± 0.8</span></td>
<td style="text-align: center;"><span class="math inline">326.9 ± 0.7</span></td>
<td style="text-align: center;"><span class="math inline">326.8 ± 0.6</span></td>
<td style="text-align: center;"><span class="math inline">326.7 ± 0.6</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">4.0</span></td>
<td style="text-align: center;"><span class="math inline">327.4 ± 1.7</span></td>
<td style="text-align: center;"><span class="math inline">327.4 ± 1.7</span></td>
<td style="text-align: center;"><span class="math inline">327.0 ± 1.5</span></td>
<td style="text-align: center;"><span class="math inline">327.0 ± 1.4</span></td>
</tr>
</tbody>
</table>

</div>

<div id="tab:demo_sim_set7_spaxs">

| Pair of spaxels (A,B) | Our estimation of $\Delta V_{AB}$ in km/s | True $\Delta V_{AB}$ in km/s | residual in km/s |
|:--:|:--:|:--:|:--:|
| $( 1, 2 )$ | $5.90 \pm 0.25$ | $6.21$ | $-0.31 \pm 0.25$ |
| $(1,21 )$ | $453.15 \pm 0.69$ | $452.59$ | $0.56 \pm 0.69$ |
| $( 2, 13 )$ | $330.27 \pm 0.78$ | $329.91$ | $0.36 \pm 0.78$ |
| $( 4, 21 )$ | $432.08 \pm 0.70$ | $431.20$ | $0.88 \pm 0.70$ |
| $( 5, 6 )$ | $12.79 \pm 0.70$ | $13.18$ | $-0.39 \pm 0.70$ |
| $(7,11 )$ | $163.76 \pm 0.44$ | $163.48$ | $0.28 \pm 0.44$ |
| $( 7,15)$ | $326.94 \pm 0.50$ | $326.83$ | $0.11 \pm 0.50$ |
| $( 9, 14 )$ | $251.14 \pm 0.78$ | $251.37$ | $-0.23 \pm 0.78$ |
| $( 10, 21 )$ | $292.45 \pm 0.34$ | $291.98$ | $0.46 \pm 0.34$ |
| $(11,15 )$ | $163.01 \pm 0.85$ | $163.34$ | $-0.33 \pm 0.85$ |
| $(11,17 )$ | $194.32 \pm 0.71$ | $193.96$ | $0.36 \pm 0.71$ |
| $(13,19 )$ | $104.20 \pm 0.89$ | $103.51$ | $0.69 \pm 0.89$ |
| $( 16, 19 )$ | $31.15 \pm 0.31$ | $31.55$ | $-0.40 \pm 0.31$ |

We compare our estimation of velocity difference $\Delta V_{AB}$ between various pair of spaxels with the corresponding truth values used in the simulation. Note that spaxel 11 is the central spaxel in the simulation, so (1,21) spans from one edge of the galaxy to the other.

</div>

To assess the technique further we estimate the velocity difference for several other pairs of spaxels spanning the range of 21 spaxels (with spaxel 11 the central one). In table <a href="#tab:demo_sim_set7_spaxs" data-reference-type="ref" data-reference="tab:demo_sim_set7_spaxs">1</a>, our estimated $\Delta V$ values are compared with the corresponding true velocity differences used in the simulation. Again we find excellent matches between our estimations and the truths, with uncertainty below $1$ km/s  in all these cases. Note that such a small uncertainty arises due to the homogeneity of the spectral properties and (low) noise across all the spectra. The remaining subsections of this section will validate the method on simulations under more challenging observational circumstances, before proceeding to real observed data in section <a href="#sec:data" data-reference-type="ref" data-reference="sec:data">5</a>.

### Combining information from different spaxel pairs

Before proceeding further we briefly explain here how we construct the galaxy rotation curves. Without loss of generality, we can assume the central spaxel has zero rotational velocity, i.e. we compute the velocity of each spaxel on the diameter (more precisely along the major axis of the galaxy) relative to the central velocity and construct the galaxy rotation curve [^5].

However, the spectrum of the central spaxel itself could be noisy or distorted, so to avoid such an issue we use the estimated velocity differences between *all* the pairs, i.e. $\Delta V_{i,j}$ where $i,j$ represents all the spaxels (at least all the spaxels with good S/N)[^6]. We then fit for the velocities of all the spaxels simultaneously using all the $\Delta V_{i,j}$ measurements, i.e. all spaxel pairs. Defining the velocity of the central spaxel to be zero, we thus have $N_{\rm spax}-1$ free parameters in the fit, and up to $N_{\rm spax}(N_{\rm spax}-1)/2$ measurements, where $N_{\rm spax}$ is the total number of spaxels. Since $N_{\rm spax}$ can be large in principle (e.g. around a few thousand for the MaNGA IFU observations on a 2D grid), we employ Hamiltonian Monte Carlo (HMC) sampling with the help of the pystan package . The fit takes care of the consistency between the velocities of the spaxels, i.e. the triangle inequality $\vec\Delta V_{AB}+\vec\Delta V_{BC}=\vec\Delta V_{AC}$, or alerts us to inconsistency by not converging or giving a poor $\chi^2$.

### Constructing the galaxy rotation curves

Now we complete the construction of the galaxy rotation curve for the galaxy in the case where the spectra in all 21 spaxels are generated from the observed spectrum in the central spaxel of MaNGA 7991-12701. All pairs of spaxels have good signal to noise ratio (S/N $\sim 60$ as evident from figure <a href="#fig:S_N_lowNoise" data-reference-type="ref" data-reference="fig:S_N_lowNoise">4</a>) so we include the $\Delta V$ estimated for all the pairs into the fit.

To ensure the method is fairly tested, we conduct each test in pairs considering two realizations (as described above in equation <a href="#eq:vrmodel" data-reference-type="ref" data-reference="eq:vrmodel">[eq:vrmodel]</a>), each with independent input parameters and noise realizations. The first test is conducted such that the input rotation curve is known, and then followed up by a second test which is similar except the input rotation curve is not revealed until the results have been collected (a blind test). In the top left panel of figure <a href="#fig:blind_tests" data-reference-type="ref" data-reference="fig:blind_tests">7</a> we compare our estimated galaxy rotation curve with the true one for the blind case[^7]. We find an excellent match between our estimations and the true velocities. The uncertainties in estimations are so small ($\sim0.1$ km/s) that they are not visible in the $v(r)$ plot. The subplot at the top of the panel shows the residuals of our estimations, which are typically $\mathcal{O}(0.1)$ km/s . Since all the $\Delta V_{ij}$ estimations, which are correlated, are considered in the fit, “chi-by-eye” is not accurate. We compute $\chi^2 \equiv \sum_{ij}({\bf V_{\rm est}-V_{\rm true}})_i \cdot {\bf Cov}^{-1}_{ij} \cdot ({\bf V_{\rm est}-V_{\rm true}})^T_j$ where ${\bf Cov}$ is the covariance matrix of the fit velocities. One expects $\chi^2 \sim 20$ since the velocity of the central spaxel out of $21$ is fixed to zero. The $\chi^2$ value is $22.29$, indicating that our method is both accurate and statistically robust for estimating the galaxy rotation curve.

In the following sections we increase the difficulty by changing the spectrum, noise, and adding inhomogeneity.

<figure id="fig:blind_tests">

<figcaption>The four panels present the results of the tests described in sections <a href="#sec:1emission" data-reference-type="ref" data-reference="sec:1emission">3.1</a> – <a href="#sec:absorption_vs_weak_emission" data-reference-type="ref" data-reference="sec:absorption_vs_weak_emission">3.4</a> clockwise from the top-left. The top two panels compare the our estimated galaxy rotation curves with the corresponding truths when the spectra in different spaxels are generated from a single base spectrum – top left panel <span><strong>(a)</strong></span>: emission line dominated (the orange spectrum in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>), top right panel <span><strong>(b)</strong></span>: absorption line dominated (the blue spectrum in figure <a href="#fig:absorption_spectra_8952-9102" data-reference-type="ref" data-reference="fig:absorption_spectra_8952-9102">3</a>). The bottom two panels corresponds to the tests when the spectral properties change like a step function along the major axis as described in sections <a href="#sec:2emission" data-reference-type="ref" data-reference="sec:2emission">3.3</a> and <a href="#sec:absorption_vs_weak_emission" data-reference-type="ref" data-reference="sec:absorption_vs_weak_emission">3.4</a>. The analyses are carried out blindly and when the truths are revealed we find that the velocities are recovered accurately for all the cases. The uncertainty in <span class="math inline"><em>v</em>(<em>r</em>)</span> estimation is so small that the errorbars are not visible in the plots. The subplot at the top of each panel shows the residual for each estimation along with the errorbars. The residuals are very small, especially for the top two cases with homogeneous spectral properties. The <span class="math inline"><em>χ</em><sup>2</sup></span> values for all four cases are close to <span class="math inline">20</span>, as expected for <span class="math inline">20</span> degrees of freedom. Note that there is (modest) correlation between the fit velocities; the <span class="math inline"><em>χ</em><sup>2</sup></span> estimation considers the whole covariance matrix, not just the diagonal terms.</figcaption>
</figure>

## Absorption line dominated spectra

Next we test how our method performs when the galaxy spectra do not contain any sharp emission line (in other words, if the galaxy is not star-forming), rather they are dominated by absorption lines. We again simulate spectra in $21$ spaxels along the major axis of a galaxy. For simplicity, the spectral properties for all spaxels here are fixed to that of the central spaxel $(32,32)$ of the MaNGA galaxy 8592–9102, shown in figure <a href="#fig:absorption_spectra_8952-9102" data-reference-type="ref" data-reference="fig:absorption_spectra_8952-9102">3</a> by the blue colour. The comparison between our estimation of rotational velocities of the spaxels with the truth is presented in the top right panel of figure <a href="#fig:blind_tests" data-reference-type="ref" data-reference="fig:blind_tests">7</a>. Again we find an excellent match with the truth and the small errorbars are not visible in the $v(r)$ plot. The residuals, shown in the top subplot, are again quite small, however the residuals and their uncertainties here are slightly larger as compared to the case with the emission line dominated spectra because the emission lines are typically stronger than the absorption lines. E.g., the average residual in the absorption line dominated case is $\sim 0.22$ km/s  which is slightly larger compared to that of the emission line dominated case ($\sim 0.14$ km/s). The $\chi^2$ value for this case (taking the full covariance matrix of the fit velocities into account) $22.32$ for 20 degrees of freedom, is again reasonable.

## Different spectral properties: emission line dominated 

In the previous two subsections, we tested the method on the simple scenarios when the spectral properties are kept the same across all the spaxels (only shifted according to the velocity differences along line of sight). But in reality, galaxies can go from having absorption to emission lines as one moves across them, because of stellar population gradients. So here we test the scenarios when the spectral properties are inhomogeneous. To challenge the technique, we take a radical step function in radius, where “inner” spaxels have a different spectrum than “outer” spaxels. This and the next subsection take two different models for the base spectra.

Here, both the inner and outer spaxels are simulated from strong emission line dominated spectra, but now only the inner spaxels come from the central spaxel ($37,37$) of the MaNGA galaxy 7991–12701, while the outer spaxels are simulated with the spaxel ($37,12$) of 7991–12701. These two emission line dominated model spectra have been shown in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>. While they have the same emission lines, their continua are quite different; the former has red slope continuum whereas the latter has a bluer continuum. This subsection tests our method on this case of spectral property inhomogeneity.

We compare our estimation of rotational velocities (of the spaxels) against the true velocities for this scenario in bottom left panel of figure <a href="#fig:blind_tests" data-reference-type="ref" data-reference="fig:blind_tests">7</a>. Since there is a sharp transition of the spectrum, we get slightly stronger correlations in the fit velocities among the inner spaxels (8-14, the central one is spaxel 11) and the outer ones. This leads to the pattern apparent in the residual plot shown at the top subplot. Nevertheless, even in this extreme step function case the $\chi^2$ is $21.12$ for $20$ degrees of freedom.

## Different spectral properties: absorption line vs weak emission line dominated spectra

Next we test the method with simulations again involving a step function in spectral properties, now with the inner spaxels based on weak absorption line dominated spectra and the outer spaxels based on weak emission line dominated spectra. Specifically, we use the (32,37) spaxel of the MaNGA galaxy 8952–9102, shown as the orange spectrum (with weak absorption lines) in figure <a href="#fig:absorption_spectra_8952-9102" data-reference-type="ref" data-reference="fig:absorption_spectra_8952-9102">3</a>, and the (32,43) spaxel of the same galaxy, the green spectrum (with weak emission lines) in that figure. Note that these two base spectra have much weaker features compared to the emission line dominated spectra shown in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a> and analysed in section <a href="#sec:2emission" data-reference-type="ref" data-reference="sec:2emission">3.3</a>.

The comparison between our estimation of the rotational velocities with the true ones appears in the bottom right panel of <a href="#fig:blind_tests" data-reference-type="ref" data-reference="fig:blind_tests">7</a>. Our estimation matches very well with the truth even with the step function variation in the spectral properties among spaxels where the features are weak and of different types (absorption vs emission). Again, due to the sharp transition in the spectra we get some structure in the fit as evident from the pattern in the residuals shown in the top subplot. Nevertheless, the $\chi^2$ value is good: $21.9$. Thus, even in this more inhomogeneous case, the method succeeds.

# Validating on simulations with different noise levels

<figure id="fig:SN_emission_spectra">
<embed src="figs/MaNGA_like_simulation/SNtest/SNtest_emission.pdf" />
<figcaption>Emission line dominated spectra are shown for four sets (used in section <a href="#sec:SN_test_emission" data-reference-type="ref" data-reference="sec:SN_test_emission">4.1</a>) with different noise levels – low, medium, high, and very high – from the top to the bottom panel. Each panel shows spectra in three spaxels, two edge spaxels and the central one. S/N for these four sets are as low as <span class="math inline">59.06, 18.56, 3.97, 0.78</span>, as shown in the respective panels. </figcaption>
</figure>

<figure id="fig:S_N_SNtest">

<figcaption>The variation of signal to noise ratio (S/N) of the spectra across the spaxels is shown for the four sets with different noise levels – low, medium, high, and very high. The left panel is for simulations from an emission line dominated spectrum (section <a href="#sec:SN_test_emission" data-reference-type="ref" data-reference="sec:SN_test_emission">4.1</a>); the right panel for an absorption line dominated spectrum (section <a href="#sec:SN_test_absp" data-reference-type="ref" data-reference="sec:SN_test_absp">4.2</a>). Note that S/N of the three spaxels in each panel of figure <a href="#fig:SN_emission_spectra" data-reference-type="ref" data-reference="fig:SN_emission_spectra">8</a> are shown by the middle (central spaxel) and the two boundary dots (edge spaxels) on the corresponding curves in the left panel. Same applies for figure <a href="#fig:SN_absorption_spectra" data-reference-type="ref" data-reference="fig:SN_absorption_spectra">11</a> and the right panel. </figcaption>
</figure>

In the previous section we apply the method to different scenarios while keeping the noise level low, giving high S/N in the spectra across the spaxels (S/N $\gtrsim 10$ in the worst cases). Because of that our estimations are not only in extremely good agreement with the truth in every case but have quite small uncertainty. In this section we systematically test the method on the spectra with different noise levels.

## Emission line dominated

We again simulate spectra in the 21 spaxels generated from the same emission line dominated spectrum, namely of the central spaxel ($37,37$) of the MaNGA galaxy 7991–12701 (shown by orange in figure <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>), now with four different noise levels. Figure <a href="#fig:SN_emission_spectra" data-reference-type="ref" data-reference="fig:SN_emission_spectra">8</a> shows the spectra in three spaxels (two edge spaxels and the central one) for the four sets with four noise levels – low (similar to in the previous section), medium, high, and very high – from top to bottom panel. Notice that the spectra of the outer spaxels have much larger noise, because of being faint, most evident in the high and very high noise sets shown in the bottom two panels. The spectra in the edge spaxels still contain the sharp emission lines, however, the continua appear extremely noisy. The S/N in the spectra of the spaxels are shown in the left panel of figure <a href="#fig:S_N_SNtest" data-reference-type="ref" data-reference="fig:S_N_SNtest">9</a>; note the rapid drop for the medium and especially for the high and very high noise sets going radially outwards. The spectra in the edge spaxels have S/N $\sim 4$ for the high noise set and S/N as low as $\sim 0.8$ for the very high noise set. Note that for all the sets we keep the true velocities the same so that the results can be compared easily.

For the higher noise sets we find that a slightly larger smoothing scale gives better accuracy and robust results. Thus, we use $\Delta=2.0$ Å for the medium and higher noise sets while keep $\Delta=1.5$ Å for the low noise set, same as before. In the three panels of figure <a href="#fig:SN_test_emission" data-reference-type="ref" data-reference="fig:SN_test_emission">10</a> we compare the estimated rotational velocities for each of the four noise level sets with the true velocities (shown by the red dots). We find that our estimated velocities for the low and medium noise levels virtually coincide with the truth, again with very little uncertainty. Remarkably, even for the higher noise level cases the velocities estimated are good, $\chi^2=24.9$ and $\chi^2=20.4$ – mostly the outermost spaxels are slightly off and the uncertainties increase (recall that S/N drops down to $\sim 4$ or $\sim 1$ in the edge spaxels). Therefore, our method can estimate the rotational velocities accurately for the emission line dominated spectra even when the noise in the data is significant.

<figure id="fig:SN_test_emission">
<p><br />
</p>
<figcaption>Velocity reconstruction for spaxels with emission line dominated spectra, for different noise levels. </figcaption>
</figure>

## Absorption line dominated

Next we test the method on absorption line dominated spectral data with four sets having different noise levels. We use the weak absorption line dominated model spectrum from the $(32,37)$ spaxel of the MaNGA galaxy 8952–9102, shown by orange colour in figure <a href="#fig:absorption_spectra_8952-9102" data-reference-type="ref" data-reference="fig:absorption_spectra_8952-9102">3</a>. The spectra in three spaxels (the two edge spaxels and the central one) are shown in figure <a href="#fig:SN_absorption_spectra" data-reference-type="ref" data-reference="fig:SN_absorption_spectra">11</a>, for the low, medium, high, and very high noise level cases. The right panel of figure <a href="#fig:S_N_SNtest" data-reference-type="ref" data-reference="fig:S_N_SNtest">9</a> portrays how the S/N of the spectra varies across the spaxels for the four sets; again, S/N decays significantly at the outer-disk spaxels for the noisier sets, reaching as low as $\sim 2$ and $\sim0.7$ in the two highest noise cases. Indeed, it is difficult to discern by eye any clear features in the bottom panels of figure <a href="#fig:SN_absorption_spectra" data-reference-type="ref" data-reference="fig:SN_absorption_spectra">11</a>.

To provide more robust estimations for spectra with lower S/N, we use $\Delta=4.0$ Å for analysing the medium and higher noise sets but keep $\Delta=1.5$ Å for the low noise set. The rotational velocities estimated for the four sets with different noise levels are compared with the truth (red dots) in the panels of the figure <a href="#fig:SN_test_abp" data-reference-type="ref" data-reference="fig:SN_test_abp">12</a>. The method is again successful, even for such low S/N, though the uncertainties increase noticeably in the higher noise cases.

<figure id="fig:SN_absorption_spectra">
<embed src="figs/MaNGA_like_simulation/SNtest/SNtest_absorption.pdf" />
<figcaption>Absorption line dominated spectra are shown for four sets (used in section <a href="#sec:SN_test_absp" data-reference-type="ref" data-reference="sec:SN_test_absp">4.2</a>) with different noise levels – low, medium, high, and very high – from the top to the bottom panel. Each panel shows spectra in three spaxels, two edge spaxels and the central one. S/N for these four sets are as low as <span class="math inline">37.39, 9.95, 2.05, 0.66</span>, as shown in the respective panels. Notice that in the bottom two panels barely any feature is visible. </figcaption>
</figure>

<figure id="fig:SN_test_abp">
<p><br />
</p>
<figcaption>Velocity reconstructions for spaxels with absorption line dominated spectra, with different noise levels. </figcaption>
</figure>

Let us now focus on the results of the very high noise sets from the two cases, with emission line dominated spectra (test demonstrated in section <a href="#sec:SN_test_emission" data-reference-type="ref" data-reference="sec:SN_test_emission">4.1</a>) and with absorption line dominated spectra (test demonstrated in section <a href="#sec:SN_test_absp" data-reference-type="ref" data-reference="sec:SN_test_absp">4.2</a>). In figure <a href="#fig:VHnoise" data-reference-type="ref" data-reference="fig:VHnoise">13</a>, we explicitly show the absolute values of the residuals of velocities (for spaxels) as a function of S/N for these two sets. The red vertical line represents S/N $=4$ below which the traditional template fitting approach struggles to estimate rotational velocities. Note that the velocity estimations, along with the uncertainties, have been shown in figures <a href="#fig:SN_test_emission_VHN" data-reference-type="ref" data-reference="fig:SN_test_emission_VHN">[fig:SN_test_emission_VHN]</a> and <a href="#fig:SN_test_abpVHN" data-reference-type="ref" data-reference="fig:SN_test_abpVHN">[fig:SN_test_abpVHN]</a> respectively for these two sets.

We find that our estimations continue to be reasonably accurate well beyond S/N $=4$ for both sets. For the case with emission line dominated spectra, we get residual $\lesssim 20$ km/s for this set when S/N $\sim 0.8$ only (due to the strong emission lines barely emerging from the noisy continua in the bottom panel of figure <a href="#fig:SN_emission_spectra" data-reference-type="ref" data-reference="fig:SN_emission_spectra">8</a>). Even for the set with absorption line dominated spectra the results are accurate till S/N $\sim 1.3$, below which we may get quite large deviations from the true velocities but still the results are consistent with the truth within $2\sigma$ as evident from figure <a href="#fig:SN_test_abpVHN" data-reference-type="ref" data-reference="fig:SN_test_abpVHN">[fig:SN_test_abpVHN]</a>. As demonstrated in appendix <a href="#tab:ppxf_comp" data-reference-type="ref" data-reference="tab:ppxf_comp">3</a>, our results for the absorption lines dominated sets with four different noise levels are superior to the velocity estimations using the traditional fitting approach based on Penalized Pixel-Fitting (pPXF) and MILES stellar spectral library .

<figure id="fig:VHnoise">
<embed src="figs/MaNGA_like_simulation/SNtest/VHnoise_SN_resi2.pdf" style="width:48.5%" />
<figcaption>The figure shows the absolute residuals as a function of S/N for the very high noise sets from the tests with the emission line dominated spectra (shown by blue stars) and absorption line dominated spectra (shown by green dots). The corresponding velocity estimations are already shown in figures <a href="#fig:SN_test_emission_VHN" data-reference-type="ref" data-reference="fig:SN_test_emission_VHN">[fig:SN_test_emission_VHN]</a> and <a href="#fig:SN_test_abpVHN" data-reference-type="ref" data-reference="fig:SN_test_abpVHN">[fig:SN_test_abpVHN]</a> with the uncertainties. The red vertical line represents S/N<span class="math inline"> = 4</span> below which the traditional template fitting approach struggles to estimate rotational velocities.</figcaption>
</figure>

# Application to an observed MaNGA galaxy

Finally, we calculate the galaxy rotation curve for the MaNGA galaxy 7991–12701 itself. We estimate the velocity differences between spaxels along a major axis on the IFU hexagon, from spaxel ($37,12$) to spaxel ($37,64$)[^8] for simplicity. The spectra have been observed with good signal to noise ratio along this axis; S/N $\sim 47$ for the spectrum in the central spaxel (37,37) and it falls down to $\sim 14$ at the outskirts. We apply the same approach to the observed data as we had to simulated data.

## Velocity difference

An example of the actual spectra for a pair of spaxels, $A=(37,37)$ and $B=(37,42)$, is plotted in figure <a href="#fig:demo_spectra" data-reference-type="ref" data-reference="fig:demo_spectra">14</a>, both are seen to be emission line dominated with the former having a redder continuum.

<figure id="fig:demo_spectra">
<embed src="figs/demo/manga_7991-12701_spectra.pdf" />
<figcaption>Observed spectra from the spaxels (37,37) and (37,42) of the MaNGA galaxy 7991-12701 are dominated by emission lines (the flux is measured in the unit of [<span class="math inline">10<sup>−17</sup></span> erg/cm<span class="math inline"><sup>2</sup></span>/s/<span class="math inline">$\AA$</span>]). We discard the data with <span class="math inline"><em>λ</em> &gt; 9850</span> Å, i.e. beyond the red vertical dashed line, for telluric contamination and divide the rest of the data into 4 bins, shown by the vertical dashed lines. Note that for these observed spectra the wavelength separation increases with wavelength, leading to different bin widths.</figcaption>
</figure>

In figure <a href="#fig:demo" data-reference-type="ref" data-reference="fig:demo">15</a>, we show the correlation coefficient as a function of the velocity difference, $r(\Delta V$), between the pair of spaxels. The left and right panels show $r_{A^sB}$ and $r_{B^s A}$ respectively for $4$ bins. For this illustration we choose $\Delta=1.5$ Å and $N_{\rm it}=10$. In either panel we find that $r$ for different bins exhibits global maxima at similar values of $\Delta V$ (and $\Delta V_{BA} \approx - \Delta V_{AB}$). More importantly, although bin 4 does not contain any strong feature, as evident from figure <a href="#fig:demo_spectra" data-reference-type="ref" data-reference="fig:demo_spectra">14</a>, due to small spectral features $r$ shows a prominent peak at a consistent $\Delta V$ in both panels of figure <a href="#fig:demo" data-reference-type="ref" data-reference="fig:demo">15</a> for this bin. This illustrates the key benefit of this method that it does not rely on strong identifiable features; rather makes use of the whole spectra. Thus we have $4 \times 2=8$ ‘good’ estimations of $\Delta V$ from both the panels. We estimate the velocity difference between these two spaxels by taking the mean and standard deviation of these eight individual estimations, obtaining $\Delta V_{AB} \approx 80.29 \pm 9.82$ km/s.

<figure id="fig:demo">

<figcaption>The correlation coefficient <span class="math inline"><em>r</em>(<em>Δ</em><em>V</em>)</span> is plotted as a function of velocity difference (<span class="math inline"><em>Δ</em><em>V</em></span>) between a pair of spaxels, <span class="math inline"><em>A</em> = (37, 37)</span> and <span class="math inline"><em>B</em> = (37, 42)</span> from the MaNGA galaxy 7991-12701. The left and right panel show <span class="math inline"><em>r</em><sub><em>A</em><sup><em>s</em></sup><em>B</em></sub></span> and <span class="math inline"><em>r</em><sub><em>B</em><sup><em>s</em></sup><em>A</em></sub></span> respectively for <span class="math inline">4</span> bins, calculated using <a href="#eq:rab" data-reference-type="eqref" data-reference="eq:rab">[eq:rab]</a>. All the bins have maxima in similar <span class="math inline"><em>Δ</em><em>V</em></span> in either panel and the peak values are the negative of each other, as expected. </figcaption>
</figure>

In table <a href="#table:manga_7991-12701_32_42" data-reference-type="ref" data-reference="table:manga_7991-12701_32_42">[table:manga_7991-12701_32_42]</a>, we present the estimations of $\Delta V$ for the same pair of spaxels as in figure <a href="#fig:demo" data-reference-type="ref" data-reference="fig:demo">15</a> but for a number of different $\Delta$, $N_{\rm it}$, and number of bins. The $\Delta V$ estimations corresponding to different values of these parameters are consistent with each other that demonstrates the robustness of this approach. Since the spectra in the spaxels we consider here have good S/N ($\gtrsim 14$), we adopt $\Delta=1.5$, $N_{\rm it}=10$ and 4 bins in the analysis of this MaNGA galaxy, same as what we used for the simulations in section <a href="#sec:validsim" data-reference-type="ref" data-reference="sec:validsim">3</a>.

Note the value of $\Delta V$ obtained from the stellar velocity map by the Marvin team is $85.89 \pm 3.34$ km/s, consistent with our estimations. There is nothing to say what the true answer is. However, the Marvin results come from their full 2D analysis, giving extra stability to the results and enforcing the full triangle equality (that the vector sum of velocity differences among a triangle of spaxels is zero). Having demonstrated our correlation method here, we plan to apply it to the 2D data in the follow-up paper.

<div class="table*">

<table>
<thead>
<tr>
<th style="text-align: center;"><span class="math inline"><em>Δ</em></span> (in Å)</th>
<th colspan="2" style="text-align: center;">4 bins</th>
<th colspan="2" style="text-align: center;">8 bins</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>2-5</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=10$</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=20$</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=10$</span></td>
<td style="text-align: center;"><span class="math inline">$N_{\rm it}=20$</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">1.5</span></td>
<td style="text-align: center;"><span class="math inline">80.3 ± 9.9</span></td>
<td style="text-align: center;"><span class="math inline">78.8 ± 10.1</span></td>
<td style="text-align: center;"><span class="math inline">83.5 ± 10.1</span></td>
<td style="text-align: center;"><span class="math inline">83.2 ± 10.6</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">2.0</span></td>
<td style="text-align: center;"><span class="math inline">84.0 ± 9.5</span></td>
<td style="text-align: center;"><span class="math inline">82.5 ± 9.9</span></td>
<td style="text-align: center;"><span class="math inline">82.0 ± 10.5</span></td>
<td style="text-align: center;"><span class="math inline">84.0 ± 9.5</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">3.0</span></td>
<td style="text-align: center;"><span class="math inline">85.1 ± 8.4</span></td>
<td style="text-align: center;"><span class="math inline">85.7 ± 8.5</span></td>
<td style="text-align: center;"><span class="math inline">84.9 ± 8.9</span></td>
<td style="text-align: center;"><span class="math inline">85.2 ± 8.4</span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">4.0</span></td>
<td style="text-align: center;"><span class="math inline">82.8 ± 9.2</span></td>
<td style="text-align: center;"><span class="math inline">83.7 ± 8.6</span></td>
<td style="text-align: center;"><span class="math inline">84.7 ± 10.6</span></td>
<td style="text-align: center;"><span class="math inline">85.4 ± 10.1</span></td>
</tr>
</tbody>
</table>

</div>

We list several more velocity differences from spaxel pairs of MaNGA galaxy 7991–12701 in table <a href="#tab:7991_12701_spaxels" data-reference-type="ref" data-reference="tab:7991_12701_spaxels">2</a>, along with the $\Delta V$ values obtained from the stellar velocity map from Marvin.

Our estimations are somewhat consistent with the Marvin values but tend to be slightly higher than that from the Marvin stellar map. However, note that two estimations based on two different approaches have uncertainties of similar order of magnitude. In the simulation studies our method estimated $\Delta V$ quite accurately, without a bias or underestimation of uncertainties, so it is not clear what the true answer is. The full 2D data analysis in our follow-up paper, now that we have demonstrated the method, will give a more parallel comparison to Marvin.

<div id="tab:7991_12701_spaxels">

| Pair of spaxels (A,B) | Our estimation of $\Delta V_{AB}$ in km/s | $\Delta V_{AB}$ in km/s from Marvin |
|:--:|:--:|:--:|
| ($37$,$12$) , ($37$,$36$) | $137.45 \pm 3.65$ | $130.45 \pm 6.39$ |
| ($37$,$16$) , ($37$,$37$) | $153.84 \pm 4.31$ | $152.60 \pm 5.95$ |
| ($37$,$20$) , ($37$,$41$) | $223.99 \pm 4.29$ | $216.36 \pm 5.33$ |
| ($37$,$22$) , ($37$,$38$) | $167.38 \pm 4.91$ | $171.15 \pm 5.16$ |
| ($37,26$) , ($37,32$) | $32.43 \pm 3.61$ | $39.54 \pm 4.78$ |
| ($37,26$) , ($37,37$) | $135.69 \pm 4.62$ | $128.94 \pm 4.45$ |
| ($37$,$28$) , ($37$,$36$) | $100.48 \pm 2.72$ | $98.94 \pm 4.15$ |
| ($37,32$) , ($37,37$) | $98.62 \pm 5.19$ | $89.40 \pm 3.37$ |
| ($37,37$) , ($37,42$) | $80.29 \pm 9.82$ | $85.89 \pm 3.34$ |
| ($37,37$) , ($37,48$) | $143.79 \pm 6.34$ | $131.70  \pm 3.65$ |
| ($37$,$37$) , ($37$,$58$) | $171.08 \pm 2.81$ | $166.68 \pm 5.19$ |
| ($37$,$38$) , ($37$,$60$) | $155.67 \pm 5.25$ | $151.91 \pm 5.85$ |
| ($37$,$41$) , ($37$,$64$) | $90.19 \pm 4.29$ | $86.77 \pm 5.42$ |

We compare our estimation of the velocity difference $\Delta V_{AB}$ between various pairs of spaxels $A$ and $B$ with that from Marvin DR15. Here the smoothing scale $\Delta=1.5$ Å, $N_{\rm it}=10$, and we divided the spectra into $4$ wavelength bins.

</div>

## Constructing the galaxy rotation curve

Now we complete constructing the galaxy rotation curve for this MaNGA galaxy, using the spectra in the spaxels along the major axis on the IFU hexagon, from spaxel ($37,12$) to spaxel ($37,64$). Calculating $\Delta V$ for all the pairs of spaxels along this major axis would be more computationally expensive than warranted now for our purpose of simple demonstration. Thus we choose the 11 central spaxels as anchor spaxels (i.e. the $j$ spaxels of section <a href="#sec:combine" data-reference-type="ref" data-reference="sec:combine">3.1.2</a>), and add 23 spaxels more over the range where the data quality is good to the $i$ spaxel set, giving a total of 34 spaxels in the HMC analysis.

In figure <a href="#fig:manga_7991_12701" data-reference-type="ref" data-reference="fig:manga_7991_12701">16</a> we compare our estimated velocities (relative to the central spaxel) with that from the Marvin for the selected spaxels. As noted in the previous section, we find reasonable agreement between Marvin results and our estimations, with some trend toward larger velocities. Again we find that the uncertainties in our estimations are comparable to that from Marvin across the spaxels; the errorbars are too small to be visible for most of the central spaxels. Uncertainties in the outer disk region are larger, but we do not find a decrease in velocity as Marvin does. Our forthcoming 2D analysis may shed further light.

<figure id="fig:manga_7991_12701">
<embed src="figs/MaNGA/MaNGA_7991-12701_GRC_fit.pdf" style="width:60.0%" />
<figcaption>Our estimations (black dots with error bars) of velocity along the line of sight of the spaxels on the chosen axis with respect to the central spaxel <span class="math inline">(37, 37)</span> of the MaNGA galaxy 7991–12701. The uncertainties are so small that the errorbars are not visible for most of the spaxels. We compare to the velocities given in the Marvin database (red dots with error bars). Note that S/N <span class="math inline"> ≈ 47.5</span> at the centre and gradually falls down to <span class="math inline"> ∼ 14</span> at outskirts.</figcaption>
</figure>

# Conclusions and discussion

Galaxy rotation curves, or the internal dynamics in general, provide one of the primary lines of evidence for the existence of dark matter. Besides merely indicating the presence of dark matter, one can map the velocity-radius relation $v(r)$ directly to the mass distribution with radius. Traditionally, rotational velocities are obtained by first fitting a template to the spectra of different regions, e.g. spaxels along a galaxy major axis, and then calculating the Doppler shift between spaxels. The Doppler shifts are then translated into the velocity differences between the pairs of spaxels. This works, but has dependence on the template accuracy for that particular galaxy type and spectral noise properties.

In this article, we present a novel and template-free method to calculate the galaxy rotation curves based on cross-correlation between the spectra in the IFU data, with each member of the comparison pair alternately smoothed to avoid spurious features from noise. We demonstrate that one can achieve accurate and precise velocity difference measurements with this method. We then globally optimize the array of velocity difference through Hamiltonian Monte Carlo to construct the full galaxy rotation curves for galaxies, with spectra simulated in a variety of observational conditions.

The test conditions include emission line dominated spectra with red/blue continuum, absorption line dominated spectra, switching between different types of spectra, injection of various levels of noise, etc. The method appears to be promising and the results are precise with small uncertainties in most cases, in particular for spaxels with S/N $\gtrsim 4.0$. Remarkably, even for very noisy spectra with S/N $\sim 1$ we are able to recover the true rotational velocities with reasonable accuracy.

After these validation tests we apply the method to data from the observed MaNGA galaxy 7991–12701. Our estimations of velocity differences (between different pairs of spaxels) appear to be slightly higher than what was obtained from the Marvin velocity field, but for most cases they are consistent with each other. Comparing the 1D rotation curve (i.e. the velocities of the spaxels with respect to the central one) between our method and Marvin, we find that the results are mostly consistent with each other (figure <a href="#fig:manga_7991_12701" data-reference-type="ref" data-reference="fig:manga_7991_12701">16</a>). However, for the outer disk our estimated rotation curve does not show the slight reduction in rotational velocities seen in Marvin. The results are sufficiently promising to pursue further.

One of the chief advantages of this method is that it does not rely on strong identifiable features in the spectra. Rather, cross-correlation can utilize many small features in the spectra, and in conjunction with smoothing, remain fairly insensitive to noise. We have found good results even for quite noisy spectra.

There are several aspects to pursue further, going beyond the present proof of concept. We will enhance the pipeline to analyse the whole 2D IFU data of a number of MaNGA galaxies, not just a 1D slice on a diameter/major axis. This should also add further stability to the results through the triangle equality within our HMC analysis. We adopted here a simplified algorithm to construct the galaxy rotation curve for illustrating our results; the general conversion from a well measured velocity field to constructing the galaxy rotation curve has additional elements. We also plan to focus on low surface-brightness galaxies where the traditional template fitting approach struggles, especially at the outskirts. Further investigation will show the degree to which this new method can improve upon, or nicely complement, traditional template fitting approaches.

# Acknowledgement

The authors acknowledge that the high performance computing facility at the Korea Institute of Science and Technology Information (KISTI), assignment no. KSC-2020-CRE-0153, has been used in this project. SB and AS thank Adarsh Ranjan for crucial helps and Alex G. Kim for useful discussions at different phases of the project. S.B. also thanks Brian Cherinka and Maria Argudo-Fernández for useful discussions and explanations regarding the MaNGA data. YSA, EL, and KY were supported in part by the Energetic Cosmos Laboratory and EL by the U.S. Department of Energy, Office of Science, Office of High Energy Physics, under contract no. DE-AC02-05CH11231. KY thanks Yessenov Foundation for funding his stay in South Korea. YSA and KY also thank KASI for hospitality during the early work.

# Data availability

The data underlying this article will be shared on reasonable request to the corresponding author.

# Comparing with Penalized Pixel-Fitting (pPXF)

In this section we compare our results with that from the traditional fitting approach based on Penalized Pixel-Fitting (pPXF) , using the MILES templates from . Since obtaining the fitting results for all the cases is beyond the scope of this article, we restrict ourselves to the data sets with absorption line dominated spectra. In particular, we consider the four data sets with different noise levels as described in section <a href="#sec:SN_test_absp" data-reference-type="ref" data-reference="sec:SN_test_absp">4.2</a>. Our results for these tests have been presented in figure <a href="#fig:SN_test_abp" data-reference-type="ref" data-reference="fig:SN_test_abp">12</a> already.

<figure id="fig:SN_test_abp_ppxf">
<p><br />
</p>
<figcaption>Comparing the velocity reconstructions from our approach (blue) and pPXF (black) for the absorption line dominated spectra data sets with different noise levels (this test and our results are explained in section <a href="#sec:SN_test_absp" data-reference-type="ref" data-reference="sec:SN_test_absp">4.2</a> in more details). Note that the errorbar from pPXF for the rightmost spaxel in the right-bottom panel is unrealistically high (<span class="math inline"> ∼ 9000</span>km/s, truncated by hand in the plot) which indicates that the automated pPXF is unstable for such low S/N cases. Also note that pPXF can overestimates the uncertainty on the fit velocity as vividly evident in the low-noise case presented in the top-left panel. </figcaption>
</figure>

As evident from figure <a href="#fig:SN_test_abp_ppxf" data-reference-type="ref" data-reference="fig:SN_test_abp_ppxf">17</a>, the velocities estimated from pPXF are in good agreement with the truths for all four sets, especially for lower noise sets (higher S/N cases) presented in the top panels. However, for the higher noise sets, pPXF results becomes less accurate which can be seen clearly in residual plots presented in the top subplots of the bottom two panels. Nevertheless, our estimations are superior than that from pPXF, as expected, in all four cases. The uncertainties from pPXF are much larger than ours for all the sets, although we find that pPXF overestimates the uncertainties for many spaxels (especially for the low noise level cases in the top panels [^9]). Also, we notice that the automated pPXF is not robust in the very high noise cases as it suffers from occasional failings as well as produces unrealistically huge errors sometimes (bottom-right panel).

We compare the accuracy of the velocities estimated from the two approaches in terms of the following quantities $$\begin{equation}
\epsilon_r=\frac{1}{N_{\rm spax}}\sum_i \left|v_{\rm est}-v_{\rm true} \right|~,~~\epsilon_p=\frac{1}{N_{\rm spax}}\sum_i \left|\frac{v_{\rm est}-v_{\rm true}}{v_{\rm true}}\right|~,~~b=\frac{1}{N_{\rm spax}}\sum_i \left(v_{\rm est}-v_{\rm true}\right)\;,
\end{equation}$$ which are the average residual, the average percentage error and the bias respectively. Table <a href="#tab:ppxf_comp" data-reference-type="ref" data-reference="tab:ppxf_comp">3</a> compares the results of these two approaches for the four sets in terms of $\epsilon_r$, $\epsilon_p$ and bias ($b$). While both method shows insignificant bias, the precision (in terms of $\epsilon_r$, $\epsilon_p$) of the spaxel cross-correlation approach is found be always better than that of pPXF.

<div id="tab:ppxf_comp">

<table>
<caption>We compare the results of the two approaches – spaxel cross-correlation vs pPXF – for the four sets with different noise levels in terms of average residual, average percentage error and bias.</caption>
<thead>
<tr>
<th style="text-align: center;">Set</th>
<th colspan="2" style="text-align: center;">Average residual (<span class="math inline"><em>ϵ</em><sub><em>r</em></sub></span>) in km/s</th>
<th colspan="2" style="text-align: center;">Percentage error (<span class="math inline"><em>ϵ</em><sub><em>p</em></sub></span>)</th>
<th colspan="2" style="text-align: center;">Bias (<span class="math inline"><em>b</em></span>) in km/s</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>2-7</span></td>
<td style="text-align: center;">This work</td>
<td style="text-align: center;">pPXF</td>
<td style="text-align: center;">This work</td>
<td style="text-align: center;">pPXF</td>
<td style="text-align: center;">This work</td>
<td style="text-align: center;">pPXF</td>
</tr>
<tr>
<td style="text-align: center;">Low noise</td>
<td style="text-align: center;"><span class="math inline">0.16</span></td>
<td style="text-align: center;"><span class="math inline">0.99</span></td>
<td style="text-align: center;"><span class="math inline">0.1%</span></td>
<td style="text-align: center;"><span class="math inline">0.6%</span></td>
<td style="text-align: center;"><span class="math inline">1.37 ⋅ 10<sup>−3</sup></span></td>
<td style="text-align: center;"><span class="math inline">−2.66 ⋅ 10<sup>−3</sup></span></td>
</tr>
<tr>
<td style="text-align: center;">Medium noise</td>
<td style="text-align: center;"><span class="math inline">0.72</span></td>
<td style="text-align: center;"><span class="math inline">3.29</span></td>
<td style="text-align: center;"><span class="math inline">0.42%</span></td>
<td style="text-align: center;"><span class="math inline">1.89%</span></td>
<td style="text-align: center;"><span class="math inline">−1.62 ⋅ 10<sup>−3</sup></span></td>
<td style="text-align: center;"><span class="math inline">−2.21 ⋅ 10<sup>−3</sup></span></td>
</tr>
<tr>
<td style="text-align: center;">High noise</td>
<td style="text-align: center;"><span class="math inline">6.14</span></td>
<td style="text-align: center;"><span class="math inline">9.20</span></td>
<td style="text-align: center;"><span class="math inline">3.62%</span></td>
<td style="text-align: center;"><span class="math inline">5.33%</span></td>
<td style="text-align: center;"><span class="math inline">1.35 ⋅ 10<sup>−2</sup></span></td>
<td style="text-align: center;"><span class="math inline">6.68 ⋅ 10<sup>−3</sup></span></td>
</tr>
<tr>
<td style="text-align: center;">Very high noise</td>
<td style="text-align: center;"><span class="math inline">25.24</span></td>
<td style="text-align: center;"><span class="math inline">28.60</span></td>
<td style="text-align: center;"><span class="math inline">14.52%</span></td>
<td style="text-align: center;"><span class="math inline">16.50%</span></td>
<td style="text-align: center;"><span class="math inline">2.87 ⋅ 10<sup>−2</sup></span></td>
<td style="text-align: center;"><span class="math inline">3.42 ⋅ 10<sup>−2</sup></span></td>
</tr>
</tbody>
</table>

</div>

This exercise thus demonstrates that our approach based on spaxel cross-correlation provides more precise estimation of velocities as it use the information from all parts of the spectra. However, this comes at the expense of moderate amount associated computation cost. pPXF takes roughly $0.5$ seconds on a 32-thread CPU to fit one MaNGA-like spectrum, whereas it takes $\sim 30$ sec to obtain the velocity difference between two such spectra using spaxel cross-correlation on the same computer. Nevertheless, the robustness for low S/N spectra and higher precision in our approach possibly justify the tread off in some particular use cases.

[^1]: satadru@kasi.re.kr

[^2]: shafieloo@kasi.re.kr

[^3]: Note that this criterion could be set according to the problem in hand, considering several factors like the signal to noise ratio of the spectra.

[^4]: We obtain the IFU data of MaNGA galaxies from Marvin DR15 given at <https://dr15.sdss.org/marvin/>.

[^5]: By setting the velocity of the central spaxel to zero, without loss generality, we are essentially measuring the LoS velocities of the spaxels relative to the reference central spaxel. In reality, the central spaxel may not be identified. In such cases one can assume the symmetry in the rotation curve to determine the centre and estimate the regularised spaxel velocities.

[^6]: When spaxels have poor S/N we still include them as $i$ spaxels but not as $j$ spaxels, i.e. we do not measure good spaxels relative to bad. This does not occur for tests in section <a href="#sec:validsim" data-reference-type="ref" data-reference="sec:validsim">3</a> but see section <a href="#sec:grcmanga" data-reference-type="ref" data-reference="sec:grcmanga">5.2</a> for further details.

[^7]: The results for the ‘known cases’ are statistically same as the blind cases and, therefore, are not shown separately in this article.

[^8]: We find maximal variation in velocity difference along this major axis. The emission line dominated spectra in some of the spaxels along this axis have been shown in figures <a href="#fig:demo_spectra" data-reference-type="ref" data-reference="fig:demo_spectra">14</a> and <a href="#fig:emission_spectra_7991-12701" data-reference-type="ref" data-reference="fig:emission_spectra_7991-12701">2</a>.

[^9]: When we apply pPXF on the base MaNGA spectrum that was used for the simulation and has similar noise level as the low-noise case, we obtain velocity errors of the same order ($\sim 3$ km/s) as in the top-left panel of figure <a href="#fig:SN_test_abp_ppxf" data-reference-type="ref" data-reference="fig:SN_test_abp_ppxf">17</a>.
