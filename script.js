async function makePrediction() {
    const inputs = [
        'battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g',
        'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height',
        'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g',
        'touch_screen', 'wifi'
    ];

    let data = {};
    let allFilled = true;

    inputs.forEach(id => {
        let element = document.getElementById(id);
        let val = element.value;

        if (val === "") {
            allFilled = false;
            element.style.borderColor = "red";
        } else {
            element.style.borderColor = "#ddd";
        }

        data[id] = val;
    });

    if (!allFilled) {
        alert("⚠️ Please fill in all fields!");
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.className = "result-box loading";
    resultDiv.innerHTML = "🔄 Predicting price range...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            resultDiv.className = "result-box result-error";
            resultDiv.innerHTML = "❌ " + result.error;
        } else {
            resultDiv.className = "result-box result-success";
            resultDiv.innerHTML = `💰 Predicted Price Range: <br><strong>${result.prediction}</strong>`;
        }
    } catch (error) {
        console.error(error);
        resultDiv.className = "result-box result-error";
        resultDiv.innerHTML = "🚫 Failed to connect to server.";
    }
}
