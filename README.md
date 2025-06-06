Quantification of Motorcyclist Risky Behavior – RA Log

Naturalistic Driving Study • MIROS SCRF ANCHOR V (EN101264) • UTAR × Taylor’s University

📑 Project Overview

This repository documents the end‑to‑end workflow and weekly reflections for the “Quantification of Motorcyclist Risky Behavior Using a Naturalistic Driving Study Approach” research assistantship (March – May 2025). The study captures real‑world ride data with an IoT sensor stack (GPS, IMU, video, CAN, and environmental probes) to identify patterns that correlate with risky maneuvers on Malaysian roads.

🔑 Key Insights (to‑date)

Regulatory Focus vs. Enforcement GapGovernment bodies predominantly want to quantify risk, but rarely enforce corrective measures at scale. Our dataset can bridge this “knowledge–action” gap by showing where and why risky riding spikes.

IoT‑Driven Personal VerificationLow‑cost sensor fusion (GPS + IMU + vision) is emerging as the de‑facto method for behavioural verification, surpassing self‑reported surveys.

Edge Processing MattersEarly feature extraction on Raspberry Pi 5 significantly reduces storage overhead and protects rider privacy by discarding raw video off‑device when not required.

Context‑Aware Labelling > Generic ThresholdsSpeed or acceleration cut‑offs alone misclassify risk; integrating road type, traffic density, and weather produces richer insights.

🎓 Lessons Learned

Understand the anatomy of GPIO pins
Double check python code
Be scientific with your steps
Be careful with electronics, dont fry
Journal when bored




🛠️ Hardware Bill‑of‑Materials (v1.2)

Raspberry Pi 5 (8 GB) + active cooler

A7670SA 4G‑GNSS module @ /dev/ttyUSB3

Arducamera IMX219 camera (30 fps, 720p)

12 V‑to‑5 V DC‑DC buck converter (3 A)

Waterproof enclosure (IP65)

Detailed wiring diagrams are found under hardware/diagrams/.

📈 Analysis Pipeline

Segmentation – rides split by ignition events.

Feature Extraction – speed, jerk, lean angle, throttle variance.

Risk Scoring – weighted logistic model calibrated on crash literature.

Visualisation – interactive maps and time‑series via Plotly Dash (planned).

🧑‍💼 Acknowledgements

Malaysian Institute of Road Safety Research (MIROS) – funding & technical input.

UTAR Research & Development Administration (IPS R) for administrative support.

All volunteer riders who made the Naturalistic Driving Study possible.

“Safety data is most powerful when it moves decision‑makers from knowing to doing.”

