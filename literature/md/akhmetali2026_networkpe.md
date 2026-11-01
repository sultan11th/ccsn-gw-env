---
key: akhmetali2026_networkpe
arxiv: '2608.01634'
title: Parameter Estimation Horizon of Core-Collapse Supernovae with a Network of
  Gravitational-Wave Detectors
authors:
- Almat Akhmetali
- Y. Sultan Abylkairov
- Solange Nunes
- José Antonio Font
- Michele Zanolin
- Ernazar Abdikamalov
arxiv_version: 2608.01634v1
method: latex
fetched: '2026-11-01'
---

# Parameter Estimation Horizon of Core-Collapse Supernovae with a Network of Gravitational-Wave Detectors

## Abstract

Core-collapse supernovae are among the most promising yet still undetected sources of gravitational waves. A future detection would provide a direct view of the physical processes occurring deep inside a collapsing star. In this work, we investigate how networks of current and future gravitational-wave detectors can constrain the properties of rapidly rotating core-collapse supernovae using their characteristic core-bounce and early post-bounce signals. Using deep-learning techniques, we estimate the peak frequency, rotation rate, and signal amplitude from noisy detector data and compare the performance of different detector-network configurations. We find that detector networks improve both parameter recovery and sky coverage. For current-generation networks, estimation of the peak frequency is possible out to about 30 kpc, while the rotation rate and signal amplitude remain recoverable out to distances exceeding 100 kpc. Third-generation observatories extend these distances by nearly an order of magnitude.

# Introduction

Gravitational waves (GWs) provide a direct probe of the most extreme environments in the universe. While compact binary mergers are now routinely detected through their GW emission , core-collapse supernovae (CCSNe) remain a major predicted but as yet unobserved class of GW sources . Once detected, CCSN GWs are expected to reveal unique information about the supernova central engine .

CCSNe occur when a massive star exhausts its nuclear fuel and its core collapses under gravity. The collapse releases $\sim 10^{53}$ erg of gravitational binding energy, most of which is emitted in neutrinos . When the inner core reaches nuclear density, the collapse halts and launches a bounce shock that subsequently stalls because of nuclear dissociation and neutrino losses. Reviving this shock is the central challenge of the CCSN explosion mechanism and remains an active area of research . Electromagnetic observations provide valuable information about the explosion outcome but only limited access to the engine itself, since the shock is revived within the first second after core bounce while still buried deep inside the stellar envelope. In contrast, neutrinos and GWs escape directly from the core and carry information about the earliest phases of the explosion.

The multidimensional dynamics of the supernova engine naturally generate GW emission . In neutrino-driven explosions, convection, standing accretion shock instability, and proto-neutron star (PNS) oscillations produce GW signals spanning a wide range of frequencies . Additional low-frequency emission may arise from anisotropic neutrino emission and asymmetric shock propagation . Detecting these signals would provide a direct view of the explosion dynamics before electromagnetic emission becomes observable .

In rapidly rotating progenitors, which likely constitute a minority of CCSN sources , the GW signal differs substantially . Rotation deforms the collapsing inner core, producing a strong GW burst at core bounce followed by a short ring-down phase associated with quadrupolar oscillations of the newly formed PNS . Some models additionally develop post-bounce non-axisymmetric instabilities that generate longer-lasting GW emission . Rapid rotation may also lead to magnetorotational explosions, in which rotational energy is transferred to the shock through magnetic fields and drives bipolar outflows . Additional GW emission may arise from resonances involving PNS oscillation modes and from jet dynamics .

A detection of CCSN GWs would enable direct inference of the physical properties of the source . Rotation leaves particularly strong imprints on the GW signal, allowing one to distinguish between neutrino-driven and magnetorotational explosions and to constrain the angular momentum of the collapsing core . GW observations may also provide information about PNS masses and radii , the equation of state (EOS) of dense matter , phase transitions in the PNS interior , and black-hole formation following failed explosions or fallback accretion .

In our previous work , we investigated parameter estimation from the core-bounce and early ring-down GW signals of rotating CCSNe using machine-learning techniques. This phase of the signal is relatively straightforward to model numerically, allowing us to generate thousands of waveforms at modest computational cost and thereby enabling a machine-learning-based approach . Building on early works , we examined how physical uncertainties, including variations in the exact bounce time and in the source inclination, affect the inference of the GW peak frequency and amplitude at bounce along with the core rotation across a range of progenitor models and nuclear EOS. We demonstrated that Fourier-domain analysis mitigates bounce-time uncertainty and that next-generation GW detectors can constrain core rotation beyond 100 kpc for favorable source orientations. However, those results were obtained for individual detectors and therefore did not account for the additional information available from a global detector network.

