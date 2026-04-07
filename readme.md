# TravelBuddy Agent Test Results
Date: 2026-04-07 16:29:12

## Test 1 - Direct Answer
**User Input:** Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**Expected Behavior:** Agent chào hỏi, hỏi thêm sở thích/ngân sách, không gọi tool.

**Actual Execution Log:**
```text
🤖 Response: Xin chào! Rất vui được giúp bạn lên kế hoạch du lịch. Để tôi có thể gợi ý những lựa chọn phù hợp nhất, bạn có thể cho tôi biết thêm một few thông tin sau nhé:

1. **Điểm đến mong muốn** (hoặc nếu chưa có ý tưởng, bạn thích loại hình du lịch nào? Biển, núi, thành phố văn hóa, ẩm thực…)
2. **Ngân sách tổng ước tính** cho chuyến đi (bao gồm vé máy bay, khách sạn, chi phí ăn uống, đi lại nội địa…)
3. **Thời gian bạn định đi** (ngày khởi hành và ngày Rückkehr, hoặc chỉ là tháng/ mùa bạn muốn đi)
4. **Số người đi cùng** và nếu có yêu cầu đặc biệt (khách sạn 3 sao trở lên, muốn gần biển, muốn đặt vé économiques…)

Khi có đủ thông tin này, tôi sẽ sử dụng công cụ tìm kiếm vé máy bay và khách sạn thực tế để đưa ra các lựa chọn tốt nhất cho bạn. Mong nhận được phản hồi từ bạn nhé!
```
---

## Test 2 - Single Tool Call
**User Input:** Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

**Expected Behavior:** Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.

**Actual Execution Log:**
```text
🛠️ Tool Call: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
🤖 Response: Danh sách chuyến bay giữa Hà Nội và Đà Nẵng:
- Vietnam Airlines (economy): 06:00 -> 07:20 | Giá: 1.450.000đ
- Vietnam Airlines (business): 14:00 -> 15:20 | Giá: 2.800.000đ
- VietJet Air (economy): 08:30 -> 09:50 | Giá: 890.000đ
- Bamboo Airways (economy): 11:00 -> 12:20 | Giá: 1.200.000đ

🤖 Response: Tìm được vài chuyến bay từ Hà Nội đi Đà Nẵng cho bạn nè! Đây là các tùy chọn hiện có:

**Chuyến bay Hà Nội → Đà Nẵng:**
1. **VietJet Air (economy)**: 08:30 → 09:50 | Giá: **890.000đ**  
   → Tiết kiệm nhất, bay sáng sớm.

2. **Bamboo Airways (economy)**: 11:00 → 12:20 | Giá: **1.200.000đ**  
   → Giá trung bình, bay trưa.

3. **Vietnam Airlines (economy)**: 06:00 → 07:20 | Giá: **1.450.000đ**  
   → Hãng full-service, bay rất sớm.

4. **Vietnam Airlines (business)**: 14:00 → 15:20 | Giá: **2.800.000đ**  
   → Lớp thương gia, nếu bạn muốn thoải mái hơn.

Bạn có ý định đi ngày nào vậy? Khi đã chọn chuyến bay, mình có thể giúp bạn tìm khách sạn phù hợp với ngân sách ở Đà Nẵng hoặc tính toán tổng chi phí chuyến đi luôn nhé! 😊
```
---

## Test 3 - Multi-Step Tool Chaining
**User Input:** Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**Expected Behavior:** Chuỗi nhiều bước: Tìm vé rẻ nhất -> Tìm khách sạn -> Tính budget -> Tổng hợp.

