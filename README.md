# No Nonsense Summary
## 🔑 Key Insights (to‑date)

1. **Regulatory Focus vs. Enforcement Gap**   Government bodies predominantly **want to quantify risk**, but **rarely enforce** corrective measures at scale. Our dataset can bridge this “knowledge–action” gap by showing *where* and *why* risky riding spikes.
2. **IoT‑Driven Personal Verification**   Low‑cost sensor fusion (GPS + IMU + vision) is emerging as the **de‑facto method for behavioural verification**, surpassing self‑reported surveys.
3. **Edge Processing Matters**   Early feature extraction on Raspberry Pi 5 significantly reduces storage overhead and protects rider privacy by discarding raw video off‑device when not required.
4. **Context‑Aware Labelling > Generic Thresholds**   Speed or acceleration cut‑offs alone misclassify risk; integrating *road type*, *traffic density*, and *weather* produces richer insights.
5. **Mastering** different types of perception modules and reading through their manual is challenging like A7670SA vs SIM7000E

---

## 🎓 Lessons Learned

Understand the anatomy of GPIO pins
Double check python code 
Be scientific with your steps
Be careful with electronics, dont fry
Journal when boared

---

## 🛠️ Hardware Bill‑of‑Materials (v1.2)

- Raspberry Pi 5 (8 GB) + active cooler
- **A7670SA** 4G‑GNSS module @ `/dev/ttyUSB3`
- Arducamera IMX219 camera (30 fps, 720p)
- 12 V‑to‑5 V DC‑DC buck converter (3 A)
- Waterproof enclosure (IP65)

Detailed wiring diagrams are found under **`hardware/diagrams/`**.

---

## 📈 Analysis Pipeline

1. **Segmentation** – rides split by ignition events.
2. **Feature Extraction** – speed, jerk, lean angle, throttle variance.
3. **Risk Scoring** – weighted logistic model calibrated on crash literature.
4. **Visualisation** – interactive maps and time‑series via Plotly Dash (planned).

---

## 🧑‍💼 Acknowledgements

- Malaysian Institute of Road Safety Research (MIROS) – funding & technical input.
- UTAR Research & Development Administration (IPS R) for administrative support.
- All volunteer riders who made the Naturalistic Driving Study possible.

> *“Safety data is most powerful when it moves decision‑makers from ****************************************************knowing**************************************************** to ****************************************************doing****************************************************.”*