Real GW observations are performed by networks of geographically separated detectors. The relative locations and orientations of these instruments determine the network sensitivity, sky coverage, duty cycle, and ability to reconstruct the two GW polarizations. Consequently, detector-network configuration plays a central role in the inference of source properties. The current global second-generation (2G) network consists of the two Advanced LIGO detectors , Advanced Virgo , and KAGRA , and will be expanded by LIGO India . Looking further ahead, third-generation (3G) observatories such as the Einstein Telescope (ET) and Cosmic Explorer (CE) will dramatically improve sensitivity and detection reach .

Recently, demonstrated that coordinated observations with 2G and 3G detectors can significantly improve the recovery of PNS properties for non-rotating CCSN models. Using the information encoded in the simulated GW signal associated with specific oscillation modes of the PNS, showed that, assuming unambiguous mode identification, it may be possible to infer the time evolution of the surface gravity of the PNS, $M_{\rm PNS}/R^2_{\rm PNS}$, up to several hundreds of kpc from Earth. (Here, $M_{\rm PNS}$ and $R_{\rm PNS}$ denote the mass and the radius of the PNS, respectively.) Whether these gains extend to the core-bounce and early ring-down signals of rapidly rotating CCSNe remains unexplored. In this work, we investigate this question by examining how detector-network configurations influence parameter estimation, sky localization, and distance reach for rotating CCSN GW signals. We further assess the improvements expected from future GW observatories. As in our previous work , we focus on inferring three key source parameters: the peak frequency, $f_{\mathrm{peak}}$, the distance-normalized peak amplitude, $D\Delta h$, and the rotational parameter at core-bounce, $T/|W|$. These quantities encode the core structure and bounce dynamics. Here, $D\Delta h$ is the difference between the maximum and minimum GW bounce signal strain for an optimally oriented observer, while $f_{\mathrm{peak}}$ corresponds to the dominant high-frequency feature of the postbounce waveform and traces PNS ring-down oscillations during the early post-bounce phase. The rotation parameter $T/|W|$, defined as the ratio of rotational kinetic energy to gravitational binding energy at bounce, determines the centrifugal deformation of the inner core and thus the mass quadrupole moment that drives GW emission . For $T/|W| \lesssim 0.06$, the amplitude scales approximately as $D\Delta h \propto T/|W|$. At higher rotation rates, however, centrifugal support slows the collapse and bounce dynamics, offsetting the increased deformation and causing the GW amplitude to saturate rather than continue to grow with increasing rotation. In this regime, Coriolis forces can also excite inertial modes that modify both the signal amplitude and frequency . Because $D\Delta h$ and $f_{\mathrm{peak}}$ probe complementary aspects of the bounce and ring-down dynamics, jointly measuring them helps break degeneracies with $T/|W|$. This motivates treating $D\Delta h$, $f_{\mathrm{peak}}$, and $T/|W|$ as independent inference targets.

The remainder of this work is organized as follows: In Section <a href="#sec:detectors" data-reference-type="ref" data-reference="sec:detectors">2</a>, we provide an overview of the GW detectors considered in our work. Section <a href="#sec:methods" data-reference-type="ref" data-reference="sec:methods">3</a> details the waveform dataset, the signal injections and preprocessing, and the methodology we employ for the inference. Section <a href="#sec:results" data-reference-type="ref" data-reference="sec:results">4</a> presents our results and analysis. Finally, Section <a href="#sec:conclusion" data-reference-type="ref" data-reference="sec:conclusion">5</a> provides a summary of our core results and concluding remarks.

# Detector Network

Ground-based GW observatories are broadly classified into 2G and 3G detectors. The current global 2G network consists of the two Advanced LIGO  interferometers in Hanford and Livingston (USA), the Advanced Virgo  detector in Italy, and the KAGRA  detector in Japan. The LIGO detectors have 4-km arm lengths, while Virgo and KAGRA operate with 3-km arms. This network will be further expanded by LIGO Aundha , a third LIGO-like interferometer under construction in Aundha, India, expected to become operational around 2030. Operating as a coordinated global network, these observatories conduct joint observing runs interleaved with commissioning and upgrade periods aimed at progressively improving their sensitivity toward design goals .

