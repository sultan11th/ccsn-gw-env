---
key: abylkairov2025_distance
arxiv: '2510.15102'
title: Assessing the Distance for Probing the Nuclear Equation of State with Supernova
  Gravitational Waves
authors:
- Y. Sultan Abylkairov
- Matthew C. Edwards
- Artyom Ostrikov
- Yersultan Tleukhanov
- Alejandro Torres-Forné
- Pablo Cerdá-Durán
- José Antonio Font
- Marek J. Szczepańczyk
- Ernazar Abdikamalov
arxiv_version: 2510.15102v2
method: latex
fetched: '2026-11-01'
---

# Assessing the Distance for Probing the Nuclear Equation of State with Supernova Gravitational Waves

## Abstract

Gravitational waves from core-collapse supernovae provide a unique probe of the equation of state (EOS) of high density matter. In this work, we focus on the bounce signal from numerical simulations of rotating supernovae and explore its potential for EOS inference. We employ a support vector machine, previously shown to perform best among tested methods, to classify GW signals simulated for 18 EOS models. For optimally oriented sources, we estimate that the Advanced LIGO A+ detector can probe the EOS for Galactic events, while third-generation observatories such as the Einstein Telescope and Cosmic Explorer can reach substantially farther. For randomly oriented sources, only these next-generation detectors are expected to have sufficient sensitivity. These results represent the potential observational range for probing the nuclear EOS, although, due to the simplifying assumptions adopted, they should be regarded as approximate upper limits.

# Introduction

Gravitational waves (GWs) offer a unique observational window into astrophysical events. Signals from compact binary mergers are now routinely observed , yielding key insights into the physics of neutron stars and black holes. Core-collapse supernovae (CCSNe) represent another promising GW source . Galactic events are within reach of current detectors , while extragalactic signals may become accessible with future instruments (see for recent reviews).

CCSNe mark the end of massive stars, whose iron cores collapse under gravity once electron degeneracy pressure can no longer hold it. The collapse halts at nuclear density, launching a shock wave that soon stalls from energy losses and must be revived to drive the explosion . Successful explosions leave behind neutron stars, while failed ones form black holes .

A small fraction of neutrinos emitted by the nascent proto-neutron star (PNS) is absorbed in the post-shock region, where it heats the material and drives convection . This convective activity, together with the standing accretion shock instability (SASI) , helps revive the stalled shock and trigger explosion. Additionally, convective eddies from the innermost nuclear burning shells can enhance post-shock turbulence when they interact with the shock, further supporting shock expansion . This explosion scenario is known as the neutrino mechanism.

In rapidly rotating progenitors, the PNS is born with high rotational kinetic energy. This energy can be transferred to the shock front via magnetic fields, potentially driving powerful explosions known as hypernovae . This process, referred to as the magnetorotational mechanism, may also produce magnetically driven jets . If such a jet successfully breaks through the stellar envelope, it can power a long gamma-ray burst . Even in cases where the jet is “choked” before breakout, its energy can still be deposited into the envelope, contributing to an explosion . However, such rapidly rotating progenitors are expected to be rare . Recently, progenitors with moderate rotation have received increasing attention , bridging the gap between the extremes of slow and rapid rotation.

Rotation plays a crucial role in shaping both the dynamics and GW emission of CCSNe. In non-rotating or slowly rotating models, convection and SASI generate GWs and also excite oscillations of the proto–neutron star, which produce the dominant GW signal . In rotating models, core collapse becomes asymmetric due to centrifugal deformation. The bounce produces a strong, short-duration GW signal, referred to as the rotating bounce signal . In sufficiently rapidly rotating models, non-axisymmetric instabilities can develop, causing the PNS to deform into a non-axisymmetric shape over multiple rotation periods . This results in sustained GW emission over many cycles, potentially producing a strong and detectable signal . Additionally, when neutrino emission is anisotropic, the resulting asymmetric energy flux varies with angle and produces a time-dependent quadrupole moment, which in turn generates GWs at lower frequencies . Asymmetric shock propagation and, if present, jets can both contribute additional low-frequency GW emission below $\sim 100$ Hz.

