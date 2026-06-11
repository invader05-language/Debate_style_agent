#!/bin/bash
# Multi-AI Debate Agent - 部署验证脚本
# 检查所有服务健康状态

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="${1:-http://localhost:8000}"
FRONTEND_URL="${2:-http://localhost:3000}"
PASS=0
FAIL=0

check() {
    local name="$1"
    local url="$2"
    local expected_status="${3:-200}"

    status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

    if [ "$status" = "$expected_status" ]; then
        echo -e "${GREEN}✓${NC} $name (HTTP $status)"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}✗${NC} $name (HTTP $status, expected $expected_status)"
        FAIL=$((FAIL + 1))
    fi
}

check_json() {
    local name="$1"
    local url="$2"
    local jq_filter="$3"

    result=$(curl -s "$url" 2>/dev/null | jq -r "$jq_filter" 2>/dev/null || echo "PARSE_ERROR")

    if [ "$result" != "PARSE_ERROR" ] && [ -n "$result" ] && [ "$result" != "null" ]; then
        echo -e "${GREEN}✓${NC} $name: $result"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}✗${NC} $name: failed to parse response"
        FAIL=$((FAIL + 1))
    fi
}

echo "========================================"
echo "  Multi-AI Debate Agent - 健康检查"
echo "========================================"
echo ""

# ── 后端服务 ─────────────────────────────
echo "Backend Services:"
check "Root endpoint" "$BASE_URL/"
check "Health endpoint" "$BASE_URL/health"
check "API docs" "$BASE_URL/docs"
check_json "Health status" "$BASE_URL/health" ".status"
echo ""

# ── API 端点 ─────────────────────────────
echo "API Endpoints:"
check "List debates" "$BASE_URL/api/debates"
check "List memories" "$BASE_URL/api/memories"
check "Search memories" "$BASE_URL/api/memories/search?q=test"
echo ""

# ── 前端服务 ─────────────────────────────
echo "Frontend:"
check "Frontend" "$FRONTEND_URL"
echo ""

# ── Redis ────────────────────────────────
echo "Redis:"
redis_result=$(curl -s "$BASE_URL/health" 2>/dev/null | jq -r '.redis.status' 2>/dev/null || echo "unknown")
if [ "$redis_result" = "connected" ]; then
    echo -e "${GREEN}✓${NC} Redis: connected"
    PASS=$((PASS + 1))
else
    echo -e "${YELLOW}!${NC} Redis: $redis_result (optional)"
fi
echo ""

# ── Metrics ──────────────────────────────
echo "Metrics:"
check "Prometheus metrics" "$BASE_URL/metrics"
echo ""

# ── 总结 ─────────────────────────────────
echo "========================================"
TOTAL=$((PASS + FAIL))
echo -e "Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC} / $TOTAL total"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed.${NC}"
    exit 1
fi
