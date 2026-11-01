---
key: akhmetali2026_realistic
arxiv: '2603.27680'
title: Toward More Realistic Machine-Learning Inference of the Dense-Matter Equation
  of State from Supernova Gravitational Waves
authors:
- Almat Akhmetali
- Y. Sultan Abylkairov
- Marat Zaidyn
- Aknur Sakan
- Alisher Zhunuskanov
- Nurzhan Ussipov
- José Antonio Font
- Alejandro Torres-Forné
- Ernazar Abdikamalov
arxiv_version: 2603.27680v2
method: latex
fetched: '2026-11-01'
---

# Toward More Realistic Machine-Learning Inference of the Dense-Matter Equation of State from Supernova Gravitational Waves

## Abstract

Gravitational waves from core-collapse supernovae offer a unique probe of the equation of state (EOS) of dense nuclear matter. For rapidly rotating stars, previous machine-learning studies demonstrated promising EOS classification accuracy. However, these analyses relied on several simplifying assumptions. In this work, we relax three key assumptions. First, we include real detector noise. Second, we expand the analysis from a single progenitor model to four models spanning 12 to 40 solar masses, and for each mass we consider multiple rotational configurations, from slow to rapid. Third, we introduce uncertainty in the core bounce time of up to 20 ms, rather than assuming it is known precisely. We find that none of these effects significantly degrades EOS classification performance. Instead, the larger dataset associated with multiple progenitor models and noise realizations improves training and classification accuracy. This study is a step in a broader effort to progressively incorporate more realistic conditions into gravitational-wave inference for core-collapse supernovae.

# Introduction

Gravitational waves (GWs) provide a powerful probe of astrophysical phenomena. In recent years, signals from compact binary mergers have been detected routinely , yielding important insights into the properties and physics of neutron stars and black holes. Another promising class of GW sources is core-collapse supernovae (CCSNe) . For CCSNe occurring within our Galaxy, the resulting GW signals are expected to be detectable with current observatories , while next-generation detectors may enable more detailed measurements and extend the reach to larger distances . Recent reviews of GW emission from CCSNe can be found in .

Massive stars reach the end of their lives when their cores exhaust nuclear fuel and can no longer support themselves against gravity. The core then collapses until the density becomes so high that repulsive nuclear forces halt the infall, launching a shock wave. This shock quickly loses energy and stalls, and must be revived in order to power a successful supernova explosion, leaving a neutron star as the remnant .

The newly formed proto-neutron star (PNS) is hot and cools by emitting neutrinos . Some of this energy is absorbed behind the stalled shock, heating the gas and stirring turbulence, which helps to energize the shock . Additional support can come from large-scale instabilities such as the standing accretion shock instability (SASI) and from convective plumes originating in the nuclear-burning shells .

In rapidly rotating progenitors, which likely represent only a small fraction of massive stars , the explosion dynamics is considerably different. The PNS is born with substantial rotational kinetic energy that magnetic fields can tap to drive the explosion, producing magnetorotational outflows and collimated jets . Even jets that fail to break out of the stellar envelope can deposit enough energy to support the explosion . At intermediate rotation rates, both neutrino heating and magnetic stresses may contribute to the outcome .

While simulations continue to refine our theoretical models of core-collapse events , the direct detection of neutrino and GW emissions from a nearby supernova would offer a transformative leap in data. Because GWs propagate directly from the engine of the star, they provide an unmediated probe into high-density regimes, potentially resolving long-standing questions regarding the explosion mechanisms of massive stars . With advanced GW detectors approaching the sensitivity required to capture such signals , developing reliable methods for identifying and studying CCSN GWs is increasingly important.

GWs arise from the multi-dimensional dynamics of the explosion engine, which depend strongly on rotation. In slowly rotating models, convection and the SASI excite PNS oscillations that dominate the signal . In rapidly rotating cores, centrifugally-deformed bounce and subsequent ring-down of the PNS produces a GW burst . Differential rotation can drive long-lived, quasi-periodic, non-axisymmetric instabilities . Additional low-frequency components may come from anisotropic neutrino emission , asymmetric shock motion , or jet activity . In rotating models, GW emission may also be enhanced by the resonance between the fundamental quadrupolar oscillation mode of the PNS and the epicyclic oscillations at the boundary of the inner core .

