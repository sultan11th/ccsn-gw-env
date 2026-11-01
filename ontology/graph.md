# Concept graph

Generated from `ontology/concepts.yaml` by `python3 src/ontology.py graph` (41 concepts, 49 relations). Do not edit by hand.

Arrows: `-->` is_a / part_of, `==>` depends_on, `-.->` estimates / uses, `---` related_to.

```mermaid
graph LR
  subgraph physics["Stellar collapse physics"]
    ccsn["Core-collapse supernova"]
    core_collapse["Core collapse"]
    core_bounce["Core bounce"]
    pns["Proto-neutron star"]
    rotation["Core rotation"]
    rotation_ratio["Rotation ratio T/|W|"]
    differential_rotation["Differential rotation (parameter A)"]
    eos["Nuclear equation of state"]
    electron_capture["Electron-capture rates"]
    inner_core_mass["Inner-core mass at bounce"]
    progenitor_mass["Progenitor and iron-core mass"]
  end
  subgraph signal["GW signal"]
    gw_signal["CCSN GW signal"]
    bounce_signal["Bounce signal"]
    bounce_amplitude["Bounce amplitude"]
    ringdown["Early post-bounce ring-down"]
    f_peak["Peak frequency f_peak"]
    dynamical_frequency["Dynamical frequency sqrt(G rho_c)"]
    pns_modes["PNS oscillation modes"]
    sasi["Standing accretion shock instability"]
    waveform_catalog["Waveform catalog"]
  end
  subgraph detection["Detectors and data"]
    detector["GW detector"]
    einstein_telescope["Einstein Telescope"]
    cosmic_explorer["Cosmic Explorer"]
    detector_network["Detector network"]
    detector_noise["Detector noise"]
    snr["Signal-to-noise ratio"]
    distance["Source distance"]
    orientation["Source orientation"]
    bounce_time_uncertainty["Bounce-time uncertainty"]
  end
  subgraph ml["Machine learning and inference"]
    ml_task["ML task"]
    eos_classification["EOS classification"]
    mass_classification["Progenitor-mass classification"]
    parameter_estimation["Parameter estimation"]
    bayesian_inference["Bayesian inference"]
    cnn["Convolutional neural network"]
    classical_ml["Classical ML models"]
    entropy_features["Entropy features"]
    validation["Validation protocol"]
    loeo["Leave-one-EOS-out validation"]
    xai["Explainable AI"]
    shap["SHAP"]
  end
  core_collapse -->|part_of| ccsn
  core_bounce -->|part_of| ccsn
  core_bounce ==>|depends_on| eos
  core_bounce ==>|depends_on| inner_core_mass
  pns -->|part_of| ccsn
  rotation_ratio -->|is_a| rotation
  differential_rotation -->|is_a| rotation
  inner_core_mass ==>|depends_on| electron_capture
  inner_core_mass ==>|depends_on| eos
  gw_signal -->|part_of| ccsn
  bounce_signal -->|is_a| gw_signal
  bounce_signal ==>|depends_on| rotation_ratio
  bounce_signal ==>|depends_on| differential_rotation
  bounce_amplitude -->|part_of| bounce_signal
  bounce_amplitude ==>|depends_on| rotation_ratio
  bounce_amplitude ==>|depends_on| distance
  ringdown -->|is_a| gw_signal
  ringdown ==>|depends_on| pns_modes
  f_peak -->|part_of| ringdown
  f_peak ==>|depends_on| dynamical_frequency
  f_peak ==>|depends_on| rotation_ratio
  dynamical_frequency ==>|depends_on| eos
  pns_modes -->|part_of| pns
  sasi -->|is_a| gw_signal
  waveform_catalog -.->|uses| gw_signal
  einstein_telescope -->|is_a| detector
  cosmic_explorer -->|is_a| detector
  detector_network -.->|uses| detector
  detector_noise ---|related_to| detector
  snr ==>|depends_on| distance
  snr ==>|depends_on| detector_noise
  snr ==>|depends_on| orientation
  eos_classification -->|is_a| ml_task
  eos_classification -.->|estimates| eos
  eos_classification -.->|uses| waveform_catalog
  mass_classification -->|is_a| ml_task
  mass_classification -.->|estimates| progenitor_mass
  parameter_estimation -->|is_a| ml_task
  parameter_estimation -.->|estimates| f_peak
  parameter_estimation -.->|estimates| rotation_ratio
  parameter_estimation -.->|estimates| bounce_amplitude
  bayesian_inference -->|is_a| parameter_estimation
  cnn -.->|uses| waveform_catalog
  classical_ml -.->|uses| waveform_catalog
  entropy_features ---|related_to| classical_ml
  validation ---|related_to| ml_task
  loeo -->|is_a| validation
  xai ---|related_to| ml_task
  shap -->|is_a| xai
```