A quark-deconfinement phase transition in the PNS core, if it occurs, may cause a pressure drop, resulting in a mini-collapse to a more compact state. In rapidly rotating models, this can excite quasi-radial and quadrupole modes of the PNS , while in slowly rotating models, it can couple to the flow asphericities , enhancing GW emission.

GW signals carry information about their sources . Once detected, a key objective is to extract the source parameters from the waveform . Because rotation strongly influences the dynamics, the GW signature may allow us to discriminate between a neutrino-driven explosion in slowly rotating progenitors and a magnetorotational explosion in rapidly rotating ones . One can constrain the PNS mass and radius as well as rotation . If a supernova fails to explode, or if the stellar envelope later falls back onto the proto-neutron star, a black hole may form . Such events produce distinct gravitational-wave signatures .

Constraining the high‐density nuclear equation of state (EOS) is another exciting prospect: since the PNS dynamics, and thus its GW signature, vary with the EOS , GW observations provide a means to probe and distinguish between competing EOS models . GW observations of neutron star mergers have already provided constraints on the EOS in the cold, $\beta$-equilibrated regime through tidal deformability measurements , and future detections of the post-merger signal are expected to probe the hot, supranuclear phase of the remnant . CCSNe, in contrast, explore a distinct thermodynamic domain characterized by hot, lepton-rich matter. Consequently, supernovae and mergers probe the EOS under complementary conditions.

In prior work , we investigated the feasibility of inferring the nuclear EOS from the GW signal produced by rotating core bounce. Building on earlier studies by , and using the waveform catalog of , we examined how accurately machine-learning methods can identify the EOS under idealized, noise-free conditions. In the present study, we extend this analysis by incorporating the effects of detector noise. Our objective is to obtain a rough estimate of the distance out to which the EOS can be probed. We adopt a simplified noise model, a discrete set of EOS candidates, and other idealized assumptions (see below). Therefore, our results should be viewed as approximate upper limits on the distance horizon and a step toward more comprehensive future studies.

The paper is organized as follows. Section <a href="#sec:method" data-reference-type="ref" data-reference="sec:method">2</a> outlines our method, Section <a href="#sec:result" data-reference-type="ref" data-reference="sec:result">3</a> presents the results. Section <a href="#sec:conclusion" data-reference-type="ref" data-reference="sec:conclusion">4</a> summarizes the main conclusions.

# Methods

## Data

<div class="center">

<div class="small">

<div class="sc">

<div class="tabular">

C1.4cm C3.6cm Label & 18 EOS models\
& BHB$\Lambda$ \
2 & BHB$\Lambda \Phi$ \
3 & HSDD2 \
4 & HSTMA \
5 & HSFSG \
6 & HSIUF \
7 & HSNL3 \
8 & HSTM1 \
9 & SFHx \
10 & SFHo \
& GShenFSU1.7 \
12 & GShenFSU2.1 \
13 & GShenNL3 \
& HShen \
15 & HShenH \
& LS180 \
17 & LS220 \
18 & LS375 \

</div>

</div>

</div>

</div>

<span id="Table:EOS_GR_ML" label="Table:EOS_GR_ML"></span>

<figure id="fig:signal_noise_fft">
<embed src="figures/fft_plot.pdf" />
<figcaption>Fourier transformed gravitational wave signals for the SFHo EOS at a distance of 10 kpc, scaled by <span class="math inline">$\sqrt{f}$</span>, for <span class="math inline">0.02 &lt; <em>T</em>/|<em>W</em>| &lt; 0.18</span> (shown in grey). The purple curve corresponds to the signal at <span class="math inline"><em>T</em>/|<em>W</em>| ≈ 0.07</span>. The blue, orange, and green curves represent the sensitivity curves of Advanced LIGO A+, the Einstein Telescope, and the Cosmic Explorer, respectively.</figcaption>
</figure>