Gravitational waves encode the internal evolution of their sources, allowing us to constrain the underlying supernova engine upon detection. Since rotation strongly influences core-collapse dynamics, GW observations can determine progenitor rotation and discriminate between neutrino-driven and magnetorotational explosion models . Beyond the explosion mechanism itself, GWs offer a way to inferring PNS parameters like mass and radius , and placing constrainghts on the nuclear equation of state (EOS) .

In previous studies , we demonstrated the feasibility of using machine learning (ML) to infer the nuclear EOS from gravitational waves produced during rotating core bounce. While promising, those results relied on several simplifying assumptions: the use of simulated detector noise, a precisely known bounce time, and a dataset limited to the rotational configurations of a single progenitor model.

In this work, we relax these three assumptions to enhance the realism of our analysis. First, we incorporate real detector noise from the LIGO Hanford Observatory’s latest O4a public release . Second, we expand our dataset to include four distinct progenitor models with zero-age main-sequence (ZAMS) masses ranging from $12$ to $40\,M_\odot$. While a progenitor can often be identified from pre-explosion images, its inner structure, which directly influences the GW signal, remains difficult to constrain . Thus, assessing the robustness of our results across a diverse range of progenitor models is essential. As in our prior work, we explore a wide spectrum of rotational configurations for each model. Third, we account for uncertainties in core-bounce timing. While the neutrino signal can estimate the bounce time to within $\sim10$ ms , we allow for larger uncertainty of up to 20 ms. Electromagnetic observations are unlikely to improve this estimate because of the uncertain delay between core bounce and shock breakout.

The paper is structured as follows: Section <a href="#sec:methods" data-reference-type="ref" data-reference="sec:methods">2</a> describes our dataset and methods. Section <a href="#sec:results" data-reference-type="ref" data-reference="sec:results">3</a> presents our results and evaluates the relative impact of noise, progenitor diversity, and bounce time uncertainty on EOS inference. Finally, Section <a href="#sec:conclusion" data-reference-type="ref" data-reference="sec:conclusion">4</a> summarizes our main conclusions.

# Methods

We begin by describing the dataset, preprocessing steps, and the classification algorithm used to classify the different EOSs used in our study.

## Data

<figure id="fig:mass" data-latex-placement="t!">
<embed src="figures/density_entropy_vs_radius.pdf" style="width:100.0%" />
<figcaption>Radial profiles of density (solid lines) and specific entropy (dashed lines) for the 12 (blue), 15 (orange), 27 (green), and 40 (red) <span class="math inline"><em>M</em><sub>⊙</sub></span> progenitor models prior to core collapse.</figcaption>
</figure>

The general relativistic `CoCoNuT` code was used to obtain GW signals[^1]. Since the details of the simulation setup (such as grid configuration or neutrino treatment) were presented in our previous works , we only highlight the key aspects here. Our simulations are axisymmetric, which is adequate during collapse, bounce, and the early post-bounce phase (see e.g. ). We employ the $Y_e(\rho)$ deleptonization scheme during collapse and bounce, and switch to a leakage/heating scheme after bounce .

We consider four solar-metallicity progenitor models with ZAMS masses $12$ , $15$ , $27$ , and $40\,M_\odot$ . The higher-mass progenitors develop more massive, higher-entropy iron cores. At core collapse onset, the iron core masses are $1.3$, $1.4$, $1.5$, and $1.8\,M_\odot$, with central entropies of $0.60$, $0.62$, $0.77$, and $1.06\,k_\mathrm{B}$/baryon, respectively. Figure <a href="#fig:mass" data-reference-type="ref" data-reference="fig:mass">1</a> shows the density and specific entropy as functions of radius. This set spans a diverse range of progenitor structures.

For each progenitor, we perform simulations with four EOSs: `SFHo` , `LS220` , `HSDD2` , and `GShenFSU2.1` . Because the focus of this work is on the effects of detector noise, progenitor variations, and bounce-time uncertainty, the particular choice of EOS does not influence how these factors affect the classification accuracy. The impact of EOS selection on classification accuracy has been examined in previous studies .

