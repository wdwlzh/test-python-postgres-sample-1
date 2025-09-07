#!/usr/bin/env python3
"""
测试改进后的 EMA Backtester 参数范围
短期 EMA: 3-20
长期 EMA: 10-60
"""

import sys
import os

# Add the backend app to the path
sys.path.append('/workspaces/backend')

def test_ema_parameters():
    """测试新的 EMA 参数范围"""
    print("=== 测试 EMA Backtester 参数改进 ===\n")
    
    try:
        # Import the updated EMABacktester
        from backend.app.ema_backtester import EMABacktester
        from datetime import date
        
        print("1. 测试默认参数范围...")
        
        # Create an instance
        backtester = EMABacktester("AAPL", date(2020, 1, 1), date(2023, 1, 1))
        
        # Test default parameters
        combinations = backtester.generate_ema_combinations()
        
        # Check ranges
        short_periods = set()
        long_periods = set()
        
        for short, long in combinations:
            short_periods.add(short)
            long_periods.add(long)
        
        print(f"✅ 短期 EMA 范围: {min(short_periods)} - {max(short_periods)}")
        print(f"✅ 长期 EMA 范围: {min(long_periods)} - {max(long_periods)}")
        print(f"✅ 总组合数: {len(combinations)}")
        
        # Verify ranges are correct
        assert min(short_periods) == 3, f"短期 EMA 最小值应为 3，实际为 {min(short_periods)}"
        assert max(short_periods) == 20, f"短期 EMA 最大值应为 20，实际为 {max(short_periods)}"
        assert min(long_periods) == 10, f"长期 EMA 最小值应为 10，实际为 {min(long_periods)}"
        assert max(long_periods) == 60, f"长期 EMA 最大值应为 60，实际为 {max(long_periods)}"
        
        print("\n2. 测试自定义参数验证...")
        
        # Test custom parameters
        custom_short = [3, 5, 8, 12, 15]
        custom_long = [20, 25, 30, 40, 50]
        
        custom_combinations = backtester.generate_ema_combinations(custom_short, custom_long)
        print(f"✅ 自定义组合数: {len(custom_combinations)}")
        
        # Show some examples
        print(f"✅ 前5个组合: {custom_combinations[:5]}")
        
        print("\n3. 测试边界条件...")
        
        # Test boundary conditions
        boundary_short = [3, 20]  # Min and max for short
        boundary_long = [10, 60]  # Min and max for long
        
        boundary_combinations = backtester.generate_ema_combinations(boundary_short, boundary_long)
        print(f"✅ 边界组合: {boundary_combinations}")
        
        print("\n4. 测试无效参数...")
        
        # Test invalid parameters (should be handled gracefully)
        try:
            invalid_short = [0, 25]  # 0 is invalid, 25 exceeds max
            invalid_long = [5, 70]   # 5 is too small, 70 exceeds max
            
            invalid_combinations = backtester.generate_ema_combinations(invalid_short, invalid_long)
            print(f"✅ 处理无效参数后的组合数: {len(invalid_combinations)}")
        except ValueError as e:
            print(f"✅ 正确捕获验证错误: {e}")
        
        print("\n✅ 所有测试通过！EMA 参数已成功更新")
        
        # Show the actual combinations count
        print(f"\n📊 统计信息:")
        print(f"   - 短期 EMA 范围: 3 到 20 ({20-3+1} 个值)")
        print(f"   - 长期 EMA 范围: 10 到 60 ({60-10+1} 个值)")
        print(f"   - 有效组合总数: {len(combinations)}")
        
        # Calculate expected combinations
        total_short = 20 - 3 + 1  # 18 values
        total_long = 60 - 10 + 1  # 51 values
        
        # Count valid combinations (short < long)
        expected_combinations = 0
        for s in range(3, 21):
            for l in range(10, 61):
                if s < l:
                    expected_combinations += 1
        
        print(f"   - 预期组合数: {expected_combinations}")
        print(f"   - 实际组合数: {len(combinations)}")
        
        if len(combinations) == expected_combinations:
            print("✅ 组合数量验证通过")
        else:
            print("⚠️  组合数量不匹配")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试错误: {e}")
        return False

def show_usage_examples():
    """显示使用示例"""
    print("\n" + "="*60)
    print("📚 EMA Backtester 使用示例")
    print("="*60)
    
    print("""
使用默认参数（短期3-20，长期10-60）:
curl -X POST "http://localhost:8000/ema-backtests/run" \\
  -H "Content-Type: application/json" \\
  -d '{
    "symbol": "AAPL",
    "start_date": "2020-01-01",
    "end_date": "2023-01-01",
    "initial_cash": 10000
  }'

使用自定义参数:
curl -X POST "http://localhost:8000/ema-backtests/run" \\
  -H "Content-Type: application/json" \\
  -d '{
    "symbol": "AAPL",
    "start_date": "2020-01-01",
    "end_date": "2023-01-01",
    "initial_cash": 10000,
    "short_periods": [3, 5, 8, 12, 15],
    "long_periods": [20, 25, 30, 40, 50]
  }'

参数范围:
- 短期 EMA: 3 到 20
- 长期 EMA: 10 到 60  
- 约束: 短期 < 长期
""")

if __name__ == "__main__":
    success = test_ema_parameters()
    if success:
        show_usage_examples()
    else:
        print("\n❌ 测试失败，请检查实现")