In this work, we use gravitational waveforms from the catalog, which comprises 1824 numerical waveforms[^1] from simulations of a 12 $M_\odot$ progenitor using the general relativistic code `CoCoNuT` . The simulations use 18 EOS models and follow the evolution up to approximately 50 ms after core bounce. See for the details of the simulations.

These 18 EOS models are listed in Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>. Among them, three (LS180, LS220, and LS375) are based on the compressible liquid-drop model , while the remaining ones are constructed within the relativistic mean-field framework. This group includes BHB$\Lambda$, BHB$\Lambda\Phi$ , HSDD2, HSTMA, HSFSG, HSIUF, HSNL3, HSTM1 , SFHx, SFHo , GShenFSU1.7, GShenFSU2.1 , GShenNL3 , HShen , and HShenH . Detailed descriptions of these EOSs can be found in . To avoid redundancy, we do not repeat this information here and refer the reader to the original references.

Not all 18 EOS models from this catalog are consistent with modern experimental and astrophysical constraints (see discussion in ). Nevertheless, we retain the full set to estimate the maximum distance over which the EOS can be probed. Excluding the inconsistent models and replacing them with more realistic alternatives would yield a more tightly clustered EOS set, making classification more difficult and thus reducing this distance. This consideration is one of the reasons why our results should be regarded as upper limits.

The waveforms were resampled at 16384 Hz to match the sampling rate of LIGO detectors. We restrict our study to the time interval from $-$<!-- -->2 ms to 6 ms, where zero corresponds to the bounce time. This interval was selected because the GW signal prior to $-$<!-- -->2 ms carries negligible energy, while the signal beyond 6 ms is affected by contributions from prompt convection , which is not accurately modeled in the catalog.

For each EOS, the catalog includes approximately 100 rotational configurations, ranging from slow to rapid rotation . We characterize the rotation at bounce by the parameter $T/|W|$, with $T$ denoting the rotational kinetic energy and $W$ the gravitational binding energy. Our analysis focuses on models with $0.02 < T/|W| < 0.18$. For $T/|W| < 0.02$, the rotation is insufficient to produce significant quadrupole deformation, leading to a weak bounce signal. For $T/|W| > 0.18$, centrifugal effects become prevalent, preventing the core from attaining the high densities where EOS distinctions are strongest. After applying this constraint, our dataset contains 1070 waveforms across 18 EOS models, with approximately 60 waveforms per EOS model on average.

## Noise

<figure id="fig:snr_TW_detector">
<embed src="figures/TW_SNR_det.pdf" />
<figcaption>Signal-to-noise ratio at 10 kpc as a function of <span class="math inline"><em>T</em>/|<em>W</em>|</span> for all 18 EOS waveforms with different detector sensitivities: Advanced LIGO A+ (blue), Einstein Telescope (orange), and Cosmic Explorer (green).</figcaption>
</figure>

The signal-to-noise ratio (SNR) quantifies the strength of a GW signal relative to the background noise in a detector. In our analysis, we consider the Advanced LIGO A+ design sensitivity . For comparison, we also include the planned sensitivities of the Einstein Telescope (ET) and Cosmic Explorer (CE) . Fig. <a href="#fig:signal_noise_fft" data-reference-type="ref" data-reference="fig:signal_noise_fft">1</a> shows the sensitivity curves of these detectors together with the Fourier transforms of the GW signals scaled by $\sqrt{f}$, where $f$ is the frequency. We adopt idealized conditions, assuming that the detector arms are optimally oriented relative to the signal. Following , the matched-filter SNR $\rho$ for a detected GW signal $h$ is defined under the assumption of a perfectly matched template, $$\begin{equation}
\rho = \sqrt{\int_0^{\infty}\frac{4\hat{h}^*(f)\hat{h}(f)}{S_n(f)}df},
\end{equation}$$ where $\hat{h}(f)$ is the Fourier transform of the template waveform and $S_n(f)$ is the one-sided noise spectral density.

