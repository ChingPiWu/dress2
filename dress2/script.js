document.addEventListener("DOMContentLoaded", function () {
    // 切換 Tab
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

    // 取得從我的衣櫥獲取服裝按鈕
    const btnGetFromWardrobe = document.getElementById("btn-get-from-wardrobe");
    const btnGetFromDatabase = document.getElementById("btn-get-from-database");

    const wardrobeContent = document.getElementById("wardrobe-content");

    btnGetFromWardrobe.addEventListener("click", function () {
        wardrobeContent.innerHTML = "<p>從我的衣櫥獲取服裝：這是您衣櫥中的所有服裝。</p>";
    });

    btnGetFromDatabase.addEventListener("click", function () {
        wardrobeContent.innerHTML = "<p>從資料庫衣櫥獲取服裝：這是資料庫中的服裝。</p>";
    });
});