For each combination of mass and EOS, we simulated a number of rotational configurations, from slow to rapid. We quantify the impact of rotation by the ratio $T/|W|$, where $T$ denotes rotational kinetic energy and $W$ denotes gravitational binding energy. We consider $T/|W|$ values ranging from 0.02 to 0.21. This results in the number models per progenitor mass and per EOS ranging from 52 to 57. The number of rotation configurations varies because some EOS models do not undergo core collapse within the given simulation time limit. The total number of gravitational waveforms is 886, obtained by summing over all rotation configurations across each EOS and progenitor mass combination. All waveform data have a sampling rate of 4096 Hz, which matches Advanced LIGO’s operational sampling rate.

We focus on the signal from $-2$ to $6$ ms relative to the time of bounce. The lower limit is motivated by the fact that there is little GW signal earlier than $\sim2$ ms before bounce. The upper limit is set because, after $\sim6$ ms post-bounce, the GW signal begins to include contributions from prompt convection, which is not accurately modeled in our axisymmetric simulations. While axisymmetry and the resolution we employ are adequate during bounce and the early post-bounce phase , convection is not well captured in 2D, particularly at the limited resolution used here . Properly resolving the turbulent scales of prompt convection demands high-resolution 3D simulations, but the computational cost of generating the large dataset required for machine learning analysis remains prohibitive . Nevertheless, in Appendix <a href="#sec:prompt_convection" data-reference-type="ref" data-reference="sec:prompt_convection">5</a> we perform a test to assess how prompt convection (albeit modeled unphysically) might affect the EOS classification accuracy. We find that its impact is small, suggesting that the classifier primarily learns from the bounce and early post-bounce ring-down signal.

## Signal injection into detector noise

For the background detector noise, we use publicly available LIGO Hanford data from the latest O4a public release , starting at GPS time $t_{\rm GPS}=1378195220$ s, corresponding to early September 2023. The data are sampled at 4096 Hz, and a 1024 s segment of detector noise is used to inject the GW signals.

To generate a realistic training dataset, simulated gravitational wave signals are injected into the detector noise in the time domain. Prior to injection, each waveform is smoothly tapered using a Tukey window  ($\alpha=0.1$) to suppress edge effects and reduce spectral leakage.

The signal-to-noise ratio (SNR) of each raw waveform is computed using a global power spectral density (PSD) estimated from the full noise segment via Welch’s method , according to $$\begin{equation}
\text{SNR} = \sqrt{\int_0^\infty \frac{4|\tilde{h}(f)|^2}{S_n(f)} \, df} \,,
\end{equation}$$ where $\tilde{h}(f)$ is the Fourier transform of the signal and $S_n(f)$ is the one-sided PSD of the detector noise. This ensures consistent scaling of the injected signals. After injection, the combined signal is whitened, bandpass filtered between 20 and 2000 Hz, and notch filtered at the power line harmonics of 60, 120, and 240 Hz. An example of a injected signal is shown in Figure <a href="#fig:Injected" data-reference-type="ref" data-reference="fig:Injected">2</a>.

For the classification task, the resulting strain is segmented into 30 ms windows. As noted previously, the injected GW signals have a duration of approximately 8 ms. To account for the uncertainty in core bounce time, we inject the signal at a random point between the beginning of this 30 ms windows and time $\Delta t_\mathrm{b}$, which represents the uncertainty. We consider three value of bounce time uncertainty $\Delta t_\mathrm{b}$: 0, 10, and 20 ms.

<figure id="fig:Injected" data-latex-placement="t!">
<embed src="figures/gw_injected.pdf" style="width:100.0%" />
<figcaption>Example of a gravitational wave signal injected into O4a detector noise with <span class="math inline">SNR = 20</span>.</figcaption>
</figure>

## Classification algorithm

To classify the EOS models using GW signals, we employ a support vector machine (SVM). This supervised ML algorithm demonstrated the best performance for similar tasks among the tested classical and deep learning models conducted by Abylkairov et al. . We use an rbf kernel SVM with a regularization parameter $C = 10$, selected through grid search cross validation to optimize performance on our dataset. We consider two input representations for the classifier: raw time series waveforms and their frequency domain counterparts. For each selected SNR level, the model is trained on 80% of the waveforms and evaluated on the remaining 20%, with both training and testing samples consisting of signal injections into detector noise.