Our dataset consists of simulated GW signals combined with detector noise, expressed as: $$\begin{equation}
d = h + n,
\end{equation}$$ where $h$ is the simulated GW signal and $n$ is the detector noise. The latter was generated using the `PyCBC` library as stationary, zero-mean Gaussian noise colored according to the detector power spectral density, with each signal assigned a unique realization. The GW signals are added directly to this colored noise without additional frequency-dependent weighting. As shown in Fig. <a href="#fig:signal_noise_fft" data-reference-type="ref" data-reference="fig:signal_noise_fft">1</a>, the detector sensitivity over the relevant frequency range ($\thicksim$<!-- -->100–1000 Hz), where most signal power resides can be approximated as flat, justifying this simplified approach.

At a fixed distance, the GW signal amplitude, and thus the SNR, varies significantly with rotation: rapidly rotating models produce stronger signals, while slowly rotating models yield weaker signals . This results in substantial variation of the SNR within each EOS class . Fig. <a href="#fig:snr_TW_detector" data-reference-type="ref" data-reference="fig:snr_TW_detector">2</a> presents the SNR variation with rotation at 10 kpc for different detector sensitivities.

## Classification algorithm

To classify EOS models, we employ the support vector machine (SVM) method, which demonstrated the best classification performance among the classical machine learning and deep learning algorithms tested by . We use an SVM with a linear kernel and regularization parameter $C = 10$, optimized for our dataset through grid search cross-validation. For a given SNR, the method is trained on 80$\%$ of the clean dataset and tested on the remaining 20$\%$ with added noise. Prior to training, $z$-normalization was applied to each time frame of the training data. The same normalization parameters were applied to the noisy test set. To enforce a fixed target SNR across different rotational configurations, we rescale only the noise component, ensuring that each signal achieves the desired SNR. We rescale the noise rather than the signal itself because $z$-normalization relies on preserving the distribution of each time frame; rescaling the signal would distort this distribution. The fixed SNR is obtained by modifying the signal-plus-noise waveform as $$\begin{equation}
H = h + n \cdot \frac{\text{SNR}_\mathrm{o}}{\text{SNR}_\mathrm{t}},
\label{eq:snr}
\end{equation}$$ where $\text{SNR}_\mathrm{o}$ is the original SNR calculated from the injected detector noise and $\text{SNR}_\mathrm{t}$ is the target SNR. This procedure ensures that the intrinsic signal strength distribution is preserved across rotational configurations while maintaining the same effective noise level. Without rescaling the noise, strong signals would be paired with artificially weak noise and weak signals with disproportionately strong noise, biasing the classifier toward recognizing strong signals more easily.

The dynamics during core bounce and the early post-bounce phase are largely axisymmetric . For axisymmetric sources, the GW strain scales as $h \propto \sin^2\alpha$, where $\alpha$ is the inclination angle between the rotation axis and the line of sight. To evaluate the impact of source orientation, we perform analysis for both optimally and randomly oriented sources. For the latter, we augment the training set with 11 isotropically distributed orientations, following .

When evaluating classification accuracy as a function of source distance (Section <a href="#sec:result" data-reference-type="ref" data-reference="sec:result">3</a>), we apply SNR-based selection criteria. For optimally oriented sources, we require all signals at a given distance to have SNR $>$ 10, while for general inclination analysis we require SNR $>$ 20. The higher threshold for general inclination provides sufficient margin such that after random scaling by $\mathrm{sin}^2\alpha$, which reduces the SNR, we retain only signals with SNR $>$ 10. This ensures reasonable freedom in inclination angle sampling while maintaining realistic detection thresholds.