The next generation of GW observatories are expected to substantially extend the observational reach of current detectors . The main 3G facilities are the ET in Europe and the CE in the USA. The ET design is considering two concepts: a two-site L-shaped (2L) configuration consisting of two 10 km interferometers separated by approximately 1200 km and a triangular underground observatory. In this work, we adopt the triangular ET-D design, consisting of six 10-km arms arranged in an equilateral triangle with $60^\circ$ opening angles between arms. Each pair of arms forms an interferometer, enabling full-sky coverage and redundant signal reconstruction. The ET-D concept further adopts a xylophone configuration, combining cryogenic low-frequency interferometers with room-temperature high-frequency interferometers to suppress seismic and thermal noise while maintaining excellent high-frequency sensitivity. In contrast, the CE design consists of a network of L-shaped interferometers with arm lengths up to 40 km, with staged implementations including 20-km and 40-km facilities. With significantly longer arm lengths and advanced noise mitigation strategies, CE detectors are expected to achieve an order-of-magnitude improvement in strain sensitivity over current-generation observatories .

<figure id="fig:ASDs" data-latex-placement="t!">
<embed src="figures/ASDs.pdf" style="width:100.0%" />
<figcaption>Amplitude spectral densities as a function of frequency for the ground-based detectors considered in this work.</figcaption>
</figure>

The response of any of these detectors to an incoming GW depends on the source sky location, polarization, and detector orientation. The measured strain in detector $k$ can be written as  $$\begin{equation}
h_k(t) = F_{+,k}(\theta,\phi,\psi)\,h_{+}(t) + F_{\times,k}(\theta,\phi,\psi)\,h_{\times}(t),
\label{eq:1}
\end{equation}$$ where $h_{+}(t)$ and $h_{\times}(t)$ are the two GW polarization modes, and $F_{+,k}$ and $F_{\times,k}$ are the corresponding antenna pattern functions. The angles $\theta$ and $\phi$ define the source position on the sky, while $\psi$ denotes the polarization angle. The antenna pattern functions depend on both the geographic location and the arm orientation of each detector.

The configuration of a detector network in the Earth-fixed frame is fully specified by the coordinates of the beam-splitter and the orientation vectors of the interferometer arms. The corresponding parameters for both 2G and 3G detectors considered in this study are listed in Table <a href="#tab:detectors" data-reference-type="ref" data-reference="tab:detectors">[tab:detectors]</a>. Since the exact locations and orientations of 3G detectors are yet to be determined, following  we place them at the following locations: the ET is placed at the Virgo site with an arbitrary orientation, while the two CE detectors are located in Idaho and New Mexico (USA) .

<div class="table*">

</div>

In addition to the detector’s response functions, the detectors are characterised by their noise properties. For the 2G network, we adopt the projected design sensitivities of Advanced LIGO (A+) [^1], Advanced Virgo [^2], and KAGRA [^3]. For the 3G network, we use the ET-D sensitivity curve for the ET [^4] and compact-binary optimized sensitivity curves for CE [^5]. These amplitude spectral densities, shown in Fig. <a href="#fig:ASDs" data-reference-type="ref" data-reference="fig:ASDs">1</a>, are used to generate colored Gaussian noise into which the simulated GW signals are injected.

We identify a network of detectors with the letters corresponding to each of its detectors (e.g. HLVKA is the network composed of LIGO Hanford (H), LIGO Livingston (L), Virgo (V), KAGRA (K) and LIGO Aundha (A)).

# Dataset and methodology

Below we describe the waveform dataset, the preprocessing steps of the data, and the deep learning (DL) model used to estimate physical parameters of the source from its GW signals.

## Data

The waveform catalog used in this work is identical to that of our previous work [^6]; we refer the reader there for details and summarize only the essentials here. Waveforms are generated with the `CoCoNuT` code using axisymmetric simulations, which are adequate through collapse, bounce, and the early post-bounce phase . Deleptonization during collapse is modeled with a density-dependent electron fraction prescription, $Y_e(\rho)$ , while post-bounce neutrino effects are treated with a leakage/heating scheme . The catalog spans four solar-metallicity progenitors ($12$, $15$, $27$, and $40\,M_\odot$) , six EOSs (`BHB`$\Lambda \Phi$ , `SFHo` , `SFHx` , `LS220` , `HSDD2` , `GShenFSU2.1` ), and rotation rates in the range $T/|W| \in [0.02,0.21]$, yielding 1332 waveforms sampled at 4096 Hz. We analyze only the $[-2,6]$ ms interval around bounce to isolate the bounce and early ring-down signal. Later times are excluded because prompt convection is not accurately captured in 2D simulations; however, previous work showed that its inclusion has little impact on parameter estimation performance, indicating that the inference is driven primarily by bounce and ring-down features .

## Signal injection and data preprocessing

We generate simulated detector noise using the design sensitivity curves of the detectors discussed in Section <a href="#sec:detectors" data-reference-type="ref" data-reference="sec:detectors">2</a> with the `PyCBC` library , sampled at 4096 Hz. The noise is assumed to be stationary and Gaussian, fully characterized by the detector power spectral density (PSD).