To enforce a fixed target SNR across different rotational configurations, we rescale only the signal component while keeping the detector noise unchanged. This ensures that all injected waveforms attain the desired SNR under statistically consistent noise conditions. The signal-plus-noise waveform is constructed as $$\begin{equation}
H = h \cdot \frac{\mathrm{SNR}{\mathrm{t}}}{\mathrm{SNR}{\mathrm{o}}} + n ,
\label{eq:2}
\end{equation}$$ where $\mathrm{SNR}{\mathrm{o}}$ is the original SNR of the injected signal in the given noise realization and $\mathrm{SNR}{\mathrm{t}}$ is the target SNR. Eq. <a href="#eq:2" data-reference-type="ref" data-reference="eq:2">[eq:2]</a> effectively corresponds to the optimally oriented case. For non-optimal orientations, the GW strain is additionally modulated by an inclination-dependent factor ($\propto \sin^2\theta$ for axisymmetric emission). However, this factor appears both in the waveform amplitude $h$ and in the measured $\mathrm{SNR}{\mathrm{o}}$, and is therefore canceled by the rescaling procedure. Consequently, all analyses presented in this work implicitly assume optimal source–detector orientations.

We evaluate the EOS classification performance using the accuracy metric, defined as $$\begin{equation}
\text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Number of Predictions}} \,.
\end{equation}$$

To obtain statistically robust results, the evaluation procedure is repeated 50 times. In each iteration, a new random train–test split is generated. This repeated evaluation mitigates potential biases arising from a particular train–test partition. The final reported performance corresponds to the mean accuracy across all iterations, while the associated uncertainty is quantified by the standard deviation of these runs. Consequently, the reported results are effectively independent of any single random choice in the evaluation pipeline.

# Results

We turn now to discuss how real detector noise, progenitor model variations, and bounce time uncertainty affect the EOS classification accuracy from core-collapse supernova gravitational waves.

## Impact of noise

In our previous work, we analyzed the impact of simulated noise on the classification accuracy . In the current work, we asses the impact of both real and simulated detector noise on EOS classification using our augmented dataset. The injection of GW signals into real O4a LIGO noise has been described in Section <a href="#sec:injection" data-reference-type="ref" data-reference="sec:injection">2.2</a>. For simulated noise, we follow the same injection procedure, but the noise is generated as stationary, zero-mean Gaussian noise colored according to the detector PSD using the `PyCBC` package . In this test assessing the impact of noise, we assume that the bounce time is known precisely; the case of uncertain bounce time is considered below in Section <a href="#sec:bounce_time" data-reference-type="ref" data-reference="sec:bounce_time">3.3</a>.

<figure id="fig:noise" data-latex-placement="t!">
<embed src="figures/Sim_vs_real.pdf" style="width:100.0%" />
<figcaption>Accuracy as a function of SNR for real and simulated detector noises. Results are shown for two waveform representations in the time and frequency domains. At <span class="math inline">SNR = 200</span>, the time series classifier achieves <span class="math inline">92.3% ± 2.9%</span> accuracy for simulated noise and <span class="math inline">91.6% ± 3.1%</span> for real noise, while the frequency domain classifier achieves <span class="math inline">87.2% ± 2.9%</span> for simulated noise and <span class="math inline">85.3% ± 2.9%</span> for real noise. The quoted uncertainties correspond to the <span class="math inline">1<em>σ</em></span> standard deviation of the accuracies obtained from the 50 independent train–test splits described above.</figcaption>
</figure>

Figure <a href="#fig:noise" data-reference-type="ref" data-reference="fig:noise">3</a> shows the classification accuracy as a function of signal-to-noise ratio (SNR) for signals injected into real and simulated noise. We analyze the data using two representations: the time-domain waveform and its frequency domain counterpart. In both cases, we find that injections into real and simulated detector noise yield similar classification accuracies. For example, at $\mathrm{SNR}=200$, for the time domain representation, the accuracies are $92.3\%\pm2.9\%$ and $87.2\%\pm2.9\%$ for real and simulated noise, respectively. For the frequency domain representation, the corresponding accuracies are $91.6\%\pm3.1\%$ and $85.3\%\pm2.9\%$, respectively. For reference, GW signals from Galactic CCSNe observed with second-generation detectors such as Advanced LIGO are expected to have signal-to-noise ratios of order $\mathrm{SNR}\sim10$–$30$, depending on the explosion dynamics and distance . Third-generation detectors (e.g., Einstein Telescope, Cosmic Explorer) could reach $\mathrm{SNR}\gtrsim100$ for the same events . The SNR range in Figure <a href="#fig:noise" data-reference-type="ref" data-reference="fig:noise">3</a> thus reflect both current and next-generation detector sensitivities.