We assess EOS classification performance using accuracy metric: $$\begin{equation}
\text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Number of Predictions}}
\end{equation}$$ In our evaluation, the calculations are repeated 100 times, with each run incorporating a random train-test split and a different realization of noise. For random oriented source analysis, each iteration also applies an independent random inclination scaling to each test waveform. This repetition ensures statistical robustness by reducing bias from any single train-test split, noise realization, or orientation sample. We average performance across all iterations and use the standard deviation as the error, making our results independent of these random choices.

<figure id="fig:18eos_confusion_matrix">
<embed src="figures/CM_18EOS_new.pdf" />
<figcaption>Confusion matrix for the classification of 18 EOS models without added noise, using signals with <span class="math inline">0.02 &lt; <em>T</em>/|<em>W</em>| &lt; 0.18</span>. EOS numerical labels correspond to those listed in Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>. The overall classification accuracy, averaged over 100 runs, is <span class="math inline">39.8% ± 3.1%</span>.</figcaption>
</figure>

<figure id="fig:tw_acc">
<embed src="figures/Accuracy_TW_new.pdf" />
<figcaption>Classification accuracy as a function of the maximum <span class="math inline"><em>T</em>/|<em>W</em>|</span> value included in the dataset, evaluated using clean (noise-free) signals.</figcaption>
</figure>

<figure id="fig:CM_low-density_test" data-latex-placement="t">

<figcaption>Confusion matrices for EOSs with the same (left) and distinct (right) treatments of low-density matter for <span class="math inline"><em>T</em>/|<em>W</em>| &lt; 0.10</span>. The corresponding classification accuracies are <span class="math inline">95.6% ± 5.5%</span> and <span class="math inline">98.3% ± 3.1%</span>, respectively. The EOS labels are provided in Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>.</figcaption>
</figure>

# Results

<figure id="fig:CM_low-density_test2" data-latex-placement="t">

<figcaption>Confusion matrices for EOSs with the same (left) and distinct (right) treatments of low-density matter at extreme rotation <span class="math inline">0.14 &lt; <em>T</em>/|<em>W</em>| &lt; 0.18</span>. The corresponding classification accuracies are <span class="math inline">61.1% ± 4.5%</span> and <span class="math inline">90.3% ± 3.1%</span>, respectively. The EOS labels are provided in Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>.</figcaption>
</figure>

<figure id="fig:10eos_confusion_matrix">
<embed src="figures/CM_10EOS_new.pdf" />
<figcaption>Confusion matrix for the reduced set of 10 EOS models. The matrix is computed using noise-free signals, with <span class="math inline"><em>T</em>/|<em>W</em>|</span> values ranging from 0.02 to 0.10. The overall classification accuracy improves significantly compared to the 18 EOS case, reaching <span class="math inline">93.1% ± 4.1%</span>. The EOS labels are provided in Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>.</figcaption>
</figure>

<figure id="fig:snr_acc">
<embed src="figures/Accuracy_SNR.pdf" />
<figcaption>EOS classification accuracy as a function of signal-to-noise ratio (SNR) for <span class="math inline"><em>T</em>/|<em>W</em>| &lt; 0.10</span>. For optimal orientation, the accuracy exceeds <span class="math inline">70%</span> for SNR <span class="math inline"> ≳ 70</span>. However, for random source orientation, this is achieved for SNR of <span class="math inline"> ∼ 100</span>.</figcaption>
</figure>

<figure id="fig:detector_distance">
<embed src="figures/Accuracy_D.pdf" />
<figcaption>Classification accuracy as a function of source distance for different detectors. The left panel corresponds to optimal orientation of the source, while the right panel corresponds to random orientation.</figcaption>
</figure>

As a first step, we run our classification algorithm on the entire dataset without adding noise. Fig. <a href="#fig:18eos_confusion_matrix" data-reference-type="ref" data-reference="fig:18eos_confusion_matrix">3</a> shows the averaged confusion matrix (in percentage) obtained from 100 runs of the 18 EOS classification on the clean dataset. The EOS numerical labels are decoded in Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>, where the first column lists the numerical labels and the second column provides the corresponding EOS model names. The overall classification accuracy is $39.8\% \pm 3.1\%$. This is consistent with the similar calculation in using a convolutional neural network model. In the following, we analyze how these results vary with rotation, EOS family, and source distance.

