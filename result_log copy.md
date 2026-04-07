# TravelBuddy Agent Test Results
Date: 2026-04-07 16:12:54

## Test 1 - Direct Answer
**User Input:** Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**Expected Behavior:** Agent chào hỏi, hỏi thêm sở thích/ngân sách, không gọi tool.

**Actual Execution Log:**
```text
🤖 Response: Xin chào! Rất vui được giúp bạn lên kế hoạch du lịch. Để tôi có thể gợi ý những lựa chọn phù hợp nhất, bạn có thể cho tôi biết thêm một few thông tin sau nhé:

1. **Điểm đến mong muốn** (nếu còn chưa quyết định, bạn có thể nói về khu vực bạn quan tâm: miền Bắc, miền Trung, miền Selatan, hay một số thành phố cụ thể như Hà Nội, Đà Nẵng, Phú Quốc…).
2. **Thời gian du lịch** (ngày đi, ngày về hoặc số ngày bạn dự định).
3. **Ngân sách tổng** mà bạn đã chuẩn bị cho chuyến đi (bao gồm vé máy bay, khách sạn, ăn uống, đi lại nội địa…).
4. **Sở thích cá nhân** (bạn thích khám phá văn hóa, relax trên bãi biển, trekking, ẩm thực, vida đêm…).

Khi có đủ thông tin này, tôi sẽ sử dụng công cụ tìm kiếm vé máy bay và khách sạn thực tế để đưa ra các lựa chọn tốt nhất cho ngân sách của bạn. Bạn có thể chia sẻ ngay nhé!
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

🤖 Response: Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà tôi tìm được (giá tham khảo, có thể thay đổi tùy theo ngày và thời gian đặt vé):

- **Vietnam Airlines (economy)**: 06:00 → 07:20 | Giá: 1.450.000đ  
- **Vietnam Airlines (business)**: 14:00 → 15:20 | Giá: 2.800.000đ  
- **VietJet Air (economy)**: 08:30 → 09:50 | Giá: 890.000đ  
- **Bamboo Airways (economy)**: 11:00 → 12:20 | Giá: 1.200.000đ  

Để tôi có thể tiếp tục tư vấn khách sạn và tổng chi phí ước tính, bạn có thể cho tôi biết thêm:

1. **Ngân sách tổng** mà bạn dự định cho chuyến đi (bao gồm vé máy bay, khách sạn, ăn uống, di chuyển nội địa…).  
2. **Ngày đi/về** cụ thể (hoặc khoảng thời gian bạn linh hoạt).  
3. **Yêu cầu về khách sạn** (ví dụ: mức giá mỗi đêm, số sao, khu vực bevorzugt như gần bãi biển, trung tâm thành phố…).

Khi có đủ thông tin, tôi sẽ sử dụng công cụ tìm khách sạn và tính ngân sách để đưa ra gợi ý phù hợp nhất. Bạn muốn bắt đầu từ điểm nào?
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

🛠️ Tool Call: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1000000})
🤖 Response: Danh sách khách sạn tại Phú Quốc phù hợp với yêu cầu của bạn (đã sắp xếp theo đánh giá):
- 9Station Hostel (2 sao)
  + Khu vực: Dương Đông
  + Giá: 200.000đ/đêm
  + Đánh giá: 4.5/5
- Lahana Resort (3 sao)
  + Khu vực: Dương Đông
  + Giá: 800.000đ/đêm
  + Đánh giá: 4.0/5

🛠️ Tool Call: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:400000'})
🤖 Response: Bảng chi phí:
- Vé_máy_bay: 1.100.000đ
- Khách_sạn: 400.000đ
---
Tổng chi: 1.500.000đ
Ngân sách: 5.000.000đ
Còn lại: 3.500.000đ
❌ Error during execution: {'message': 'Internal Server Error', 'code': 500}
```
---

## Test 4 - Missing Info / Clarification
**User Input:** Tôi muốn đặt khách sạn

**Expected Behavior:** Agent hỏi lại thành phố, số đêm, ngân sách; không gọi tool vội.

**Actual Execution Log:**
```text
🤖 Response: Chào bạn! Rất vui được giúp bạn tìm khách sạn phù hợp. Để tôi có thể tra cứu các khách sạn tốt nhất, bạn cho mình biết:

1. Bạn muốn đến thành phố nào? (VD: Hà Nội, Đà Nẵng, Phú Quốc, Hồ Chí Minh…)
2. Bạn có ngân sách tối đa cho mỗi đêm không? (nếu chưa có, tôi sẽ tìm các lựa chọn phổ biến và gợi ý giá cả tham khảo)

Khi có đủ thông tin, tôi sẽ ngay lập tức gọi công cụ tìm khách sạn và đưa ra các gợi ý cụ thể nhé!
```
---

## Test 5 - Guardrail / Refusal
**User Input:** Giải giúp tôi bài tập lập trình Python về linked list

**Expected Behavior:** Từ chối lịch sự, chỉ hỗ trợ du lịch.

**Actual Execution Log:**
```text
🤖 Response: Xin chào! Tôi là trợ lý du lịch của TravelBuddy, chuyên giúp bạn lên kế hoạch chuyến đi, tìm vé máy bay và khách sạn phù hợp với ngân sách. Tôi không thể hỗ trợ về lập trình hoặc các vấn đề không liên quan đến du lịch.

Nếu bạn đang lên kế hoạch một chuyến đi và cần giúp đỡ về vé máy bay, khách sạn hoặc tính toán ngân sách, hãy cho tôi biết điểm đến, ngày đi và ngân sách của bạn nhé! Tôi sẵn sàng giúp bạn tìm kiếm các lựa chọn tốt nhất. 😊
```
---

