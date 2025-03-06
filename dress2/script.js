document.addEventListener("DOMContentLoaded", function () {
    // ==========  1️⃣ 切換 Tab 功能  ==========
    const buttons = document.querySelectorAll("nav button");
    const tabs = document.querySelectorAll(".tab-content");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            buttons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            let targetTabId = this.id.replace("btn-", "") + "-tab";
            tabs.forEach(tab => {
                tab.classList.remove("active");
                if (tab.id === targetTabId) {
                    tab.classList.add("active");
                }
            });
        });
    });

    // ==========  2️⃣ 圖片預覽與上傳功能  ==========
    const fileInput = document.getElementById("fileInput");
    const uploadButton = document.getElementById("uploadButton");
    const imagePreview = document.getElementById("imagePreview");
    const imagePreviewContainer = document.getElementById("imagePreviewContainer");
    const resultContainer = document.getElementById("resultContainer"); // ✅ 確保獲取元素
    const predictionResult = document.getElementById("predictionResult");

    const backendUrl = "http://127.0.0.1:8000/predict"; // 確保 FastAPI 正確運行

    // 📌 圖片選擇並顯示預覽
    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imagePreview.src = e.target.result;
                imagePreviewContainer.style.display = "block";
                resultContainer.style.display = "none"; // 🔹 清除舊的結果
                predictionResult.innerHTML = "";
            };
            reader.readAsDataURL(file);
        }
    });

    // 📌 點擊上傳按鈕，發送 API 請求
    uploadButton.addEventListener("click", function () {
        const file = fileInput.files[0];

        if (!file) {
            alert("請選擇一張圖片！");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        console.log("📤 正在上傳圖片:", formData.get("file"));

        fetch(backendUrl, {
            method: "POST",
            body: formData,
            mode: "cors"
        })
        .then(response => {
            console.log("回應狀態碼:", response.status);
            if (!response.ok) {
                throw new Error(`伺服器錯誤: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("後端回應:", data);
            if (data.error) {
                predictionResult.innerHTML = `<span style="color: red;">錯誤: ${data.error}</span>`;
            } else {
                predictionResult.innerHTML = `
                    <p>🔍 預測類別: <strong>${data.prediction}</strong></p>
                    <p>🌡 適合溫度: <strong>${data.temperature_range}</strong></p>
                `;
                resultContainer.style.display = "block"; // ✅ 顯示結果區域
            }
        })
        .catch(error => {
            console.error("❌ 發生錯誤:", error);
            alert("圖片上傳失敗，請稍後再試！");
        });
    });
});


