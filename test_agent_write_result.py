import os
from datetime import datetime

# Giả định agent_app đã được compile từ file agent.py của bạn
# from agent import agent_app 
# Import đối tượng agent_app từ file agent.py
try:
    from agent import graph as agent_app
except ImportError:
    print("❌ Lỗi: Không tìm thấy file agent.py hoặc biến agent_app.")
    exit(1)


def run_and_log_tests():
    # Danh sách các test cases dựa trên yêu cầu bài Lab
    test_cases = [
        {
            "id": "Test 1 - Direct Answer",
            "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
            "expected": "Agent chào hỏi, hỏi thêm sở thích/ngân sách, không gọi tool."
        },
        {
            "id": "Test 2 - Single Tool Call",
            "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
            "expected": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay."
        },
        {
            "id": "Test 3 - Multi-Step Tool Chaining",
            "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
            "expected": "Chuỗi nhiều bước: Tìm vé rẻ nhất -> Tìm khách sạn -> Tính budget -> Tổng hợp."
        },
        {
            "id": "Test 4 - Missing Info / Clarification",
            "input": "Tôi muốn đặt khách sạn",
            "expected": "Agent hỏi lại thành phố, số đêm, ngân sách; không gọi tool vội."
        },
        {
            "id": "Test 5 - Guardrail / Refusal",
            "input": "Giải giúp tôi bài tập lập trình Python về linked list",
            "expected": "Từ chối lịch sự, chỉ hỗ trợ du lịch."
        }
    ]

    with open("result_log.md", "w", encoding="utf-8") as f:
        # Viết header cho file log
        f.write(f"# TravelBuddy Agent Test Results\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for tc in test_cases:
            f.write(f"## {tc['id']}\n")
            f.write(f"**User Input:** {tc['input']}\n\n")
            f.write(f"**Expected Behavior:** {tc['expected']}\n\n")
            f.write(f"**Actual Execution Log:**\n")
            f.write("```text\n")
            
            # Chạy Agent qua LangGraph stream
            initial_state = {"messages": [("user", tc['input'])]}
            
            try:
                for event in agent_app.stream(initial_state):
                    for value in event.values():
                        msg = value["messages"][-1]
                        
                        # Ghi log gọi Tool nếu có
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool in msg.tool_calls:
                                f.write(f"🛠️ Tool Call: {tool['name']}({tool['args']})\n")
                        
                        # Ghi log phản hồi văn bản
                        if msg.content:
                            f.write(f"🤖 Response: {msg.content}\n")
            except Exception as e:
                f.write(f"❌ Error during execution: {str(e)}\n")
                
            f.write("```\n")
            f.write("---\n\n")

    print("✅ Đã hoàn thành 5 test cases. Kết quả được lưu tại result_log.md")

if __name__ == "__main__":
    run_and_log_tests()