## Dependence on Rotation

In our earlier work , it was shown that for extremely rapid rotation, EOS classification accuracy decreases with increasing $T/|W|$. This decline is attributed to the growing influence of centrifugal support, which prevents the stellar core from reaching the extreme densities where EOS-dependent effects are most pronounced. To further quantify this effect, we evaluate the classification accuracy as a function of the maximum value of $T/|W|$ included in the dataset, hereafter denoted $\max{ \{ T/|W|\} }$. As shown in Fig. <a href="#fig:tw_acc" data-reference-type="ref" data-reference="fig:tw_acc">4</a>, the accuracy decreases approximately linearly from $76.3\%\pm5.5\%$ at $\max{ \{ T/|W|\} } = 0.04$ to $61.1\%\pm3.3\%$ at $\max{ \{ T/|W|\} } = 0.10$, and further to $39.8\%\pm3.1\%$ at $\max{ \{ T/|W|\}} = 0.18$. Reducing $\max{ \{ T/|W|\} }$ below $0.04$ yields a dataset with too few waveforms, which increases the statistical uncertainty. Therefore, we do not consider that limit.

Based on these results, we restrict our subsequent analysis to the range $0.02 < T/|W| < 0.10$, ensuring a balance between classification performance and dataset size (664 waveforms), while retaining a physically relevant portion of the parameter space. Because rapid rotation is rare, the condition $T/|W| < 0.10$ does not constitute a substantial additional constraint, as progenitors with faster rotation are probably extremely uncommon . For a detected signal, the value of $T/|W|$ can be inferred using the method of .

## Dependence on EOS family

As we saw above, the classification accuracy of the full set of 18 EOSs is $61.1\%\pm3.3\%$ for $T/|W| < 0.10$. This relatively low accuracy can be understood by examining Fig. <a href="#fig:18eos_confusion_matrix" data-reference-type="ref" data-reference="fig:18eos_confusion_matrix">3</a>, which shows substantial confusion among EOSs that share the same low-density physics[^2]. As noted by , the bounce dynamics, and thus the GW signal, depend on both the low- and high-density treatments. For example, GShenFSU2.1 and GShenFSU1.7 differ only at densities above nuclear saturation. Similarly, HShenH extends HShen by including hyperons. BHB$\Lambda$ extends HSDD2 by including hyperons, while BHB$\Lambda\Phi$ introduces an additional hyperonic interaction. All Hempel-based EOS families (HS, SFH, BHB) share the same treatment of low-density nonuniform matter .

This raises an important question: is our classifier probing the low-density regime, the high-density regime, or both? To address this, we perform the following test. Among the full set of 18 EOSs, there are four distinct treatments of the low-density regime. From this, we select four EOSs with different low-density prescriptions (labels 10, 12, 14, and 17; see Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>). We then select another four EOSs that share the same low-density prescription (labels 3, 6, 8, and 10). The resulting classification accuracies are $98.3\%\pm 3.1\%$ and $95.6\%\pm 5.5\%$, respectively. The corresponding confusion matrices are shown in Fig. <a href="#fig:CM_low-density_test" data-reference-type="ref" data-reference="fig:CM_low-density_test">5</a>. These results indicate that even for EOSs sharing the same low-density physics, the models can still be distinguished.

To further examine the influence of low-density matter treatment, we perform another test under extreme rotation $0.14 < T/|W| < 0.18$. The resulting confusion matrices are shown in Fig. <a href="#fig:CM_low-density_test2" data-reference-type="ref" data-reference="fig:CM_low-density_test2">6</a>. For EOSs sharing the same low-density prescription, the overall classification accuracy reduces to $61.1\%\pm4.5\%$, significantly lower than $95.6\%\pm5.5\%$ obtained in the $T/|W| < 0.10$ case. This reduction is expected: at extremely high rotation rates, the core does not reach high densities, where EOS differences are largest, limiting our ability to probe the high-density regime.