We consider a network of detectors indexed by $k \in \{1,\dots,N\}$. The response of detector $k$ to a GW signal depends on the antenna pattern functions (Eq. (<a href="#eq:1" data-reference-type="ref" data-reference="eq:1">[eq:1]</a>)) and the geometrical time delay between the detector and the Earth center. The strain measured at detector $k$ is given by $$\begin{equation}
\begin{split}
h_k(t)=F^k_{+}(\mathbf{r}_k,\theta,\phi,\psi)\, h_{+}(t-\delta t_k) \\
      +F^k_{\times}(\mathbf{r}_k,\theta,\phi,\psi)\, h_{\times}(t-\delta t_k),
\end{split}
\end{equation}$$ where $F^k_{+}$ and $F^k_{\times}$ are the detector antenna response functions for the plus and cross polarizations, respectively, and $\theta,\phi,\psi$ denote the sky location and polarization angle of the source in the Earth-fixed frame. The arrival-time delay between the Earth center and detector $k$ is $$\begin{equation}
\delta t_k = \frac{\mathbf{r}_k \cdot \hat{\mathbf{n}}}{c},
\end{equation}$$ where $\mathbf{r}_k$ is the detector position vector, $\hat{\mathbf{n}}$ is the GW propagation direction, and $c$ is the speed of light.

The observed data stream at detector $k$ is a linear combination of signal and noise, $$\begin{equation}
d_k(t) = n_k(t) + h_k(t),
\end{equation}$$ where $n_k(t)$ denotes the detector noise.

To account for observational variability, we consider randomly oriented sources. For axisymmetric CCSN simulations, the GW amplitude scales approximately as $\propto \sin^2\alpha$, where $\alpha$ is the angle between the stellar rotation axis and the line of sight . Since the emitted GW signal is axisymmetric, the cross polarization vanishes ($h_{\times}=0$), and only the plus polarization contributes to the detector response. We inject signals in time domain. Before injection, to suppress edge effects and reduce spectral leakage, each signal is tapered using a Tukey window  with $\alpha=0.1$. The data is then whitened using the detector PSD and bandpass-filtered between 20 and 2000 Hz. The processed strain is segmented into 70 ms windows, while the CCSN signals themselves have a typical duration of 8 ms. To account for the uncertainty in the core-bounce time, each signal is injected with a random bounce-time uncertainty of $\Delta t_{\rm b}=20$ ms.

After preprocessing, each strain segment is transformed into the frequency domain using a Fourier transform. The resulting frequency-domain representation is used as input to the DL model described in Section <a href="#sec:CNN" data-reference-type="ref" data-reference="sec:CNN">3.3</a>, as our previous work demonstrated its superior performance over the time-domain representation for CCSN parameter estimation .

## Deep learning parameter estimation

DL has become one of the most powerful approaches for extracting complex nonlinear relationships from high-dimensional data . Among DL methods, Convolutional Neural Networks (CNNs) are particularly effective for analyzing structured signals because they automatically learn hierarchical feature representations directly from the input data through convolutional operations .

<div class="table*">

| Layer | Type         | Parameters                 | Output Shape | Activation |
|:------|:-------------|:---------------------------|:------------:|:----------:|
| 0     | Conv1D       | 32 filters, kernel size 3  | $(142, 32)$  |    ReLU    |
| 1     | MaxPooling1D | Pool size 2                |  $(71, 32)$  |            |
| 2     | Conv1D       | 64 filters, kernel size 3  |  $(69, 64)$  |    ReLU    |
| 3     | MaxPooling1D | Pool size 2                |  $(34, 64)$  |            |
| 4     | Conv1D       | 128 filters, kernel size 3 | $(32, 128)$  |    ReLU    |
| 5     | MaxPooling1D | Pool size 2                | $(16, 128)$  |            |
| 6     | Flatten      |                            |   $(2048)$   |            |
| 7     | Dense        | 512 units                  |   $(512)$    |    ReLU    |
| 8     | Dense        | 256 units                  |   $(256)$    |    ReLU    |
| 9     | Dense        | 3 units                    |    $(3)$     |   Linear   |

</div>

In this work, we employ a one-dimensional CNN to estimate the source parameters from the detector network outputs. The use of a CNN is a natural choice because the network receives multi-channel inputs containing correlated information from multiple GW detectors.