We find that the classification accuracy saturates at $\mathrm{SNR} \gtrsim 100$, with no significant gains at higher SNR. This behavior is likely driven by limitations in the size and diversity of the training dataset. Indeed, we observe that increasing the dataset size leads to improved classification performance (see next subsection). This trend indicates that further expanding the dataset (e.g., by more finely sampling rotational configurations in angular frequency) could yield additional gains in accuracy. However, the asymptotic performance limit remains unclear, as saturation with respect to dataset size has not yet been observed.

These results indicate that the classifier performs similarly for signals injected into real and simulated detector noise. The small differences in accuracy likely arise from non-Gaussian and non-stationary features present in real detector noise that are not captured by the simulated Gaussian noise model. Nevertheless, the overall agreement suggests that simulated noise colored by the detector power spectral density provides a reasonable approximation for evaluating EOS classification performance in this and similar studies.

## Impact of progenitor diversity

We now analyze how EOS classification depends on the diversity of progenitor models included in the dataset. Our dataset contains four progenitor models with masses $12\,M_\odot$, $15\,M_\odot$, $27\,M_\odot$, and $40\,M_\odot$ and we consider four different configurations. Configuration 1 includes a single progenitor mass, with results evaluated separately for each of the four progenitors and then combined using the root-mean-square (RMS) average. Configuration 2 includes all possible pairs of progenitor masses, configuration 3 includes all possible triplets, and configuration 4 includes all four progenitors simultaneously. For each configuration, we evaluate all possible combinations of progenitor masses of that size and report the classification accuracy as the mean and standard deviation over these combinations. Table <a href="#tab:unbalanced" data-reference-type="ref" data-reference="tab:unbalanced">1</a> summarizes the classification accuracy for these configurations.

<div id="tab:unbalanced">

|  | 1 | 2 | 3 | 4 |
|:---|:--:|:--:|:--:|:--:|
| Frequency domain | $74.0\!\pm\!9.7$ | $80.4\!\pm\!5.9$ | $83.7\!\pm\!4.2$ | $85.3\!\pm\!2.9$ |
| Time domain | $83.9\!\pm\!8.1$ | $87.7\!\pm\!4.9$ | $90.7\!\pm\!3.6$ | $91.6\!\pm\!3.1$ |

Classification accuracy (%) for various progenitor mass configurations at $\mathrm{SNR}=200$ and $\Delta t_\mathrm{b}=0$. Results are reported as the mean $\pm$ standard deviation over 50 iterations.

</div>

<div id="tab:balanced">

|  | 1 | 2 | 3 | 4 |
|:---|:--:|:--:|:--:|:--:|
| Frequency domain | $73.1\!\pm\!8.6$ | $68.6\!\pm\!9.3$ | $69.3\!\pm\!7.5$ | $66.8\!\pm\!12.2$ |
| Time domain | $83.9\!\pm\!8.1$ | $80.3\!\pm\!7.9$ | $78.0\!\pm\!8.9$ | $79.7\!\pm\!9.0$ |

Classification accuracy (%) for various progenitor mass configurations of balanced dataset at $\mathrm{SNR}=200$ and $\Delta t_\mathrm{b}=0$. Results are reported as the mean $\pm$ standard deviation over 50 iterations.

</div>

As we can see, classification accuracy increases—and standard deviation decreases—as additional progenitor masses are included. For the frequency domain representation, the accuracy rises from $74.0\%\pm9.7\%$ for a single progenitor to $85.3\%\pm2.9\%$ when all four progenitors are used. Similarly, for time domain representation, the accuracy increases from $83.9\%\pm8.1$ to $91.6\%\pm3.1\%$. While adding progenitor diversity should complicate the classification task, this upward trend stems from two primary factors. First, progenitors of different masses yield similar bounce GW signals if they possess the same specific angular momentum for a given enclosed mass. . Second, the inclusion of more progenitor models expands the training dataset. Because machine learning models typically generalize better when trained on larger datasets, the overall classification performance increases.

<figure id="fig:accuracies" data-latex-placement="ht">
<embed src="figures/accuracies.pdf" style="width:95.0%" />
<figcaption>EOS classification accuracy as a function of SNR. Blue triangles represent classification results in the time domain, red circles indicate classification in the frequency domain, and green rectangles show frequency-domain classification using an expanded dataset. The left, middle, and right panels correspond to the case with 0, 10, and 20 ms bounce time uncertainty cases. The title of each sub-panel indicates the assumed bounce time uncertainty <span class="math inline"><em>Δ</em><em>t</em><sub>b</sub></span>.</figcaption>
</figure>

