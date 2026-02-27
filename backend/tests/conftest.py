"""
Pytest configuration for iStock backend tests
"""

import pytest
import asyncio
from typing import AsyncGenerator

# 设置异步测试事件循环
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_connection() -> AsyncGenerator[None, None]:
    """
    Test database connection fixture.
    In CI/CD, this connects to the test PostgreSQL instance.
    """
    # 这里可以设置测试数据库连接
    # 在实际测试中，我们会使用测试数据库
    yield


@pytest.fixture(scope="session")
async def test_redis_connection() -> AsyncGenerator[None, None]:
    """
    Test Redis connection fixture.
    In CI/CD, this connects to the test Redis instance.
    """
    # 这里可以设置测试Redis连接
    yield


@pytest.fixture(scope="function")
async def clean_test_environment():
    """
    Clean test environment before each test.
    """
    # 在每个测试前清理环境
    yield
    # 在每个测试后清理环境