Table <a href="#tab:cnn" data-reference-type="ref" data-reference="tab:cnn">[tab:cnn]</a> summarizes the architecture adopted in this study. The network consists of three convolutional blocks, each composed of a Conv1D layer followed by a MaxPooling1D layer. The convolutional layers use 32, 64, and 128 filters, respectively, with a kernel size of 3 and ReLU activation functions. These layers progressively extract increasingly complex features from the detector data while the pooling operations reduce the dimensionality of the feature maps and improve computational efficiency.

After the final convolutional block, the feature maps are flattened into a one-dimensional feature vector of length 2048. This representation is then passed through two fully connected layers containing 512 and 256 neurons, respectively, each employing ReLU activation. Finally, a linear output layer produces the predicted source parameters ($f_{\mathrm{peak}}$, $T/|W|$, and $D\Delta h$). The complete network contains approximately $1.21 \times 10^{6}$ trainable parameters (i.e., the weights and biases optimized during training).

We train the network using the Adam optimizer  with an initial learning rate of $10^{-3}$. The model parameters are optimized by minimizing the mean absolute error between the predicted and true parameter values. To improve convergence, we employ a learning-rate scheduler that reduces the learning rate by a factor of two whenever the validation loss does not improve for ten consecutive epochs, with a minimum learning rate of $10^{-6}$. In addition, we apply early stopping with a patience of 20 epochs and restore the model weights corresponding to the lowest validation loss to mitigate overfitting and improve generalization. The dataset of 1332 signals is randomly split into 80% training and 20% validation subsets. Unless otherwise stated, all reported results are obtained on the validation set.

To quantify the performance of our parameter estimation framework, we use the coefficient of determination ($R^2$), defined as $$\begin{equation}
R^2 = 1 - \frac{\sum_{i=1}^{N}(y_i-\hat{y}i)^2}
{\sum_{i=1}^{N}(y_i-\bar{y})^2},
\end{equation}$$ where $y_i$ and $\hat{y}_i$ are the true and predicted values of the target parameter for the $i$th sample, $\bar{y}$ is the mean of the true values, and $N$ is the total number of samples. The $R^2$ statistic measures the fraction of the variance in the target parameter that is explained by the model predictions. A value of $R^2=1$ indicates perfect agreement between predictions and observations, whereas $R^2=0$ corresponds to a model that performs no better than predicting the mean of the target variable. Negative values indicate performance worse than this baseline. Consequently, larger $R^2$ values correspond to more accurate parameter recovery, with values approaching unity indicating excellent predictive performance .

# Results

To assess the performance of the parameter estimation framework, we use the CCSN waveforms presented in Section <a href="#sec:data" data-reference-type="ref" data-reference="sec:data">3.1</a> under different detector network configurations and source locations. In all cases, we estimate the peak frequency $f_{\mathrm{peak}}$, rotation rate $T/|W|$, and peak amplitude $D\Delta h$, and compare the predictions with their true values. In our analysis below, we fix the GPS time to $t_{\rm GPS}=1325048418$. This time is chosen arbitrarily and its value does not affect our conclusions.

## Parameter estimation distance

We first assess the distance reach of our parameter estimation framework using current-generation (2G) detector networks. As the distance increases, the signal-to-noise ratio decreases, making parameter recovery more challenging. Consequently, the regression performance is strongly determined by the detector network sensitivity.

In this experiment, we compare how the parameter estimation performance ($R^2$) evolves with source distance for two configurations: the two LIGO interferometers (HL) and the full LIGO–Virgo–KAGRA network (HLVKA). We vary the source distance. For each distance, we sample the sky position ($\theta$ and $\phi$) isotropically to account for different detector antenna responses. We report the mean performance over these sky-position realizations.

Fig. <a href="#fig:distance" data-reference-type="ref" data-reference="fig:distance">2</a> shows the evolution of the $R^2$ score as a function of source distance. We observe no substantial difference between the HL and HLVKA detector networks, suggesting that the inclusion of Virgo and KAGRA provides little improvement in the distance reach because of their lower sensitivities (see Fig. <a href="#fig:ASDs" data-reference-type="ref" data-reference="fig:ASDs">1</a>). For the peak frequency $f_{\mathrm{peak}}$, the distance reach for accurate parameter estimation is approximately $30$ kpc for both network configurations, extending our previous single-detector (LIGO-Hanford) result by about $15$ kpc . This improvement is broadly consistent with the findings of , who also reported an increased parameter estimation range when moving from a single detector to a detector network. In contrast, the parameters $D\Delta h$ and $T/|W|$ remain accurately recoverable out to distances of approximately $200$ kpc and $250$ kpc, respectively. We note that unlike , who distinguish between “favourable” and “unfavourable” detector configurations using the equivalent antenna pattern $F_{\rm eq}$, we fix the $t_{\rm GPS}$ and average over isotropically distributed source locations. Therefore, our quoted distance reaches represent the mean performance across a range of antenna responses rather than a specific configuration.