To test this hypothesis, we repeat the same calculations using a balanced dataset. To construct this dataset, we randomly subsample signals in each class so that the total number of training examples is equal across all scenarios, regardless of the number of progenitors. Specifically, the balanced dataset contains 220 signals for each configuration. This ensures that differences in classification accuracy are not driven by unequal dataset sizes.

Table <a href="#tab:balanced" data-reference-type="ref" data-reference="tab:balanced">2</a> presents the results for the balanced dataset. As expected, in this case, the trend is opposite: classification accuracy decreases as additional progenitor models are included, and the standard deviation also increases. For the frequency domain representation, accuracy drops from $73.1\%\pm8.6\%$ for a single progenitor to $66.8\%\pm12.2\%$ when all four progenitors are included. For the time domain representation, accuracy decreases from $83.9\%\pm8.1\%$ to $79.7\%\pm9.0\%$ across the same range.

Time domain representation consistently achieve accuracies a few percentage points higher than those based on frequency domain across all configurations (cf. Tables <a href="#tab:unbalanced" data-reference-type="ref" data-reference="tab:unbalanced">1</a>-<a href="#tab:balanced" data-reference-type="ref" data-reference="tab:balanced">2</a>). This likely reflects their ability to preserve the sharp, short-duration structures of the bounce signal, which are partially smoothed out in the Fourier amplitude spectrum. As we will see below, however, the situation changes drastically once bounce time uncertainty is introduced.

Overall, the comparison highlights that dataset size plays a more important role in classification performance than progenitor diversity. In the unbalanced dataset, the observed improvement in accuracy and reduction in standard deviation with additional progenitors is primarily driven by the larger amount of training data, which helps the classifier better learn EOS specific features. When the dataset is balanced and the number of training examples is kept fixed, classification accuracy decreases only modestly as additional progenitor masses are included. This indicates that, although different progenitors introduce some variability in the gravitational wave signals, these differences do not significantly degrade the model’s ability to identify EOS dependent features.

## Impact of bounce time uncertainty

We now analyze how bounce time uncertainty affects EOS classification. Figure <a href="#fig:accuracies" data-reference-type="ref" data-reference="fig:accuracies">4</a> shows the classification accuracy across different SNR levels for time and frequency domain representations. The left, middle, and right panels correspond to bounce time uncertainty of 0, 10, and 20 ms, respectively. As mentioned before, when bounce time is known precisely, both time and frequency domain representations achieve high accuracies of $91.6\% \pm 3.1\%$ and $85.3\% \pm 2.9\%$ at $\mathrm{SNR}=200$, respectively.

The results change markedly when bounce time uncertainty is introduced. As shown in the middle and right panels of Figure <a href="#fig:accuracies" data-reference-type="ref" data-reference="fig:accuracies">4</a>, the time domain classifier struggles, achieving only $39.8\%$ at $\Delta t_{b}=10$ ms and $34.3\%$ at $\Delta t_{b}=20$ ms. This behavior is expected, as random shifts in the bounce time obscure the bounce and post-bounce features that are essential for distinguishing among EOSs .

In contrast, the frequency-domain classifier remains largely unaffected by bounce time uncertainty. Even for $\Delta t_\mathrm{b}=20$ ms, it maintains an accuracy of $85.3\% \pm 3.1\%$ at $\mathrm{SNR}=200$, indicating that the spectral features used for classification are robust against time shifts in the signal.

Moreover, we explore whether increasing the size of the training dataset can further improve the performance of the frequency-domain classifier. To this end, we repeat the training while injecting the signals with a time step of 2 ms when applying the bounce time shifts. This procedure effectively increases the number of training samples elevenfold. As shown in the right panel of Figure <a href="#fig:accuracies" data-reference-type="ref" data-reference="fig:accuracies">4</a> (green rectangles), the classification accuracy improves even further in this case, reaching $91.6\% \pm 2.7\%$ at $\mathrm{SNR}=200$. This result suggests that the frequency-domain classifier can benefit from larger training sets while remaining robust to bounce time uncertainty.