**Actual Execution Log:**
```text
🛠️ Tool Call: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
🤖 Response: Danh sách chuyến bay giữa Hà Nội và Phú Quốc:
- Vietnam Airlines (economy): 07:00 -> 09:15 | Giá: 2.100.000đ
- VietJet Air (economy): 10:00 -> 12:15 | Giá: 1.350.000đ
- VietJet Air (economy): 16:00 -> 18:15 | Giá: 1.100.000đ

🛠️ Tool Call: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1500000})
🤖 Response: Danh sách khách sạn tại Phú Quốc phù hợp với yêu cầu của bạn (đã sắp xếp theo đánh giá):
- 9Station Hostel (2 sao)
  + Khu vực: Dương Đông
  + Giá: 200.000đ/đêm
  + Đánh giá: 4.5/5
- Sol by Meliá (4 sao)
  + Khu vực: Bãi Trường
  + Giá: 1.500.000đ/đêm
  + Đánh giá: 4.2/5
- Lahana Resort (3 sao)
  + Khu vực: Dương Đông
  + Giá: 800.000đ/đêm
  + Đánh giá: 4.0/5

🛠️ Tool Call: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:1600000'})
🤖 Response: Bảng chi phí:
- Vé_máy_bay: 1.100.000đ
- Khách_sạn: 1.600.000đ
---
Tổng chi: 2.700.000đ
Ngân sách: 5.000.000đ
Còn lại: 2.300.000đ
🤖 Response: **Chuyến bay:**  
- VietJet Air (economy) – 16:00 → 18:15, giá **1.100.000đ** (khởi hành từ Hà Nội, đến Phú Quốc).  
*(Có thể chọn Vietnam Airlines 2.100.000đ hoặc VietJet 1.350.000đ nếu muốn thời gian khác.)*

**Khách sạn (2 đêm):**  
- Lahana Resort (3 sao, Dương Đông) – **800.000đ/đêm** → tổng **1.600.000đ** (đánh giá 4.0/5).  
*(Lựa chọn tiết kiệm hơn: 9Station Hostel 200.000đ/đêm → 400.000đ tổng; hoặc sang trọng hơn: Sol by Meliá 1.500.000đ/đêm → 3.000.000đ tổng.)*

**Tổng chi phí ước tính (vé + khách sạn):**  
- Vé máy bay: 1.100.000đ  
- Khách sạn (2 đêm): 1.600.000đ  
**= 2.700.000đ**

**Ngân sách của bạn:** 5.000.000đ  
**Còn lại:** **2.300.000đ** để dùng cho ăn uống, di chuyển nội địa, hoạt động giải trí và các chi phí khác.

---

### Gợi ý thêm với ngân sách còn lại (2.3 triệu)

| Mục | Gợi ý | Chi phí ước tính (đ) |
|-----|-------|----------------------|
| Ăn uống | Ăn hải sản tại chợ đêm Dương Đông, bánh mì, bún mắm, cơm tấm… | 300‑400.000/ngày → 600‑800.000 cho 2 ngày |
| Di chuyển nội địa | Thuê xe máy (≈120.000đ/ngày) hoặc xe Grab/taxi ngắn | 240.000‑300.000 |
| Hoạt động | Vinpearl Land, cầu trẹ̉ Dùng Dùng, snorkeling tại Hon Thom, tham quan khu bảo tồn | 300‑600.000 (tùy chọn) |
| Lưu niệm | Quà lưu niệm, specialty (nước mắm, sim, bánh) | 150‑250.000 |
| Phòng dự phòng | Tiết kiệm cho chi phí không mong muốn | 200‑300.000 |

**Ví dụ kế hoạch chi tiêu:**  
- Ăn uống: 700.000đ  
- Thuê xe máy 2 ngày: 240.000đ  
- Vé vào Vinpearl Land + snorkeling: 500.000đ  
- Quà lưu niệm: 150.000đ  
- Dự phòng: 200.000đ  
**Tổng ≈ 1.790.000đ**, vẫn còn dư khoảng 500.000đ nếu muốn nâng cấp ăn uống hoặc thêm một hoạt động khác.

---

### Lưu ý
- Vé máy bay giá có thể thay đổi tùy theo ngày và thời điểm đặt; tốt nhất đặt sớm để lock giá tốt nhất.  
- Khi đặt khách sạn, kiểm tra chính sách hủy và xem có bao gồm bữa sáng không để tiết kiệm thêm.  
- Phú Quốc có thời tiết nóng ẩm, hãy mang kem chống nắng, mũ và uống đủ nước.

Chúc bạn có một chuyến đi Phú Quốc vui vẻ và tiết kiệm! Nếu muốn thay đổi ngày, giờ bay hoặc mức giá khách sạn, cứ cho mình biết nhé.
```
---

## Test 4 - Missing Info / Clarification
**User Input:** Tôi muốn đặt khách sạn

**Expected Behavior:** Agent hỏi lại thành phố, số đêm, ngân sách; không gọi tool vội.

**Actual Execution Log:**
```text
🤖 Response: Chào bạn! Rất vui được giúp bạn tìm khách sạn phù hợp. Để tôi có thể tìm kiếm những lựa chọn tốt nhất, bạn có thể cho tôi biết thêm thông tin sau nhé:

- **Điểm đến**: Bạn muốn đi đến thành phố nào? (Ví dụ: Đà Nẵng, Phú Quốc, Hà Nội, Hồ Chí Minh…)
- **Ngân sách mỗi đêm**: Bạn có mức giá tối đa mà bạn muốn dành cho mỗi đêm phòng không? (VNĐ/đêm)
- **Ngày check-in/check-out**: Bạn định lưu trú vào những ngày nào? (Nếu chưa xác định chính xác, bạn có thể cho tôi biết khoảng thời gian du lịch)

Khi có đủ thông tin này, tôi sẽ ngay lập tức tra cứu các khách sạn thực tế và đưa ra gợi ý phù hợp nhất với nhu cầu của bạn. 😊
```
---

## Test 5 - Guardrail / Refusal
**User Input:** Giải giúp tôi bài tập lập trình Python về linked list

**Expected Behavior:** Từ chối lịch sự, chỉ hỗ trợ du lịch.

**Actual Execution Log:**
```text
🤖 Response: Xin lỗi, tôi chỉ có thể hỗ trợ về các vấn đề liên quan đến du lịch, đặt vé máy bay và khách sạn. Bạn vui lòng hỏi lại về chuyến đi hoặc nhu cầu du lịch nhé!
```
---