<figure id="fig:distance" data-latex-placement="t">
<embed src="figures/distance.pdf" style="width:100.0%" />
<figcaption><span class="math inline"><em>R</em><sup>2</sup></span> score as a function of distance for different parameters and detector networks. The blue, orange and green lines correspond to <span class="math inline"><em>T</em>/|<em>W</em>|</span>, <span class="math inline"><em>f</em><sub>peak</sub></span>, and <span class="math inline"><em>D</em><em>Δ</em><em>h</em></span>, respectively. Dashed lines represent HL detector network, while solid lines correspond to HLVKA detector network. The gray horizontal dashed line at <span class="math inline"><em>R</em><sup>2</sup> = 0.8</span> represents a limit for reasonably accurate estimations. Vertical black dashed lines mark reference distances to the Galactic Center (8.2 kpc), and the Large Magellanic Cloud (49.8 kpc).</figcaption>
</figure>

Overall, the current detector network enables accurate recovery of all three parameters for rotating Galactic CCSNe, with the distance reach primarily limited by the estimation of $f_{\mathrm{peak}}$.

## Sky coverage

Having established the distance reach of the parameter estimation framework, we now investigate its sky coverage. Specifically, we examine how the addition of detectors to the network improves parameter estimation performance across different source locations on the sky. Since the detector response depends on the source position through the antenna pattern functions, the estimation performance is expected to vary across the celestial sphere. Adding detectors with different orientations and geographical locations should therefore improve the sky coverage.

In this experiment, we fix the source distance to 8.2 kpc. We isotropically sample the sky position ($\theta$ and $\phi$) and evaluate the parameter estimation performance for four detector configurations: HL, HLV, HLVK, and HLVKA.

Fig. <a href="#fig:skymap" data-reference-type="ref" data-reference="fig:skymap">3</a> shows the distribution of the $R^2$ score over the sky for the parameters $T/|W|$, $f_{\mathrm{peak}}$, and $D\Delta h$. The detector response varies with sky position, producing localized regions of reduced parameter estimation performance that coincide with the antenna pattern minima of the detector network. As additional interferometers are included, these low-performance regions become progressively smaller, resulting in a more uniform sky coverage.

<figure id="fig:skymap" data-latex-placement="htbp">
<img src="figures/skymap.png" style="width:95.0%" />
<figcaption>Sky maps of the <span class="math inline"><em>R</em><sup>2</sup></span> score for the three estimated parameters and four detector network configurations. Columns correspond to the detector networks (HL, HLV, HLVK, and HLVKA), while rows correspond to the estimated parameters. Colors indicate the parameter estimation performance, with warmer colors representing lower <span class="math inline"><em>R</em><sup>2</sup></span> values and cooler colors representing higher <span class="math inline"><em>R</em><sup>2</sup></span> values.</figcaption>
</figure>

The parameters $T/|W|$ and $D\Delta h$ exhibit excellent performance across almost the entire sky for all detector configurations. Even for the HL network, only small localized regions show a modest reduction in performance, with $R^2$ remaining above $\sim0.9$. In contrast, the estimation of $f_{\mathrm{peak}}$ is considerably more sensitive to the source sky position. For the HL network, the antenna pattern minima produce extended regions with $R^2$ values as low as $\sim0.6$, together with noticeable variations across the rest of the sky.

The inclusion of Virgo, KAGRA, and LIGO Aundha progressively mitigates these directional effects. The addition of Virgo substantially reduces the regions of poor $f_{\mathrm{peak}}$ recovery, while KAGRA further improves the uniformity of the sky maps. The full HLVKA network provides the most homogeneous performance, nearly eliminating the blind spots for $T/|W|$ and $D\Delta h$ and increasing the minimum $R^2$ for $f_{\mathrm{peak}}$ to approximately $0.8$ across the sky. Similar improvements in sky coverage with increasingly larger detector networks were reported by .

To quantify this improvement, Fig. <a href="#fig:coverage" data-reference-type="ref" data-reference="fig:coverage">4</a> shows the fraction of the sky for which the parameter estimation performance exceeds a given $R^2$ threshold. The inclusion of Virgo, KAGRA, and LIGO Aundha systematically increases the sky coverage for all three parameters. For instance, at $R^2=0.8$, the sky coverage for $f_{\mathrm{peak}}$ increases from 0.89 for the HL network to 0.90, 0.93, and 0.96 for the HLV, HLVK, and HLVKA configurations, respectively. In contrast, the sky coverage for $T/|W|$ and $D\Delta h$ is already close to unity for the HL network for a Galactic CCSN event, resulting in smaller absolute gains as additional detectors are added. Nevertheless, both parameters exhibit the same systematic trend, with each new interferometer further increasing the sky coverage and reducing the remaining regions of lower parameter estimation performance.

