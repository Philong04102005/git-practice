/**
 * Tự động cuộn trang Facebook và thu thập Tên (Name) và Liên kết hồ sơ (Link) 
 * của tất cả bạn bè hiện có trên trang.
 */

const SCROLL_INTERVAL_MS = 2000; // Thời gian chờ giữa các lần cuộn
let autoCollectInterval;
let lastHeight = 0;
let runCount = 0;
const uniqueProfiles = new Set();
const finalResult = [];

// --- HÀM TẢI FILE CSV ---
function downloadCSV(data) {
    if (data.length === 0) {
        console.log("[LỖI TẢI] Không có dữ liệu để tạo file CSV.");
        return;
    }
    
    // Tạo nội dung CSV: Header
    const header = Object.keys(data[0]).join(',') + '\n';
    
    // Tạo nội dung CSV: Data rows
    const csvContent = data.map(row => Object.values(row).map(e => `"${String(e).replace(/"/g, '""')}"`).join(',')).join('\n');
    // Đảm bảo e là chuỗi trước khi gọi .replace()   
    const fullCSV = header + csvContent;
    
    // Tạo Blob và URL cho file
    const blob = new Blob([fullCSV], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    // Tạo liên kết tải xuống ảo và tự động click
    const a = document.createElement('a');
    a.href = url;
    a.download = 'friends_acc_.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    console.log(`[TẢI VỀ] Tải file 'friends_acc_.csv' thành công (${data.length} hồ sơ).`);
}

function collectProfileLinksAndScroll() {
    runCount++;
    console.log(`\n============================`);
    console.log(`[VÒNG LẶP] Lần chạy thứ ${runCount}.`);

    // --- 1. THU THẬP DỮ LIỆU TỪ NỘI DUNG ĐÃ TẢI ---
    const allLinks = document.querySelectorAll('a[role="link"]');
    let collectedThisRun = 0;
    
    allLinks.forEach(link => {
        const name = link.textContent.trim();
        // Lấy href và loại bỏ các tham số tracking ('?' và '&')
        let href = link.href

        // Bỏ qua các liên kết không phải hồ sơ cá nhân
        if (!name || name.length <= 2 || !href || 
            href.includes('/groups/') || 
            href.includes('/onthisday/') || 
            href.includes('/saved/') || 
            href.includes('/marketplace/') || 
            href.includes('/policies') || 
            href.includes('/help/') || 
            href.includes('/business/') || 
            href.includes('/stories/') || 
            href.includes('/GoogleAds') || 
            href.includes('/notifications/') || 
            href.includes('/watch/') ||
            href.includes('friends_mutual') || // Loại trừ bạn chung
            href.includes('/videos/') || // Loại trừ video
            href.includes('/pages/') || // Loại trừ trang fanpage
            !href.startsWith('https://www.facebook.com/') || // Phải là link Facebook
            href.includes('/friends/') ||
            href.includes('/professional_dashboard/overview/') || 
            href.includes('&sk=')  

        ) {
            return;
        }
        
        // Chỉ thêm vào danh sách nếu là link mới
        if (!uniqueProfiles.has(href)) {
            uniqueProfiles.add(href);
            finalResult.push({
                name: name,
                link: href,
                status: false
            });
            collectedThisRun++;
        }
    });

    console.log(`[THU THẬP] Đã tìm thấy thêm ${collectedThisRun} hồ sơ mới. Tổng cộng: ${finalResult.length} hồ sơ.`);
    
    // --- 2. CUỘN XUỐNG CUỐI TRANG VÀ KIỂM TRA DỪNG ---
    const currentHeight = document.body.scrollHeight;
    window.scrollTo(0, currentHeight); 
    
    console.log("[CUỘN] Đã cuộn xuống cuối trang. Đang chờ nội dung tải...");
    
    // Thiết lập thời gian chờ để kiểm tra điều kiện dừng
    setTimeout(() => {
        const newHeight = document.body.scrollHeight;
        
        // ĐIỀU KIỆN DỪNG: Chiều cao không đổi VÀ không có hồ sơ mới nào được thu thập trong lần chạy này
        if (newHeight <= lastHeight && collectedThisRun === 0) {
            console.log(`\n============================`);
            console.log("[KẾT THÚC] Đã cuộn đến cuối trang và không còn nội dung mới.");
            console.log(`[TỔNG KẾT] Đã thu thập ${finalResult.length} hồ sơ.`);
            clearInterval(autoCollectInterval); // Dừng vòng lặp tự động
            console.table(finalResult); // In bảng kết quả cuối cùng

            // TẢI FILE TỰ ĐỘNG Ở ĐÂY
            downloadCSV(finalResult);

            return;
        }
        
        // Tiếp tục vòng lặp nếu có nội dung mới
        lastHeight = newHeight;
        
    }, SCROLL_INTERVAL_MS - 500);
}

// Bắt đầu vòng lặp tự động
console.log(`[BẮT ĐẦU] Script sẽ chạy và cuộn lặp lại mỗi ${SCROLL_INTERVAL_MS / 1000} giây.`);
autoCollectInterval = setInterval(collectProfileLinksAndScroll, SCROLL_INTERVAL_MS);


// CÁCH DỪNG: Nhập 'clearInterval(autoCollectInterval)' vào Console bất cứ lúc nào để dừng.