In contrast, for EOSs with different low-density treatments, the accuracy remains high at $90.3\%\pm3.1\%$ even under extremely high rotation, though still somewhat lower than the $98.3\%\pm3.1\%$ value obtained in the $T/|W| < 0.10$ case. In summary, at very rapid rotation the GW signal becomes less sensitive to high-density physics, but remains sensitive to differences in the low-density regime.

One caveat must be noted. Because the current set of EOS models is limited in size, we cannot robustly quantify how much of the classification accuracy arises from variations in the low- versus high-density regions of the EOS. Overcoming this limitation will require a large, parametrized family of EOS models, enabling a systematic study of the respective impacts of the low- and high-density components on the GW signal. We leave this for future work.

In the following analysis, we select ten well distinguishable EOS models (labeled 3, 6, 8, 10, 12, 13, 14, 16, 17, and 18), encompassing both the same and different low-density treatments. The corresponding confusion matrix is shown in Fig. <a href="#fig:10eos_confusion_matrix" data-reference-type="ref" data-reference="fig:10eos_confusion_matrix">7</a>. The overall classification accuracy is $93.1\%\pm 4.1\%$, which is significantly higher than that obtained for the full 18 EOS dataset.

## Dependence on Distance

We now investigate classification performance under noisy conditions, assuming a detected GW signal. The orange circles in Fig. <a href="#fig:snr_acc" data-reference-type="ref" data-reference="fig:snr_acc">8</a> show the classification accuracy as a function of SNR for optimally oriented sources. The accuracy reaches $68.0\%\pm4.8\%$ at SNR = 70 and $87.1 \pm 3.9\%$ at SNR = 200. This is notable performance for a ten-class classification problem. For randomly oriented sources (blue squares in Fig. <a href="#fig:snr_acc" data-reference-type="ref" data-reference="fig:snr_acc">8</a>), the accuracy is lower by about $10\%$, reaching $69.1\%\pm5.1\%$ at SNR = 100. We also notice somewhat larger standard deviations for randomly oriented sources, which reflects the variability introduced by averaging over different orientations and corresponding signal amplitudes.

We now evaluate classification performance as a function of distance to the source for different detectors. This is shown in Fig. <a href="#fig:detector_distance" data-reference-type="ref" data-reference="fig:detector_distance">9</a>. For optimal orientation, shown on the left panel, Advanced LIGO A+ achieves $\gtrsim 70\%$ classification accuracy up to 20 kpc, encompassing the most probable region for Galactic CCSNe. The next-generation detectors Einstein Telescope and Cosmic Explorer extend the horizon substantially, achieving accuracies above $\sim 90\%$ within 10 kpc, and maintaining $\gtrsim 70\%$ accuracy out to $\sim$<!-- -->80 kpc and $\sim$<!-- -->100 kpc, respectively.

For randomly oriented sources, the corresponding accuracy values are shown on the right panel of Fig. <a href="#fig:detector_distance" data-reference-type="ref" data-reference="fig:detector_distance">9</a>. For Advanced LIGO A+, the accuracy drops below $70\%$ already at a distance of $\sim$<!-- -->10 kpc. For ET and CE, the classification accuracy decreases from $92.4\%\pm2.9\%$ (both detectors) for optimal orientation to $75.0\%\pm11.4\%$ (ET) and $77.5\%\pm7.5\%$ (CE) for sources around 10 kpc. The accuracy drops below $\sim 70\%$ beyond a distance of 30 kpc. Moreover, we observe significant increase in the standard deviation of the accuracy values. This suggests that source orientation plays a significant role in achieving accurate classification. For non-optimal orientations, only next-generation detectors such as ET and CE may enable EOS inference for Galactic sources.

