import unittest
import types
import sys


def _fake_tool_decorator(func):
    class _ToolWrapper:
        def __init__(self, wrapped_func):
            self._wrapped_func = wrapped_func

        def invoke(self, payload):
            return self._wrapped_func(**payload)

    return _ToolWrapper(func)


fake_langchain_core = types.ModuleType("langchain_core")
fake_langchain_tools = types.ModuleType("langchain_core.tools")
fake_langchain_tools.tool = _fake_tool_decorator
fake_langchain_core.tools = fake_langchain_tools
sys.modules["langchain_core"] = fake_langchain_core
sys.modules["langchain_core.tools"] = fake_langchain_tools

import tools


class TestSearchFlights(unittest.TestCase):
    def test_search_flights_returns_flights_for_valid_route(self):
        result = tools.search_flights.invoke(
            {"origin": "Hà Nội", "destination": "Đà Nẵng"}
        )
        self.assertIn("Danh sách chuyến bay giữa Hà Nội và Đà Nẵng", result)
        self.assertIn("Vietnam Airlines", result)
        self.assertIn("VietJet Air", result)
        self.assertIn("890.000đ", result)

    def test_search_flights_supports_reverse_lookup(self):
        result = tools.search_flights.invoke(
            {"origin": "Đà Nẵng", "destination": "Hà Nội"}
        )
        self.assertIn("Danh sách chuyến bay giữa Đà Nẵng và Hà Nội", result)
        self.assertIn("Vietnam Airlines", result)

    def test_search_flights_returns_not_found_message(self):
        result = tools.search_flights.invoke(
            {"origin": "Huế", "destination": "Cần Thơ"}
        )
        self.assertEqual(
            result,
            "Không tìm thấy chuyến bay từ Huế đến Cần Thơ.",
        )


class TestSearchHotels(unittest.TestCase):
    def test_search_hotels_filters_by_budget_and_sorts_by_rating(self):
        result = tools.search_hotels.invoke(
            {"city": "Đà Nẵng", "max_price_per_night": 700_000}
        )
        self.assertIn("Danh sách khách sạn tại Đà Nẵng", result)
        self.assertIn("Memory Hostel", result)
        self.assertIn("Christina's Homestay", result)
        self.assertNotIn("Sala Danang Beach", result)

        # Rating 4.7 should appear before 4.6 in sorted output.
        self.assertLess(result.find("Christina's Homestay"), result.find("Memory Hostel"))

    def test_search_hotels_returns_city_not_available_message(self):
        result = tools.search_hotels.invoke({"city": "Nha Trang"})
        self.assertEqual(
            result,
            "Xin lỗi, hiện tại tôi chưa có dữ liệu khách sạn tại thành phố 'Nha Trang'.",
        )

    def test_search_hotels_returns_no_match_under_budget_message(self):
        result = tools.search_hotels.invoke(
            {"city": "Phú Quốc", "max_price_per_night": 100_000}
        )
        self.assertEqual(
            result,
            "Không tìm thấy khách sạn tại Phú Quốc với giá dưới 100.000đ/đêm. Hãy thử tăng ngân sách.",
        )


class TestCalculateBudget(unittest.TestCase):
    def test_calculate_budget_returns_remaining_budget(self):
        result = tools.calculate_budget.invoke(
            {
                "total_budget": 5_000_000,
                "expenses": "ve may bay:890000,khach san:650000",
            }
        )
        self.assertIn("Tổng chi: 1.540.000đ", result)
        self.assertIn("Ngân sách: 5.000.000đ", result)
        self.assertIn("Còn lại: 3.460.000đ", result)

    def test_calculate_budget_returns_over_budget_warning(self):
        result = tools.calculate_budget.invoke(
            {
                "total_budget": 1_000_000,
                "expenses": "ve may bay:900000,khach san:300000",
            }
        )
        self.assertIn("Vượt ngân sách 200.000 đồng! Cần điều chỉnh.", result)

    def test_calculate_budget_returns_error_for_invalid_format(self):
        result = tools.calculate_budget.invoke(
            {"total_budget": 2_000_000, "expenses": "ve may bay-890000"}
        )
        self.assertEqual(
            result,
            "Lỗi: Định dạng chuỗi chi phí sai. Vui lòng dùng định dạng 'tên:số_tiền,tên:số_tiền'.",
        )


if __name__ == "__main__":
    unittest.main()
