#!/bin/bash
# Docker部署测试脚本
# 此脚本用于测试Docker部署是否正常工作

echo "=========================================="
echo "  跑步助手 Docker 部署测试脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
echo "1. 检查Docker是否安装..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker 已安装${NC}"
    docker --version
else
    echo -e "${RED}✗ Docker 未安装${NC}"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo ""

# 检查Docker Compose是否安装
echo "2. 检查Docker Compose是否安装..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Docker Compose 已安装${NC}"
    docker-compose --version
else
    echo -e "${RED}✗ Docker Compose 未安装${NC}"
    echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo ""

# 检查端口是否被占用
echo "3. 检查端口占用情况..."
check_port() {
    local port=$1
    
    # 尝试使用lsof（最常用）
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
            echo -e "${YELLOW}⚠ 端口 $port 已被占用${NC}"
            echo "占用进程:"
            lsof -Pi :$port -sTCP:LISTEN
            return 1
        else
            echo -e "${GREEN}✓ 端口 $port 可用${NC}"
            return 0
        fi
    # 尝试使用ss（现代Linux系统）
    elif command -v ss &> /dev/null; then
        if ss -tln | grep -q ":$port "; then
            echo -e "${YELLOW}⚠ 端口 $port 已被占用${NC}"
            echo "占用情况:"
            ss -tlnp | grep ":$port "
            return 1
        else
            echo -e "${GREEN}✓ 端口 $port 可用${NC}"
            return 0
        fi
    # 尝试使用netstat（旧系统）
    elif command -v netstat &> /dev/null; then
        if netstat -tln | grep -q ":$port "; then
            echo -e "${YELLOW}⚠ 端口 $port 已被占用${NC}"
            echo "占用情况:"
            netstat -tlnp | grep ":$port "
            return 1
        else
            echo -e "${GREEN}✓ 端口 $port 可用${NC}"
            return 0
        fi
    else
        echo -e "${YELLOW}⚠ 无法检查端口 $port (lsof/ss/netstat 未安装)${NC}"
        return 0
    fi
}

check_port 80
PORT_80_OK=$?

check_port 443
PORT_443_OK=$?

if [ $PORT_80_OK -ne 0 ] || [ $PORT_443_OK -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}建议：您可以修改 docker-compose.yml 中的端口映射${NC}"
    echo "例如："
    echo "  ports:"
    echo "    - \"8080:80\"    # 使用8080替代80端口"
    echo "    - \"8443:443\"   # 使用8443替代443端口"
fi

echo ""

# 检查SSL证书
echo "4. 检查SSL证书..."
if [ -f "ssl/fullchain.pem" ] && [ -f "ssl/privkey.key" ]; then
    echo -e "${GREEN}✓ 找到SSL证书文件${NC}"
    echo "  - ssl/fullchain.pem"
    echo "  - ssl/privkey.key"
    
    # 检查证书有效性（如果openssl可用）
    if command -v openssl &> /dev/null; then
        if openssl x509 -in ssl/fullchain.pem -noout -checkend 0 2>/dev/null; then
            echo -e "${GREEN}✓ SSL证书有效${NC}"
        else
            echo -e "${RED}✗ SSL证书可能无效或已过期${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ openssl未安装，无法验证证书有效性${NC}"
    fi
else
    echo -e "${YELLOW}⚠ 未找到SSL证书文件${NC}"
    echo "如需启用HTTPS，请将证书放置在以下位置："
    echo "  - ssl/fullchain.pem"
    echo "  - ssl/privkey.key"
    echo ""
    if command -v openssl &> /dev/null; then
        echo "可以使用以下命令生成自签名证书（仅测试用）："
        echo "  mkdir -p ssl"
        echo "  openssl req -x509 -newkey rsa:4096 -nodes \\"
        echo "    -keyout ssl/privkey.key \\"
        echo "    -out ssl/fullchain.pem \\"
        echo "    -days 365 \\"
        echo "    -subj \"/CN=localhost\""
    else
        echo "提示：需要安装openssl工具来生成证书"
        echo "  sudo apt-get install openssl  # Debian/Ubuntu"
        echo "  sudo yum install openssl      # CentOS/RHEL"
    fi
fi

echo ""

# 检查配置文件
echo "5. 检查配置文件..."
if [ -f "config.ini" ]; then
    echo -e "${GREEN}✓ 找到配置文件 config.ini${NC}"
    
    # 检查SSL配置
    if grep -q "ssl_enabled = true" config.ini 2>/dev/null; then
        echo -e "${GREEN}  ✓ SSL已启用${NC}"
    else
        echo -e "${YELLOW}  ⚠ SSL未启用${NC}"
    fi
else
    echo -e "${YELLOW}⚠ 未找到配置文件，首次运行时将自动创建${NC}"
fi

echo ""

# 检查Docker镜像
echo "6. 检查Docker镜像..."
if docker images | grep -q "python-running-helper"; then
    echo -e "${GREEN}✓ 找到Docker镜像${NC}"
    docker images | grep "python-running-helper"
else
    echo -e "${YELLOW}⚠ 未找到Docker镜像${NC}"
    echo "将在首次运行时自动构建"
fi

echo ""

# 检查运行中的容器
echo "7. 检查运行中的容器..."
if docker ps | grep -q "python-running-helper"; then
    echo -e "${GREEN}✓ 容器正在运行${NC}"
    docker ps | grep "python-running-helper"
else
    echo -e "${YELLOW}⚠ 容器未运行${NC}"
fi

echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""

# 提供下一步操作建议
echo "下一步操作："
echo ""
echo "1. 构建并启动容器："
echo "   docker-compose up -d --build"
echo ""
echo "2. 查看日志："
echo "   docker-compose logs -f"
echo ""
echo "3. 停止容器："
echo "   docker-compose down"
echo ""
echo "4. 访问应用："
if [ -f "ssl/fullchain.pem" ] && [ -f "ssl/privkey.key" ]; then
    echo "   HTTPS: https://localhost"
fi
echo "   HTTP: http://localhost"
echo ""

# 询问是否立即启动
read -p "是否立即启动Docker容器？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "正在启动容器..."
    docker-compose up -d --build
    
    echo ""
    echo "等待容器启动..."
    sleep 5
    
    echo ""
    echo "容器状态："
    docker-compose ps
    
    echo ""
    echo "查看日志："
    docker-compose logs --tail=50
    
    echo ""
    echo -e "${GREEN}容器已启动！${NC}"
    echo "访问应用: http://localhost"
fi