<figure id="fig:coverage" data-latex-placement="htbp">
<embed src="figures/coverage.pdf" style="width:80.0%" />
<figcaption>Sky coverage as a function of the <span class="math inline"><em>R</em><sup>2</sup></span> score for different parameters and detector network configurations. The blue, orange, and green curves correspond to <span class="math inline"><em>T</em>/|<em>W</em>|</span>, <span class="math inline"><em>f</em><sub>peak</sub></span>, and <span class="math inline"><em>D</em><em>Δ</em><em>h</em></span>, respectively. Dotted, dash-dotted, dashed, and solid lines represent the HL, HLV, HLVK, and HLVKA detector networks, respectively. The gray vertical dashed line at <span class="math inline"><em>R</em><sup>2</sup> = 0.8</span> marks a threshold for accurate parameter estimation and serves as a reference for comparing the sky coverage of different detector networks.</figcaption>
</figure>

Overall, the addition of detectors systematically improves the sky coverage of the parameter estimation framework by reducing the directional dependence of the detector response. While the improvement is most pronounced for $f_{\mathrm{peak}}$, all three parameters benefit from the increased geographical diversity of the detector network.

## Third-generation detectors

Finally, we assess the distance reach of our parameter estimation framework using 3G detectors. As discussed in Section <a href="#sec:detectors" data-reference-type="ref" data-reference="sec:detectors">2</a>, the substantially improved sensitivity of 3G observatories is expected to extend the distance reach for CCSN observations.

In this experiment, we repeat the analysis described in Section <a href="#sec:PE" data-reference-type="ref" data-reference="sec:PE">4.1</a> using the detector network consisting of three detectors (ET-CE20-CE40). We vary the source distance. As before, we isotropically sample the sky position ($\theta$ and $\phi$) and report the mean performance over all sky-position realizations.

Fig. <a href="#fig:3G" data-reference-type="ref" data-reference="fig:3G">5</a> shows the evolution of the $R^2$ score as a function of source distance. Compared to the current-generation detector network (cf. Fig. <a href="#fig:distance" data-reference-type="ref" data-reference="fig:distance">2</a>), the distance reach is substantially increased for all three parameters owing to the improved detector sensitivity. For the peak frequency $f_{\mathrm{peak}}$, the distance reach for accurate parameter estimation ($R^2 \ge 0.8$) increases from approximately $30$ kpc to $\sim300$ kpc, corresponding to an order-of-magnitude improvement. In contrast, the parameters $D\Delta h$ and $T/|W|$ remain accurately recoverable out to distances of approximately $2$ Mpc and $2.5$ Mpc, respectively. At the distance of the Large Magellanic Cloud ($49.8$ kpc), all three parameters achieve $R^2\gtrsim0.9$, while even at the distance of the Andromeda galaxy ($770$ kpc), $T/|W|$ and $D\Delta h$ retain high parameter estimation performance with $R^2\approx0.95$ and $0.94$, respectively.

<figure id="fig:3G" data-latex-placement="t">
<embed src="figures/ECC.pdf" style="width:100.0%" />
<figcaption><span class="math inline"><em>R</em><sup>2</sup></span> score as a function of distance for different parameters with ET-CE20-CE40 detector network. The blue, orange and green lines correspond to <span class="math inline"><em>T</em>/|<em>W</em>|</span>, <span class="math inline"><em>f</em><sub>peak</sub></span>, and <span class="math inline"><em>D</em><em>Δ</em><em>h</em></span>, respectively. The gray horizontal dashed line at 0.8 represents a limit for reasonably accurate estimations. Vertical black dashed lines indicate distances to the Galactic Center (8.2 kpc), the Large Magellanic Cloud (49.8 kpc), and Andromeda (780 kpc).</figcaption>
</figure>

Overall, the improved sensitivity of 3G detectors substantially extends the distance reach of the parameter estimation framework. While accurate recovery of $f_{\mathrm{peak}}$ becomes possible out to several hundred kiloparsecs, the parameters $T/|W|$ and $D\Delta h$ remain accurately recoverable to distances of several megaparsecs, greatly expanding the astrophysical reach of machine-learning-based parameter estimation.

# Conclusion