# Conclusion

In this work, we investigated the feasibility of classifying the nuclear equation of state (EOS) from gravitational wave (GW) signals from rotating during core-collapse supernovae. Using a catalog of 18 EOS models simulated across a broad range of rotational configurations, we quantified the classification performance of a support vector machine classifier.

We estimated the distances out to which the nuclear EOS can be probed. For optimally oriented sources, Advanced LIGO A+ may enable EOS classification within $\sim$<!-- -->20 kpc. Next-generation detectors, such as the Einstein Telescope (ET) and Cosmic Explorer (CE), substantially extend this reach, allowing classification at distances of up to $\sim$<!-- -->80 kpc and $\sim$<!-- -->100 kpc, respectively. However, this capability is strongly dependent on source orientation. For orientation is not optimal, the classification accuracy decreases considerably. In such cases, only ET and CE are expected to probe the EOS for Galactic events (cf. Section <a href="#sec:result" data-reference-type="ref" data-reference="sec:result">3</a>).

We emphasize that these results represent an optimistic scenario with several limitations. We rely on a limited set of EOS models. Ideally, one would perform a regression analysis on underlying nuclear physics parameters, but this is left to future work. We also focus on bounce signals from rotating progenitors and restrict the analysis to the first $\sim$<!-- -->6 ms after bounce. Such signals are relatively easier to detect, even at moderate SNR, compared to those from non-rotating or slowly rotating stars . Extending the framework to longer timescales remains computationally prohibitive, as producing sufficiently large sets of long-duration simulations for machine-learning analyses remains computationally demanding with present simulation codes. Moreover, accurately determining the bounce time in real GW data may be difficult , limiting the ability to align signals within the $-2$ to $6$ ms window used in our analysis. Also, rapid rotation is expected to be rare , and it remains uncertain how our results extrapolate to more slowly rotating models. Furthermore, our dataset is restricted to waveforms from a single progenitor mass. In realistic cases, uncertainties in the progenitor mass may impose additional constraints, an aspect we leave for future investigation.

Despite these caveats, our study provides an approximate estimate of EOS distinguishability across detector sensitivities, rotation rates, and noise levels. This work is a step toward more realistic studies integrating detector modeling, improved machine learning, and multi-messenger data to probe dense matter.

<div class="acknowledgments">

We thank Evan O’Connor for useful discussions. This research was funded by the Science Committee of the Ministry of Science and Higher Education of the Republic of Kazakhstan (Grant No. AP26103591) and partially supported by the Nazarbayev University Faculty Development Competitive Research Grant Program (no. 040225FD4713). MCE kindly acknowledges support by the Marsden Grant No. MFP-UOA2131 from New Zealand Government funding, administered by the Royal Society Te Apārangi. PCD, ATF and JAF are supported by the Spanish Agencia Estatal de Investigación (grants PID2021-125485NB-C21 and PID2024-159689NB-C21) funded by MCIN/AEI/10.13039/501100011033 and ERDF A way of making Europe, and by the Generalitat Valenciana (grant CIPROM/2022/49). M.S. acknowledges Polish National Science Centre Grants No. UMO-2023/49/B/ST9/02777 and No. UMO-2024/03/1/ST9/00005, and the Polish National Agency for Academic Exchange within Polish Returns Programme Grant No. BPN/PPO/2023/1/0001.

</div>

[^1]: We exclude 60 waveforms from this analysis due to the absence of core bounce in extreme rotation cases, and an additional 60 waveforms with artificially enhanced or reduced electron capture rates. Waveforms with minor numerical artifacts were cleaned using a low-pass filter .

[^2]: In Table <a href="#Table:EOS_GR_ML" data-reference-type="ref" data-reference="Table:EOS_GR_ML">[Table:EOS_GR_ML]</a>, different low-density treatments are separated by horizontal lines.