These results show that bounce-time uncertainty affects the two approaches differently. Time-series classification is sensitive to shifts in signal timing: when the temporal features become misaligned between the training and testing samples, the classification accuracy decreases significantly. In contrast, the frequency-domain representation depends primarily on the spectral content of the signal rather than its exact temporal position. As a result, the frequency domain classifier maintains high performance even for large timing uncertainties.

There is, however, one caveat. In our analysis we use GW signals around bounce time and exclude contribution of the prompt convection. In Appendix <a href="#sec:prompt_convection" data-reference-type="ref" data-reference="sec:prompt_convection">5</a>, we perform additional tests by including the contribution of the prompt convection (albeit in an approximate way) and find that it does not affect significantly the classification accuracy, suggesting that the classifier mainly learns EOS features from the bounce and early post-bounce ring-down signal. See Appendix <a href="#sec:prompt_convection" data-reference-type="ref" data-reference="sec:prompt_convection">5</a> for further details.

# Conclusion

In this work, we have investigated the prospect of classifying the nuclear equation of state using gravitational-wave signals under more realistic observational conditions than those employed in . Compared to our previous studies, we improve the realism in three ways: by using O4a LIGO detector noise, incorporating more progenitor models, and accounting for uncertainty in the bounce time.

First, we find that the inclusion of real detector noise degrades the classification accuracy by only a few percent (cf. Section <a href="#sec:noise" data-reference-type="ref" data-reference="sec:noise">3.1</a>). Second, our results show that variations in the progenitor mass do not significantly affect the EOS classification performance. On the contrary, because this introduces additional models into the dataset, increasing the dataset size through progenitor mass variation improves the overall training and classification accuracy (cf. Section <a href="#sec:mass" data-reference-type="ref" data-reference="sec:mass">3.2</a>). Finally, we evaluate the machine-learning performance under bounce time uncertainties of up to 20 ms. We perform the analysis in both the time and frequency domains. The frequency-domain representation consistently achieves high classification accuracy across all bounce time uncertainty cases. In contrast, the time-domain representation maintains high accuracy only when the bounce time is known precisely, which is difficult to achieve in realistic scenarios (cf. Section <a href="#sec:bounce_time" data-reference-type="ref" data-reference="sec:bounce_time">3.3</a>).

These results indicate that real detector noise, progenitor variations, and bounce-time uncertainty do not significantly affect the EOS classification accuracy. We also observe a clear trend that the accuracy improves as the size of the training dataset increases. While these results are encouraging, several limitations remain that prevent more definitive conclusions. In particular, our analysis is based on a discrete set of representative EOS models, and the machine-learning task is therefore formulated as a classification problem among these EOSs. While the selected EOSs span a range of neutron-star properties, they do not fully capture the uncertainty in the high-density matter EOS. A more general approach would be to construct a parameterized family of EOS models spanning the relevant high-density nuclear matter properties, and to treat the inference problem as a regression task aimed at recovering the underlying EOS parameters directly from the signal. Moreover, our simulations do not fully capture physical processes that occur at later stages of the evolution, such as convection and anisotropic neutrino emission. Finally, we assume optimal source and detector orientations. A more realistic treatment should also include detector antenna responses, polarization mixing, and off-axis source configurations, requiring a detailed analysis with networks of current and future GW detectors. We plan to address these limitations systematically in future work.

# Contribution of prompt convection

In analysis presented in the main body of this article, we focused on short GW signals of 8 ms duration around core bounce. Those are dominated by the bounce and early ring-down phases of the PNS. At later times, however, the GW signal contains additional physical contributions, such as prompt convection. To assess whether the presence of this component affects EOS classification, we perform an additional experiment using GW signals from the CCSN simulations of , which follow the evolution up to 50 ms after bounce and thus include the contribution of the prompt convection.

<figure id="fig:bounce_uncertainty" data-latex-placement="t">
<embed src="figures/bounce_uncertin.pdf" style="width:100.0%" />
<figcaption>Examples of two GW signals with two different bounce time assignments. The bounce time uncertainty is <span class="math inline"><em>Δ</em><em>t</em><sub>b</sub> = 20</span> ms. Red and blue lines show the same signal with different assigned bounce times, illustrating that variations arise from both shifted bounce times and intrinsic waveform differences. The gray shaded region indicates the bounce time possible position interval.</figcaption>
</figure>