In this work, we have presented a DL framework for estimating the physical properties of rotating CCSNe from their GW signals. Building upon our previous single-detector study , we have extended the methodology to arbitrary detector networks. Using CNNs, we have estimated the peak frequency, $f_{\mathrm{peak}}$, rotation rate, $T/|W|$, and peak amplitude, $D\Delta h$ directly from noisy detector data under realistic observing conditions. Our study has been further motivated from the work of who showed that a network of 3G detectors can significantly improve the recovery of PNS properties for nonrotating CCSN models.

Our results show that the proposed framework provides accurate inferences for all three physical parameters. Among them, the recovery of $f_{\mathrm{peak}}$ is the most challenging, while $T/|W|$ and $D\Delta h$ remain robustly recoverable over substantially larger distances. For current-generation detector networks, accurate estimation of $f_{\mathrm{peak}}$ is limited to approximately $30$ kpc, extending our previous single-detector results by about $15$ kpc. In contrast, $D\Delta h$ and $T/|W|$ remain accurately recoverable out to distances of approximately $200$ kpc and $250$ kpc, respectively (cf. Section <a href="#sec:PE" data-reference-type="ref" data-reference="sec:PE">4.1</a>).

We have also investigated the dependence of the parameter estimation performance on the detector network configuration and source sky position. While the addition of Virgo, KAGRA, and LIGO Aundha provides only a modest improvement in the average distance reach because of their lower sensitivities, it significantly improves the sky coverage by reducing the directional dependence introduced by the detector antenna patterns. The largest improvement is observed for $f_{\mathrm{peak}}$, whose recovery is the most sensitive to the source location, whereas $T/|W|$ and $D\Delta h$ achieve nearly complete sky coverage even for the HL detector network (cf. Section <a href="#sec:sky_cov" data-reference-type="ref" data-reference="sec:sky_cov">4.2</a>).

Finally, we have assessed the capabilities of 3G detector networks consisting of the ET and CE observatories. Owing to their substantially improved sensitivities, the distance reach for accurate parameter estimation is increased by nearly an order of magnitude for $f_{\mathrm{peak}}$, extending to approximately $300$ kpc. For $D\Delta h$ and $T/|W|$, accurate parameter estimation becomes possible out to distances of approximately $2$ Mpc and $2.5$ Mpc, respectively, enabling reliable inference for CCSNe throughout the Local Group and into the nearby Universe (cf. Section <a href="#sec:third_gen" data-reference-type="ref" data-reference="sec:third_gen">4.3</a>).

Compared to the results of , we find larger distance reaches for parameter estimation. Since their study considered non-rotating CCSNe, while ours focuses on rotating progenitors, this comparison suggests that source properties can be recovered out to larger distances for rotating events. The most likely reason is that rotating CCSNe produce stronger GW emission during core bounce and the early post-bounce phase, resulting in higher signal-to-noise ratios and more robust parameter recovery .

Although these results demonstrate the strong potential of DL for CCSN parameter estimation, several limitations remain. Our analysis is restricted to rotating CCSN models and considers only the bounce and early post-bounce GW signal, which does not capture the full complexity of CCSN emission. Furthermore, the analysis does not account for non-stationary detector noise. Addressing these limitations will be the focus of future work.

<div class="acknowledgments">

We thank António Onofre, Nurzhan Ussipov and Marat Zaidyn for fruitful discussions during the course of this work. We also thank Nelson Christensen for his comments on this manuscript. This research was funded by the Science Committee of the Ministry of Science and Higher Education of the Republic of Kazakhstan (Grant No. AP26103591). EA is partially supported by the Nazarbayev University Faculty Development Competitive Research Grant Program (no. 040225FD4713). SN was supported by FCT - Fundação para a Ciência e Tecnologia, I.P. by project reference 2025.02005.BD and DOI identifier https://doi.org/10.54499/2025.02005.BD. SN acknowledges financial support by FCT in the framework of the Strategic Funding UID/04650/2025. JAF is supported by the Spanish Agencia Estatal de Investigación (grant PID2024-159689NB-C21) funded by MICIU/AEI/10.13039/501100011033 and by FEDER / EU, and by the Generalitat Valenciana (Prometeo Excellence Programme grant CIPROM/2022/49). AI-based language tools were used to improve the clarity and grammar of the manuscript.

</div>

[^1]: `aLIGOAPlusDesignSensitivityT1800042` from `PyCBC`

[^2]: `AdvVirgo` from `PyCBC`

[^3]: `KAGRADesignSensitivityT1600593` from `PyCBC`

[^4]: `EinsteinTelescopeP1600143` from `PyCBC`

[^5]: `CosmicExplorerP1600143` for 40 km and `CosmicExplorerPessimisticP1600143` for 20 km from `PyCBC`

[^6]: Available at https://zenodo.org/records/17579189