The original dataset from contains 18 EOS models. To maintain a consistent classification task, we select the four EOSs that are also present in our dataset. We inject each signal to random 30 ms noise window by randomly selecting the bounce time from 2 ms to $\Delta t_\mathrm{b} + 2$ ms, where $\Delta t_\mathrm{b}$ is the bounce time uncertainty. See Figure <a href="#fig:bounce_uncertainty" data-reference-type="ref" data-reference="fig:bounce_uncertainty">5</a> for examples with two bounce times at 4 and 12 ms for $\Delta t_\mathrm{b} = 20$ ms.

The classification results for this dataset are shown in Figure <a href="#fig:prompt_convection" data-reference-type="ref" data-reference="fig:prompt_convection">6</a>. The classifier achieves $80.2\% \pm 5.5$ classification accuracy for $\Delta t_\mathrm{b} = 20$ ms at $\mathrm{SNR}=200$. This is $11.4\%$ lower than the corresponding accuracy for our dataset without prompt convection ($91.6 \pm 2.6\%$). This reduction is expected, since the analysis window may now include different portions of the post-bounce evolution, where prompt convection contributes stochastic variations to the waveform. Such variability increases the diversity of signal realizations and makes EOS classification more challenging.

<figure id="fig:prompt_convection" data-latex-placement="t">
<embed src="figures/Richers.pdf" style="width:100.0%" />
<figcaption>EOS classification accuracy as a function of SNR for GW data that contains the contribution of prompt convection. Legends corresponds to different values of bounce time uncertainty <span class="math inline"><em>Δ</em><em>t</em><sub>b</sub></span>.</figcaption>
</figure>

<figure id="fig:prompt_convection_overfitting" data-latex-placement="t">
<embed src="figures/Richers_overfitting.pdf" style="width:100.0%" />
<figcaption>Overfitting test with <span class="math inline"><em>Δ</em><em>t</em><sub>b</sub> = 20</span> ms. In this test, we restrict <span class="math inline"><em>Δ</em><em>t</em><sub>b</sub> = [18, 20]</span> ms in our test data to exclude parts of the signals dominated by prompt convection. This test verifies that our classifies learns from the bounce and early post-bounce PNS oscillations as opposed to the convection signal.</figcaption>
</figure>

Because convection is inherently stochastic, each simulation produces only a single realization of this process. As a result, there is a risk that the classifier could learn features specific to that particular realization of the convective signal rather than properties robustly related to the EOS. This raises an important question: can we be sure that the classifier is not relying on the stochastic component instead of the bounce signal itself? To address this, we perform an additional test in which the training procedure remains unchanged, but for testing we use data with the bounce time selected in the interval $[18,20]$ ms. This constraint ensures that most of the prompt convection signal lies outside our 30 ms window and is therefore not included in the classification test.

Figure <a href="#fig:prompt_convection_overfitting" data-reference-type="ref" data-reference="fig:prompt_convection_overfitting">7</a> shows that the classification performance remains essentially unchanged when the test data are restricted to bounce times between $18$ and $20$ ms. The accuracy for this restricted dataset is $79.6\% \pm 6.2\%$, compared to $80.2\% \pm 5.5\%$ for the original dataset that includes prompt convection. This demonstrates that excluding the portion of the signal potentially affected by stochastic variations from prompt convection has a negligible effect on the classifier’s predictions. Thus we conclude that the model primarily relies on physically meaningful features associated with the bounce and early post-bounce PNS oscillations, which encode EOS-dependent information.

<div class="acknowledgments">

This research was funded by the Science Committee of the Ministry of Science and Higher Education of the Republic of Kazakhstan (Grant No. AP26103591). EA is partially supported by the Nazarbayev University Faculty Development Competitive Research Grant Program (no. 040225FD4713). JAF and ATF are supported by the Spanish Agencia Estatal de Investigación (grant PID2024-159689NB-C21) funded by MICIU/AEI/10.13039/501100011033 and by FEDER / EU, and by the Generalitat Valenciana (Prometeo Excellence Programme grant CIPROM/2022/49).

AI-based language tools were used to improve the clarity and grammar of the manuscript.

This research has made use of data or software obtained from the Gravitational Wave Open Science Center (gwosc.org), a service of the LIGO Scientific Collaboration, the Virgo Collaboration, and KAGRA.

</div>

[^1]: The data are available at https://zenodo.org/records/17579189
